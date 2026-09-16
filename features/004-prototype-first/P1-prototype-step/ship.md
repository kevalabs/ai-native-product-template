# Confirm a prototype before writing its spec — Ship

**Status:** delivered
**Stage:** ship
**Outcome:** 004-prototype-first
**Phase:** P1-prototype-step
**Parent issue:** https://github.com/kevalabs/ai-native-product-template/issues/22
**Stage issue:** https://github.com/kevalabs/ai-native-product-template/issues/30
**Predecessor PR:** https://github.com/kevalabs/ai-native-product-template/pull/48
**Build commit:** 3ee3aea5d08b4dacbc73d18baab7f4ceeb6519de
**Proof commit:** 5482e89ea5a198fe52f26a397c368fe5d3cff4be
**Artifact identity:** 3ee3aea5d08b4dacbc73d18baab7f4ceeb6519de
**Artifact source:** 3ee3aea5d08b4dacbc73d18baab7f4ceeb6519de
**Destination:** kevalabs/ai-native-product-template default branch main
**Result:** success
**Delivery evidence:** https://github.com/kevalabs/ai-native-product-template/commit/5482e89ea5a198fe52f26a397c368fe5d3cff4be

## Delivery

The proved P1 implementation is available on main. For this source-only
template, that reviewed default-branch version is the approved delivery
target. There is no runtime deployment, required release tag, or newly
configured provider. The immutable artifact identity remains the merged
Build SHA above; it has not been rebuilt or replaced.

On 2026-09-16, Suraj Chhetry [approved Proof PR #48][proof-review] for
exact head `8bd519d560c82d90b1bdda263fc03dee13eab7d8` at 11:50:39 UTC.
Both required [Proof CI checks][proof-ci] passed. The PR merged into
main at 11:50:50 UTC as the Proof commit above. Task #29 records its
approved permalink, merged PR, and completed status.

The live Ship entry gate passed before this worktree was created from
that merged Proof. Git comparisons establish that:

- The merged Proof tree matches the exact reviewed Proof head.
- The Build and Proof commits are both ancestors of fetched main.
- Only this phase's `proof.md` differs between the proved Build and
  the delivered main snapshot. All implementation and planning content
  remains unchanged.
- Proof's Build commit, artifact identity, and artifact source all equal
  the Build SHA recorded here. The version at the delivery destination
  therefore contains the same proved implementation.

`make test` passed all 86 tests again in the Ship checkout, including
the existing syntax and whitespace checks. Proof also records the
executed evidence exercises, manual results for
S1–S26, and the human Build review against this same implementation.

P1's accepted Spec predates the new prototype step. No real prototype
confirmation is back-filled and no confirmed prototype ref is deleted
by this shipment. Proof's example fixtures remain explicitly synthetic.
Future adopting work retains its confirmed commit and decision through
shipment under the delivered guidance.

This PR records successful source delivery. Task #30 and phase task
#25 remain open until this Ship evidence receives human review and
merges. Then record the approved Ship permalink and merged PR on the
task, verify phase completion, and close those P1 records. Record this
PR's own final merge on the issues; do not create another evidence PR.
The parent Intent remains open for P2, P3, and their success criteria.

## Intent results

P1 delivers its approved documentation outcome: contributors have one
prototype workflow, three forms, owner confirmation of an exact version,
preserved examples, a justified skip, and consistent stage and delivery
instructions. [Proof][proof] covers every P1 Spec rule and distinguishes
manual review from automated checks.

The shared Intent's six success criteria have these results:

1. **Confirmation before Spec:** the delivered skills and templates
   require exact-version owner confirmation or a concrete skip, and
   preserve reviewable evidence. Proof exercised the positive and
   negative procedures; downstream product adoption is not asserted.
2. **Same examples in Build tests:** the Markdown examples format and
   direct JSON reader preserve the same file. Proof verified its bytes,
   normal calculation, changed-data case, and retained Git evidence.
3. **Prototype branch and sandbox checks:** not delivered by P1.
   P2 owns the new lane and enforcement. The current skill requires
   an already permitted workspace and does not bypass existing gates.
4. **One-command lifecycle tracking:** not delivered by P1. P3 owns
   automation; capability R24 still records its absence.
5. **Existing gates and human approval:** Intent PR #43, Spec PR #45,
   Plan PR #46, Build PR #47, and Proof PR #48 have their separate
   reviewed merges. Current validators remain unchanged. This Ship
   evidence has the same required human review and merge gate.
6. **Adoption note:** P1's guide explains adoption before Spec, retained
   evidence, and unchanged accepted history. The final cross-phase
   adoption note remains part of P3's Ship and is not claimed complete.

No feature flag or regional rollout applies to this template change.
Expiry, confirmation, and retention are manual instructions and human
review checks. No sandbox enforcement, automatic expiry or retention
service, or background issue/PR automation is included.

After this Ship PR merges and P1 completion is recorded, dependent
P2 and P3 stages must pass their own live entry checks. The full parent
outcome is not complete merely because P1 is delivered.

[proof-review]: https://github.com/kevalabs/ai-native-product-template/pull/48#pullrequestreview-5222234300
[proof-ci]: https://github.com/kevalabs/ai-native-product-template/actions/runs/35092424989
[proof]: https://github.com/kevalabs/ai-native-product-template/blob/5482e89ea5a198fe52f26a397c368fe5d3cff4be/features/004-prototype-first/P1-prototype-step/proof.md
