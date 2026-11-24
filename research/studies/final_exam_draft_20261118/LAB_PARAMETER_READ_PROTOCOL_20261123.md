# Lab parameter-read diagnostic, 2026-11-23

## Decision and stop rule

Recommend launching lab Stage 1 only if each of the four tool-by-condition timeout counts is at most **1/200 (0.5%)**. Above the threshold in any cell, keep the launch on hold and propose the best-supported environment fix without applying it. After a threshold breach, finish collecting the four fixed-denominator counts and stop. Keep other bad replies separate from command timeouts. An incomplete condition or lost fixture leaves the gate unresolved. No held-out or laptop work is part of this diagnostic.

## Evidence and rationale

The previous lab test found 7/200 timeouts for each of the two parameter tools at 32 concurrent calls. Its quiet serial probe passed 12/12 across four tools. The open question is whether native timeouts persist under the actual synchronous exam dispatch pattern. This is a lab readiness decision with a plain matched control (headless navigation off versus on). It evaluates no new agent mechanism and uses no model inference. [Preflight](LAB_PREFLIGHT_20261123.md)

The public dress rehearsal run `rehearsal_144_20261122` provided 48 completed rows. Join each full result's `run_id` to its worker trace once. The public evidence path is `research/_artifacts/runs/exam_dress_rehearsal_20261122/custody/stage1_rehearsal/queue/rehearsal_144_20261122`. Count requested tool calls in `model_end.message.tool_calls`, actual in-flight tools from matched callback start/end/error IDs, wrapper calls from `tool_start.name`, and native attempts from `ros_start.command`.

| System | Public episodes | Maximum requested together | Maximum executing together | List wrapper / native | Get wrapper / native |
|---|---:|---:|---:|---:|---:|
| EX-M | 24 | 4 | 1 | 10 / 10 | 44 / 43 |
| E1 | 24 | 2 | 1 | 10 / 10 | 44 / 44 |

Concatenated trace SHA-256 in full-result log order by system is `1293e6be1f0693c61f0105c9e648f6c40afb80876b158d006c884621ca2cb021` for EX-M and `d93167117d3d03ae97298c93041a654232d7b6af7dd3df5a731e9ed88dbf7703` for E1. The synchronous executor iterates through actions individually. Use one active request stream. The disabled-versus-enabled simulator conditions use the same node, checks, alternating tool order, exam guard, container and ROS domain.

## Procedure

Use the lab's verified `f64baf6` Stage 1 deployment. In a dedicated localhost-only ROS domain 221, start a public fixture with a known integer parameter. Verify the domain is empty before each condition. Use the real `ros2_param_list` and `ros2_param_get` wrappers with the frozen `guarded_native` function and its 15-second command timeout. Use one uncounted readiness check via ROS discovery. Alternate list and get for 200 successive pairs in each condition. Close each call before starting the next. Use one worker and no retries. Log every attempt, result validation and guard event. For the second condition start the existing headless TurtleBot3/Nav2 stack on the same isolated domain, initialize pose using its public navigation check, and require simulator clock evidence before and after the series. Stop that stack and the diagnostic's discovery daemon on exit. Use a 55-minute hard cap per read series to cover a large number of 15-second timeouts with teardown headroom. Start the no-simulator series first.

For each condition, multiply native list/get attempts per public episode by their corresponding measured timeout rates and sum. Use 10/24 and 43/24 for EX-M, and 10/24 and 44/24 for E1. Report the absolute difference as timeout exposure only. The diagnostic does not estimate answer-quality bias. Preserve raw evidence in the lab's public diagnostic directory. Verify the ROS overlay against its lab setup record without altering the shared exam freeze.
