---
name: feature
description: Read-only product board showing shipped, accepted, and proposed outcomes, their current stage, and the next verified gate.
---

Read product/capabilities/ and the outcome artifacts under features/.
With an NNN argument, report that chain; otherwise show the product board.
Read `.githooks/README.md` for stage tasks and evidence fields.

For each chain or phase, inspect both artifacts and their linked GitHub
issues/PRs. Distinguish stage from status. Intent, Spec, Plan, Build,
Test + Review, and Ship each require their own approved merged PR.
A file's existence, accepted marker, local Plan commit, or closed task
alone does not unlock the next stage. Name missing approvals, merges,
links, inaccessible evidence, stale proof, and unmet phase dependencies.
Use the read-only handoff check where appropriate; do not mutate records.

Show Proposed for draft intents, Accepted for accepted outcomes before
Build, In build after the Plan merge, and In review/proof/delivery as
supported by current work. Show Shipped only after successful delivery
and merged Ship evidence, with all phases and success criteria complete.
A Build merge or capability update alone is not shipment. Keep cancelled
outcomes separate and do not treat their dependencies as complete.

Older shipped chains retain their actual historical completion evidence;
do not retroactively require artifacts that did not exist under their
workflow. Report missing evidence explicitly for active-chain adoption.
If GitHub is unavailable, mark the result unverified rather than infer
remote success. Current capability text may state release restrictions.

For the whole board, show shipped, accepted/in-flight, then proposed
outcomes. Detail only relevant health issues. For one chain, show phase
progress and its next command/gate. This is read-only; never advance a
stage, close an issue, or rewrite an artifact to make a report look green.
