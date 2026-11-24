# Stage 1 lab preflight, 2026-11-23

**22:10 Asia/Taipei update — recommend launching Lab Stage 1.** The serial follow-up passed the precommitted parameter-read threshold. The launch was held during the preflight below. No held-out episode ran during this diagnostic.

## Serial follow-up

The [protocol](LAB_PARAMETER_READ_PROTOCOL_20261123.md) and driver were committed as `334b750` before execution. Across 24 public rehearsal episodes per system, EX-M requested at most four tools in a model reply and E1 at most two. Both executed one at a time. Each averaged 10/24 parameter-list wrapper calls and 44/24 parameter-get wrapper calls. Native get attempts were 43/24 for EX-M and 44/24 for E1.

| Lab condition | List timeouts | Get timeouts | Other failures |
|---|---:|---:|---:|
| Navigation off | 0/200 | 0/200 | 0 |
| Headless navigation on | 0/200 | 0/200 | 0 |

All four rates passed the **at most 1/200** rule. Multiplying the native call counts by the measured rates gives **0.000 expected timeouts per episode** for both systems in both conditions. This estimates timeout exposure under the tested conditions.

The first graph check detected its own temporary ROS node before any parameter reads. A self-excluding observer passed. The first navigation setup reached its goal, but a reader in a second container did not receive the clock, so it scored zero reads. The counted conditions used the same lab container and domain. In the successful navigation condition, the simulator clock advanced from 39.692 to 681.521 seconds, and cleanup reported zero surviving simulation processes.

The lab setup record `ops/ROS_OVERLAY_SETUP.txt` now records **883 verified files** for the lab-only ROS overlay. Manifest SHA-256 is `c551f3dc7239d9515c6d762ad4e6a84737a13cbb161b778f9294a00244ec80ed`. The environment-script manifest SHA-256 is `b9ac37f72365c53e9fa0a6c9f4d23b32e2f4cda6643f78a56da39020eeb5479b`. Both were checked again after the run. The overlay is a lab-vs-laptop environment difference, recorded separately from the shared freeze.

Raw diagnostic evidence remains on the lab under `parameter-read-334b750-r2/without-nav` and `parameter-read-334b750-nav-local/with-nav`. The corresponding native log SHA-256 values are `f93e2efc6660a726e798a5bd0dd2fd212d7ddb89cf928c2744dcad411f319359` and `fe8a2fde9b350d1d23469d8e3cc6e8940942f257dc3716d7b16b6aeca006d94b`.

## Deployment and recovery

- The user approved transferring the selected Stage 1 files to the existing shared-login lab custody directory. The transfer contained the 15 hash-bound fixture and pool input files. It carried no run output or unrelated study. The frozen verifier passed in the lab with Ollama 0.40.17 and seven matching model digests. The container uses `--init`, read-only code and inputs, and separate writable output directories. The pinned Forge environment was verified. Forge still has its separate held-out adapter prerequisite.
- The bundled ROS image lacked the demo nodes and example service interfaces used by a Stage 1 fixture. The two laptop packages passed the installed-file checksum check. Their package files were added as a lab-only ROS overlay and the relevant executables and service type support were verified. The frozen research files were unchanged.
- With the real launcher and two public cases, I killed the runner after it saved its first full result. Restart repaired exactly one missing compact summary and stopped one leftover ROS discovery process. The queue finished with two unique full rows, two compact rows, two worker starts, zero missing or duplicate rows, and an empty ROS graph. One answer scored supported and the other unsupported. The test establishes persistence, restart and scoring behavior for those cases.
- The headless public navigation check reached its goal and stopped its owned processes. The host GPU sampler identified the lab Ollama process. The lab ntfy topic is configured and the historical sender log records a successful send. Phone delivery was not checked in this preflight.

## Read reliability and stop decision

- Initial four-lane public read diagnostics with and without headless navigation exceeded their time caps. These diagnostics used the direct ROS tool path without the exam's 15-second per-command bound. The diagnostic processes and their child commands were stopped, and the headless stack reported a clean shutdown.
- A serial follow-up through the actual read wrappers and the frozen command guard returned valid results on three calls of each of four tools. The second audit stripped indentation in the three parameter lists, all of which contained the expected parameter.
- A bounded 200-per-tool follow-up with the same guard ran concurrent calls without the headless simulator. The native command records show 7/200 parameter-list timeouts, 7/200 parameter-get timeouts, and 0/200 failures each for node-info and service-info. The high concurrency differs from the serial follow-up. The result shows a lab failure under the tested load and does not establish its rate under the live exam workload. The guarded follow-up with headless navigation was not started. The lab queue was not launched.

This preflight motivated the serial follow-up recorded above. The concurrent failure counts remain evidence from that condition.

[Frozen protocol](PROTOCOL_DRAFT.md) · [Setup log](LAB_SETUP_LOG.md) · [Revision 2 recovery rules](../exam_dress_rehearsal_20261122/REV2_FREEZE_DRAFT.md)
