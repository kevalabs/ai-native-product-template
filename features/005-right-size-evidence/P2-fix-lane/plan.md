# A fix to shipped behavior lands in one reviewed PR — Plan

**Stage:** plan
**Outcome:** 005-right-size-evidence
**Phase:** P2-fix-lane
**Parent issue:** https://github.com/kevalabs/ai-native-product-template/issues/51
**Stage issue:** https://github.com/kevalabs/ai-native-product-template/issues/61
**Predecessor PR:** https://github.com/kevalabs/ai-native-product-template/pull/79

**Status:** approved
**Approved by:** Suraj Chhetry, who approved this plan as written in the working conversation on 2026-09-17.
**Spec:** [A fix to shipped behavior lands in one reviewed PR](spec.md)
**Branch:** feature/005-P2-fix-lane

The plan answers HOW. This is where tables, endpoints, components,
and services belong. The whole plan must fit one PR a human can
review in one sitting; if it doesn't, go back and split the phase.

## Approach

The fix lane is a fifth branch kind, not a second workflow. Today
`branch_kind()` recognises artifact, feature, proof, and ship, and
`context()` routes each to a stage. A `fix/<short-name>` branch becomes
its own kind whose validation is short and self-contained: the changed
paths must include a test file and a fix record, must exclude
`features/`, and nothing else about stages applies. That keeps the
existing four lanes untouched and makes the new one cheap to read.

Fix records live in a new top-level `fixes/` directory, one Markdown
file per fix, numbered in its own sequence. A new
`templates/fix-template.md` gives the shape. The number check reads the
committed tree rather than a registry, so numbering cannot drift from
what is actually in the repository.

The failing-test rule is enforced as "at least one changed path lies
under the declared Test paths", reusing the `Delivery settings` block
P1 added. That works for any language and needs no new setting. It
cannot prove the test failed before the fix; the reviewer judges that,
and `REVIEW.md` says so plainly.

The delivery-mode defect is a two-word change in `graph()`. Today an
untracked-stage task is skipped only when its `state_reason` is
`not_planned`. It should be skipped whenever the task is closed, because
a phase that shipped under the previous six-stage rules has genuine
Proof and Ship tasks closed as completed. Only an open untracked task is
a real error. The test locks both halves so the tolerance cannot widen
by accident.

Ordering puts the defect first. It is one line, it unblocks every chain
004 pull request including the pending cancellation record, and it is
the smallest thing in the phase. The lane itself follows, then the
prose. Each step ends with `make test` passing.

The rejected alternative for the fix record was a single append-only
log file. One file per fix matches the numbered directories already used
for outcomes, keeps merges conflict-free when two fixes land close
together, and makes immutability a file-level rule rather than a diff
rule.

## Touched surface (collision check)

- AGENTS.md
- README.md
- REVIEW.md
- .githooks/README.md
- docs/agentic-sdlc.md
- scripts/check_sdlc.py
- scripts/check_github.py
- tests/test_sdlc.py
- tests/test_github.py
- templates/fix-template.md
- fixes/README.md
- product/glossary.md
- product/capabilities/sdlc-workflow.md
- .agents/skills/build/SKILL.md
- features/005-right-size-evidence/P2-fix-lane/build.md

Fifteen files, about 450 changed lines. No other plan is in flight:
outcome 004 phase P2 is cancelled, its phase P3 has no plan yet, and
outcome 005 phase P3 is cancelled. Nothing under `packages/`,
`.github/workflows/`, or any shipped feature directory changes.

`fixes/README.md` explains the directory's purpose and numbering; the
first real fix record is written by the first contributor who needs
one, not by this Build.

## Steps

1. **Correct the delivery-mode tracking defect.** Failing test first:
   a merged-source outcome whose untracked-stage task is closed as
   completed validates, while an open one is still rejected. Then skip
   any closed untracked-stage task in `graph()`. Confirm the pending
   chain 004 cancellation validates against the fixed check. (S13)
2. **Recognise the fix lane.** Failing tests first: a `fix/` branch
   carrying a test change and a record passes; the same content on an
   unsupported branch name fails. Then add `fix` to `branch_kind()` and
   a `fix` route in `context()` that skips every stage rule. (S1, S2)
3. **Enforce the fix PR's shape.** Failing tests first: a PR with no
   changed file under the declared Test paths fails; one that changes
   anything under `features/` fails with the path named; one that adds
   a stage artifact fails. Then validate the changed paths against the
   Test paths from `Delivery settings` and the `features/` exclusion.
   (S8, S9, S15, S16)
4. **Enforce the fix record.** Failing tests first: a missing record, a
   misnumbered name, and a number already present in the committed tree
   each fail with the reason named; a correct record passes. Then check
   `fixes/NNN-short-name.md` exists in the change, matches the naming
   pattern, and does not reuse a number. Add
   `templates/fix-template.md` with the required fields. (S5, S11, S17)
5. **Apply the review gate.** Failing test first: a fix PR without a
   current non-author approving review is reported as unreviewed. Then
   reuse the Build review rule for the fix lane in `check_github.py`,
   with no stage task lookup, since a fix has no tracking issue.
   (S7, S18)
6. **Guidance and capability.** Update the conventions file, README,
   review policy with the restore-only judgement and the refusal case,
   the gate guide, the process model, the glossary, the build skill's
   correction paragraph, and `product/capabilities/sdlc-workflow.md`.
   (S3, S4, S6, S10, S12, S14, S19, S20)

## Migrations

No data migration. Two repository-state changes:

- A new empty `fixes/` directory with its README. Fix numbering starts
  at 001 and never reuses.
- Once step 1 merges, the pending chain 004 cancellation
  ([PR #78](https://github.com/kevalabs/ai-native-product-template/pull/78))
  passes its history check on a rerun. Chain 004's Proof and Ship tasks
  stay closed as completed, because they record work that happened.

Reversibility: every step is a reviewed commit on one branch. Reverting
the Build removes the fix lane and restores the previous check, at the
cost of reintroducing the defect.

## Test plan

Written first, per the bug-fix and new-check rule. Tests extend the
existing `WorkflowTests` disposable-repository fixture and
`EvidenceTests` fake-API fixture.

| Spec | Test |
|---|---|
| T1 (S1, S2) | `test_fix_branch_carries_test_change_and_record` |
| T2 (S3, S4, S19) | `test_review_policy_states_the_restore_only_rule` |
| T3 (S5, S17) | `test_fix_record_numbering_is_checked` |
| T4 (S6, S9, S16) | `test_fix_cannot_touch_features_or_add_stage_artifacts` |
| T5 (S7, S18) | `test_fix_merge_requires_non_author_approval` |
| T6 (S8, S15) | `test_fix_requires_a_changed_test` |
| T7 (S10) | `test_fix_follows_the_existing_contracts_rule` |
| T8 (S11, S12) | `test_merged_fix_record_is_immutable` |
| T9 (S13) | `test_historical_stage_tasks_still_validate` |
| T10 (S14, S20) | `test_guidance_describes_the_fix_lane_once` |

The accepted Spec records a prototype skip, so there is no confirmed
examples file and no example reader.

## Rollout

No feature flag and no region order. `product/capabilities/sdlc-workflow.md`
gains rules for the fix lane and its gates, and R38 is corrected in
place to say that any closed task for an untracked stage is accepted.
The glossary gains fix, fix record, and fix lane.

Delivery follows this repository's `merged source` setting. The Build PR
carries its S-rule results and Intent results, receives a non-author
approving review, and merges. Shipment is an annotated tag
`shipped/005-right-size-evidence-P2-fix-lane` on that merge commit,
whose message names the Build PR. No Proof or Ship PR is opened, and
tasks #63 and #64 are already closed as not planned.

<!-- On owner approval, add **Approved by:** with the person and actual approval source. -->
