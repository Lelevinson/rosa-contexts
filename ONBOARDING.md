# Member onboarding

This workflow works with Codex, Claude Code, or another assistant that can run Git and Python. You do not need to reorganize your local ROSA research documents.

## 1. Clone and read the shared rules

```bash
git clone https://github.com/Lelevinson/rosa-contexts.git
cd rosa-contexts
git fetch --prune origin
```

Read `README.md`, `PROTOCOL.md`, and this guide. The repository is private and readable by invited collaborators only. Its contents are shared with every collaborator and their AI tools. Assistants use the member's own authenticated Git access. Anonymous clone is unavailable. Do not put private context in it.

## 2. Create your branch

Choose a short lowercase name, such as `martin` or `alex`:

```bash
git switch --create member/<name> --track origin/main
```

The branch starts with the shared docs and helper. Do not create a root `AGENTS.md`. Do not create or populate another member's branch.

## 3. Find your authoritative local context

In your ROSA research repository, read its local AI instructions and research entrypoint. Identify the files that best explain active work, previous decisions, results, negative findings, and how to navigate deeper studies. Keep your existing hierarchy. Exclude credentials, private paths/maps, raw traces, archives, code, and large or unrelated artifacts. Include only files that are safe to share with every collaborator and their AI tools.

## 4. Create a manifest allowlist

Copy the starter file and edit the member name, source repository, expected source branch, and exact repository-relative `include` paths:

```bash
mkdir -p .context-sync
cp templates/manifest.example.json .context-sync/manifest.json
```

The manifest is the allowlist. It also receives source commit, UTC time, protocol commit, per-file hashes, and source Git status when sync runs. A source commit SHA does not prove that ignored or uncommitted context files are included in that commit.

Paste the optional instruction block in [templates/AGENTS_SNIPPET.md](templates/AGENTS_SNIPPET.md) into your local AGENTS.md or CLAUDE.md. Do not create a root AGENTS.md in this repository.

Integrate this repository's workflow into your local AI instructions. Tell your assistant to inspect relevant teammate branches before substantial research, treat their conclusions as reported evidence, preserve your local source as authoritative, and publish only meaningful context updates.

## 5. Preview and publish your first snapshot

Make sure the current branch is `member/<name>`. Set `--source` to your local ROSA research checkout. Run:

```bash
python3 scripts/context_sync.py preview --source ../rosa-research
python3 scripts/context_sync.py sync --source ../rosa-research --first-publish
git diff --check
git diff --stat
git diff
```

The first command is a read-only preview. The second copies the approved files locally and records their provenance; `--first-publish` allows a missing remote member branch. The helper does not stage, commit, or push. Review every diff for research accuracy and suitability for sharing with every collaborator and their AI tools. The helper redacts local home paths and private IPv4 addresses, and blocks common token, private-key, credential-assignment, and email patterns; these checks can miss sensitive material.

When the diff is ready:

```bash
git add .context-sync/manifest.json research/
git diff --cached --check
git diff --cached
git commit -m "Publish initial ROSA research context"
git push --set-upstream origin member/<name>
```

Then verify the branch on GitHub or with `git fetch origin member/<name>` and `git log -1 origin/member/<name>`. The initial branch becomes visible to teammates only after the push succeeds.

## 6. Read other member branches

```bash
git fetch --prune origin
git branch --remotes --list 'origin/member/*'
git show origin/member/<teammate>:.context-sync/manifest.json
git show origin/member/<teammate>:research/START_HERE.md
git show origin/member/<teammate>:research/ACTIVE_STATE.md
git show origin/member/<teammate>:research/STUDY_INDEX.md
```

If a member uses other paths, read their entry point and follow its links with `git show origin/member/<teammate>:<path>`. These commands inspect remote files without changing your checked-out branch.

## 7. Maintain your context

After a meaningful finding, failure, decision, or active-status change, update your authoritative local documents first. Then:

```bash
git switch member/<name>
git fetch --prune origin
git merge --no-edit origin/main
python3 scripts/context_sync.py preview --source ../rosa-research
python3 scripts/context_sync.py sync --source ../rosa-research
git diff --check
git diff
```

Review the shared diff, then stage, commit, and push manually as in Step 5. The helper refuses an unexpected remote update or conflict. Inspect and merge the intended history; never force-push. To intentionally remove a file, remove it from the committed manifest allowlist, preview, and pass `--confirm-deletions` to sync. A missing source file that remains allowlisted is an error, not a deletion request.
