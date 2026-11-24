# Stage 2 custody readiness, November 24, 2026

All 14 candidate tasks passed model-free feasibility on local Jazzy Turtlesim.
The final check covered 16 simulator trials and made zero model requests. Every
task required a dispatched action and a separate simulator state check. The
judge rejected attempts with missing required evidence or incorrect reports.
Task contracts, the candidate bank, and all trial records remain in custody.

The worker interface supplies the request, fixture and independent truth. It
checks the private bank digest and returns opaque scoring fields for the three
acting systems. The existing action and judge regression suites passed 29
tests. The full Stage 2 queue and lab deployment still need verification
before the freeze. [Custody worker interface](../exam_actions_20261121/custodian.py)

For the held-out worker, open `Stage2Custodian.episode(task_id, seed, ros_directory)`
and use the yielded request and backend for the entire episode. The custody
fixture starts and resets Turtlesim and owns the independent reader. Attach
`CustodyRecorder` to the model, native command guard, action kit and tool
callbacks. Call `score` and `write_evidence` before teardown. Use a private
worker directory and the custody-supplied planner index and bank digest.

The request-and-judge callbacks in the in-progress runner still start their own
simulator and pass a development trace to the judge. The held-out branch needs
the custody context manager so the planned reset, live read order, native
terminal receipts and independent checkpoints reach the judge. Keep the
development branch available for the public smoke. The held-out row can take
goal counts, ending class, arrival claim and observed arrival directly from
`score`.
