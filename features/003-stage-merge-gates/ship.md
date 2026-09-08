# Review linked outcomes and merge each stage before advancing — Ship

**Status:** delivered
**Stage:** ship
**Outcome:** 003-stage-merge-gates
**Phase:** single
**Parent issue:** https://github.com/kevalabs/ai-native-product-template/issues/10
**Stage issue:** https://github.com/kevalabs/ai-native-product-template/issues/16
**Predecessor PR:** https://github.com/kevalabs/ai-native-product-template/pull/20
**Build commit:** 54764fe2237ca9098360acc99b13a2fdc0d9df57
**Proof commit:** 154dac1d6e098a205cb10c7bb004f1afc1689a8d
**Destination:** kevalabs/ai-native-product-template default branch main
**Result:** success
**Delivery evidence:** https://github.com/kevalabs/ai-native-product-template/commit/154dac1d6e098a205cb10c7bb004f1afc1689a8d

## Delivery

The proved implementation is available on main. For this template,
that default-branch version is the delivery target; no deployment
service or release tag is required by the approved Plan.

On 2026-09-08, [Proof PR #20][proof-pr] merged after Suraj Chhetry approved
its final head `270361e4c95596fa9bb2b06d767ebcf3e3939dfe`. Both required
[CI checks][proof-ci] passed. [Proof task #15][proof-task] records the
human review, merged PR, and exact approved artifact permalink.

The live Ship entry check passed before this worktree was created from
that merged Proof. A Git comparison confirms that only proof.md differs
between the named Build and the delivered default-branch version. The
merged Proof also matches the exact file reviewed in PR #20. No tested
implementation or planning content changed after the Build was proved.

`make test` passed all 86 tests, Python and shell syntax checks, and
whitespace checks in this Ship worktree before handoff.

The setup report confirms the Intent issue type, both required checks,
and renewed human approval are configured. Administrator enforcement
and the existing branch protection remain in place. The bot creates
and pushes this Ship PR; the human owner reviews and approves it.

This record supplies the successful default-branch delivery evidence.
Ship task #16 and parent #10 remain open until this evidence PR receives
human approval and merges. After that merge, record its final commit
permalink and PR on task #16, rerun the final success check, and close
the task and parent as completed. The final links belong on those
issues; no additional evidence PR is needed.

## Intent results

This is the intent's single phase. Its six success criteria have the
following evidence, with final closure gated by this Ship PR's merge:

1. **Planning and Build wait for their predecessors.** Accepted Intent
   PR #6, Spec PRs #7/#8, and approved Plan PR #9 precede Build PRs
   #17/#18. The committed checks reject early or bundled stages.
2. **Proof and Ship wait for reviewed merges.** Proof PR #20 checked
   the corrected Build from PR #18. Ship started only after #20 merged
   and its live handoff passed. No unmerged Proof branch authorized it.
3. **One parent tracks the whole outcome.** Intent issue #10 has the
   six stage tasks #11–#16. The first five tasks are completed. Ship
   task #16 and the parent stay open until the final shipment gate.
4. **Artifacts and tracking remain connected.** Completed stage tasks
   retain immutable approved links and merged PRs. Build, Proof, and
   Ship artifacts link their tasks; the parent indexes the available
   artifacts. Earlier planning backlinks remain an explicitly recorded
   legacy gap, as accepted in the Build transition.
5. **Status alone cannot authorize work.** Proof documents the passing
   negative tests for local-only approvals, closed issues, unmerged
   PRs, wrong-phase evidence, and additional dependencies. The live
   Ship gate was checked against actual merged Proof evidence.
6. **Guidance and checks identify the same final gate.** Conventions,
   stage skills, status reports, templates, and checks use Intent →
   Spec → Plan → Build → Test + Review → Ship. The only remaining
   stage completion gate is human approval and merge of this Ship PR,
   followed by recording its completion on the existing issues.

The result is limited to this repository template and its installed
GitHub policy. Repositories created from the template still need their
own app installation, tracking records, and remote protection setup.
Future behavior changes start a new intent after this outcome ships.

[proof-pr]: https://github.com/kevalabs/ai-native-product-template/pull/20
[proof-ci]: https://github.com/kevalabs/ai-native-product-template/actions/runs/34178057219
[proof-task]: https://github.com/kevalabs/ai-native-product-template/issues/15
