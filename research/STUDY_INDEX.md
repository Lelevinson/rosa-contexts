# Study index

Snapshot 2026-11-15 (Forge pilot and validity qualifications included; other rows retain their stated dates). Status and results below are reported by linked studies, not independently rerun during migration. Read original protocols, amendments, source, raw records and adjudication before making claims. Local `_artifacts` is Git-ignored. In this index **archive** and **previous** refer to historical sibling checkouts, not portable repository links. Resolve their current paths using the optional local-only `research/.local/WORKSPACE_MAP.md` if available; otherwise use the [migration manifest](_artifacts/knowledge_migration_20261112/MIGRATION_MANIFEST.md) and original archive inventories. See [manifest](_artifacts/knowledge_migration_20261112/MIGRATION_MANIFEST.md) and [migration report](_artifacts/knowledge_migration_20261112/MIGRATION_REPORT.md) for gaps and ZIP coverage.

## Current checkout

Study bundles live under `studies/`; production code remains in `src/rosa/`.
The 2026-11-12 physical migration kept original frozen manifests and raw data.
Some relocated runtime files have path-only edits, so their bytes need not match
historical freezes. For the original layout, paths, and verification see
[`_artifacts/backups/restructure_20261112/`](_artifacts/backups/restructure_20261112/).
The frozen `ARTIFACTS.json` in capability discovery records original bytes;
verify those bytes in the pre-migration snapshot, not against edited relocated
navigation or runtime files. Original review ZIPs retain their own layout.
Some historical READMEs still show old commands; resolve their paths using the
[migration mapping](_artifacts/backups/restructure_20261112/path-mapping.json),
and check the current code and authorization before running them.
Historical package builders target fixed filenames or frozen manifests; do not
run them against this checkout. Use the original ZIP verifier or restore the
snapshot into a separate directory before investigating a legacy build.

To inspect the original captured files without changing this checkout, create an
empty temporary directory and extract the snapshot there:

```bash
review_dir=$(mktemp -d [local path redacted])
tar -xzf research/_artifacts/backups/restructure_20261112/pre-migration.tar.gz \
  -C "$review_dir"
```

The snapshot contains affected research and navigation files, not the separately
preserved `_artifacts/`, `inbox/`, production checkout, virtual environment, or
other worktrees. It was hash-verified after a test extraction; it shares this
machine's filesystem and is not independent disaster recovery. Never extract it
over current work. Full runtime reproduction may require the original external
artifacts, ROS/Python environment, and sibling paths; use an isolated copy and
verify its inputs before executing anything.

| Study | Result / status | Protocol and code | Raw evidence and review |
|---|---|---|---|
| [Forge baseline 2026-11-15](studies/forge_baseline_20261115/REPORT.md) | Complete: 80 cells, Forge 55/80 vs historical C1 70/80 and A1 47/80; 643 requests, 2.216M reported tokens; missed-trigger validity flags retained; smoke separate | [full protocol/amendment](studies/forge_baseline_20261115/PROTOCOL_FULL.md), [driver](studies/forge_baseline_20261115/run_full.py), [same-cell comparison](studies/forge_baseline_20261115/SAME_CELL_COMPARISON.md), [smoke](studies/forge_baseline_20261115/REPORT_THINKING_ON_SMOKE.md) | [_artifacts/runs/forge_baseline_20261115](_artifacts/runs/forge_baseline_20261115/), [matched ledger](studies/forge_baseline_20261115/RESULTS_MATCHED.jsonl), [validation](studies/forge_baseline_20261115/FINAL_VALIDATION.json), [fixture audit](studies/forge_baseline_20261115/FIXTURE_EVENT_AUDIT.json); no model reruns |
| [Build round 1 2026-11-15](studies/build_round1_20261115/REPORT.md) | Complete: answer gate and list arguments on the fixed loop, 320 episodes; both meet frozen criteria literally, neither attributable (gate wins have no firing / control defects; list savings come from episodes without a list call; adoption 4/80); 0 false rejections | [protocol](studies/build_round1_20261115/PROTOCOL.md), [results log](studies/build_round1_20261115/RESULTS_LOG.jsonl), [tables](studies/build_round1_20261115/REPORT_TABLES.md), [validity](studies/build_round1_20261115/validity_round1.json) | [_artifacts/runs/build_round1_20261115](_artifacts/runs/build_round1_20261115/); smoke rows separate |
| [Headroom diagnostic 2026-11-12](studies/headroom_diagnostic_20261112/REPORT.md) | Diagnostic complete through Stage 3d (Qwen arm A2, six generic prompt sentences: supported 20/24 vs 24/24, so the frozen rule stops at correctness; bare-name recovery gone, repeats unchanged; [Stage 3d](studies/headroom_diagnostic_20261112/REPORT_STAGE3D.md)). Stage 3 (arm A0): frozen rule “room for a method” (Qwen 85.4% excess; Luna 25.3%). Stage 3b (arm A1, strongest ordinary prompt control tried): “weak-model room remains” (Qwen 49.0%; Luna 14.3%, one request from the 15% line); A0 and A1 ran in different sessions. Synthetic development evidence; no algorithm selected; no independent review recorded. [Stage 1](studies/headroom_diagnostic_20261112/REPORT_STAGE1.md), [1c](studies/headroom_diagnostic_20261112/REPORT_STAGE1C.md), [2a](studies/headroom_diagnostic_20261112/REPORT_STAGE2A.md), [3](studies/headroom_diagnostic_20261112/REPORT_STAGE3.md), [3b](studies/headroom_diagnostic_20261112/REPORT_STAGE3B.md), [ledger](studies/headroom_diagnostic_20261112/DECISION_LEDGER.md) | [stage 0](studies/headroom_diagnostic_20261112/PROTOCOL_STAGE0.md), [1](studies/headroom_diagnostic_20261112/PROTOCOL_STAGE1.md), [1c](studies/headroom_diagnostic_20261112/PROTOCOL_STAGE1C.md), [2a](studies/headroom_diagnostic_20261112/PROTOCOL_STAGE2A.md), [3](studies/headroom_diagnostic_20261112/PROTOCOL_STAGE3.md); [driver](studies/headroom_diagnostic_20261112/run_stage1.py), [replay](studies/headroom_diagnostic_20261112/replay_stage2a.py) | [_artifacts/runs/headroom_diagnostic_20261112](_artifacts/runs/headroom_diagnostic_20261112/) (hash [manifest](_artifacts/runs/headroom_diagnostic_20261112/MANIFEST_STAGE1.sha256.json) covers Stage 1 only), [decision record](studies/headroom_diagnostic_20261112/DECISION_RECORD.md), [labels](studies/headroom_diagnostic_20261112/labeled_requests.csv) |
| [Headroom diagnostic Stages 3b–3c 2026-11-14](studies/headroom_diagnostic_20261112/REPORT_STAGE3C.md) | Stage 3b (arm A1, [report](studies/headroom_diagnostic_20261112/REPORT_STAGE3B.md)): Qwen 49.0% excess, Luna 14.3%; frozen rule “weak-model room remains”. Stage 3c (offline replay of the 60 A1 excess requests, no model run): Qwen removable 43/47, all judged O (an untested prompt sentence could plausibly prevent them), 0 F; frozen branch “prompt control, not a method”, not fragile. The branch flips to “a target exists” if all P1 and P3 items are treated as F. Replay upper bound, synthetic, one analyst, no independent review; no method selected. [tables](studies/headroom_diagnostic_20261112/STAGE3C_TABLES.md), [protocol](studies/headroom_diagnostic_20261112/PROTOCOL_STAGE3C.md), [ledger](studies/headroom_diagnostic_20261112/DECISION_LEDGER.md) |
| [AutoTool iteration 2026-11-12](studies/autotool_iteration_20261112/RESEARCH_REPORT.md) | Offline negative; live gate blocked | [protocol](studies/autotool_iteration_20261112/PROTOCOL_FROZEN.md), [replay](studies/autotool_iteration_20261112/replay.py), [amendments](studies/autotool_iteration_20261112/PROTOCOL_AMENDMENTS.md) | [_artifacts/autotool_iteration_20261112](_artifacts/autotool_iteration_20261112/), [review ZIP](_artifacts/ROSA_AUTOTOOL_ITERATION_REVIEW_20261112.zip), [independent review](studies/autotool_iteration_20261112/INDEPENDENT_REVIEW.md) |
| [GPT coverage 2026-11-11](studies/gpt_coverage_investigation_20261111/REPORT.md) | 92/92 fields; 7/10 strict completion | [protocol](studies/gpt_coverage_investigation_20261111/PROTOCOL.md), [driver](studies/gpt_coverage_investigation_20261111/run_study.py) | [_artifacts/gpt_coverage_investigation_20261111](_artifacts/gpt_coverage_investigation_20261111/), [review](studies/gpt_coverage_investigation_20261111/INDEPENDENT_RESULTS_REVIEW.md), [ZIP](_artifacts/ROSA_GPT_COVERAGE_REVIEW_20261111.zip) |
| [Action narration 2026-11-11](studies/action_narration_20261111/REPORT.md) | Terse arms lost supported fields | [protocol](studies/action_narration_20261111/PROTOCOL.md), [driver](studies/action_narration_20261111/run_study.py) | [_artifacts/action_narration_20261111](_artifacts/action_narration_20261111/), [review](studies/action_narration_20261111/INDEPENDENT_ANSWER_REVIEW.md), [ZIP](_artifacts/ROSA_ACTION_NARRATION_REVIEW_20261111.zip) |
| [Native read 2026-11-11](studies/native_read_investigation_20261111/REPORT.md) | Transport engineering benefit; no adaptive promotion | [protocol](studies/native_read_investigation_20261111/PROTOCOL.md), [executor](studies/native_read_investigation_20261111/executor.py) | [evidence](studies/native_read_investigation_20261111/evidence/), [manifest](studies/native_read_investigation_20261111/MANIFEST.json), [ZIP](_artifacts/ROSA_NATIVE_READ_REVIEW_20261111.zip) |
| [CPAW 2026-11-10](studies/cpaw_prototype_20261110/REPORT.md) | Isolated synthetic negative; 0/47 default eligibility | [protocol](studies/cpaw_prototype_20261110/PROTOCOL.md), [revisions](studies/cpaw_prototype_20261110/PROTOCOL_FINAL.md), [implementation](studies/cpaw_prototype_20261110/cpaw.py) | [artifacts](studies/cpaw_prototype_20261110/artifacts/), [review ZIP](studies/cpaw_prototype_20261110/CPAW_REVIEW_PACKAGE.zip) |
| [Capability discovery 2026-11-10](studies/capability_discovery_20261110/REPORT.md) | Observer only; no equivalence authority | [protocol](studies/capability_discovery_20261110/PROTOCOL.md), [implementation](studies/capability_discovery_20261110/discovery.py) | [original results](studies/capability_discovery_20261110/results/), [corrected results](studies/capability_discovery_20261110/results_corrected/), [manifest](studies/capability_discovery_20261110/ARTIFACTS.json) |
| [Bottleneck gate 2026-11-10](studies/bottleneck_gate_20261110/ROSA_Bottleneck_Evidence_Gate_2026-11-10.md) | Retrospective evidence audit; do not infer prospective gain | [analysis](studies/bottleneck_gate_20261110/analyze_traces.py) | [inputs, calls and hashes](studies/bottleneck_gate_20261110/) |
| Design investigations 2026-11-08–10 | Design and reviews; not interchangeable with experiments | [design directory](studies/design_investigations_20261108_20261110/) | Original packet [inbox](inbox/), source references in individual reports; Mission C completed report not found in searched locations. |

## Previous checkout: November 6–8

| Study | Result / status | Protocol and code | Evidence |
|---|---|---|---|
| Menu retrieval | Coverage loss; see original protocol | `previous/research/menu_retrieval/` | `previous/research/_artifacts/`; report and manifest inside archive |
| Structured dependency / multistep | Incomplete raw evidence; no recovered 64 original traces | `previous/research/multistep/report.md`, `protocol.json`, `read_plan.py` | `previous/research/_artifacts/rosa-multistep-review-20261107-reconstructed.zip` is reconstructed, not original traces |
| Baseline diagnostic | Retrospective failure and cost evidence | `previous/research/baseline_diagnostic/report.md`, `protocol.json`, `run_diagnostic.py` | `previous/research/_artifacts/rosa-baseline-diagnostic-review-20261107.zip` |
| CodeAct-style paper pilot | One complete program of nine; incomplete strong comparison | `previous/research/paper_pilot/report.md`, `protocol.md`, `run_study.py` | `previous/research/_artifacts/rosa-paper-pilot-review-20261108.zip` |

## Archived rounds

Summary: the rows below record conditional gains at most, several ties or losses against strong ordinary controls, and several NO-GO decisions; none is recorded as a promoted algorithm. Read the per-round report before citing a result.

The following entries are direct original-report pointers discovered in the sibling checkout. A generic status means the actual result and limitations must be read there; it is not a success claim. R1–4 are not separately identified by this filename scan; consult `archive/research/internal/INDEX.md`, `archive/research/README.md` and canonical §5. Evidence may be in per-round archives, shared directories or manifests, not necessarily the suggested pattern. [History inventory](studies/autotool_iteration_20261112/HISTORY_AND_SOURCE_INVENTORY.md) gives independently recorded R19–28 links and limitations.

| Round | Status | Report | Code | Evidence |
|---|---|---|---|---|
| R5 | Credit 11/12 completion; conditional call saving on supported pairs. | `archive/research/internal/round5_results.md` | See report / shared experiments | See report / archive manifest |
| R6 | No incremental native call benefit over strongest controls. | `archive/research/internal/round6_results.md` | See report / shared experiments | See report / archive manifest |
| R7 | Guarded variant 70 vs 76 calls in 176 supported episodes; guard regresses in simulation. | `archive/research/internal/round7_results.md` | `archive/src/rosa/round7_policy.py` | See report / archive manifest |
| R8 | Conditional gains; 240 primary and 24 supplemental supported; no call advantage over unguarded control. | `archive/research/internal/round8_results.md` | `archive/src/rosa/round8_policy.py` | See report / archive manifest |
| R9 | Conditional savings; initial gain failed confirmation and later correction did not establish cost superiority. | `archive/research/internal/round9_results.md` | `archive/src/rosa/round9_policy.py` | See report / archive manifest |
| R10 | Conditional 53 vs 56 calls on 10 matched supported tasks; no invocation-time gain. | `archive/research/internal/round10_results.md` | `archive/src/rosa/round10_policy.py` | See report / archive manifest |
| R11 | Three calls saved on 14 complete pairs; fixed-field ties native adaptive choices. | `archive/research/internal/round11_results.md` | `archive/src/rosa/round11_policy.py` | See report / archive manifest |
| R12 | Lean/metadata conditional results; retain binding_fixed; inspect later revisions. | `archive/research/internal/round12_results.md` | `archive/src/rosa/round12_policy.py` | See report / archive manifest |
| R13 | Cost-aware recovery not promoted; simpler equal-access controls. | `archive/research/internal/round13_results.md` | `archive/src/rosa/round13_policy.py` | See report / archive manifest |
| R14 | 14/20 exact intent compilation; conditional native gains and no universal winner. | `archive/research/internal/round14_results.md` | See report / shared experiments | See report / archive manifest |
| R15 | Conditional lean gains; strong controls tie most structures. | `archive/research/internal/round15_results.md` | See report / shared experiments | `archive/research/raw/coverage-round15-*`; report manifests |
| R16 | Neither candidate promoted; budget loses recoverable cases and economic stopping sacrifices completion. | `archive/research/internal/round16_results.md` | `archive/src/rosa/round16_policy.py` | `archive/research/raw/coverage-round16-*`; report manifests |
| R17 | NO-GO for new candidate; evidence and workload gate. | `archive/research/internal/round17_decision_audit.md` | See report / shared experiments | See report / archive manifest |
| R18 | NO-GO for new acquisition/recovery algorithm on inspected opportunities. | `archive/research/internal/round18_opportunity_validation.md` | See report / shared experiments | See report / archive manifest |
| R19 | Router not promoted; simple batching/discovery better on workload. | `archive/research/internal/round19_experimental_results.md` | `archive/research/experiments/round19/` | `archive/research/raw/round19-comparison-v1/`; report manifests |
| R20 | Hybrid ties strongest equal-fallback control; retain simple controller. | `archive/research/internal/round20_experimental_results.md` | `archive/research/experiments/round20/` | `archive/research/raw/round20-mission-v1/` |
| R21 | Cascade ties supported completion but slower on mutually exact cases. | `archive/research/internal/round21_experimental_results.md` | `archive/research/experiments/round21/` | `archive/research/raw/round21-mission-v1/` |
| R22 | 24/24 each and 141 native operations: strong verification control ties. | `archive/research/internal/round22_experimental_results.md` | `archive/research/experiments/round22/` | `archive/research/raw/round22-mission-v1/` |
| R23 | Strong ordinary status-aware control matches; feedback probe adds eight dispatches. | `archive/research/internal/round23_experimental_results.md` | `archive/research/experiments/round23/` | `archive/research/raw/round23-mission-v1/` |
| R24 | No incremental advantage over ordinary concurrent and estimation controls. | `archive/research/internal/round24_experimental_results.md` | `archive/research/experiments/round24/` | `archive/research/raw/round24-mission-v1/` |
| R25 | Conditional systems gain; stronger graph-aware control defeats novelty claim. | `archive/research/internal/round25_experimental_results.md` | `archive/research/experiments/round25/` | `archive/research/raw/round25-mission-v1/` |
| R26 | Ordinary dynamic ready-list expresses repair; stronger graph control 18 vs 14 completions. | `archive/research/internal/round26_experimental_results.md` | `archive/research/experiments/round26/` | `archive/research/raw/round26-mission-v1/` |
| R27 | 64 episodes closed; graph controllers 6/14 feasible Nav2 requests. | `archive/research/internal/round27_experimental_results.md` | `archive/research/experiments/round27/` | `archive/research/raw/round27-mission-v1/` |
| R28 | Selective gate 6/8 vs 8/8 strong flat compiler and original ROSA. | `archive/research/internal/round28_experimental_results.md` | `archive/research/experiments/round28/` | `archive/research/raw/round28-mission-v1/` |

The sibling archives contain additional protocols, revised results, independent reviews and raw records: use `archive/research/internal/INDEX.md`, `archive/research/results/`, `archive/research/raw/`, and per-round reproduction records; do not treat this index as an exhaustive per-file inventory. Older externally referenced Method Lab material is not asserted to be present in either checkout.
