# Lab Stage 1 launch record, 2026-11-23

Written by Claude Code. Status counts only: no held-out, custodian, trace or runner-log content was opened. Follows [LAB_LAUNCH_HANDOVER_20261123.md](LAB_LAUNCH_HANDOVER_20261123.md). The lab stratum is never pooled with the laptop run.

## What was done

- Access: `ssh <LAB_USER>@<LAB_HOST>` (host `n`) with key login, no password prompt.
- Before start: `verify_freeze_rev2.py http://127.0.0.1:11435` exited 0 with `VERIFIED (FREEZE.json + FREEZE_REV1.json + FREEZE_REV2.json)`. `launch.sh status` said "no status file yet".
- Start: `bash ops/launch.sh start` (once) exited 0 at 2026-11-23 22:32:50 (lab host clock, CST). The detached tmux session `exam-stage1_lab_20261123` has four windows (gpu, guard, monitor, runner). It does not depend on the SSH connection. Run `stage1_lab_20261123`, machine `lab`, queue `lab:1`, status `started_at` 22:32:52.
- Observation: a second container, `rosa-exam-stage1-preflight`, was also running. The handover does not mention it. `launch.sh start` passed its idle-ROS-graph check anyway.

## First cells (status counts at 22:36:28 and 22:38:11)

| Time | done / total | current cell | heartbeat age |
|---|---|---|---|
| 22:36:28 | 5 / 7752 (tier 1: 5 / 1824) | EX-M:lfm3:1.7b | 5 s |
| 22:38:11 | 8 / 7752 (tier 1: 8 / 1824) | E1:lfm3:1.7b | 18 s |

Skipped 0, contended 0, quarantined none, Ollama ok, disk 392.4 GB free. `gpu_used_mib` is null in the status file on the lab (the laptop reports a value); the lab GPU sampler writes only to the custodian bundle, so this was not investigated. Host `nvidia-smi` showed 3058 / 16376 MiB.

## Checks

- ROS graph between cells: six `ros2 node list` samples (domain 219, localhost only) inside the container gave 1, 23, 23, 23, 0, 23 nodes. The 0 shows the graph empties between episodes. Six samples cannot show it is clean after every cell.
- Infra share: not available from the status-only view; it would need trace content, which is custodian-only. Not measured.
- ntfy: the monitor logged a `daily` send at 22:33:23 (`ntfy: True`). `notify.py test KIND` crashes (`send() got multiple values for argument 'kind'`, a bug in the unfrozen helper), so one test message was sent directly with `notify.send_ntfy`. The call returned without an error. Phone receipt is not verified by the sender.

## Speed and projection (early, optimistic)

8 cells in 319 s is about 40 s per cell. The first cells are the smallest model (lfm3 1.7b) of the tier, so this is a lower bound. At 40 s per cell: tier 1 (1824 cells) about 20 h, finishing about 2026-11-24 19:00; the full queue (7752 cells) about 86 h, finishing about 2026-11-27 12:30. For comparison, the laptop averaged about 87 s per cell (1162 cells in 28 h). At that speed the lab would need about 44 h for tier 1 and about 187 h for the full queue. Re-project once larger models start.

## Laptop (counts only, 2026-11-23 22:38)

Running, tier 1, 1162 / 1824 tier 1 cells done (1162 / 7752 overall), 16 skipped, 0 contended, block 43, disk 989.5 GB free, heartbeat 18 s. Infra share is not available from the status view. Alerts: the laptop `notify.log` records a `crash` send at 2026-11-23 20:42:21, although the run still shows `running` with a fresh heartbeat. Cause not investigated.

## Incident on 2026-11-26, 12:29–14:09 Asia/Taipei

- The host package log records Docker 29.6.1 to 29.10.1 and containerd 2.2.5 to 2.4.2 upgrades at 12:29. The service journal records containerd starting at 12:29:37, and Docker stopping and starting at 12:29:38. Docker inspection places both exam containers' exits at 12:29:38.
- The existing Stage 1 container started again at 13:41:06 with the same image, host networking and init enabled. The Stage 1 runner's status records its new start at 14:09:22, about 1 hour 40 minutes after the interruption. The Stage 2 container remained stopped at inspection.
- The Ollama listener's process start was November 23 at 20:30:58. It served version 0.40.17. The lab verifier matched the local verifier's SHA-256 and exited 0 against the running server. All frozen files and all seven pinned model digests verified. Checks used the package and service journal, container metadata, read-only Ollama metadata and counts-only queue status.
