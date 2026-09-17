---
name: ship
description: Deliver a proved outcome after its Proof PR merges and record successful shipment in a separate ship.md PR.
---

Read the Delivery setting in AGENTS.md first; it decides this stage's
shape.

For `merged source`: the reviewed Build merge is the delivery. Verify
the Build PR merged with a current non-author approving review and that
its record's results are complete. Then push one annotated tag on that
exact merge commit, named `shipped/<outcome>` or
`shipped/<outcome>-<Pn-name>`, whose message names the merged Build PR.
Never tag another commit, never move an existing tag, and never tag work
that has not merged. Record the tag and merge commit on the Build Task,
then close it. There is no ship.md and no Ship PR.

For `runtime artifact`: read the Intent, accepted Spec, approved Plan,
proof.md, REVIEW.md, and `.githooks/README.md`. Find the existing Ship
Task, run make handoff, and start a ship/NNN[-Pn]-name worktree from the
updated default branch. Verify the exact passing Proof PR and Build
version before delivery.

Read the proved artifact identity, originating Build commit, and result
evidence. Deliver that same artifact and compare its identity at the
destination. If it is unavailable, differs from Proof, or the destination
requires rebuilding it, leave shipment unsuccessful; obtain reviewed
Build changes and renewed Proof rather than claiming equivalent output.
For this template, the merged Build source SHA is the artifact identity.
See [delivery rules](../../../docs/agentic-sdlc.md#branches-and-delivery).
Retain the confirmed prototype commit and decision through shipment;
check their reachability before any later cleanup under product policy.

Perform only the delivery authorized by the approved Plan and session.
Use `templates/ship-template.md` to record the proved Build SHA, merged
Proof SHA, destination, result, and delivery evidence. For this template,
delivery is the approved default-branch version; a tag is optional.
Never record delivered or success while delivery is incomplete or failed.

Commit only ship.md and open its reviewed PR to main with the Stage issue link.
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
