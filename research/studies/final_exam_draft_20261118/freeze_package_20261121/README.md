# Stage 1 freeze package (DRAFT, 2026-11-21; nothing here is hashed or frozen)

| file | what it is |
|---|---|
| `make_exam_spec.py` | generator of the exam spec and cell counts (`write`, `counts`); no custodian file opened |
| `exam_spec_stage1_DRAFT.json` | generated spec: 4 tiers in the owner's laptop order, seeds 1-3, master seed 20261122 (draft value), pool from the custodian's file named by `ROSA_HELDOUT_V2_TASKS` |
| `MODEL_DIGESTS_DRAFT.json` | full digests of the 4 core and 3 extra models from the laptop Ollama (the 4 core digests equal those of `steady_loop_ablation_20261117/FREEZE.json`); the lab's copies are compared at the lab pre-run gate |
| `SUCCESS_AND_INVALIDATION_DRAFT.md` | the criteria and invalidation text of draft section 9c items 4 and 8 |

Expected cells with 76 tasks: tier 1 1,824; tier 2 1,824; tier 3 2,736; tier 4 1,368; total 7,752 (6,384 core + 1,368 extras). Tier 2 contains F, which has **no runner adapter**: the queue refuses its cells until the smoke gate result and an adapter exist (see the [exam prep report](../../exam_prep_20261121/REPORT_STAGE1_FREEZE_PREP.md)).

**Still needed before hashing (not done here):** the custodian's manifest and held-out v2 task file (Codex), the hold-out adapter that lets `run_exam.py` score held-out ids (today it knows development tasks only), the final master seed, the git revision of the code, the freeze file listing file hashes (as the dev studies' `make_freeze.py` do), and the owner's confirmation of the text. Cell order inside a tier follows the queue's generic rule (seed, task shuffle, model, system shuffle in the pair); the dev studies' per-(model, environment) fixture-session grouping is **not** used and whether the exam needs it is open.

To hash after approval (a command, not run): `sha256sum exam_spec_stage1_DRAFT.json MODEL_DIGESTS_DRAFT.json SUCCESS_AND_INVALIDATION_DRAFT.md`.
