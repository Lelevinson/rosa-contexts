"""Non-destructive tests for scripts/context_sync.py using temporary Git repos."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts" / "context_sync.py"
TARGET_URL = "https://github.com/Lelevinson/rosa-contexts.git"


def git(repository: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", "-C", str(repository), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if check and result.returncode != 0:
        raise AssertionError(result.stderr)
    return result


def commit_all(repository: Path, message: str) -> None:
    git(repository, "add", "--all")
    git(repository, "commit", "-m", message)


def write_manifest(repository: Path, include: list[str], contents: dict[str, bytes]) -> None:
    files = []
    for relative, data in contents.items():
        if relative in include:
            files.append(
                {
                    "path": relative,
                    "source_sha256": hashlib.sha256(data).hexdigest(),
                    "published_sha256": hashlib.sha256(data).hexdigest(),
                    "source_git_state": "committed",
                    "source_commit_contains_bytes": True,
                    "redactions": {"local_paths": 0, "private_network_addresses": 0},
                }
            )
    manifest = {
        "schema_version": 1,
        "member": "test",
        "target_repository": "Lelevinson/rosa-contexts",
        "source_repository": "Example/rosa-research",
        "expected_source_branch": "research/test",
        "protocol_version": 1,
        "protocol_commit": "",
        "source_branch": "research/test",
        "source_commit_sha": "",
        "synchronized_at_utc": "2026-11-13T00:00:00Z",
        "include": include,
        "files": files,
        "important_missing_context": [],
    }
    path = repository / ".context-sync" / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


class ContextSyncTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="rosa-context-sync-")
        self.base = Path(self.temporary.name)
        self.remote = self.base / "remote.git"
        self.seed = self.base / "seed"
        self.target = self.base / "target"
        self.source = self.base / "source"
        git(self.base, "init", "--bare", "--initial-branch=main", str(self.remote))
        git(self.base, "init", "--initial-branch=main", str(self.seed))
        git(self.seed, "config", "user.name", "Context Sync Test")
        git(self.seed, "config", "user.email", "test@example.invalid")
        (self.seed / "README.md").write_text("Shared protocol fixture.\n", encoding="utf-8")
        commit_all(self.seed, "Add test protocol")
        git(self.seed, "remote", "add", "origin", str(self.remote))
        git(self.seed, "push", "origin", "main")
        self._create_source()
        self._create_member_branch(["research/a.md", "research/b.md"])
        git(self.base, "clone", str(self.remote), str(self.target))
        git(self.target, "config", "user.name", "Context Sync Test")
        git(self.target, "config", "user.email", "test@example.invalid")
        git(self.target, "remote", "set-url", "origin", TARGET_URL)
        git(
            self.target,
            "config",
            "url.file://" + str(self.remote) + ".insteadOf",
            TARGET_URL,
        )
        git(self.target, "fetch", "origin", "--prune")
        git(self.target, "switch", "--track", "-c", "member/test", "origin/member/test")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _create_source(self) -> None:
        git(self.base, "init", "--initial-branch=research/test", str(self.source))
        git(self.source, "config", "user.name", "Context Source Test")
        git(self.source, "config", "user.email", "source@example.invalid")
        git(self.source, "remote", "add", "origin", "https://github.com/Example/rosa-research.git")
        (self.source / "research").mkdir(parents=True, exist_ok=True)
        (self.source / "research/a.md").write_bytes(b"Original A\n")
        (self.source / "research/b.md").write_bytes(b"Original B\n")
        commit_all(self.source, "Add source contexts")

    def _create_member_branch(self, include: list[str]) -> None:
        git(self.seed, "switch", "-c", "member/test")
        contents = {
            "research/a.md": b"Original A\n",
            "research/b.md": b"Original B\n",
        }
        for relative, data in contents.items():
            destination = self.seed / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
        write_manifest(self.seed, include, contents)
        commit_all(self.seed, "Add initial member context")
        git(self.seed, "push", "origin", "member/test")
        git(self.seed, "switch", "main")

    def run_helper(self, action: str, *options: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(SCRIPT), action, "--source", str(self.source), *options],
            cwd=self.target,
            capture_output=True,
            text=True,
            check=False,
        )

    def read_manifest(self) -> dict:
        return json.loads((self.target / ".context-sync/manifest.json").read_text(encoding="utf-8"))

    def test_preview_is_read_only_and_sync_copies_changed_file(self) -> None:
        source_file = self.source / "research/a.md"
        source_file.write_bytes(b"Updated A\n")
        target_file = self.target / "research/a.md"
        before_target = target_file.read_bytes()
        before_manifest = (self.target / ".context-sync/manifest.json").read_bytes()

        preview = self.run_helper("preview")
        self.assertEqual(preview.returncode, 0, preview.stdout + preview.stderr)
        self.assertIn("UPDATE", preview.stdout)
        self.assertEqual(target_file.read_bytes(), before_target)
        self.assertEqual((self.target / ".context-sync/manifest.json").read_bytes(), before_manifest)
        self.assertEqual(source_file.read_bytes(), b"Updated A\n")

        synced = self.run_helper("sync")
        self.assertEqual(synced.returncode, 0, synced.stdout + synced.stderr)
        self.assertEqual(target_file.read_bytes(), b"Updated A\n")
        manifest = self.read_manifest()
        record = next(item for item in manifest["files"] if item["path"] == "research/a.md")
        self.assertEqual(record["source_git_state"], "modified-or-staged")
        self.assertFalse(record["source_commit_contains_bytes"])

    def test_missing_allowlisted_source_blocks_without_deleting_or_writing(self) -> None:
        (self.source / "research/b.md").unlink()
        before = (self.target / "research/b.md").read_bytes()
        result = self.run_helper("sync")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Allowlisted source file is missing", result.stdout)
        self.assertEqual((self.target / "research/b.md").read_bytes(), before)

    def test_intentional_deletion_requires_explicit_confirmation(self) -> None:
        manifest = json.loads((self.target / ".context-sync/manifest.json").read_text())
        manifest["include"].remove("research/b.md")
        (self.target / ".context-sync/manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
        )
        preview = self.run_helper("preview")
        self.assertEqual(preview.returncode, 2)
        self.assertIn("REMOVE", preview.stdout)
        self.assertTrue((self.target / "research/b.md").exists())

        result = self.run_helper("sync", "--confirm-deletions")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse((self.target / "research/b.md").exists())

    def test_secret_pattern_blocks_publication(self) -> None:
        (self.source / "research/a.md").write_text(
            "token = ghp_123456789012345678901234567890123456\n", encoding="utf-8"
        )
        result = self.run_helper("preview")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Credential-like token", result.stdout)
        self.assertEqual((self.target / "research/a.md").read_bytes(), b"Original A\n")

    def test_local_paths_and_private_addresses_are_redacted(self) -> None:
        (self.source / "research/a.md").write_text(
            "Source at /home/alice/project/rosa-research uses 10.20.30.40.\n", encoding="utf-8"
        )
        result = self.run_helper("sync")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        public_text = (self.target / "research/a.md").read_text(encoding="utf-8")
        self.assertIn("[local path redacted]", public_text)
        self.assertIn("[private network address]", public_text)
        record = next(item for item in self.read_manifest()["files"] if item["path"] == "research/a.md")
        self.assertEqual(record["redactions"]["local_paths"], 1)
        self.assertEqual(record["redactions"]["private_network_addresses"], 1)

    def test_remote_advance_blocks_sync(self) -> None:
        collaborator = self.base / "collaborator"
        git(self.base, "clone", str(self.remote), str(collaborator))
        git(collaborator, "config", "user.name", "Context Sync Test")
        git(collaborator, "config", "user.email", "test@example.invalid")
        git(collaborator, "switch", "--track", "-c", "member/test", "origin/member/test")
        (collaborator / "research/other.md").write_text("Remote change\n", encoding="utf-8")
        commit_all(collaborator, "Advance remote member branch")
        git(collaborator, "push", "origin", "member/test")

        result = self.run_helper("sync")
        self.assertEqual(result.returncode, 2)
        self.assertIn("commits not integrated locally", result.stderr)
        self.assertEqual((self.target / "research/a.md").read_bytes(), b"Original A\n")

    def test_wrong_branch_is_rejected(self) -> None:
        git(self.target, "switch", "--create", "member/other")
        result = self.run_helper("sync")
        self.assertEqual(result.returncode, 2)
        self.assertIn("belongs to 'member/test'", result.stderr)

    def test_teammate_context_can_be_read_without_checkout(self) -> None:
        current = git(self.target, "branch", "--show-current").stdout.strip()
        content = git(self.target, "show", "origin/member/test:research/a.md").stdout
        after = git(self.target, "branch", "--show-current").stdout.strip()
        self.assertEqual(content, "Original A\n")
        self.assertEqual(after, current)

    def test_first_publish_requires_and_accepts_explicit_flag(self) -> None:
        git(self.target, "switch", "--create", "member/new", "--track", "origin/main")
        manifest = {
            "schema_version": 1,
            "member": "new",
            "target_repository": "Lelevinson/rosa-contexts",
            "source_repository": "Example/rosa-research",
            "expected_source_branch": "research/test",
            "protocol_version": 1,
            "include": ["research/a.md"],
            "important_missing_context": [],
        }
        manifest_path = self.target / ".context-sync/manifest.json"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

        blocked = self.run_helper("sync")
        self.assertEqual(blocked.returncode, 2)
        self.assertIn("Use --first-publish", blocked.stderr)
        self.assertFalse((self.target / "research/a.md").exists())

        first = self.run_helper("sync", "--first-publish")
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        self.assertEqual((self.target / "research/a.md").read_bytes(), b"Original A\n")


if __name__ == "__main__":
    unittest.main()
