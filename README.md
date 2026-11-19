# ROSA research contexts

This private repository is readable by invited collaborators only. Its contents are shared with every collaborator and their AI tools. Assistants use each member's own authenticated Git access. Anonymous clone is unavailable.

It shares small, readable snapshots of each team member's authoritative ROSA research context. It helps assistants find active work, prior results and negative findings before proposing overlapping work. It is not a code repository, experiment database, or replacement for local research files.

## Branch model

- `main` owns this repository's shared operating protocol and onboarding material. It contains no member-specific research context.
- `member/<name>` contains one member's published context mirror and synchronization manifest. The member branch starts from `main`, so it also carries the shared files from its common history. New protocol commits do not change an existing member branch until that member merges them.
- A member's local research repository remains authoritative. The matching `member/<name>` branch is a private, one-way mirror. Members publish only their own branch.

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

## Reading a snapshot

A snapshot is a curated allowlist, not the full research archive. Read `important_missing_context` in the manifest first.

Relative links to files outside the allowlist are unavailable by design. `research/START_HERE.md` may refer to `../AGENTS.md`, but the helper never publishes `AGENTS.md`. Treat that link as unavailable.

If a file has `source_git_state` `ignored` or `untracked`, `source_commit_sha` does not identify those bytes. Use the per-file hashes instead.

## Publish and onboard

Read [PROTOCOL.md](PROTOCOL.md) for reading, overlap checks, updates, deletion handling, privacy, and stale-branch recovery. Read [ONBOARDING.md](ONBOARDING.md) to create a member branch and the first snapshot.

The sync helper supports a preview and a local copy operation. It checks the allowlist, scans public text, verifies the target branch and current remote history, and never stages, commits, or pushes. A member reviews the resulting diff and publishes it manually.

## Questions for teammates

Please see the [test design open questions](research/decisions/2026-11-17-test-design-open-questions.md) for model selection, Nav2 pool, comparisons, temperature, rounds and time budget.

**Status, 2026-11-19.** The [Round 2 development report](research/studies/build_round2_20261116/REPORT.md), [exam draft](research/studies/final_exam_draft_20261118/PROTOCOL_DRAFT.md), and [lab setup checklist](research/studies/final_exam_draft_20261118/LAB_SETUP_CHECKLIST.md) are available. The exam protocol is still a draft.
