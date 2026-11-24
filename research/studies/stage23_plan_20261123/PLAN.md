# Stage 2 and Stage 3 plan (2026-11-23, late evening, Asia/Taipei)

Written by Claude Code (Sonnet 5.5). **Planning plus one small tested helper. No Stage 1 file, run, held-out file or custodian file was opened or changed.** No model episode was run. Hour figures are my estimates, not measurements. Sources: [ACTIVE_STATE](../../ACTIVE_STATE.md), [lab launch record](../final_exam_draft_20261118/LAB_LAUNCH_RECORD_20261123.md), [Stage 2 wiring report](../stage2_prep_20261121/REPORT.md), [action readiness report](../action_readiness_20261121/REPORT.md), [protocol draft](../final_exam_draft_20261118/PROTOCOL_DRAFT.md), [RUNBOOK](../final_exam_draft_20261118/RUNBOOK.md).

## 0. Decision record (research context sections 12.2 and 14.2, short form)
- **Observed opportunity:** none to claim. Stage 2 and 3 are not a new idea; they test, on acting tasks, the same three systems (M, E1, S0) that Stage 1 tests on questions. Dev evidence for actions is class B (no effect, 128 episodes, [report](../action_dev_switch_20261118/REPORT.md)). Expect a possible null result and report it.
- **Candidate versus control:** XM, XE1 and XS0 all get the identical typed action tool and pose read tool; only the system's own loop and menu differ (unit-tested, [wiring report](../stage2_prep_20261121/REPORT.md) section 2).
- **Closest prior failure:** the dev switch study (action_dev_switch_20261118) and the judge unwrap defect (0 of 126 wrapped structured answers scored).
- **Smallest decision-changing next action:** run Stage 2 once under a frozen protocol; stop rule is the hard stop on 30 Nov 18:00.
- **Status of prerequisites:** Stage 2 = *wired, not held-out-ready* (custodian interface missing, 14-task feasibility "pending" per the custodian's own record). **Stage 3 = `BLOCKED / NOT YET JUSTIFIED` for major implementation** until the owner confirms it should be built in parallel and Codex confirms the 10-task Nav2 design is feasible model-free. This plan does not start it.

## 1. What exists and what is missing

| Piece | Status (evidence) | Missing | Est. hours |
|---|---|---|---:|
| Guarded action tool, turtlesim | Done as workbench: S1 executor 19 fake-robot tests, S2 turtlesim backend 7 real-turtlesim tests, 128-episode dev study | nothing for turtlesim | 0 |
| Same tool on all systems (XM, XS0, XE1) | Done as code: 10 tests, 6/6 dev smoke through the queue launcher ([report](../stage2_prep_20261121/REPORT.md)) | one episode per cell only; not a comparison | 0 |
| Runner | `exam_actions_20261121/run_actions.py`: dev tasks only | parameterised episode taking request, fixture and truth from the custodian bridge (needs custodian items 1-3 below) | 4-6 mine, plus Codex's side (unknown to me) |
| Held-out turtlesim pool (14) | exists as a protected design (custodian record; I did not open it) | model-free feasibility on the deployment; loader; placement check | 2-4 (Codex) |
| Judge | v1.2 plus `judge_exam.py` wrapper (six answer forms agree, 116 each). Ordered events and read-before-dispatch implemented in `judge_v1_2.verify_sequence`. Not frozen, no hash | freeze with hash; held-out step contracts are custodian-owned | 3-4 |
| "Claims arrival but did not arrive" counter | **Not built.** The wiring report says it is not in the row yet | count a row where the final answer asserts success while the independent final state is outside tolerance; plus the "agent-caused unresolved motion" class; unit tests on dev traces | 2-3 |
| Final-fixture-check fix | **Built and tested tonight** (section 2) | wire into runner | 1-2 |
| Stage 2 protocol | draft text only (PROTOCOL_DRAFT sections 3-5) | hypothesis, controls, metrics, cells, stop rule, hashes, frozen before first request | 3-4 |
| Stage 3 backend (Nav2 navigate-to-pose with lifecycle/TF readiness and cancel) | **missing**; only a smoke script and a lab goal check exist | build and test against real Gazebo/Nav2 | 8-12 |
| Stage 3 fixture reset and independent pose oracle | missing | 6-10 |
| Stage 3 judge and step contracts, runner, queue adapter | missing | 8-12 |
| Stage 3 model-free feasibility on the lab | pending; lab headless timing item still open | 3-6 |
| Stage 3 protocol | missing | 3-4 |

**Totals (estimates):** Stage 2 about **13-20 h**; Stage 3 about **28-44 h** more. Stage 3 by Thursday needs two people or agents building in parallel, and every Stage 3 hour depends on Codex confirming the pool. If Stage 3 is not frozen by Wednesday night it is reported as **incomplete, never silently dropped** (protocol draft).

**What the custodian must add (from the wiring report, section 4, interface only):** an opaque-id task source inside custody; fixture reset, stable-state check and independent observation; an event feed for goal receipts; the judge on the custody path with the answer-form normalisation; row fields for goals sent and ending classes; the three systems in the bridge list; held-out tolerances.

## 2. Lesson from Stage 1: the final fixture check and short-lived ROS CLI nodes

**Mechanism (verified in isolation tonight; not verified to be the cause of the 54 of 59 laptop failures, which I did not look at):** every `ros2` command creates a helper node named `/_ros2cli_<pid>`. While a command is alive, `ros2 topic info --verbose` lists it as an extra PUBLISHER or SUBSCRIPTION, and `ros2 node list --all` lists it. A check that compares endpoints with an exact expected set fails if one is still shutting down. More tool calls leave more of them, which matches your observation that E1 is hit more. The Codex review of 2026-11-22 recorded one public case with the same signature.

**Design for Stage 2 and Stage 3** ([graph_settle.py](graph_settle.py), new file, nothing frozen is imported):
1. **Wait:** poll `ros2 node list --all --no-daemon` until no transient CLI node is visible, up to 30 s, requiring **two clean listings in a row**.
2. **Ignore and record:** after the wait, `compare_endpoints` drops only names matching the CLI pattern (`_ros2cli_<id>`, `_ros2cli_daemon_...`) and **returns the dropped names**. A fixture node, or any real extra node, is never dropped. The row must store `settled`, `waited_s` and the names seen, so a timeout is data and not an error.
3. A hung CLI process that never exits yields `settled=False`; the check then still runs. That keeps a real fault visible.

**Tests (6, all pass, 3 consecutive runs; `research/studies/stage23_plan_20261123/tests`):** pattern separates CLI from fixture names (including `/my_ros2cli_tool`); a real extra node is still reported; wait returns when the node disappears; wait reports a timeout; the listing command's own node is not counted; and one **real ROS test** in isolated domain 231 (Stage 1 uses 220; `--no-daemon`, localhost only): a live `ros2 topic echo` appears as a SUBSCRIPTION, the wait returns settled after it ends, and nothing is left.

**Two findings the tests produced (both would have broken a naive version):**
- `ros2 node list --all` **sees its own helper node**, so a naive wait never settles. The listing command's own pid is now excluded.
- A single short discovery spin on the busy laptop sometimes listed **no** nodes at all (even the fixture). One clean listing is therefore not proof; hence the two-in-a-row rule and a 4 s spin. The same discovery miss could produce a false "node not listed" in any fixture check; Stage 2/3 should apply the same retry rule to that check.

**Not done:** wiring into `run_actions.py` (1-2 h, once the runner is parameterised); testing against Gazebo/Nav2 (many more nodes); checking that this explains the Stage 1 failures (needs trace-level reads, which are custodian-only).

## 3. Per-episode time (not measured, by your instruction)
No episode was run. Do this only after laptop Stage 1 tier 1 finishes. At 87 s per cell and 649 cells left at 22:53, that is about **Tuesday 24 Nov 14:30** (estimate).
**Warning that changes the instruction:** a dev episode loads a model on the laptop GPU. The queue treats any other process using at least 1 GiB as contention, re-runs the affected Stage 1 cell, and each re-run counts toward the 3-try quarantine. So the timing episodes should run while the laptop queue is **paused with STOP at a tier boundary**, then resume. Needs your OK. On the lab the same rule applies: no model episode while lab Stage 1 runs. Model-free checks (task feasibility, Nav2 goal check) use no GPU, but headless Gazebo is CPU-heavy and could slow Stage 1 cells; I would run them on the lab only in a gap or after the lab pause.
Prior numbers, for planning only: Stage 1 lab about 40 s per cell (smallest model only), laptop about 87 s; dress rehearsal 2.6 min per cell with stand-in overhead. A turtlesim cell adds a simulator reset and stable check (a few seconds) and at most about 5 requests. My **unmeasured guess**: Stage 2 about 1-2 min per cell on the lab and 2-3 min on the laptop; Stage 3 about 3-6 min per cell (Gazebo reset, navigation 7-35 s of simulated time).

## 4. Cell counts

Systems = 3 (XM, XE1, XS0). F is not included: it cannot act without an adapter.

| Plan | Stage 2 | Stage 3 | Cells | Est. time |
|---|---|---|---:|---|
| **Lab (proposed)** | 14 tasks x 3 systems x 4 models x **2 seeds** = 336 | 10 x 3 x 4 x **2 seeds** = 240 | **576** | Stage 2 about 6-11 h, Stage 3 about 12-24 h; total about 18-35 h |
| **Laptop backup (pre-written)** | 14 x 3 x 4 x **1 seed** = 168 | 10 x 3 x 4 x 1 = 120 | **288** | Stage 2 about 6-8 h, Stage 3 about 6-12 h, plus about 15% fixture overhead: about 14-24 h, **about 1 day** |
| Laptop fallback if too slow | same, but 2 models (qwen3.5:9b, gpt-oss:20b) | same | 144 | about 7-12 h |

All time figures are guesses until section 3 is done. The model subset for the fallback is a choice for you; I made it only so the fallback is concrete. Lab and laptop remain separate strata, never pooled. The cell order should follow the queue rules (complete pairs, seeds first) so any stop leaves usable data. Ten Stage 3 tasks give a wide interval, so Stage 3 is descriptive only (as the draft says).
**Owner decision needed:** the laptop is still running the full Stage 1 queue. A laptop backup of Stage 2/3 needs the laptop paused after its tier 2 (or tier 1), otherwise two GPU jobs collide.

## 5. Can lab Stage 1 be paused with STOP after tier 2 and resumed under the same frozen verifier?
**From the code and earlier tests: yes, with two caveats. Not tested live on the lab (I did not touch it).**
- `touch research/_artifacts/exam/RUN/STOP` makes the runner finish the current episode and exit (`make_dispatcher` checks the file before each episode, raises `StopRequested`). Resume = remove STOP and run the same start command; finished cells are skipped, orphans are killed, the interrupted cell is re-run. Dummy kill-and-resume and the real-path mini exam passed on the laptop (RUNBOOK section 12).
- **Same verifier:** the lab launch ran `verify_freeze_rev2.py` before starting (exit 0). Resuming works if no frozen file changes. Stage 2/3 code must stay in new files and register systems at run time (as `run_actions_queue.py` already does), never edit `systems.py` or `queue_core.py`.
- **Caveat 1, no automatic "stop after tier 2":** the code has no such flag. Someone (or a small watcher) must read the tier counts and touch STOP. Blocks never cross tiers, but a STOP touched only after tier 2 reads 100% may let one tier-3 episode start. That is harmless and resumable, but it would be a tier-3 row recorded earlier than planned. A watcher that touches STOP when tier 2 has 0 cells left in its last block is cleaner; I have not written it.
- **Caveat 2, relaunch command:** I did not open `ops/launch.sh` and cannot say whether running `start` again on the same run name is accepted or refuses. Verify on the lab with a dummy run, or rely on the plain queue command.
- Also check: Stage 1's lab Ollama and container stay up while paused; the `--init` zombie warning for turtlesim; and that Stage 2 runs under a **different run name** with its own freeze.

## 6. Day-by-day plan to 2 December (proposal)

| Day | Plan |
|---|---|
| **Mon 23 (tonight)** | Done: this plan, settle helper and tests. Do not touch either run. |
| **Tue 24** | Build with Codex: custodian bridge items 1-6; claim-arrival counter; judge freeze candidate; wire the settle check; Stage 2 protocol draft. Laptop tier 1 should finish about 14:30 (estimate). Evening: your decision on pausing the laptop for the 1-2 public dev timing episodes (section 3). |
| **Wed 25** | Stage 2 model-free feasibility (Codex); freeze Stage 2 protocol and hashes in the evening. Stage 3: only if you say go, Nav2 backend, reset and pose oracle on the lab (CPU load caveat). Decide at 18:00 whether Stage 3 is frozen or reported incomplete. Pause the lab queue after tier 2 (if tier 2 is done by then) or decide to drop the pause. |
| **Thu 26** | Lab: Stage 2 (336 cells). Laptop: backup Stage 2 in parallel only if its queue is paused. Check status counts only. |
| **Fri 27** | Lab: Stage 3 (240 cells) if frozen. Re-run only infrastructure failures, not task failures; report both. |
| **Sat 28** | Buffer for failed cells and quarantines. Resume lab Stage 1 tier 3 if tier 2 was the pause point. |
| **Sun 29** | Stage 1 tiers continue; frozen analysis gate for tier 1. Stage 2 analysis after its run is COMPLETE. |
| **Mon 30** | Hard stop of all runs at 18:00 (RUNBOOK). |
| **Tue 1 Dec** | Tables, report, slides; negative and null results included; the live Gazebo demo is rehearsed and kept separate from evidence. |
| **Wed 2 Dec** | Presentation. |

## 7. Limits
- I read no log, row, trace, status file, spec or custodian path. The laptop `status_stage1.py` printed "no status file yet" from this worktree (custody path not resolved here), so I used only the counts in your message and the launch record. I did not verify the 54 of 59 figure.
- Hour and time figures are estimates. The 14-task and 10-task pools are known to me only through the custodian's reports.
- The settle helper is tested against a stand-in fixture, not Gazebo/Nav2 and not the real Stage 1 oracle.
- The real-ROS test ran on the laptop in domain 231 while Stage 1 was running; it created no GPU load, but it did use a little CPU for about 35 s per run (4 runs plus debugging). I used `--no-daemon`, so no discovery daemon was started or stopped.

## Open search (unfiltered)
- `ros2 topic pub` has no `--no-daemon` flag and is itself a `_ros2cli_` node, so a "fixture" built from it looks like a transient CLI node.
- ROS domain ids above 232 are invalid on this machine (my first test used 241 and failed).
- ROS's pytest plugin breaks `uv run pytest` here (missing `lark`); the tests need `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` and system Python.
- The exam spec template puts F in the Nav2 tier 2b; F cannot act, so the Stage 2/3 spec needs its own system list.
- The laptop run will take far longer than the 1-day backup window if it keeps running all tiers (at 87 s per cell, 7,752 cells is about 187 h). The "laptop runs everything" rule conflicts with a laptop Stage 2/3 backup.
- Unexplained from the handoff: the laptop heartbeat gap at 20:42 and the 103 s GPU sampler gap; `notify.py test` bug.
- Lab status does not expose per-system infrastructure counts, so the Stage 1 infra share on the lab cannot be seen until the analysis gate.

## 8. Stage 2 custodian interface (proposal for Codex, 2026-11-24; replaces the older list in the wiring report section 4)
The runner is now parameterised. Codex supplies **one Python file in custody**, named by `ROSA_ACTION_BRIDGE_FILE` (the runner refuses to start without a valid file when the variable is set, and never falls back to the dev tasks). Contract, from [action_bridge.py](../exam_actions_20261121/action_bridge.py):
- `request_text(task_id) -> str`: the request for the opaque id (the pool itself still comes through the queue's `tasks_file_env`).
- `judge(task_id, answer, true_state, *, ending, trace) -> dict(success, reasons, claim_audit, judge_version)`: `true_state` = `dict(heading, x, y, still)` read by the runner's independent node; `trace` = the dev-format trace (executor receipts and parameter reads in order, `action_trace.dev_trace`). Inside, Codex can call `judge_stage2.judge(..., contract=ArrivalContract(...))` and add the ordered-step and read-before-dispatch contracts of v1.2 (`judge_v1_2.Step`, `judge_contract`).
- optional `start_state_ok(state) -> bool` (default: still and heading within 0.05 of 0).
What the runner now does without custodian help: fresh simulator per episode; graph check before and after (class (a) / (c)); independent state read; `claimed_but_not_arrived` audit; class (b) unresolved motion; extra ending classes `unscored` and `unresolved_motion` patched into the queue at run time.
**Still needed from Codex:** the bridge file; the task contracts and tolerances; model-free feasibility; for held-out tasks whose truth is not a heading (position, refusal), the `ArrivalContract(None)` or an extended contract; confirm that read events for the held-out read sources use the `ros2_param_get` tool the stock and M arms already expose. Open question for Codex: do any held-out tasks need a true-state field other than heading, x, y, still?

**Update 2026-11-24 (custody bridge delivered).** Codex's bridge is a context-manager contract, not the callback contract above. Section 8's callback list is superseded: the runner (`run_actions.episode_custody`, `action_bridge.load_bridge`) opens `episode(task_id, seed, ros_dir)` before any model, uses `active.request` and `active.backend`, builds one `recorder(path, active)` for the model, guard, kit and tool callbacks, calls `judge(active, answer, executor, requests_started, evidence_path=...)` inside the context, and keeps trace and evidence under `ROSA_ACTION_CUSTODY_DIR` (mode 0700). The queue folder receives only `custody_result.json` (opaque fields). Bridge ending classes map to queue endings: `pre_start_fixture_failure` -> infrastructure (retry), `post_start_oracle_loss` -> `unscored`, `agent_unresolved_motion` -> `unresolved_motion`. Tested on a synthetic bridge only.
