# Test + Review and Ship evidence land where they are produced — Plan

**Stage:** plan
**Outcome:** 005-right-size-evidence
**Phase:** P1-evidence-in-build
**Parent issue:** https://github.com/kevalabs/ai-native-product-template/issues/51
**Stage issue:** https://github.com/kevalabs/ai-native-product-template/issues/55
**Predecessor PR:** https://github.com/kevalabs/ai-native-product-template/pull/73

**Status:** approved
**Approved by:** Suraj Chhetry, who approved this plan as written in the working conversation on 2026-09-17.
**Spec:** [Test + Review and Ship evidence land where they are produced](spec.md)
**Branch:** feature/005-P1-evidence-in-build

The plan answers HOW. This is where tables, endpoints, components,
and services belong. The whole plan must fit one PR a human can
review in one sitting; if it doesn't, go back and split the phase.

## Approach

The delivery mode drives everything else. `AGENTS.md` gains a
`## Delivery settings` section next to `## Prototype settings`, holding
`**Delivery:** merged source` and `**Test paths:** tests/`. Both
validators read it from the committed tree at the reviewed commit, so
the setting is reviewed like any other rule and never read from a
working file or an environment variable.

`check_sdlc.py` already routes every stage through `context()` and
`validate_change()`. The merged-source path is a branch inside that
existing routing, not a second validator. For a merged-source product,
`build` gains two record requirements, and the `proof` and `ship`
stages keep working unchanged so shipped chains 003 and 004 still
validate. Nothing is deleted from the runtime-artifact path; the spec's
S2 requires it to behave exactly as today, and the existing tests for it
stay green as the proof of that.

S-rule evidence is a literal string search, chosen because the template
must work for any product stack. The Build record writes
`- S1: PASS — <test identifier> …`, and the check greps the declared
test paths for that identifier as a literal. It does not parse Python,
resolve a test node, or run anything per rule. `make test` already
proves the suite passes; the check only proves the named test is real.
A test identifier that appears in a comment would satisfy it, which is
why human review still judges whether the test proves the rule. The
rejected alternative was a `file::name` form: precise for pytest and
useless for a Go or Vitest product.

The shipped tag is verified at the next handoff rather than at Build
time, because the `pull_request` event carries no tags and the checkout
that CI performs would need a second fetch to see one. `check_github.py`
already fetches and resolves commits for predecessor evidence; the tag
lookup joins that work. A tag that does not exist yet blocks only the
dependent stage, which is exactly when shipment matters.

The review requirement reuses `Evidence.review()`, which already
computes whether a current non-author approval exists for a PR's head.
Today `merged()` only enforces it for bot merges. For a Build
predecessor the enforcement becomes unconditional.

Build order puts the validator work first and the prose last. Each of
the six steps ends with `make test` passing. Step 1 carries the riskiest
assumption, that a committed setting can be read at an arbitrary
reviewed commit by both validators, and it is proven before any rule
depends on it.

## Touched surface (collision check)

- AGENTS.md
- README.md
- REVIEW.md
- docs/agentic-sdlc.md
- .githooks/README.md
- features/README.md
- Makefile
- scripts/check_sdlc.py
- scripts/check_github.py
- tests/test_sdlc.py
- tests/test_github.py
- templates/build-template.md
- templates/plan-template.md
- templates/spec-template.md
- product/glossary.md
- product/capabilities/sdlc-workflow.md
- .agents/skills/build/SKILL.md
- .agents/skills/plan/SKILL.md
- .agents/skills/proof/SKILL.md
- .agents/skills/ship/SKILL.md
- .agents/skills/spec/SKILL.md
- .agents/skills/intent/SKILL.md
- .agents/skills/feature/SKILL.md
- .agents/skills/product-status/SKILL.md
- .agents/skills/bootstrap-product/SKILL.md
- features/005-right-size-evidence/P1-evidence-in-build/build.md

Twenty-six files. No other plan is in flight: outcome 004's P2 and P3
have no plan, and their tasks are blocked placeholders. Outcome 004 P2
will touch `AGENTS.md` for its sandbox section and the prototype rules
in `docs/agentic-sdlc.md`; this plan adds a separate settings section
and edits different paragraphs, so the two can land in either order.
No change under `packages/`, `.github/workflows/`, or any shipped
feature directory.

Reviewability: about 900 changed lines, roughly half of them validator
code and tests. One reviewer can read it in one sitting.

## Steps

1. **Delivery settings, read by both validators.** Add the failing
   tests first: a merged-source fixture passes, a missing section
   fails, and a misspelled value fails naming both accepted values.
   Then add `## Delivery settings` to `AGENTS.md` and a
   `delivery_settings(ref)` helper in `check_sdlc.py` that reads
   `AGENTS.md` at a given ref and returns the mode and test paths.
   `check_github.py` imports it. (S1, S20)
2. **S-rule results in the Build record.** Failing tests first: a
   record with one PASS line per S-rule naming an existing test passes;
   a missing rule, a FAIL, an unknown test name, and an S-rule added to
   the Spec after the record each fail with the rule named. Then extend
   `validate_record()`'s `build` branch to parse `## Requirement results`
   for merged-source products, compare its rule set with the Spec's
   S-rules, and grep the declared test paths for each identifier.
   Add `## Intent results` as a required section on the record, and
   require every Intent success criterion on the outcome's last phase.
   (S3, S4, S5, S21, S22)
3. **Non-author review on every Build PR.** Failing tests first: a
   merged Build with a current non-author approval passes; a
   human-merged Build without one fails, naming the merged head. Then
   make `Evidence.merged()` require approval when the predecessor stage
   is `build`, and report the failure at the dependent handoff.
   (S6, S24)
4. **Shipped tag as the Ship record.** Failing tests first: a tag on a
   merged Build commit on the default branch counts as shipped; a tag
   on another commit, a tag whose commit has no Build record, and a
   missing tag each fail. Then add `shipped_tag(outcome, phase)` to
   `check_github.py`, fetch tags during handoff, and treat a
   merged-source predecessor as shipped when the tag resolves. Keep the
   runtime-artifact path on its merged Ship PR. Make shipped-phase
   directories immutable by the tag as `ship.md` did.
   (S7, S8, S9, S10, S11)
5. **Four-task tracking shape.** Failing tests first: a merged-source
   phase with Intent, Spec, Plan, and Build tasks passes; the same
   phase with six tasks fails; a runtime-artifact phase still requires
   six. Then make `graph()`'s expected stage set depend on the delivery
   mode, and accept a Proof or Ship task closed as not planned without
   counting it as a completed dependency. (S13, S18, S26)
6. **Guidance, templates, skills, and capability.** Update the
   conventions file, README setup with the authoring-identity
   explanation, the process model, the gate guide, review policy, the
   features ledger, the build and plan and spec templates, the eleven
   skills, the glossary, and `product/capabilities/sdlc-workflow.md`.
   Add the setup check's authoring-identity line. Remove every
   instruction that contradicts the merged-source path.
   (S12, S15, S16, S17, S19)

## Migrations

No data migration. Two repository-state changes:

- Chains 001 to 004 keep their records untouched. Chain 003 and chain
  004 P1 shipped with `ship.md` files; the tag rule applies to phases
  that ship after this change, and the handoff accepts a merged Ship PR
  as shipment for any phase that already has one.
- Outcome 005's own Proof and Ship tasks (#57, #58 for P1, and the
  equivalents for P2 and P3) close as not planned in the Build PR's
  tracking updates, with a note naming this Spec's S18.

Reversibility: every step is a reviewed commit on one branch. Reverting
the Build PR restores the six-stage behavior, because the
runtime-artifact path is never removed.

## Test plan

Written first, per the bug-fix and new-check rule. All tests extend the
existing `tests/test_sdlc.py` `WorkflowTests` disposable-repository
fixture and `tests/test_github.py` `EvidenceTests` fake-API fixture.

| Spec | Test |
|---|---|
| T1 (S1, S20) | `test_delivery_setting_modes_and_errors` |
| T2 (S2, S25) | `test_runtime_artifact_path_is_unchanged` |
| T3 (S3, S4, S21, S22) | `test_build_record_requires_result_per_s_rule` |
| T4 (S5, S14) | `test_last_phase_records_every_intent_criterion` |
| T5 (S6, S24) | `test_build_merge_requires_non_author_approval` |
| T6 (S7, S8, S23) | `test_shipped_tag_must_be_on_merged_build` |
| T7 (S9) | `test_moved_shipped_tag_is_rejected` |
| T8 (S10, S11) | `test_dependent_handoff_requires_shipped_tag` |
| T9 (S12) | `test_records_carry_each_tracking_fact_once` |
| T10 (S13, S18, S26) | `test_task_shape_follows_delivery_mode` |
| T11 (S15, S16) | `test_setup_report_names_authoring_identity` |
| T12 (S17, S19) | `test_guidance_states_one_consistent_policy` |

The Spec records a prototype skip, so there is no confirmed examples
file and no example reader. No example data is invented.

## Rollout

No feature flag and no region order. `product/capabilities/sdlc-workflow.md`
updates in this outcome's Build PR: R10 gains the two delivery paths,
R19 splits into the merged-source and runtime-artifact forms, R23 gains
the task-shape rule, and a new rule records the review requirement. The
glossary gains delivery mode, shipped tag, and S-rule result.

Delivery follows this Spec's own merged-source path, as the owner chose
on 2026-09-17. The Build PR carries its S-rule results and Intent
results, receives a non-author approving review, and merges. Shipment
is an annotated tag `shipped/005-P1-evidence-in-build` on that merge
commit, whose message names the Build PR. No Proof or Ship PR is opened
for this phase, and tasks #57 and #58 close as not planned. If the new
checks prove wrong during Build review, the fallback is the existing
Proof and Ship path, which this plan leaves intact.

<!-- On owner approval, add **Approved by:** with the person and actual approval source. -->
