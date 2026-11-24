# Martin's branches — review, 2026-11-21

I fetched `Lelevinson/rosa-research` in an isolated Git clone and reviewed each Martin tip in a separate detached worktree outside our checkout. I checked all current remote heads for Martin's authorship, including commits unique to the other heads. Four branches matched. Companion `rosa-evaluation` branches are cited as evidence for those four. They are a separate repository. The team context at `rosa-contexts` listed only Levinson and krln member heads. Krln matched its `main`; Martin's UR5e comparison and turtlesim merge plan were in the research and evaluation branches.

Git gives the branch facts below. Goals and rule checks come from the cited code and documents. Fit, effort and verdict are **inferences**. An effort is engineering time and excludes live model runs.

| Branch | Goal | Exam stage | Rules check | Fit with M | Merge effort | Verdict |
|---|---|---|---|---|---|---|
| [member/martin](martin.md) | Put routine read, write and verify steps in a skill | Stage 2 idea, UR5e demo | Training-free with guarded registered writes. Fixed targets and inspection maps need their own deployment scope. | Overlaps in short menu, text feedback and structured finish. Different schema, loop and write transport. | 12–15 h for a narrow port | needs change |
| [member/martin-gazebo](martin-gazebo.md) | Compare skill modes on a Gazebo UR5e | Demo only | Both modes use fixed arm skills. Keep equal permissions in any comparison. | Pointer only here. Companion runner calls Martin's macro loop and arm transport. | 0–1 h to reference. Nav2 build unestimated. | demo only |
| [member/martin-parity](martin-parity.md) | Check structured tool transport on specific models | Stage 1 infrastructure, possibly reusable later | Training-free. No new rights. Share any chosen profile across arms. | No tool change here. Later adapter changes wire prompts and model options outside M. | 4–6 h if a relevant failure is reproduced | needs change |
| [member/martin-merge](martin-merge.md) | Propose a typed turtlesim bundle in M | Stage 2 dev | Model supplies the heading. Keep equal rights and the existing guards. | Conceptually compatible as a tool replacement. Plan only, pending a dev opportunity check and trace validation. | 12–15 h if the gates clear | merge-candidate |

## Three decisions for the owner

1. **Scope.** Decide whether to keep Martin's UR5e study as a separate demo and allow an offline sizing check for a separate Stage 2 dev comparison. The published plan and the existing evidence provide no basis to change the frozen M components.
2. **Allowed action and control.** If sizing is authorized, use a parameterized heading and allow repeated calls within the shared goal budget. Use XM with its existing pose receipt enabled as the decisive control. This tests whether the bundle adds anything beyond returning the pose after the existing guarded action.
3. **Judge and transport.** Require the independent judge to accept a scripted trace with real read and dispatch order before any live comparison. Decide model transport separately, by model, with one shared setting across arms. Treat Martin's parity gates as evidence about his tool surface.

Only a merged live development comparison can tell whether small models call the new tool correctly, finish more reliably, or reduce requests and tokens after counting the bundle's native work. A separate live Nav2 check would be needed for navigation. This review used source, saved reports, aggregate gate files and CPU tests.

## CPU test record

**Verified by his tests.** On Python 3.12.3 in a separate uv environment from Martin's `uv.lock`, each of `member/martin`, `member/martin-gazebo` and `member/martin-parity` ran 107 top-level unittest cases. Each returned **106 passed, 1 skipped**. The skip was an opt-in Windows protected-storage integration test. Source files were imported directly from each pinned worktree. The pass used local loopback for OAuth and async fixtures, with non-loopback bind/connect blocked. The first restricted pass blocked local sockets and stalled async fixtures. A bounded intermediate run excluding two stalled cases showed three local-socket errors. Both async cases and the three socket cases passed in the loopback rerun.

**Verified by his tests.** The plan branch adds no Martin test or runtime. Its inherited baseline test discovery returned **43 passed, 80 errors** out of 123 in the ROS-free Python environment. Missing ROS packages and unregistered ROS 1/2 modules accounted for most errors. This does not evaluate any merged implementation. Four companion Gazebo runner tests that cover dev resume, budget, deadline and reset passed. These results are fixture checks. No model, simulator or robot execution was started.

**Review integrity.** The first companion Gazebo test command was too broad. It automatically read Martin's tracked held-out case and schedule fixtures before I identified that dependency. The command output showed unit-test names and results, and I did not inspect, quote, or use the fixture contents in any conclusion. I excluded that invocation from the evidence above and reran only the four checked dev-safe tests. No private custodian files were opened. The original worktree's Git index lock was absent at the start. No branch was pushed.
