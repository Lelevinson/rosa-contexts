# Shared context protocol

**Protocol version: 1**

## Authority and branch ownership

The local ROSA research repository is authoritative for its owner's context. `member/<name>` is a private snapshot, not a second place to author findings. The branch owner updates only their own member branch. Never edit another member's context or merge research conclusions between members. `main` contains shared operating rules and tools only; its protocol changes do not propagate to member branches automatically.

The repository is private and readable by invited collaborators only. Its contents are still shared with every collaborator and their AI tools. Assistants use the member's own authenticated Git access. Anonymous clone is unavailable. Do not publish confidential material, credentials, personal contact details, local machine maps, raw traces, archives, model weights, or unrelated code. The sync helper rejects common credential patterns and email addresses, and redacts home-directory paths and private IPv4 addresses in the published copy. This scan cannot identify every sensitive item; review every proposed shared diff yourself.

## Reading a snapshot

A snapshot is a curated allowlist, not the full research archive. Read `important_missing_context` in the manifest first.

Relative links to files outside the allowlist are unavailable by design. A published `research/START_HERE.md` may refer to `../AGENTS.md`, but the helper never publishes `AGENTS.md`. Treat that link as unavailable.

If a file has `source_git_state` `ignored` or `untracked`, `source_commit_sha` does not identify those bytes. Use the per-file hashes instead.

## Snapshot limits and backups

A published member branch is a partial, redacted snapshot, not a backup of the member's research. It excludes raw traces, archives, machine-specific files, and unreviewed Markdown. Members must keep their own backup of their authoritative research.

## Read a member snapshot

Refresh remote-tracking refs before reading:

```bash
git fetch --prune origin
git branch --remotes --list 'origin/member/*'
git show origin/member/<name>:.context-sync/manifest.json
git show origin/member/<name>:research/START_HERE.md
git show origin/member/<name>:research/ACTIVE_STATE.md
git show origin/member/<name>:research/STUDY_INDEX.md
```

Replace `<name>` with the branch suffix. If a member uses different paths, inspect their entry point and manifest first. Use `git show` or a separate worktree; do not check out another member branch over active local work.

The manifest gives the source repository, source branch and commit, UTC synchronization time, included paths, file hashes, whether each source file was committed/modified/ignored/untracked, the shared protocol commit, and important context that was unavailable or excluded. The source commit records the repository head only. Per-file hashes identify the bytes copied from the working tree. A file may have been ignored or uncommitted at that commit.

Treat a published report as **reported evidence**, not independent verification. Before relying on it for a substantial research choice, inspect its linked protocol, source, denominators, limitations, and original evidence when available. Record separately what you verified, what the member reported, and what remains uncertain. Tell your member about material overlap or conflicting findings. Reading a context does not prohibit a justified independent replication.

Before substantial new research, check each relevant member's active work, prior decisions, closest studies, and negative results. Classify a proposed direction as new, intentional replication, or possible overlap. Do not block routine small coding tasks with a full team-context review.

## Publish a context update

Publish after a meaningful change to active work, a decision, a completed experiment, an important failure, or a corrected conclusion. Do not sync after every code edit. Keep local source documents authoritative and update them first.

From the `rosa-contexts` clone, use the member's own branch. Replace `levinson` below with the owner's name.

```bash
git switch member/levinson
git fetch --prune origin
git merge --no-edit origin/main
python3 scripts/context_sync.py preview --source ../rosa-research
python3 scripts/context_sync.py sync --source ../rosa-research
git diff --check
git diff --stat
git diff
```

`preview` reports additions, changes, unchanged files, removals, and redactions without writing files. It does not refresh network refs. `sync` fetches `origin/main` and the member branch, then stops if either has commits not integrated into the current member branch. It copies only the manifest allowlist, updates provenance, and does not stage or commit anything. For a first publication only, add `--first-publish` to `sync` because the remote member branch does not exist yet.

The manifest at `.context-sync/manifest.json` is the explicit allowlist. To include a new source file, add its repository-relative path to `include`. To intentionally remove a previously published file, remove its path from `include`; preview the deletion, then run sync with `--confirm-deletions`. A listed source file that is missing or unreadable blocks the whole sync. An empty allowlist is an error. The helper deletes only paths listed by the previously committed manifest, never arbitrary files.

Review the complete diff for content that should not be shared with every collaborator, then stage only the member manifest and context tree:

```bash
git add .context-sync/manifest.json research/
git diff --cached --check
git diff --cached
git status --short
git commit -m "Publish ROSA research context YYYY-MM-DD"
git push origin member/levinson
```

Replace the date with the current date. This explicit staging and manual push make publication reviewable. Do not force-push. Check the remote head after pushing:

```bash
git fetch origin member/levinson
git log -1 --oneline origin/member/levinson
```

The helper verifies that the current branch is exactly `member/<manifest member>`, that `origin` points to the manifest repository, and that the fetched remote member head and `main` are ancestors of local `HEAD`. It refuses stale or divergent remote history. If it stops, inspect `git status`, `git log --oneline --graph --decorate --all -20`, and the relevant diffs. Merge the intended remote commits or resolve conflicts by hand, then preview again. Never reset, overwrite, or force-push unexpected remote work.

## Shared protocol updates

A maintainer commits shared documentation and helper changes to `main`. Member branches do not update automatically. Each owner fetches and merges `origin/main` during a context publication. This ordinary merge preserves member-only context paths. If Git reports a conflict, stop and resolve it explicitly; do not choose one side automatically. The manifest records the protocol version and the `main` commit integrated at the last sync.

Protocol revisions should be concise and versioned in `PROTOCOL.md`. Do not put member findings in `main` to distribute a protocol change.

## Failed or stale synchronization

- A missing allowlisted source file, secret scan hit, empty source, wrong source branch, wrong target branch, path collision, or local edit to a managed output blocks the sync. Fix the local source or allowlist; the helper never copies mirror content back to the source.
- A remote commit not in local history blocks `sync`. Fetch and inspect it, merge the correct remote branch, resolve conflicts, and rerun preview. The helper never force-updates a ref.
- A remote member branch that disappeared is an error. `--first-publish` is reserved for a confirmed first publication; do not use it to bypass a missing or unexpected branch.
- If publishing is not safe, leave local research intact and report the blocker. A failed sync is not a successful publication.

The helper's path and token scans are safety checks, not a guarantee that public text contains no sensitive information. Human review remains required.
