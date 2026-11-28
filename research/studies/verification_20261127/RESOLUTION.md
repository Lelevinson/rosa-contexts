# Resolution of the 2026-11-27 verification round (A to C), recorded 2026-11-28

Records how items A to C of [REPORT.md](REPORT.md) were settled. The report is not edited; where this file corrects it, it says so. Task-free: no task text, coordinates or answer text. Sources: the owner's reply relayed by the orchestrator (marked **[reported]** where I have not seen the underlying evidence myself), and my own reading of code (marked **[CC]**).

## A. Paired counts: settled

- **[reported]** Codex independently obtained the same 70 units, the same two 2x2 tables (48/6/7/9 and 28/26/4/12), the same intervals and the same explanation of 54 versus 55. I have not seen Codex's output; my own recomputation is in `A_output.txt` and agrees.
- **Decision:** use the corrected sentence in REPORT.md section A: paired over the 70 of 72 (seed, model, task) units in which all three systems have a judge verdict (2 units dropped for an unscored post-start oracle loss, the 2 timeout cells kept as failures); XM minus XE1 = -0.014 (-0.114 to +0.086; XM 54/70, XE1 55/70); XM minus XS0 = +0.314 (+0.171 to +0.443; XM 54/70, XS0 32/70).
- The without-gpt-oss figure (XM minus XS0 = +0.250, +0.096 to +0.404, 52 units) is a **post-hoc sensitivity**, to be reported as such.

## B. Bridge versus replay mismatch (`1002__bonsai-2_4b__T01__XM`, pack 1df1f5): settled

**Cause (identified by Codex from the bridge code; [CC] I confirmed the code path, not the numbers):** two different definitions of "still" are used in the same run.

1. **Bridge, simulation-time speed.** `custody_bridge.py` lines 346-350 (`observe_pose`): the comment says "Transport can deliver consecutive physics frames in one burst. Use simulation time for velocity and monotonic receipt time for event order". The stored speed is `distance / sample_dt`, where `sample_dt` is the simulation-time difference; the row's `t` is the receipt time. `still_window` (line 308 onward) and `true_state()` (about line 469) judge stillness from that stored speed. `finish_evidence()` (line 482) calls it, and the result is what `evidence.json` stores as `true_state` (still True in this cell).
2. **Live judge, receipt-time speed.** `judge()` (line 769) writes that bridge state to the evidence, but then scores with `score(contract, rows, active.truth, answer, active.config)` (line 785), which does **not** use the bridge's state. In `judge_adapter.py` line 67 the final state is recomputed by `custody_parts.true_state_at(pose_rows, ...)`, and `custody_parts.speeds()` (lines 25-30) computes speed from `current["t"] - previous["t"]`, the receipt-time difference.

When two physics frames are delivered in a burst, the receipt-time interval is tiny and the recomputed speed is inflated. **[reported]** At t = 23.065 s in this cell two frames 17 ms apart in simulation time arrived 0.187 ms apart in receipt time, giving 0.024 m/s instead of about 0.0003 m/s, above the 0.01 m/s threshold. The live verdict therefore said "not still, not arrived". My own sanity arithmetic on those two quoted numbers: the displacement implied by 0.0003 m/s over 17 ms is about 5e-6 m, and 5e-6 m over 0.187 ms is about 0.027 m/s, consistent with the quoted 0.024 m/s within rounding.

**What I did not do.** I tried to read this cell's `ros/true_pose.jsonl` to check the two frame intervals myself. That file is not on the list of files I was allowed to read, and the read was blocked; I did not look for another way. The numeric instance rests on Codex's reading. The code path above I read myself in the three permitted regions of `custody_bridge.py` and in the two adapter files.

**Consistent with my earlier finding:** the stillness window was complete before the judge row (arrival row at 22.83 s, bridge `settled` row still=True at 23.55 s, judge row at 23.59 s); the discrepancy comes from the second definition, not from judging too early. The hypothesis in the results file ("the bridge judged before the still window was complete") is therefore wrong as a cause.

**Effect on reported numbers:** unchanged from the results file. The frozen live verdict is the reported one; the replayed `outcome_ok` would move XM's from 58/70 to 59/70; no primary-success count changes (the answer in that cell said the robot failed while it arrived, a false claim either way).

**Open follow-up, not a blocker:** the same receipt-time recomputation could in principle flip other cells in either direction. The replay of the frozen judge on each cell's own evidence agreed with the live `outcome_ok` in 211 of 212 cells, and that replay uses the stored bridge state, so the agreement shows no other cell flipped on this mechanism; the single exception is this cell.

## C. Stage 1 lab tier-3 look: settled

- **[reported]** Codex reproduced the published intervals exactly. **Decision: keep the published intervals.**
- My own re-pairing (`C_independent_pairing.py`) agrees on every count and point estimate; my interval for the short-menu row differs from the published one by 0.1 to 0.2 points (the frozen analyser on my pairs also gives -6.22 to +0.69, against the published -6.1 to +0.8). **Recorded as unexplained, low impact.** It does not change any sign or any statement in the look report.
- **Correction to the published look table (short-menu row, token ratio):** the lower bound of the 95% interval is **0.62** (0.6246), not 0.63. My independent value was 0.624. The upper bound 0.75 stands.

## D and the wording rule

- In any text, use **"unhandled tool-argument exceptions under the stock loop"**, not "reasoning failures" and not "the stock loop ended without an answer". The cause of the 35 XS0 no-answer cells and of the Stage 2 `validation_abort` cells is described in REPORT.md section D.
- The per-model by system table already in `STAGE3_REAL_RUN_RESULTS.md` is sufficient. The paper manuscript is owned by the paper chat and is not edited here.

## A note on one sentence in the results file

`STAGE3_REAL_RUN_RESULTS.md` says `per_cell.csv` is "git-ignored". It is not: in the Stage 3 checkout `results/real_run_scoring/per_cell.csv` shows as an untracked, not ignored file. It contains per-cell outcomes for the held-out run (pack ids, labels, no task or answer text). It was not committed (see the Stage 3 branch commit list); the results file was not edited, because only its status line may change.
