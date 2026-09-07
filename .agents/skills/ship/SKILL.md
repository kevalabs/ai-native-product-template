---
name: ship
description: Deliver a proved outcome after its Proof PR merges and record successful shipment in a separate ship.md PR.
---

Read the Intent, accepted Spec, approved Plan, proof.md, REVIEW.md, and
`.githooks/README.md`. Find the existing Ship Task, run make handoff,
and start a ship/NNN[-Pn]-name worktree from the updated default branch.
Verify the exact passing Proof PR and Build version before delivery.

Perform only the delivery authorized by the approved Plan and session.
Use `templates/ship-template.md` to record the proved Build SHA, merged
Proof SHA, destination, result, and delivery evidence. For this template,
delivery is the approved default-branch version; a tag is optional.
Never record delivered or success while delivery is incomplete or failed.

Commit only ship.md and open its reviewed PR with the Stage issue link.
Update the existing Task; verify identities before writes and unknown
write results before retries. Failure keeps Ship and the parent open.
After successful delivery and this evidence PR's merge, record the final
approved permalink and PR on the Task and close it as completed. Record
its own merge on the issue, without creating recursive evidence PRs.

Check all required phase shipments and every Intent success criterion
before closing the parent. A cancelled outcome is not shipped and does
not unlock dependencies. Reopened work needs its evidence checked again.
Shipped artifacts become immutable; later behavior changes use new
intents. Do not close an outcome just because its Build PR merged.
