#!/usr/bin/env python3
"""Preview or copy an explicit context allowlist into this member branch."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlsplit

SCHEMA_VERSION = 1
MAX_FILE_BYTES = 2 * 1024 * 1024
MAX_TOTAL_BYTES = 20 * 1024 * 1024

LOCAL_PATH_PATTERN = re.compile(
    r"/(?:home|Users|tmp)/[A-Za-z0-9._~-]+(?:/[A-Za-z0-9._~-]+)*|"
    r"/mnt/[A-Za-z0-9._~-]+/Users/[A-Za-z0-9._~-]+(?:/[A-Za-z0-9._~-]+)*"
)
WINDOWS_PATH_PATTERN = re.compile(
    r"(?i)\b[A-Z]:\\Users\\[A-Za-z0-9._~-]+(?:\\[A-Za-z0-9._~-]+)*"
)
PRIVATE_IPV4_PATTERN = re.compile(
    r"(?<![\d.])(?:"
    r"10\.(?:\d{1,3}\.){2}\d{1,3}|"
    r"172\.(?:1[6-9]|2\d|3[01])\.(?:\d{1,3}\.)\d{1,3}|"
    r"192\.168\.(?:\d{1,3}\.)\d{1,3}"
    r")(?!\d)"
)
EMAIL_PATTERN = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
TOKEN_PATTERNS = [
    re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
]
CREDENTIAL_ASSIGNMENT_PATTERN = re.compile(
    r"(?im)^\s*(?:api[_ -]?key|access[_ -]?token|client[_ -]?secret|password)"
    r"\s*[:=]\s*[\"']?[^\s\"']{12,}"
)
ABSOLUTE_PATH_PATTERN = re.compile(
    r"(?m)(?:/(?:home|Users|tmp)/|/mnt/[A-Za-z0-9._~-]+/Users/|\b[A-Z]:\\Users\\)"
)


class SyncError(Exception):
    """A safe-to-display reason that blocks synchronization."""


@dataclass
class PlannedFile:
    path: str
    source_bytes: bytes
    published_bytes: bytes
    source_sha256: str
    published_sha256: str
    source_git_state: str
    source_commit_contains_bytes: bool
    redactions: dict[str, int]
    action: str = ""


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run_git(repository: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", "-C", str(repository), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if check and result.returncode != 0:
        detail = result.stderr.strip()
        raise SyncError(f"git {' '.join(args[:2])} failed: {detail}")
    return result


def run_git_bytes(repository: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        ["git", "-C", str(repository), *args],
        check=False,
        capture_output=True,
    )
    if check and result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise SyncError(f"git {' '.join(args[:2])} failed: {detail}")
    return result


def repository_root(start: Path) -> Path:
    result = run_git(start, "rev-parse", "--show-toplevel")
    return Path(result.stdout.strip()).resolve()


def validate_relative_path(value: Any) -> str:
    if not isinstance(value, str) or not value:
        raise SyncError("Every include entry must be a non-empty relative path.")
    if "\\" in value:
        raise SyncError(f"Use forward slashes in include paths: {value!r}")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise SyncError(f"Unsafe include path: {value!r}")
    if path.name.casefold() == "agents.md":
        raise SyncError("AGENTS.md is not allowed in rosa-contexts.")
    if path.parts[0] in {".context-sync", "scripts", "tests", "templates"}:
        raise SyncError(f"Include path overlaps shared repository files: {value!r}")
    if len(path.parts) == 1 and path.name in {
        "README.md",
        "PROTOCOL.md",
        "ONBOARDING.md",
    }:
        raise SyncError(f"Include path overlaps shared repository documentation: {value!r}")
    return path.as_posix()


def validate_manifest_path(value: Any) -> str:
    if not isinstance(value, str) or "\\" in value:
        raise SyncError("Manifest path must be relative and use forward slashes.")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise SyncError("Manifest path must stay inside the repository.")
    if path.parts[0] != ".context-sync" or path.suffix != ".json":
        raise SyncError("Manifest must be a JSON file under .context-sync/.")
    return path.as_posix()


def validate_manifest(manifest: Any) -> dict[str, Any]:
    if not isinstance(manifest, dict):
        raise SyncError("The synchronization manifest must be a JSON object.")
    if manifest.get("schema_version") != SCHEMA_VERSION:
        raise SyncError(f"Manifest schema_version must be {SCHEMA_VERSION}.")
    member = manifest.get("member")
    if not isinstance(member, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", member):
        raise SyncError("Manifest member must be lowercase letters, digits, or hyphens.")
    for field in ("target_repository", "source_repository"):
        value = manifest.get(field)
        if not isinstance(value, str) or not re.fullmatch(
            r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", value
        ):
            raise SyncError(f"Manifest {field} must use owner/repository form.")
    expected_branch = manifest.get("expected_source_branch")
    if not isinstance(expected_branch, str) or not expected_branch.strip():
        raise SyncError("Manifest expected_source_branch is required.")
    include = manifest.get("include")
    if not isinstance(include, list) or not include:
        raise SyncError("Manifest include must contain at least one reviewed file path.")
    normalized = [validate_relative_path(path) for path in include]
    if len(set(normalized)) != len(normalized):
        raise SyncError("Manifest include contains duplicate paths.")
    manifest["include"] = normalized
    if not isinstance(manifest.get("protocol_version"), int):
        raise SyncError("Manifest protocol_version must be an integer.")
    missing = manifest.get("important_missing_context", [])
    if not isinstance(missing, list) or not all(isinstance(item, str) for item in missing):
        raise SyncError("important_missing_context must be a list of strings.")
    return manifest


def read_manifest(root: Path, relative_manifest: str) -> tuple[Path, dict[str, Any]]:
    manifest_relative = validate_manifest_path(relative_manifest)
    manifest_path = root / manifest_relative
    if manifest_path.is_symlink() or not manifest_path.is_file():
        raise SyncError(f"Manifest file is missing or is not a regular file: {manifest_relative}")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise SyncError(f"Cannot read JSON manifest {manifest_relative}: {error}") from error
    return manifest_path, validate_manifest(manifest)


def read_previous_include(root: Path, manifest_relative: str) -> list[str]:
    result = run_git(root, "show", f"HEAD:{manifest_relative}", check=False)
    if result.returncode != 0:
        return []
    try:
        previous = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise SyncError("The manifest committed at HEAD is not valid JSON.") from error
    include = previous.get("include", []) if isinstance(previous, dict) else []
    if not isinstance(include, list):
        raise SyncError("The committed manifest include field is not a list.")
    return [validate_relative_path(path) for path in include]


def source_git_details(source: Path, relative_path: str, data: bytes) -> tuple[str, bool]:
    tracked = run_git(source, "ls-files", "--error-unmatch", "--", relative_path, check=False)
    head_file = run_git_bytes(source, "show", f"HEAD:{relative_path}", check=False)
    in_head = head_file.returncode == 0 and sha256(head_file.stdout) == sha256(data)
    if tracked.returncode == 0:
        state = "committed" if in_head else "modified-or-staged"
    else:
        ignored = run_git(source, "check-ignore", "-q", "--", relative_path, check=False)
        state = "ignored" if ignored.returncode == 0 else "untracked"
    return state, in_head


def check_sensitive_source(path: str, text: str) -> None:
    name = PurePosixPath(path).name.casefold()
    if name.startswith(".env") or any(word in name for word in ("credential", "secret", "private-key")):
        raise SyncError(f"Sensitive-looking filename is not publishable: {path}")
    if EMAIL_PATTERN.search(text):
        raise SyncError(f"Email address found in {path}; remove or exclude the file after review.")
    if any(pattern.search(text) for pattern in TOKEN_PATTERNS):
        raise SyncError(f"Credential-like token or private key found in {path}.")
    if CREDENTIAL_ASSIGNMENT_PATTERN.search(text):
        raise SyncError(f"Credential assignment found in {path}.")


def replace_local_path(match: re.Match[str]) -> str:
    value = match.group(0)
    suffix = ""
    while value and value[-1] in ".,;:!?":
        suffix = value[-1] + suffix
        value = value[:-1]
    return "[local path redacted]" + suffix


def redact_public_copy(text: str) -> tuple[str, dict[str, int]]:
    local_paths = 0
    private_addresses = 0

    def redact_path(match: re.Match[str]) -> str:
        nonlocal local_paths
        local_paths += 1
        return replace_local_path(match)

    def redact_address(match: re.Match[str]) -> str:
        nonlocal private_addresses
        private_addresses += 1
        return "[private network address]"

    public_text = LOCAL_PATH_PATTERN.sub(redact_path, text)
    public_text = WINDOWS_PATH_PATTERN.sub(redact_path, public_text)
    public_text = PRIVATE_IPV4_PATTERN.sub(redact_address, public_text)
    return public_text, {
        "local_paths": local_paths,
        "private_network_addresses": private_addresses,
    }


def check_public_text(path: str, text: str) -> None:
    if EMAIL_PATTERN.search(text):
        raise SyncError(f"Email address remains in public copy {path}.")
    if any(pattern.search(text) for pattern in TOKEN_PATTERNS):
        raise SyncError(f"Credential-like token or private key remains in public copy {path}.")
    if CREDENTIAL_ASSIGNMENT_PATTERN.search(text):
        raise SyncError(f"Credential assignment remains in public copy {path}.")
    if ABSOLUTE_PATH_PATTERN.search(text):
        raise SyncError(f"Absolute home-directory path remains in public copy {path}.")
    if PRIVATE_IPV4_PATTERN.search(text):
        raise SyncError(f"Private network address remains in public copy {path}.")


def source_commit_sha(source: Path) -> str:
    return run_git(source, "rev-parse", "HEAD").stdout.strip()


def source_branch(source: Path) -> str:
    branch = run_git(source, "branch", "--show-current").stdout.strip()
    if not branch:
        raise SyncError("The source repository is detached; switch to its authorized source branch.")
    return branch


def target_is_dirty(root: Path, relative_path: str) -> bool:
    result = run_git(root, "diff", "--quiet", "HEAD", "--", relative_path, check=False)
    return result.returncode != 0


def old_published_hash(root: Path, relative_path: str, manifest_relative: str) -> str | None:
    result = run_git(root, "show", f"HEAD:{manifest_relative}", check=False)
    if result.returncode != 0:
        return None
    try:
        previous = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None
    for item in previous.get("files", []):
        if isinstance(item, dict) and item.get("path") == relative_path:
            value = item.get("published_sha256")
            return value if isinstance(value, str) else None
    return None


def target_path_action(
    root: Path,
    relative_path: str,
    published_bytes: bytes,
    was_managed: bool,
    manifest_relative: str,
) -> str:
    destination = root / relative_path
    if destination.is_symlink():
        raise SyncError(f"Published path is a symlink and will not be followed: {relative_path}")
    if destination.exists() and not destination.is_file():
        raise SyncError(f"Published path is not a regular file: {relative_path}")
    if destination.exists() and not was_managed:
        raise SyncError(f"Unmanaged file already occupies the publish path: {relative_path}")
    if not destination.exists():
        return "ADD"
    current = destination.read_bytes()
    if current == published_bytes:
        return "UNCHANGED"
    tracked = run_git(root, "ls-files", "--error-unmatch", "--", relative_path, check=False)
    if tracked.returncode == 0:
        if target_is_dirty(root, relative_path):
            raise SyncError(f"Local edit would be overwritten; review or commit it first: {relative_path}")
    else:
        previous_hash = old_published_hash(root, relative_path, manifest_relative)
        if previous_hash is None or sha256(current) != previous_hash:
            raise SyncError(f"Uncommitted or unexpected file occupies a managed path: {relative_path}")
    return "UPDATE"


def build_plan(
    root: Path,
    source: Path,
    manifest_relative: str,
    manifest: dict[str, Any],
) -> tuple[list[PlannedFile], list[str], list[str], list[str]]:
    previous_include = read_previous_include(root, manifest_relative)
    current_include = manifest["include"]
    removed = sorted(set(previous_include) - set(current_include))
    old_managed = set(previous_include)
    planned: list[PlannedFile] = []
    errors: list[str] = []
    total_bytes = 0

    source_branch_name = source_branch(source)
    expected_source_branch = manifest["expected_source_branch"]
    if source_branch_name != expected_source_branch:
        errors.append(
            f"Source branch is {source_branch_name!r}; manifest expects {expected_source_branch!r}."
        )
    source_remote = run_git(source, "config", "--get", "remote.origin.url", check=False)
    if source_remote.returncode != 0:
        errors.append("The source repository has no origin remote to verify against source_repository.")
    else:
        try:
            actual_source_repository = normalize_github_repository(source_remote.stdout.strip())
            if actual_source_repository != manifest["source_repository"].casefold():
                errors.append("The source origin does not match manifest source_repository.")
        except SyncError as error:
            errors.append(str(error))

    for relative_path in current_include:
        source_path = source / relative_path
        if source_path.is_symlink() or not source_path.is_file():
            errors.append(f"Allowlisted source file is missing or not regular: {relative_path}")
            continue
        size = source_path.stat().st_size
        total_bytes += size
        if size > MAX_FILE_BYTES:
            errors.append(f"Source file exceeds {MAX_FILE_BYTES} bytes: {relative_path}")
            continue
        try:
            source_bytes = source_path.read_bytes()
            source_text = source_bytes.decode("utf-8")
        except (OSError, UnicodeDecodeError) as error:
            errors.append(f"Source file is unreadable UTF-8 text: {relative_path} ({error})")
            continue
        try:
            check_sensitive_source(relative_path, source_text)
            public_text, redactions = redact_public_copy(source_text)
            check_public_text(relative_path, public_text)
            public_bytes = public_text.encode("utf-8")
            state, in_head = source_git_details(source, relative_path, source_bytes)
            action = target_path_action(
                root,
                relative_path,
                public_bytes,
                was_managed=relative_path in old_managed,
                manifest_relative=manifest_relative,
            )
        except SyncError as error:
            errors.append(str(error))
            continue
        planned.append(
            PlannedFile(
                path=relative_path,
                source_bytes=source_bytes,
                published_bytes=public_bytes,
                source_sha256=sha256(source_bytes),
                published_sha256=sha256(public_bytes),
                source_git_state=state,
                source_commit_contains_bytes=in_head,
                redactions=redactions,
                action=action,
            )
        )

    if total_bytes > MAX_TOTAL_BYTES:
        errors.append(f"Allowlisted sources total more than {MAX_TOTAL_BYTES} bytes.")
    for relative_path in removed:
        destination = root / relative_path
        if destination.is_symlink():
            errors.append(f"Managed deletion path is a symlink: {relative_path}")
        elif destination.exists() and not destination.is_file():
            errors.append(f"Managed deletion path is not a regular file: {relative_path}")
        elif destination.exists():
            tracked = run_git(root, "ls-files", "--error-unmatch", "--", relative_path, check=False)
            if tracked.returncode == 0 and target_is_dirty(root, relative_path):
                errors.append(f"Local edit prevents managed deletion: {relative_path}")
            elif tracked.returncode != 0:
                previous_hash = old_published_hash(root, relative_path, manifest_relative)
                if previous_hash is None or sha256(destination.read_bytes()) != previous_hash:
                    errors.append(f"Unexpected uncommitted file prevents managed deletion: {relative_path}")

    return planned, removed, errors, previous_include


def check_local_remote_refs(root: Path, branch: str) -> tuple[list[str], list[str]]:
    head = run_git(root, "rev-parse", "HEAD").stdout.strip()
    warnings: list[str] = []
    blockers: list[str] = []
    for ref in ("refs/remotes/origin/main", f"refs/remotes/origin/{branch}"):
        local_ref = run_git(root, "rev-parse", "--verify", ref, check=False)
        if local_ref.returncode != 0:
            warnings.append(f"remote-tracking ref {ref} is unavailable; sync will check the live remote")
            continue
        remote_sha = local_ref.stdout.strip()
        ancestor = run_git(root, "merge-base", "--is-ancestor", remote_sha, head, check=False)
        if ancestor.returncode != 0:
            blockers.append(f"{ref} is not integrated into the current branch")
    return warnings, blockers


def check_unmerged_paths(root: Path) -> None:
    result = run_git(root, "ls-files", "--unmerged")
    if result.stdout.strip():
        raise SyncError("The repository has unresolved Git conflicts; resolve them before syncing.")


def normalize_github_repository(value: str) -> str:
    if value.startswith("git@github.com:"):
        path = value[len("git@github.com:") :]
    else:
        parsed = urlsplit(value)
        if parsed.hostname != "github.com" or parsed.username or parsed.password:
            raise SyncError("origin must be a credential-free GitHub HTTPS or SSH URL.")
        path = parsed.path.lstrip("/")
    if path.endswith(".git"):
        path = path[:-4]
    return path.strip("/").casefold()


def verify_remote(root: Path, manifest: dict[str, Any], first_publish: bool) -> str:
    raw_remote = run_git(root, "config", "--get", "remote.origin.url", check=False)
    if raw_remote.returncode != 0:
        raise SyncError("The rosa-contexts origin remote is not configured.")
    if normalize_github_repository(raw_remote.stdout.strip()) != manifest["target_repository"].casefold():
        raise SyncError("origin does not match the manifest target_repository.")

    member = manifest["member"]
    branch = f"member/{member}"
    current_branch = run_git(root, "branch", "--show-current").stdout.strip()
    if current_branch != branch:
        raise SyncError(f"Current branch is {current_branch!r}; sync requires {branch!r}.")

    head = run_git(root, "rev-parse", "HEAD").stdout.strip()
    main_refspec = "refs/heads/main:refs/remotes/origin/main"
    fetched_main = run_git(root, "fetch", "--quiet", "--no-tags", "origin", main_refspec, check=False)
    if fetched_main.returncode != 0:
        raise SyncError("Could not fetch origin/main; no files were changed.")
    main_sha = run_git(root, "rev-parse", "refs/remotes/origin/main").stdout.strip()
    if run_git(root, "merge-base", "--is-ancestor", main_sha, head, check=False).returncode != 0:
        raise SyncError("The member branch does not include current origin/main; merge protocol updates first.")

    remote_listing = run_git(
        root,
        "ls-remote",
        "--heads",
        "origin",
        f"refs/heads/{branch}",
        check=False,
    )
    if remote_listing.returncode != 0:
        raise SyncError("Could not inspect the remote member branch; no files were changed.")
    if not remote_listing.stdout.strip():
        if not first_publish:
            raise SyncError(
                f"Remote {branch} is missing. Use --first-publish only for the initial publication."
            )
        return main_sha
    if first_publish:
        raise SyncError("--first-publish was set, but the remote member branch already exists.")

    member_refspec = f"refs/heads/{branch}:refs/remotes/origin/{branch}"
    fetched_member = run_git(root, "fetch", "--quiet", "--no-tags", "origin", member_refspec, check=False)
    if fetched_member.returncode != 0:
        raise SyncError("Could not fetch the remote member branch; no files were changed.")
    remote_member_sha = run_git(root, "rev-parse", f"refs/remotes/origin/{branch}").stdout.strip()
    if run_git(
        root,
        "merge-base",
        "--is-ancestor",
        remote_member_sha,
        head,
        check=False,
    ).returncode != 0:
        raise SyncError(
            f"Remote {branch} has commits not integrated locally; inspect and merge them first."
        )
    return main_sha


def manifest_for_sync(
    root: Path,
    source: Path,
    manifest: dict[str, Any],
    planned: list[PlannedFile],
    protocol_commit: str,
) -> dict[str, Any]:
    updated = dict(manifest)
    updated["source_branch"] = source_branch(source)
    updated["source_commit_sha"] = source_commit_sha(source)
    updated["synchronized_at_utc"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    updated["protocol_commit"] = protocol_commit
    updated["source_commit_note"] = (
        "source_commit_sha identifies Git HEAD only; per-file hashes and source_git_state "
        "show whether each published byte exists in that commit."
    )
    updated["files"] = [
        {
            "path": item.path,
            "source_sha256": item.source_sha256,
            "published_sha256": item.published_sha256,
            "source_git_state": item.source_git_state,
            "source_commit_contains_bytes": item.source_commit_contains_bytes,
            "redactions": item.redactions,
        }
        for item in planned
    ]
    return updated


def print_plan(
    planned: list[PlannedFile], removed: list[str], errors: list[str], preview: bool
) -> None:
    title = "PREVIEW (no files written)" if preview else "SYNC PLAN"
    print(title)
    for item in planned:
        print(f"{item.action:9} {item.path}")
        if any(item.redactions.values()):
            print(f"          redactions: {item.redactions}")
    for relative_path in removed:
        print(f"REMOVE    {relative_path}")
    if not planned:
        print("No source files passed validation.")
    if errors:
        for error in errors:
            print(f"BLOCKED   {error}")
    elif not removed:
        print("No deletions requested.")
    if removed:
        print("Deletions are allowed only after removing paths from the committed allowlist and passing --confirm-deletions.")
    if (
        preview
        and not errors
        and planned
        and all(item.source_git_state in {"ignored", "untracked"} for item in planned)
    ):
        print(
            "NOTE      All published files are untracked or ignored in the source repository; "
            "source_commit_sha does not identify them, and this branch may be their only version history."
        )
    print("Review the resulting Git diff before staging, committing, or pushing.")


def apply_plan(
    root: Path,
    source: Path,
    manifest_path: Path,
    manifest_relative: str,
    manifest: dict[str, Any],
    planned: list[PlannedFile],
    removed: list[str],
    protocol_commit: str,
) -> None:
    output_manifest = manifest_for_sync(root, source, manifest, planned, protocol_commit)
    manifest_bytes = (json.dumps(output_manifest, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    check_public_text(manifest_relative, manifest_bytes.decode("utf-8"))

    writes: list[tuple[Path, bytes]] = [
        (root / item.path, item.published_bytes) for item in planned if item.action in {"ADD", "UPDATE"}
    ]
    writes.append((manifest_path, manifest_bytes))
    temporary_paths: list[Path] = []
    try:
        for destination, data in writes:
            destination.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(
                mode="wb", prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent, delete=False
            ) as temporary:
                temporary.write(data)
                temporary.flush()
                os.fsync(temporary.fileno())
                temporary_paths.append(Path(temporary.name))
        for (destination, _), temporary_path in zip(writes, temporary_paths):
            os.replace(temporary_path, destination)
        for relative_path in removed:
            destination = root / relative_path
            if destination.exists():
                destination.unlink()
    finally:
        for temporary_path in temporary_paths:
            if temporary_path.exists():
                temporary_path.unlink()


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy a reviewed context allowlist into the current rosa-contexts member branch."
    )
    parser.add_argument("action", choices=("preview", "sync"))
    parser.add_argument("--source", required=True, type=Path, help="Authoritative local research repository.")
    parser.add_argument(
        "--manifest",
        default=".context-sync/manifest.json",
        help="Member branch manifest path (default: .context-sync/manifest.json).",
    )
    parser.add_argument(
        "--first-publish",
        action="store_true",
        help="Allow sync when this member branch has never been published; does not push.",
    )
    parser.add_argument(
        "--confirm-deletions",
        action="store_true",
        help="Allow deletion of previously managed files removed from the committed allowlist.",
    )
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    try:
        root = repository_root(Path.cwd())
        check_unmerged_paths(root)
        source = arguments.source.resolve()
        if not source.is_dir():
            raise SyncError("The --source directory does not exist.")
        manifest_relative = validate_manifest_path(arguments.manifest)
        manifest_path, manifest = read_manifest(root, manifest_relative)
        branch = f"member/{manifest['member']}"
        current_branch = run_git(root, "branch", "--show-current").stdout.strip()
        if current_branch != branch:
            raise SyncError(f"Current branch is {current_branch!r}; this manifest belongs to {branch!r}.")
        if manifest["target_repository"].casefold() != normalize_github_repository(
            run_git(root, "config", "--get", "remote.origin.url").stdout.strip()
        ):
            raise SyncError("origin does not match the manifest target_repository.")

        planned, removed, errors, _ = build_plan(root, source, manifest_relative, manifest)
        if removed and not arguments.confirm_deletions:
            errors.append("Allowlist removals need --confirm-deletions after preview and review.")

        if arguments.action == "preview":
            remote_warnings, remote_blockers = check_local_remote_refs(root, branch)
            errors.extend(f"BLOCKED: {item}" for item in remote_blockers)
            print_plan(planned, removed, errors, preview=True)
            for warning in remote_warnings:
                print(f"NOTE      {warning}")
            if not errors:
                print("Remote freshness is not checked by preview; sync fetches and validates live refs.")
            return 2 if errors else 0

        protocol_commit = verify_remote(root, manifest, arguments.first_publish)
        # Rebuild after fetching so the final operation uses the current source and manifest bytes.
        planned, removed, sync_errors, _ = build_plan(root, source, manifest_relative, manifest)
        if removed and not arguments.confirm_deletions:
            sync_errors.append("Allowlist removals need --confirm-deletions after preview and review.")
        errors.extend(sync_errors)
        print_plan(planned, removed, errors, preview=False)
        if errors:
            return 2
        apply_plan(
            root,
            source,
            manifest_path,
            manifest_relative,
            manifest,
            planned,
            removed,
            protocol_commit,
        )
        print("Local mirror updated. No files were staged, committed, or pushed.")
        return 0
    except (OSError, SyncError) as error:
        print(f"BLOCKED: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
