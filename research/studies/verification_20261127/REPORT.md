# Independent verification round, 2026-11-27 (read-only; Claude Code)

Scope and rules followed: no cell was rerun; no frozen file or existing results table was edited; Codex's output was not read or requested. Everything here is task-free (task labels and pack ids only; no task text, coordinates or answer text). The scripts and their raw outputs are in this folder: `A_paired_recompute.py` / `A_output.txt`, `C_independent_pairing.py` / `C_output.txt` / `C_seed_spread.txt`, `C_crosscheck_with_frozen_bootstrap.py` / `C_crosscheck_output.txt`.

Where the data lives (so the numbers can be rechecked): Stage 3 compact table and scorer are in the sibling checkout `rosa-research-stage3` (`research/studies/stage3_nav2_20261124/results/real_run_scoring/per_cell.csv`, `score_real_run.py`, git-ignored); private Stage 3 evidence is under `~/rosa_stage3_custody/real_queue/`; the Stage 1 and Stage 2 lab compact rows and traces are in `research/_artifacts/lab-evidence-20261127.xFpJtU/`.

What I did **not** open, on purpose: `~/rosa_stage3_custody/custody_bridge.py` (the frozen bridge: a custodian file that sits next to `TASKS.md`; the standing owner rule is to ask before opening custodian files), the labelling key, and the other Stage 3 `TASKS.md`. This matters for item B (see there).

Labels: **[V]** verified by me from the files named; **[H]** hypothesis, not verified.

---

## A. Stage 3 paired-count discrepancy

**Answer in one line.** `score_real_run.py` used one fixed rule for both comparisons: drop a (seed, model, task) unit if *any of the three systems* has a `post_start_oracle_loss` cell; keep a unit that contains an `episode_timeout` and count that cell as a failure. That gives 70 units for both comparisons. The label "70 complete units" is correct for XM vs XE1 under any reading of the rule; for XM vs XS0 it is correct only as "70 units complete for all three systems" (XM and XS0 alone are both scored in 71 units). The 54-versus-55 puzzle is a denominator difference, not an error. Confidence: high. [V]

**Evidence.**
- Cells without a judge verdict, recomputed from `per_cell.csv` (216 rows) [V]:

| ending class | system | model | seed | task | pack id |
|---|---|---|---|---|---|
| post_start_oracle_loss | XE1 | bonsai-2_4b | 1001 | T01 | 044918 |
| post_start_oracle_loss | XM | bonsai-2_4b | 1002 | T03 | 0d9157 |
| episode_timeout | XE1 | bonsai-2_4b | 1001 | T08 | d9f488 |
| episode_timeout | XM | qwen3_5_9b | 1002 | T05 | f5a4f8 |

- Rule actually used: `score_real_run.py` lines 273-277 build `units` only from units where `all(u[s]["ending_class"] != "post_start_oracle_loss" for s in SYSTEMS)`. Timeout cells carry `codex_success = False` (lines 194-197), oracle-loss cells carry `None`, so a timeout unit stays in and counts as a failure. The pre-set rule (`PROTOCOL_DRAFT.md`, section on infrastructure classes (a)-(c); `EPISODE_TIMEOUT_RECORD.md` item 4) says timeouts are outcomes and only post-start oracle loss is unscored. The script follows it. [V]
- The two dropped units: (1001, bonsai-2_4b, T01) where XM succeeded, XS0 failed and XE1 is the oracle loss; (1002, bonsai-2_4b, T03) where XM is the oracle loss and XE1 and XS0 both failed. 72 units - 2 = 70. [V]

**Recomputed tables** (my own script; primary success = `codex_success`; bootstrap = the script's own method, 10,000 draws over units, seed 1, same percentile rule). `A_output.txt` has every line.

| rule | comparison | units | both | only X | only Y | neither | X total / Y total | mean difference (95% interval) |
|---|---|---:|---:|---:|---:|---:|---|---|
| **as run** (drop unit if any of 3 systems is oracle-loss) | XM vs XE1 | 70 | 48 | 6 | 7 | 9 | 54 / 55 | -0.014 (-0.114 to +0.086) |
| **as run** | XM vs XS0 | 70 | 28 | 26 | 4 | 12 | 54 / 32 | +0.314 (+0.171 to +0.443) |
| rule (i), pairwise: drop a unit only if one of *the two compared* cells is unscored | XM vs XE1 | 70 | 48 | 6 | 7 | 9 | 54 / 55 | -0.014 (-0.114 to +0.086) |
| rule (i), pairwise | XM vs XS0 | 71 | 28 | 27 | 4 | 12 | 55 / 32 | +0.324 (+0.197 to +0.465) |
| rule (ii), pairwise: also drop a unit if one compared cell is a timeout | XM vs XE1 | 68 | 48 | 5 | 6 | 9 | 53 / 54 | -0.015 (-0.103 to +0.088) |
| rule (ii), pairwise | XM vs XS0 | 70 | 28 | 27 | 3 | 12 | 55 / 31 | +0.343 (+0.214 to +0.471) |
| rule (ii), all three systems (drop any unit with a timeout or oracle loss) | XM vs XE1 | 68 | 48 | 5 | 6 | 9 | 53 / 54 | -0.015 (-0.103 to +0.088) |
| rule (ii), all three systems | XM vs XS0 | 68 | 27 | 26 | 3 | 12 | 53 / 30 | +0.338 (+0.206 to +0.471) |

The results file's two lines (48/6/7/9 and 28/26/4/12) are reproduced exactly. No rule changes the conclusion: XM-XE1 is about zero with an interval spanning zero; XM-XS0 is +0.31 to +0.34 with an interval above zero.

**Why XM is 54 in the table but 55/70 in the per-system table.** [V] They are different populations of 70:
- The per-system line "55/70" counts the 70 *scored* XM cells (72 cells minus 1 oracle loss minus 1 timeout; the timeout is outside the denominator there). Successes: 55.
- The paired table counts the 70 *units* kept for all three systems. For XM that is 70 scored cells - 1 (the unit (1001, bonsai-2_4b, T01) was dropped because of the *XE1* oracle loss, and XM succeeded in it) + 1 (XM's own timeout cell, kept as a failure) = 70 cells and 55 - 1 = 54 successes.
- XE1 coincides: 55 successes both times (the dropped unit (1002, bonsai-2_4b, T03) was an XE1 failure, and the XE1 timeout is added as a failure).
- XS0 is 32 of 72 per system and 32 of 70 in the units (both dropped units were XS0 failures).

**Corrected sentence for the paper/poster** (replace "Paired over 70 complete (seed, model, task) units"):

> Paired over the 70 of 72 (seed, model, task) units in which all three systems have a judge verdict (2 units are dropped because one system's cell was an unscored post-start oracle loss; the 2 timeout cells stay in as failures), the primary-success difference XM minus XE1 is -0.014 (bootstrap 95% interval -0.114 to +0.086; XM 54/70, XE1 55/70), and XM minus XS0 is +0.314 (+0.171 to +0.443; XM 54/70, XS0 32/70).

Also: the per-system "55/70" and the paired "54/70" must not appear next to each other without this explanation. If XM vs XS0 is quoted on its own pair-by-pair, the count of units with both cells scored is 71 (+0.324), but the pre-set rule gives 70; do not switch.

---

## B. Bridge-vs-replay mismatch (`1002__bonsai-2_4b__T01__XM`, pack 1df1f5) and `1002__lfm3_1_7b__T02__XE1`

### B1. "The bridge judged before the stillness window completed"

**Answer: the cell's own timestamps do not support the hypothesis; the true cause is not identified, and I could not read the frozen bridge to settle it.** Confidence that the hypothesis as stated is wrong: moderate to high. Confidence in any alternative: low (all alternatives below are [H]).

**What I could read** [V]: the cell's event rows (`evidence.json`) and trace, and the public code the bridge's `judge()` calls (`judge_adapter.py`, `custody_parts.py`, `nav_judge.py`). I did not open `custody_bridge.py`, so the sentence "the bridge code was not read" in the results file remains true after this round.

**Timeline of the cell** (seconds from episode start, evidence rows):

| t | event |
|---:|---|
| 14.02 | dispatch of the first and only goal (the goal matches the target, read before dispatch at t=9.9 and 12.8) |
| 21.58 | Nav2 terminal `SUCCEEDED` |
| 22.28 | model reads the robot pose |
| **22.83** | **`arrival` row: the robot is within tolerance (0.031 m) and the still window (1.0 s, 0.01 m/s) is already complete** |
| 23.54 | model's final message |
| **23.55** | **`settled` row: true state `still: True`**, 0.153 m from the target (tolerance 0.25 m) |
| 23.59 | bridge `judge` row (live verdict written: `scored`, `success False`) |

So the stillness window was complete about 0.7 s before the final message and about 0.76 s before the judge row. `custody_parts.true_state_at` and `still_since` look *backwards* over the pose rows: a robot that has been still for 1.0 s before the judge call counts as still at once. For the hypothesis to hold, the bridge would have had to evaluate a pose log that did not yet contain the window, which contradicts both the `arrival` row (22.83) and the `settled` row (23.55, still True, written before the judge row). [V on the timestamps; H on what the bridge actually fed to the judge]

**Why the replay and the live verdict differ is therefore still open.** The live compact result says `arrived False`, `trips_completed 0`, `outcome_ok False`. The same judge replayed on `evidence.json` says arrived and ok. Candidates that fit the timestamps (none verified): [H] (a) the live `events` list or `pose_rows` the bridge passed to `judge_adapter.score` differed from what `evidence.json` stores (for example the read or dispatch rows were not yet in the list, or the pose log used for `true_state_at` was a snapshot with the last samples missing); (b) the bridge passed a `true_state` of its own that is not the one stored as `settled`; (c) an ordering effect between the `judge` call and the `settled` write (the `settled` row is written at 23.550, the `judge` row at 23.593; I do not know which state object the judge received). The decisive check is a 10-line excerpt of `judge()` in the frozen bridge (sha256 `74fcbc78...80bdb`) or the live verdict's `reasons`/`states_used` field, which the compact result does not keep. **Request for the owner:** permission for me to read `judge()` in `custody_bridge.py`, or ask Codex for the lines that build `rows`, `pose_rows` and `final` before the call.

Effect on the numbers (unchanged from the results file) [V]: the replayed `outcome_ok` would move XM's by one cell (58 -> 59 of 70); no primary-success count changes, because the answer in this cell says the robot did not arrive while it did (a false claim either way).

### B2. `1002__lfm3_1_7b__T02__XE1` fails only on "first dispatched goal does not match target"

**Answer: a real agent error, correctly caught by a rule that is deliberately strict; not a judge defect.** Confidence: high for the mechanism, moderate on whether the rule should count a self-corrected slip as an outcome failure (that is a protocol choice, not a defect). [V]

Event rows and trace of the cell (task details left out on purpose):
- The task needs the agent to read some values and compute its goal from them. All reads succeeded before the first dispatch.
- The agent's first goal did not equal the correct goal (a calculation slip). Nav2 aborted it.
- The agent then sent a second goal equal to the correct target; Nav2 SUCCEEDED; the true pose is within the 0.25 m tolerance and still. So the robot did arrive.
- The judge's reason list contains only "the first dispatched goal does not match the target for this episode" (`nav_judge._check_trip`, `dispatch_tolerance_m` 0.25). Every other check passes (`arrived`, last status SUCCEEDED, read before dispatch).

So the judge did what the frozen rule says. The rule exists to catch a goal that was sent without using the value read; here the agent did read the values but computed them wrong, then corrected itself after an abort. The consequence for the study is that this XE1 cell is "arrived, outcome not ok", counted as a primary-success failure: that is a conservative reading of the pre-set rule and was fixed before the run, so it must be reported as it is. It is one cell (1 of 212).

---

## C. Stage 1 lab tier-3 ablation look: independent re-pairing

**Answer: every count, point estimate and the token ratio reproduce the published table exactly; the intervals reproduce to within 0.2 points (differences and the worst case) and 0.01 (token ratio); no conclusion changes.** Confidence: high on counts and point estimates; moderate on the unexplained interval differences. [V]

My pairing (`C_independent_pairing.py`) does not import or copy the shim or the analyser code. It reads only the opaque compact rows (`compact_lab.jsonl`: 6,244 rows; 1,781 tier 1, 1,780 tier 2, 2,683 tier 3) and applies the definitions in the analyser's documented header: pair = (pool, task, model, seed); the ablation arm's tier-3 cell against `EX-M`'s tier-1 cell; a pair is excluded if either cell has no row (skipped); difference = 100 x (supported M - supported arm) / pairs; token ratio = summed (input + output) tokens of M over the arm; task-cluster bootstrap, 10,000 draws, `random.Random(20261122)`, the documented percentile rule; "capped" endings = iteration_cap, backend_error, timeout, no_answer, validation_abort; worst case for M = excluded pairs put back with M's missing cell unsupported and the arm's missing cell supported.

| row | quantity | published | mine | match |
|---|---|---|---|---|
| short menu (EX-NO_MENU) | pairs | 885 | 885 (27 excluded: 16 M-missing, 20 arm-missing) | yes |
| | supported M / arm | 334 / 358 | 334 / 358 | yes |
| | M minus arm (95%) | -2.7 (-6.1 to +0.8) | -2.71 (-6.31 to +0.67) | point yes; interval -0.2 / -0.1 |
| | token ratio | 0.685 (0.63 to 0.75) | 0.685 (0.624 to 0.750) | yes |
| | worst case for M | -4.9 (-8.9 to -1.0) | -4.93 (-9.10 to -1.10) | point yes; interval -0.2 / -0.1 |
| | without capped | -4.3 (-7.9 to -0.8), 739 pairs | -4.33 (-8.06 to -0.91), 739 pairs | point and pairs yes |
| structured finish (EX-NO_FINISH) | pairs | 880 | 880 | yes |
| | supported M / arm | 331 / 301 | 331 / 301 | yes |
| | M minus arm | +3.4 (+0.8 to +6.0) | +3.41 (+0.79 to +6.04) | yes |
| | token ratio | 0.858 (0.79 to 0.94) | 0.858 (0.788 to 0.939) | yes |
| | worst case | +0.9 (-2.1 to +3.7) | +0.88 (-2.08 to +3.73) | yes |
| | without capped | +2.0 (-1.0 to +5.1), 699 | +2.00 (-1.02 to +4.99), 699 | yes (upper +0.1) |
| errors as text (EX-NO_ERRORTEXT) | pairs | 892 | 892 | yes |
| | supported M / arm | 334 / 295 | 334 / 295 | yes |
| | M minus arm | +4.4 (+1.5 to +7.3) | +4.37 (+1.46 to +7.25) | yes |
| | token ratio | 1.458 (1.30 to 1.63) | 1.458 (1.293 to 1.631) | yes |
| | worst case | +3.4 (+0.3 to +6.5) | +3.40 (+0.33 to +6.47) | yes |
| | without capped | -0.8 (-3.6 to +2.0), 623 | -0.80 (-3.66 to +1.99), 623 | yes |

**The one unexplained difference.** For the short-menu row only, the main interval (and the worst-case interval) differ from the published one by 0.1 to 0.2 points. I checked it three ways: (1) 8 different bootstrap seeds move my interval by about 0.1 at the lower end and 0.01 at the upper end (`C_seed_spread.txt`), so resampling noise alone does not explain a published upper bound of +0.8 against my +0.67 to +0.69; (2) task order in the resampling list moves it by 0.01 to 0.15 (a variant I ran in the scratchpad); (3) feeding my own pairs to the frozen `analyze_primary.analyse` (cross-check only of the bootstrap step, `C_crosscheck_with_frozen_bootstrap.py`) gives -6.22 to +0.69, i.e. the same as mine and not the published -6.1 to +0.8. So the published short-menu interval is not what the frozen analyser produces on these 885 pairs with these rows and seed. Possible reasons [H]: the look used a slightly different row set at the time (for example the contended-episode file or the compact file before its last rewrite at 05:36 on 27 November), or a different pair order. It changes nothing qualitatively (the interval includes zero both ways; the uncapped and worst-case rows keep their signs), but the published interval for that row should be re-derived by whoever owns the look before it goes on a poster. I did not try to reproduce the shim's exact inputs.

Other observations [V]: the 912 planned pairs are all recoverable from the union of pair ids in the rows; M has 16 skipped tier-1 cells, the arms 20, 25 and 8; the published "27 / 32 / 20 pairs excluded" matches.

---

## D. XS0 failure mechanism: was stock ROSA crippled by our harness?

**Answer: no, not by the harness in a way that changes the outcome. The 35 no-answer cells are model-produced arguments that the stock tool schemas or stock tool code reject, plus 2 server-side parse errors; XS0 is a faithful stock executor, and by design it has no error handler. But the XS0 "gap" is mostly one model's argument habit under one-shot scoring, and it must be described that way.** Confidence: high on the mechanism and the stock-equivalence; moderate on the Ollama side (whether the empty-string argument comes from the model itself or from Ollama's tool-call parsing of that model: I did not isolate it). [V unless marked]

### D1. Classification of the 35 XS0 no-answer cells

All 35 XS0 `answer_given False` cells have ending `no_answer` and goals_sent 0 or 1-2 (36 XS0 cells sent no goal in total). Counts by error kind recorded by the worker, with the traces behind each class opened (error text and last tool call only):

| class | cells | what the trace shows | verdict |
|---|---:|---|---|
| ValidationError on `ros2_node_list` | 18 (all gpt-oss) | The model's first call is `ros2_node_list` with `blacklist=''` (and `pattern=''`) in 16 of 18 cells (and in all 18 at some point). The stock schema is `blacklist: Optional[List[str]]`, so pydantic rejects the string `''`; the exception ends the episode at the first tool call (12 s, 0 goals). | (1) bad arguments stock would also reject |
| ValidationError on other tools | 9 | `calculate_line_angle_and_distance` 3 and `atan2` 1 (a list passed as a text string, with typos in 2); `ros2_node_info` 1 (`nodes` passed as a string); `read_log` 2 (`level_filter=''` is not in the allowed literals); `ros2_service_call` 1 (`request={}` given as a dict, the schema wants a string); `NavigateArgs` 1 (x, y, yaw given as '?'). | (1) bad arguments; the last one is our navigation tool, which in XS0 has no handler by the same arm definition |
| TypeError 3 and ValueError 3 | 6 | The exception comes from the body of the stock `distance_between_points` / `calculate_line_angle_and_distance` (`for (x1, y1), (x2, y2) in point_pairs`, `src/rosa/tools/calculation.py` lines 398 and 420) when the model passes a flat pair or a one-element nesting instead of a list of pairs. | (1) bad arguments reaching stock code that does not validate their shape (a stock robustness gap, not our wiring) |
| ResponseError | 2 (lfm3) | The Ollama server fails to parse the model's own tool-call text ("XML syntax error"). The same error occurs in XM (1) and XE1 (3). | (3) model output / model-server, not an arm difference |
| **Total** | **35** | | no cell is class (2) |

By model: gpt-oss 18, bonsai 8 (6 of them also show a first call to an `invalid_tool` name with a leading space, which stock LangChain handles), lfm3 8, qwen 1.

### D2. Is any of it a schema/version mismatch or a wiring bug of ours? Checks made

- Stock code identical: `src/rosa/tools/ros2.py`, `calculation.py`, `rosa.py` and every other `.py` under `src/rosa` are byte-identical to `rosa-baseline` (`diff -rq` shows only `__pycache__` differences). The same `langchain~=0.3.23`, `langchain-core~=0.3.52`, `pydantic` pins appear in both `pyproject.toml` files. The runtime pydantic is 2.14 (error text); the baseline's own pin is unconstrained, so that version is what a stock install would resolve today. [V]
- XS0 definition: `run_pilot.StockArm` ("stock tools, stock executor, no handlers": `AgentExecutor(... handle_parsing_errors=True)`, the same as stock `ROSA._get_executor`, `src/rosa/rosa.py` line 264) and `action_arms.ActionS0x` ("no error handler is added (a validation error is the stock behaviour of this arm)"). The only additions are the two navigation tools, shared by all systems. [V]
- One real difference from stock-as-deployed: our worker calls the inner executor directly (`run_nav.py`, `run_model_agent`, line 129) and records an exception as `no_answer`. Stock `ROSA.invoke` (`rosa.py` lines 155-165) would catch it and return the text "An error occurred: <exception>" as the answer. This changes the recorded ending, not the robot's outcome: in all 35 cells the loop ended without a goal or at the same point either way, and Codex's label for such a cell is `no_claim` in any case. It does matter for the sentence "the stock loop ended without an answer" in the results file; the precise statement is "ended with an unhandled tool exception, which stock `invoke` would turn into an error message". [V]
- Why XM and XE1 do not die the same way: XE1 returns the error text to the model (the experimental component under test), XM likewise. In XE1, gpt-oss also produces bad arguments (4 validation errors returned as text, on `ros2_param_get`, `ros2_param_list` and `ros2_topic_list`) and keeps going. Under XS0 16 of 18 gpt-oss cells start with `ros2_node_list`; under XE1 only 0 of 18 do (13 start with `ros2_param_get`). The cause of that difference in first call (the stock prompt and the stock menu against E1's own menu or prompt) is not established. [V on the counts, H on the cause]

### D3. Stage 2 gpt-oss under XS0 (`validation_abort` in about 35 of 42)

Same mechanism. In the Stage 2 lab run (`run_stage2_lab_01`, 42 XS0 gpt-oss cells) the episode-end error is `ros2_node_list`, field `blacklist`, `list_type`, input type `str` in **35 of 42 cells**, and 1 more is a `ResponseError` from a malformed tool call that also contains `"blacklist":""`; the 6 others end with no error recorded (`None`). Every episode ended after 1 or 2 tool calls. So the Stage 3 and Stage 2 XS0 failures of gpt-oss are the same stock-schema incompatibility. [V]

### D4. Is the XS0 baseline fair as run?

- **As a measurement of "stock ROSA, as released, with these four small local models, given one request"**: fair, and faithful to the stock executor. [V]
- **As evidence about stock ROSA's ability to do the task**: it is not, for gpt-oss: that model's habit of passing `''` for optional list arguments makes the very first stock call fail, and stock ROSA has no recovery, so gpt-oss has 0 correct outcomes of 18 under XS0 by that one habit. The XM-vs-XS0 gap shrinks from +0.314 (70 units) to +0.250 (+0.096 to +0.404, 52 units) when gpt-oss is left out (`A_output.txt`, extra lines), XM-vs-XE1 stays about zero (-0.038). The rest of the gap (about 25 points) comes from the other three models and was not decomposed. [V]
- Interactive stock use gives the user a second try after "An error occurred"; the one-shot protocol does not. That is a property of the protocol, identical for all three systems, and should be stated.
- Not fair to claim: that the method "beats stock ROSA" on reasoning. XE1 (stock plus returned errors) is the control that isolates the method; XM vs XE1 shows no visible difference in primary success.

**A fair fix, not applied** (for the owner to decide, and it would be a new, separately labelled protocol revision, not a replacement of the frozen numbers): (a) report XS0 per model and with gpt-oss shown separately (descriptive; no new run); (b) if a new run is allowed, add an arm "XS0 as invoked by `ROSA.invoke`" that records the returned error text as the answer, plus an optional single retry turn after an error, matched across systems; (c) before blaming the model, run a model-only check on the stock `ros2_node_list` schema without our harness (direct `ChatOllama.bind_tools` call for gpt-oss) to see whether `blacklist=''` comes from the model or from the Ollama tool-call layer; that is cheap and could decide whether to call this "model incompatibility" or "serving-layer incompatibility". Until then the paper should say "unhandled tool-argument exceptions under the stock loop", not "reasoning failures".

---

## Summary of the answers

- **A.** The rule used: drop a unit if any of the three systems has an oracle-loss cell; timeouts stay in as failures. 70 units for both comparisons. "70 complete units" is right for XM vs XE1, and right for XM vs XS0 only as "complete for all three systems" (71 if only XM and XS0 are required). Tables and corrected sentence above. XM is 54 in the pairing because the dropped unit (1001, bonsai, T01) was an XM success and XM's timeout cell is kept as a failure; per-system 55/70 uses scored cells only.
- **B.** Timestamps refute "judged before the window completed" (still window complete at 22.83, `settled` still=True at 23.55, judge at 23.59); the true cause needs the bridge `judge()` lines (not read; owner permission needed). `1002__lfm3_1_7b__T02__XE1` is a real calculation error in the first dispatch, corrected on the second dispatch, flagged by a deliberate rule.
- **C.** Counts, point estimates and token ratios reproduce exactly; intervals within 0.2 points; the short-menu interval differs by 0.1-0.2 from the frozen analyser's own output on the same pairs (unexplained, low impact).
- **D.** 35 no-answer cells: 27 schema ValidationErrors (18 of them the gpt-oss `blacklist=''` case), 6 TypeError/ValueError inside stock calculation tools, 2 model-server parse errors; no harness bug found; same cause as Stage 2's 35/42. XS0 is faithful to stock but one-shot and unhandled; the gap partly reflects gpt-oss.

## Open search (unfiltered; other patterns seen while reading, counts and trace locations)

- In XS0, the first model action of every gpt-oss cell is a tool call that fails at once (Stage 3: 16 of 18 first calls are `ros2_node_list` with `blacklist=''`; Stage 2: 35 of 42). Under XE1, gpt-oss's first call is `ros2_param_get` in 13 of 18 cells. Traces: `~/rosa_stage3_custody/real_queue/stage3_laptop_20261127__1001__gpt-oss_20b__T01__XS0` (example), and the 18 gpt-oss XE1 folders.
- The `invalid_tool` call with a leading space in the tool name occurs in 6 of the 8 bonsai XS0 no-answer cells (pack ids 801a4b, 0b04f4, feb850, 60c2e4, b51f69, a11355). Whether this is bonsai's formatting or the Ollama template was not checked.
- Math-tool arguments: 6 XS0 cells fail inside `distance_between_points` / `calculate_line_angle_and_distance` because the model passes one pair instead of a list of pairs (pack ids 0b04f4, a11355, feb850, 7a6405, b51f69, 732a9a); the same tools in XE1/XM were not searched for the same mistake returned as text.
- `1002__lfm3_1_7b__T02__XE1`: the model made a calculation slip on a read-then-compute task and recovered after an abort; how often other recovered first-goal slips (counted as successes by the judge only when the first goal matches) happen in XM/XE1 was not counted.
- The `settled` row is written 0.043 s before the `judge` row in the B cell. I did not check whether the same gap (and the same agent timing: final message within about 1 s of the still window) appears in the other 211 scored cells, which would show whether this cell's order was unusual.
- Lab tier 3: the short-menu interval differences listed in section C are the only mismatch; I did not look into why `compact_lab.jsonl` was last rewritten at 05:36 on 27 November.
