# A fix to shipped behavior lands in one reviewed PR — Build

**Status:** ready
**Stage:** build
**Outcome:** 005-right-size-evidence
**Phase:** P2-fix-lane
**Parent issue:** https://github.com/kevalabs/ai-native-product-template/issues/51
**Stage issue:** https://github.com/kevalabs/ai-native-product-template/issues/62
**Predecessor PR:** https://github.com/kevalabs/ai-native-product-template/pull/80
**Plan commit:** 4fc4c4b10c42f256e04b06746d48ad8eb3c49c26
**Verification:** make test passed all 109 tests, lint, and template verification on this branch; 10 tests are new and each failed before its check existed.

<!-- Fill only with verified results. Do not claim passed/delivered while blocked. -->

## Requirement results

- S1: PASS — test_fix_branch_carries_test_change_and_record accepts a fix/ branch and rejects an unsupported name.
- S2: PASS — test_fix_branch_carries_test_change_and_record passes a fix carrying only a test, a change, and its record, with no stage artifact.
- S3: PASS — test_review_policy_states_the_restore_only_rule checks the review policy states the restore-only judgement and the refusal.
- S4: PASS — test_review_policy_states_the_restore_only_rule checks the policy says size never decides.
- S5: PASS — test_fix_record_numbering_is_checked requires exactly one record named fixes/NNN-short-name.md.
- S6: PASS — test_fix_cannot_touch_features_or_add_stage_artifacts rejects a change under features/.
- S7: PASS — test_fix_merge_requires_non_author_approval rejects a fix PR with no current non-author approval.
- S8: PASS — test_fix_requires_a_changed_test rejects a fix with no changed file under the declared test paths.
- S9: PASS — test_fix_cannot_touch_features_or_add_stage_artifacts rejects a stage artifact added on a fix branch.
- S10: PASS — test_fix_follows_the_existing_contracts_rule checks the packages contracts rule is unchanged.
- S11: PASS — test_fix_record_numbering_is_checked rejects a reused number and an edited merged record.
- S12: PASS — test_merged_fix_record_is_immutable shows a fix needs no tag and its record is final after merge.
- S13: PASS — test_historical_stage_tasks_still_validate accepts Proof and Ship tasks closed as completed and still rejects an open one.
- S14: PASS — test_guidance_describes_the_fix_lane_once checks every guidance file describes the lane consistently.
- S15: PASS — test_fix_requires_a_changed_test names the declared test paths in the failure.
- S16: PASS — test_fix_cannot_touch_features_or_add_stage_artifacts names the offending path.
- S17: PASS — test_fix_record_numbering_is_checked reports a missing, misnamed, and reused record separately.
- S18: PASS — test_fix_merge_requires_non_author_approval blocks the merge without a current review.
- S19: PASS — test_review_policy_states_the_restore_only_rule checks the policy tells reviewers to reject new work and ask for an intent.
- S20: PASS — test_guidance_describes_the_fix_lane_once covers the review policy, which tells reviewers to read check changes as code.

## Intent results

- OPEN — for a merged-source product, one outcome takes four merged PRs after Intent acceptance. This phase took four, but one was a Plan revision, so the claim is not yet observed at three.
- TRUE — every Spec S-rule has a named test and a recorded result against the merged Build, and CI fails when one is missing. This record is the second to be checked that way.
- TRUE — a bug fix or small correction to a shipped outcome lands in one reviewed PR that starts with a failing test and links the outcome it corrects. The fix lane is implemented and checked.
- TRUE — a solo developer following the README can get a PR approved and merged under required branch protection without a bypass. Unchanged by this phase.
- TRUE — every existing human gate still applies. The fix lane adds a required non-author approving review and removes no gate.

## Changes

A fix branch is a fifth branch kind. `fix/<short-name>` routes to its own
short validation and skips every stage rule: no intent, spec, plan,
build record, tracking issue, or shipped tag. The checks require the
change to include a file under the test paths already declared in
`Delivery settings`, exactly one record at `fixes/NNN-short-name.md`
with an unused number, nothing under `features/`, and an unedited
record. Its one remote gate is a current approving review from someone
other than the PR's author.

`fixes/` is new, with a README stating the rule and
`templates/fix-template.md` giving the record's shape. No fix record is
written by this Build; the first one belongs to the first real fix.

The checks prove a test file changed, not that it failed first. The
review policy says so and tells the reviewer what to judge instead:
whether the change restores behavior a shipped rule already states.
Anything that adds or alters a rule is new work and needs an intent.
Size never decides. Capability rules R39 to R41 record the lane, its
review gate, and the immutability of records.

The delivery-mode defect is corrected. A task for a stage the delivery
mode does not track is now accepted whenever it is closed, whether as
not planned or as completed under the previous six-stage rules. Only an
open one is an error. R38 is corrected in place.

## Transition

Started from merged Plan PR #80 at the Plan commit above. The live entry
gate for Task #62 passed on 2026-09-17. Accepted Spec PR #79 and the
revised Intent PR #77 are on the base.

No deviation from the approved Plan. All fourteen changed files are
inside its declared surface, and each of its ten named tests exists.

This Build corrects a defect in outcome 005 phase P1, which shipped
earlier the same day. P1's artifacts and its shipped tag are unchanged,
because the phase is immutable; the correction is a reviewed change to
the checks in this later phase, which is what the workflow requires
when a shipped phase turns out to be wrong. The fix lane that would
have handled it more cheaply did not exist yet.

The defect blocked every chain 004 pull request, including the pending
cancellation record in PR #78. With this Build merged, that PR passes
its history check on a rerun. Chain 004's Proof task #29 and Ship task
#30 stay closed as completed, because they record work that actually
happened under the rules in force at the time.

## Confirmed examples

The accepted Spec records a prototype skip: process rules, checks, and
documentation only, with nothing to inspect before Build. There is no
confirmed examples file and no example reader. No example data is
invented here.

## Delivery preparation

Delivery is `merged source`, so the reviewed merge of this PR is the
delivery. Shipment is one annotated tag,
`shipped/005-right-size-evidence-P2-fix-lane`, pushed on that merge
commit with a message naming this PR. No artifact is built, no Proof or
Ship PR opens, and tasks #63 and #64 are already closed as not planned.
The merge SHA is not yet known and is not invented here.
