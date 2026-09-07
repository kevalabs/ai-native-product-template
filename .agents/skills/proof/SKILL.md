---
name: proof
description: Test and review an exact merged Build against its Spec and Intent, then prepare a separate proof.md evidence PR before Ship.
---

Read the accepted Intent, Spec, Plan, Build record, REVIEW.md, and
`.githooks/README.md`. Resolve the exact outcome or phase and its
existing Test + Review Task. Run make handoff for that Task before
starting, and create a proof/NNN[-Pn]-name worktree from updated main.
The Build PR must already be merged; ordinary Build tests came before
that merge and are not deferred to this stage.

Use `templates/proof-template.md`. Record the full merged Build SHA,
its PR, parent and Task links, and a result for every Spec S-rule.
Use one `- S1: PASS — evidence` line per rule only when it actually
passes. Link test results, human review, and Intent success results.
Set passed only when every requirement has evidence and no blocking
finding remains. A model's PASS text does not establish human review.

Run make test on the named Build and check that no product or planning
changes have made its evidence stale. Resolve blocking findings through
a reviewed Build correction or revised approved scope, then repeat
proof for the new version. A proof branch cannot change implementation.

Commit only proof.md, open its PR with the Stage issue link, and update
the existing Task. Verify existing identities before writes and unknown
write results before retries. After review and merge, record the approved
permalink and merged PR, mark the Task Done, and close as completed.
Keep the parent open. Ship starts only after this passing Proof PR merges.
