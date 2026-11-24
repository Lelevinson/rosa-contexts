# Lab Stage 1 launch handover for Claude Code

Claude Code owns the lab launch. The [serial parameter-read diagnostic](LAB_PREFLIGHT_20261123.md) passed all four thresholds. At handover the lab container was running, the verifier exited 0, and the lab exam had no session or status file. Leave the laptop run alone.

## Paths on the lab

- Deployment root `<LAB_PATH>/stage1-release-f64baf6`. The frozen checkout is its `repo/` directory, and the host launcher and service logs are in `ops/`.
- Container `rosa-exam-stage1-lab`. Enter from the lab host with `docker exec -it rosa-exam-stage1-lab bash`. It starts in the frozen checkout. For a manual ROS environment check, source `/opt/ros/jazzy/setup.bash` and then the deployment's `forge/ros-overlay.env`.
- Run name `stage1_lab_20261123`, machine `lab`, queue assignment `lab:1`, tmux session `exam-stage1_lab_20261123`.
- Held-out bundle path `<LAB_PATH>/custodian/stage1_deploy_f64baf6/stage1_20261121`. Claude Code must not open, list, or search the bundle. The frozen launcher accesses it through the custodian bridge.
- The launcher stores full outputs under `<bundle>/queue/stage1_lab_20261123/` and compact results under `<bundle>/compact/stage1_lab_20261123/`. Treat those directories and the runner log as custodian-only. Use the status command below for progress.
- The lab-only ROS overlay is under the deployment's `forge/ros-overlay/`. The setup record is `ops/ROS_OVERLAY_SETUP.txt`. It records 883 verified files, the hashes of `ops/ROS_OVERLAY.sha256` and `ops/ROS_OVERLAY_ENV.sha256`, and the package versions.

## Verify and start

Run these commands on the **lab host**, in order.

```bash
stage=<LAB_PATH>/stage1-release-f64baf6
python3 -B "$stage/repo/research/studies/final_exam_draft_20261118/freeze_package_20261121/verify_freeze_rev2.py" http://127.0.0.1:11435
```

Expect exit **0** and `VERIFIED (FREEZE.json + FREEZE_REV1.json + FREEZE_REV2.json)`. If it returns another code, stop and contact the custodian.

```bash
bash <LAB_PATH>/stage1-release-f64baf6/ops/launch.sh start
bash <LAB_PATH>/stage1-release-f64baf6/ops/launch.sh status
```

Run `start` once. It checks for fresh output directories, an idle ROS graph, GPU and disk headroom, and guard readiness. It starts a detached session with the GPU sampler, version guard, monitor, and runner. Use `status` again after the runner has created its first status file. If start fails or a prior run exists, preserve the existing directories and contact the custodian before attempting recovery.

## Lab differences

The lab uses the same frozen Stage 1 spec and localhost-only ROS domain **219**. It runs inside the lab container with the ROS overlay and uses **Ollama 0.40.17 at `http://127.0.0.1:11435`**. The GPU sampler, guard, monitor, and ntfy sender run on the lab host. The launcher handles these differences. Keep lab results separate from laptop results.

Use the existing lab ntfy topic in `~/.config/rosa-exam/notify.env` on the lab host (mode `0600`). Keep the value private and retain the existing topic so the owner's subscription keeps working. The monitor sends status counts. A historical send was acknowledged, and phone receipt was not checked in the latest preflight.
