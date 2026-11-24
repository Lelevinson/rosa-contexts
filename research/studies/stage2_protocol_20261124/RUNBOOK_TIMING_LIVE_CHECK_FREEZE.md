# Stage 2 runbook: timing episodes, live check, freeze (prepared 2026-11-24, CPU-only; nothing here has been run)

Written for the person at the keyboard (owner, or Claude Code on the owner's word). Read with the [protocol draft](PROTOCOL_STAGE2_DRAFT.md). All commands run from the repository root. A command line `A=b cmd` sets the variable `A` for that one command; `uv run --with pytest` borrows pytest for one run; `tmux attach -t NAME` looks at a detached run and `Ctrl-b d` leaves it.

## 0. Preconditions (the launcher checks most of them and refuses with a message)
- The laptop is released by the owner and **no Stage 1 runner is alive on this machine** (STOP file, wait for the runner to exit). `stage2_env.py` refuses otherwise. On the lab the same, after Stage 1 is paused.
- Ollama up with the four core models. Disk above 30 GB. One GPU job at a time.
- ROS domain: the launcher uses **220** (`ROSA_STAGE2_ROS_DOMAIN` can change it; **219 is refused**: it belongs to the Stage 1 custody runs), localhost only, a private `ROS_HOME` and `ROS_LOG_DIR` inside the custody directory.
- Code is committed: `python3 research/studies/exam_actions_20261121/freeze_stage2.py write` then `verify` print `VERIFIED` (candidate manifest).

## 1. Timing episodes (PUBLIC dev action tasks, dev bridge, no custody file)
Design: 3 public dev tasks (S3 out-of-range heading, R1 act-then-read, M1 two-step) x 4 models x 3 systems x seed 1 = **36 cells**, expected about 1-2 hours on the laptop (a guess; the point is to measure it).
```
python3 research/studies/exam_actions_20261121/stage2_spec.py timing --out research/studies/exam_actions_20261121/specs/timing_spec_stage2.json   # already generated
bash research/studies/exam_actions_20261121/start_stage2.sh timing s2time_laptop_01 research/studies/exam_actions_20261121/specs/timing_spec_stage2.json laptop
```
Look at counts only (`python3 research/studies/final_exam_draft_20261118/exam_queue/queue_core.py status --run-name s2time_laptop_01 --machine laptop`). When it ends:
```
python3 research/studies/exam_actions_20261121/timing_report.py --run-name s2time_laptop_01 --machine laptop --hours-available 36 --out research/studies/exam_actions_20261121/TIMING_RECORD_laptop.json
```
It prints seconds per cell by system x model (infrastructure and contended rows excluded and counted), the projected hours of the exam design for 1, 2 and 3 seeds, and which seed count fits the time with a 20% margin. **Read it as laptop time on public tasks**: the lab factor is an assumption unless the same 36 cells are run on the lab (preferred: run them there once it is free), and held-out tasks may be longer. The seed count is the owner's decision; the report only recommends.

## 2. Live check (two public tasks in custody format)
The public bridge comes with a bank and planner index for a successful rotation and a rotation the fixture cancels after acceptance. The runner refuses the held-out bridge in this mode by checking its hash against the candidate manifest.
```
export ROSA_ACTION_BRIDGE_FILE=<custody>/<public bridge>.py
export ROSA_ACTION_CUSTODY_DIR=<custody>/s2check_run       # must exist, mode 0700
export ROSA_STAGE2_TASKS_FILE=<custody>/<public index>.json
python3 research/studies/exam_actions_20261121/stage2_spec.py live_check --model qwen3.5:9b --out research/studies/exam_actions_20261121/specs/live_check_spec_stage2.json
bash research/studies/exam_actions_20261121/start_stage2.sh live_check s2check_laptop_01 research/studies/exam_actions_20261121/specs/live_check_spec_stage2.json laptop
```
Six episodes cover two tasks, XM, XE1 and XS0, qwen3.5:9b, and seed 1. Record counts and classes for each pass criterion.
1. 6 of 6 cells have a row; no `pre_start_fixture_failure` after a retry; no queue crash; no leftover `turtlesim_node` or discovery daemon afterwards.
2. In each custody episode folder: `trace.jsonl` and `evidence.json` exist (evidence mode 0600, folder 0700); the queue folder holds only `custody_result.json` and the worker log.
3. `custody_result.json` ending classes are in the expected set (`scored`, or an explainable `agent_unresolved_motion` / `post_start_oracle_loss`); `goals_sent` is consistent with the typed tool being called; the model request count is at least 1.
4. The judge ran inside the context: `evidence.json` contains the final pose (custody's own check; the runner never reads it).
5. The same three systems' tool schemas were identical (already unit-tested; no new check).
6. Seconds per cell recorded for the real bridge, which is the number that matters for timing.
7. All three cancellation cells have one dispatched goal with a native `CANCELED` receipt and a supported-complete report confirmed by the independent final pose. Record the count for each system.

Write the result in plain text to `research/studies/stage2_protocol_20261124/LIVE_CHECK_RECORD.md` (counts, ending classes, pass or fail per criterion, any anomaly). A fail stops the freeze.

## 3. Freeze (minutes, after sections 1 and 2 and the owner's approval of the protocol)
1. Owner decides the seed count from the timing record (1, 2 or 3) and approves `PROTOCOL_STAGE2_DRAFT.md`.
2. Generate the exam spec: `python3 research/studies/exam_actions_20261121/stage2_spec.py exam --seeds N --out research/studies/exam_actions_20261121/specs/exam_spec_stage2.json`.
3. Commit everything (the freeze refuses uncommitted listed files).
4. `python3 research/studies/exam_actions_20261121/freeze_stage2.py freeze --spec research/studies/exam_actions_20261121/specs/exam_spec_stage2.json --live-check-record research/studies/stage2_protocol_20261124/LIVE_CHECK_RECORD.md --timing-record research/studies/exam_actions_20261121/TIMING_RECORD_laptop.json --approved-by NAME`
   It refuses unless: both records and the spec exist and are non-empty; the approver is named; the custody bridge file is present; the listed files have no uncommitted changes; the spec equals the generated exam spec; the unit tests pass. It also refuses if a listed file is not tracked by git, and if Ollama cannot be read (it pins the Ollama version and the digests of the four core models; `--ollama-url` if the server is not at the default). Then it writes `FREEZE_STAGE2.json` (hashes of every listed file: the code and tests of the runner, the arms and harness they build on, the queue and monitor, the frozen analyzer, both analysis scripts, the ROSA baseline source, `pyproject.toml` and `uv.lock`; plus the held-out bridge hash, the spec hash, seeds, expected cells, the record hashes, the Ollama state, git head and approver) and verifies it. Commit `FREEZE_STAGE2.json`.
5. `python3 research/studies/exam_actions_20261121/freeze_stage2.py verify-frozen --check-ollama` must print `VERIFIED (frozen)` (the flag also compares the running Ollama with the frozen versions and digests; run it on each machine that will run Stage 2).

## 4. The exam launch (only after the freeze; Stage 1 paused on this machine)
```
export ROSA_ACTION_BRIDGE_FILE=<custody>/action_runner_bridge.py   ROSA_ACTION_CUSTODY_DIR=<custody>/stage2_run   ROSA_STAGE2_TASKS_FILE=<custody>/index-v2.json
bash research/studies/exam_actions_20261121/start_stage2.sh exam stage2_lab_01 research/studies/exam_actions_20261121/specs/exam_spec_stage2.json lab
```
`exam` mode re-verifies the freeze, the bridge hash and the spec hash before the queue starts and refuses on any difference. Before the freeze exists, the held-out bridge cannot run in any mode (`live_check` refuses it by hash, `exam` needs the freeze).

## 5. Monitoring, alerts and analysis
- `start_stage2.sh` starts three things: the **runner** window (its exit code goes to `notify_exit.py`, so a refusal or a crash marks the run `crashed` at once), the **monitor** window (`monitor.py`: status-file counts only, fixed ntfy templates for finished, crash, no progress for 15 minutes, Ollama down, low disk, daily 08:00; it never reads a trace and never commits results) and the `gpusample` session if none exists. ntfy goes to the topic in `~/.config/rosa-exam/notify.env` on that machine. `STAGE2_DRY=1 bash start_stage2.sh ...` prints what would start and creates nothing. The refusal path was checked by hand: the launcher refuses, the exit hook writes a `crashed` status, the monitor reports it.
- Analysis (after the run is complete or all remaining cells are skipped; run on the machine that holds the logs; one machine at a time, never pooled):
  `python3 research/studies/stage2_analysis_20261124/analysis_stage2.py check --spec SPEC --run-name RUN --machine lab --machines lab:1` prints counts and states only (supported and unsupported are merged into `answered`).
  `... analyze ... --out PREFIX --result-look-approved` computes the comparisons XM against XE1x (primary, with the worst-case-for-M sensitivity), XM against XS0x, XE1x against XS0x, the ending classes including `unscored` and `unresolved_motion`, the validity flags (more than 3% unscored stops the study, more than 5% class (a) plus (c) flags a system, more than 10% overall is compromised), the claim-counter 2x2 and the unscored-excluded secondary. The flag means the owner has opened the result look.

## 6. Lab: auto-stop at the end of Stage 1 tier 1, then Stage 2 (prepared; NOTHING here has been started)
Facts used (from `LAB_LAUNCH_HANDOVER_20261123.md` and the launch record, not re-verified): run `stage1_lab_20261123`, machine `lab`, container `rosa-exam-stage1-lab`, deployment root `<LAB_PATH>/stage1-release-f64baf6`, bundle `<LAB_PATH>/custodian/stage1_deploy_f64baf6/stage1_20261121`, queue folder `<bundle>/queue/stage1_lab_20261123/`, Ollama `http://127.0.0.1:11435`, ntfy topic in `~/.config/rosa-exam/notify.env` on the host.

**6.1 Auto-stop watcher.** [lab_autostop_stage1_tier1.sh](../exam_actions_20261121/lab_autostop_stage1_tier1.sh) has the same decision rule as the laptop's `auto_stop_tier1.sh` (STOP when the queue has moved past tier 1, or tier-1 done plus skipped reaches the tier total) but needs only bash and python3, because the frozen lab release lacks the helper scripts added later. It reads the whitelisted status counts and creates the empty STOP file; tested with synthetic status files (WAIT, STOP A, STOP B, END, unreadable, not-yet).
```
scp research/studies/exam_actions_20261121/lab_autostop_stage1_tier1.sh <LAB_USER>@<LAB_HOST>:<LAB_PATH>/stage1-release-f64baf6/ops/
# on the lab host:
B=<LAB_PATH>/custodian/stage1_deploy_f64baf6/stage1_20261121/queue/stage1_lab_20261123
W=<LAB_PATH>/stage1-release-f64baf6/ops/lab_autostop_stage1_tier1.sh
AUTO_STOP_ONCE=1 bash $W $B/status_lab.json $B/STOP          # TEST: prints WAIT tier_done=... ; never creates STOP
tmux new-session -d -s autostop-stage1_lab_20261123 "bash $W $B/status_lab.json $B/STOP"      # arm it (checks every 300 s; log ~/.config/rosa-exam/auto_stop_lab.log)
```
Not verified: that `status_lab.json` is at that path (the test mode shows it: "status unreadable" means the path is wrong) and that the tool-permission policy lets a Claude session read the protected queue folder (an earlier attempt was blocked); if so the owner runs the test line. Arm only after the owner says so. The runner finishes its current episode after STOP and exits; a few tier-2 cells may start first.

**6.2 After the lab runner has exited.** Check (host): `bash .../ops/launch.sh status` shows a stopped state; `docker exec rosa-exam-stage1-lab pgrep -af queue_bridge.py` prints nothing (`stage2_env.py` refuses to start while any queue runner is alive in the container it runs in).

**6.3 Starting Stage 2 on the lab (commands; the lab layout is not verified, items marked ?).**
1. Put the **frozen commit** on the lab as its own release (not inside the Stage 1 release): `stage2-release-<commit8>/repo` ?(how the Stage 1 release was staged is not documented in the files I read; ask the custodian). `FREEZE_STAGE2.json` is part of that commit.
2. Put Codex's held-out bridge file, bank, provenance and index in lab custody, **byte-identical** to the frozen hashes ?(the freeze checks the bridge hash; the worker checks the bank digest).
3. Choose the container ?(the Stage 1 container mounts the Stage 1 release; Stage 2 needs the Stage 2 repo, the custody directory and the ROS overlay; a second container from the same image with `--init` and those mounts is the cleaner option).
4. Inside that container:
```
cd <stage2 repo>; source /opt/ros/jazzy/setup.bash; source <deployment>/forge/ros-overlay.env
export ROSA_OLLAMA_URL=http://127.0.0.1:11435
export ROSA_ACTION_BRIDGE_FILE=<custody>/action_runner_bridge.py ROSA_ACTION_CUSTODY_DIR=<custody>/stage2_run_lab ROSA_STAGE2_TASKS_FILE=<custody>/index-v2.json
mkdir -m 700 <custody>/stage2_run_lab
python3 research/studies/exam_actions_20261121/freeze_stage2.py verify-frozen --check-ollama     # must print VERIFIED (frozen)
bash research/studies/exam_actions_20261121/start_stage2.sh exam stage2_lab_01 research/studies/exam_actions_20261121/specs/exam_spec_stage2.json lab
```
5. If `tmux` is not in the container, run `STAGE2_DRY=1 bash start_stage2.sh ...` to print the wrapper, save it, and start it from a host tmux window with `docker exec`. The monitor must run where it can read `research/_artifacts/exam/stage2_lab_01/status_lab.json` and where ntfy has network and the host's `notify.env`: on the host if the repo folder is a bind mount, otherwise inside the container ?.
6. Stage 1 on the lab resumes afterwards with its own start command and the same frozen verifier; the Stage 2 run uses its own run name and folders and does not touch the Stage 1 folders.

## 7. What this does not cover
No live episode through the real bridge has run. Time per cell on the lab is unmeasured. The custody path does not use `graph_settle` (custody owns the fixture checks). The quarantine and result analysis for Stage 2 (paired exclusion, sensitivity) needs the same revision as Stage 1 with the Stage 2 spec and the extra ending classes `unscored` and `unresolved_motion`: not written.
