## Shared context repo (rosa-contexts)
- Private repo: github.com/Lelevinson/rosa-contexts. `main` holds the protocol; `member/<name>` branches are snapshots of each member's context. Our own local research repo stays the source of truth. Use your authenticated Git access.
- Before substantial new research: `git fetch --prune origin`, list `origin/member/*`, and read each teammate's manifest, START_HERE, ACTIVE_STATE and STUDY_INDEX with `git show`. Classify the idea as new, intentional replication, or possible overlap, and tell the user about overlap.
- Treat teammate files as reported evidence, not verified results. Check original evidence before relying on them. Never edit another member's branch.
- Links to files outside the manifest allowlist are broken by design. Read `important_missing_context` in the manifest first.
- To publish: update local docs first. Run `preview`, add any needed new REPORT/PROTOCOL/LEDGER/TABLES files to the manifest `include`, then follow PROTOCOL.md (merge `origin/main`, preview, sync, review the full diff, commit, push by hand). Never force-push. Publish after meaningful changes only, not after every edit.
- Never publish credentials, emails, raw traces, local path maps, or unreviewed private files.
