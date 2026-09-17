# Test + Review and Ship evidence land where they are produced — Build

**Status:** ready
**Stage:** build
**Outcome:** 005-right-size-evidence
**Phase:** P1-evidence-in-build
**Parent issue:** https://github.com/kevalabs/ai-native-product-template/issues/51
**Stage issue:** https://github.com/kevalabs/ai-native-product-template/issues/56
**Predecessor PR:** https://github.com/kevalabs/ai-native-product-template/pull/75
**Plan commit:** c3523c238bb21e043345f97753cbc27ee7d09a00
**Verification:** make test passed all 99 tests, lint, and template verification on this branch; 13 tests are new and each failed before its check existed.

<!-- Fill only with verified results. Do not claim passed/delivered while blocked. -->

## Requirement results

- S1: PASS — test_delivery_setting_modes_and_errors declares each mode in the conventions file and stages a Build under it.
- S2: PASS — test_runtime_artifact_path_is_unchanged builds under runtime artifact with no S-rule results, and the 86 pre-existing tests still cover that path unchanged.
- S3: PASS — test_build_record_requires_result_per_s_rule accepts one PASS line per S-rule naming its test.
- S4: PASS — test_build_record_requires_result_per_s_rule rejects a missing rule, a FAIL, and a name absent from the declared test paths.
- S5: PASS — test_last_phase_records_every_intent_criterion requires one TRUE or OPEN line per criterion.
- S6: PASS — test_build_merge_requires_non_author_approval rejects no review, a self-approval, and a stale approval.
- S7: PASS — test_shipped_tag_must_be_on_merged_build resolves the tag for a single phase and a named phase.
- S8: PASS — test_shipped_tag_must_be_on_merged_build rejects an absent tag and a commit with no ready Build record.
- S9: PASS — test_moved_shipped_tag_is_rejected rejects a tag outside the default branch.
- S10: PASS — test_dependent_handoff_requires_shipped_tag unlocks a dependent stage only when the predecessor phase is tagged.
- S11: PASS — test_shipped_tag_freezes_the_phase blocks a change under a tagged phase.
- S12: PASS — test_records_carry_each_tracking_fact_once checks the build template and this record for a repeated commit hash.
- S13: PASS — test_task_shape_follows_delivery_mode expects four tracked stages for merged source and six for runtime artifact.
- S14: PASS — test_last_phase_records_every_intent_criterion blocks a last phase that leaves a criterion OPEN.
- S15: PASS — test_guidance_states_one_consistent_policy checks the README setup section for the authoring-identity rule.
- S16: PASS — test_setup_report_names_authoring_identity prints the requirement when required review is configured, and not otherwise.
- S17: PASS — test_guidance_states_one_consistent_policy checks every guidance file for instructions that contradict merged-source delivery.
- S18: PASS — test_task_shape_follows_delivery_mode keeps a not-planned task out of the graph.
- S19: PASS — test_guidance_states_one_consistent_policy checks that each named human gate still appears in the conventions file and review policy.
- S20: PASS — test_delivery_setting_modes_and_errors names both accepted values for an absent or misspelled setting.
- S21: PASS — test_build_record_requires_result_per_s_rule names the absent test in the failure.
- S22: PASS — test_build_record_requires_result_per_s_rule fails when the Spec gains a rule the record does not cover.
- S23: PASS — test_shipped_tag_must_be_on_merged_build reports an invalid tag rather than treating the phase as shipped.
- S24: PASS — test_build_merge_requires_non_author_approval blocks the dependent handoff for an unreviewed Build merge.
- S25: PASS — test_runtime_artifact_path_is_unchanged keeps the runtime-artifact Proof and Ship requirements in place.
- S26: PASS — test_task_shape_follows_delivery_mode rejects a cancelled task as a completed dependency.

## Intent results

- OPEN — for a merged-source product, one outcome takes four merged PRs after Intent acceptance. The checks and guidance now allow it, but this outcome's own P2 and P3 still have to run under the new rules before the claim is observed end to end.
- TRUE — every Spec S-rule has a named test and a recorded result against the merged Build, and CI fails when one is missing or does not pass. S3, S4, S21, and S22 enforce it.
- OPEN — a bug fix to a shipped outcome lands in one reviewed PR. P2 owns the fix lane.
- OPEN — a product can turn stage issues off. P3 owns optional tracking. This phase makes the tracked stage set depend on the delivery mode, which is the smaller step.
- TRUE — a solo developer following the README can get a PR approved and merged under required branch protection without a bypass. The setup section states the rule and the setup check reports it.
- TRUE — every existing human gate still applies. No stage order changed, no artifact PR was removed, and Build gained a required non-author approving review.

## Changes

A product declares `Delivery: merged source` or `Delivery: runtime
artifact` with its test paths in a new `## Delivery settings` section of
the conventions file. Both validators read that section from the
reviewed version, so the setting is reviewed like any other rule.

For merged source, the Build record carries one result per Spec S-rule
naming the test that proves it, and one line per Intent success
criterion. The check compares the record's rules with the accepted
Spec's, rejects a FAIL, and searches the declared test paths for each
named test as a literal string. The outcome's last phase cannot leave a
criterion open. Shipment is an annotated `shipped/<outcome>[-<Pn-name>]`
tag on the merged Build commit: the dependent handoff requires it before
a later phase starts, and the local check freezes a tagged phase the way
a delivered `ship.md` did. Those products track Intent, Spec, Plan, and
Build tasks; a task for an untracked stage is closed as not planned and
unlocks nothing.

Every Build PR now needs a current approving review from someone who is
not its author, whoever merges it. That review is the Test + Review
step. The setup report states that required review implies a separate PR
authoring identity, because GitHub ignores an approval from a PR's
author.

For runtime artifact, nothing changes. Proof and Ship keep their
branches, records, PRs, and tasks, and the 86 pre-existing tests still
cover that path.

Guidance, templates, skills, the glossary, and the capability doc now
describe both paths once. Capability rules R34 to R38 record the new
behavior; R10, R19, and R22 are updated in place.

## Transition

Started from merged Plan PR #46's successor, the revised Plan at the
commit above, after PR #75 widened the approved surface. The live entry
gate for Task #56 passed on 2026-09-17. Accepted Spec PR #73 and Intent
PRs #71 and #72 are on the base.

Three deviations from the approved Plan, all recorded rather than
hidden. First, the Plan's touched surface grew from 26 to 29 files in
reviewed PR #75, because the capability skill and the proof and ship
templates carried instructions that contradict merged-source delivery
and S17 requires the Build to update them. Second, the Plan's test table
maps T8 to one test; it is proven by two, because S10 is a GitHub
evidence rule and S11 is a local one. Third, the setup requirement is
reported as an advisory note rather than a pass/fail check, so an
unverifiable fact cannot turn `make setup-check` red.

One design correction during Build: the first version read the delivery
setting from the PR base, which made every PR fail until the setting
existed on the default branch. It now reads from the reviewed head and
falls back to the six-stage shape when a product has not declared a
mode, so the explicit failure stays where S1 puts it, on the Build
check.

Shipped chains 001 to 004 are unchanged. Their `ship.md` records remain
valid shipment evidence. This phase does not back-fill tags for them.

## Confirmed examples

The accepted Spec records a prototype skip: process rules, templates,
and documentation only, with nothing to inspect before Build. There is
no confirmed examples file, no preserved evidence, and no example
reader. No example data is invented here.

## Delivery preparation

Delivery is `merged source`, so the reviewed merge of this PR is the
delivery. Shipment is one annotated tag,
`shipped/005-right-size-evidence-P1-evidence-in-build`, pushed on that
merge commit, with a message naming this PR. No artifact is built, no
Proof or Ship PR opens, and tasks #57 and #58 close as not planned under
S18. The merge SHA is not yet known and is not invented here.
