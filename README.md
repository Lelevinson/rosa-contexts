# ROSA research contexts

This public repository shares small, readable snapshots of each team member's authoritative ROSA research context. It helps assistants find active work, prior results and negative findings before proposing overlapping work. It is not a code repository, experiment database, or replacement for local research files.

## Branch model

- `main` owns this repository's shared operating protocol and onboarding material. It contains no member-specific research context.
- `member/<name>` contains one member's published context mirror and synchronization manifest. The member branch starts from `main`, so it also carries the shared files from its common history. New protocol commits do not change an existing member branch until that member merges them.
- A member's local research repository remains authoritative. The matching `member/<name>` branch is a public, one-way mirror. Members publish only their own branch.

There is no root `AGENTS.md` in this repository. Each member integrates the protocol into their own local AI instructions.

## Read a teammate context without switching branches

```bash
git clone https://github.com/Lelevinson/rosa-contexts.git
cd rosa-contexts
git fetch --prune origin
git branch --remotes --list 'origin/member/*'
git show origin/member/levinson:.context-sync/manifest.json
git show origin/member/levinson:research/START_HERE.md
git show origin/member/levinson:research/ACTIVE_STATE.md
git show origin/member/levinson:research/STUDY_INDEX.md
```

The manifest's `synchronized_at_utc` says when the snapshot was prepared. Its source commit is not proof that every included byte was committed there; inspect each file's hashes and `source_git_state`. Reports are evidence reported by their author until you check the linked source and original evidence. See [PROTOCOL.md](PROTOCOL.md) before using a teammate result to guide a research decision.

## Publish and onboard

Read [PROTOCOL.md](PROTOCOL.md) for reading, overlap checks, updates, deletion handling, privacy, and stale-branch recovery. Read [ONBOARDING.md](ONBOARDING.md) to create a member branch and the first snapshot.

The sync helper supports a preview and a local copy operation. It checks the allowlist, scans public text, verifies the target branch and current remote history, and never stages, commits, or pushes. A member reviews the resulting diff and publishes it manually.
