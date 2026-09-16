# Confirm a prototype before writing its spec — Proof

**Status:** passed
**Stage:** proof
**Outcome:** 004-prototype-first
**Phase:** P1-prototype-step
**Parent issue:** https://github.com/kevalabs/ai-native-product-template/issues/22
**Stage issue:** https://github.com/kevalabs/ai-native-product-template/issues/29
**Predecessor PR:** https://github.com/kevalabs/ai-native-product-template/pull/47
**Build commit:** 3ee3aea5d08b4dacbc73d18baab7f4ceeb6519de
**Artifact identity:** 3ee3aea5d08b4dacbc73d18baab7f4ceeb6519de
**Artifact source:** 3ee3aea5d08b4dacbc73d18baab7f4ceeb6519de
**Test destination:** isolated source checkout at the exact merged Build
**Artifact evidence:** [merged source][build-commit], [Build CI][build-ci], and the verification below
**Blocking findings:** none

## Requirement results

P1 implements docs, skills, and templates. Results below distinguish
executed Git/data exercises from manual review of the written procedure.
They do not claim automated prototype enforcement, real user trials,
production deployment, or confirmation of a real prototype. Synthetic
owner decisions used in walkthroughs are not human approval records.

- S1: PASS — Manual startup review rejects an unmerged Intent and permits
  the workspace check after its accepted merge. [Prototype skill][prototype]
  step 1 also blocks work when no permitted workspace exists.
- S2: PASS — Screen, count calculation, and provider cases select a screen
  walkthrough, worked example, and integration trial respectively. The
  [guide][guide] and [examples][examples] supply each form's inputs.
- S3: PASS — A mixed screen/rule/service case requires all three forms.
  The guide permits one owner decision only for a shared exact version
  and evidence set; omitting the trial leaves the record incomplete.
- S4: PASS — Manual review of a test-bearing prototype requires removal
  of its automated product tests. A runnable demonstration without them
  can proceed. [Review policy][review-policy] retains normal Build tests.
- S5: PASS — Removing screen sample data, calculation expected outputs,
  or the provider failure case makes each record incomplete. The guide's
  readiness list and examples template identify the missing element.
- S6: PASS — A user-feedback-only record cannot confirm a version. The
  [note][note] records the owner's decision and how available feedback
  affected it; unavailable real users do not add a mandatory gate.
- S7: PASS — Reviewed omission of each of the seven required confirmation
  fields: form, commit, evidence, examples, owner, date, and source.
  Each omission blocks the record. The [Spec template][spec-template]
  carries those fields and links to the preserved evidence.
- S8: PASS — Changing either a confirmed or rejected version requires a
  new version while preserving the prior decision. The guide names both
  final states and uses the latest explicit confirmation for a new Spec.
- S9: PASS — Executed retention and preservation exercises below recover
  identical examples from a fresh clone after working-branch deletion.
  The existing validator accepts the Spec's Markdown evidence and rejects
  executable prototype source. The guide keeps the working note off main.
- S10: PASS — Manual comparison permits a tracking placeholder but blocks
  substantive Spec drafting without confirmation or a concrete skip.
  [Spec skill][spec-skill] makes this distinction before its interview.
- S11: PASS — UTC age fixtures warn at 30 days, not one second before;
  a seven-day override behaves likewise. The guide makes expiry a manual
  warning, allows explicit refresh to ready, and preserves original dates.
- S12: PASS — An unaccepted Spec at 30 days needs reconfirmation or explicit
  age acceptance. A refreshed note retains that requirement; an already
  accepted Spec has none. The Spec template records the dated decision.
- S13: PASS — Manual review blocks inaccessible commit, decision source,
  evidence, or examples. The guide and Spec skill require reviewable
  evidence; only a justified, owner-accepted skip is an alternative.
- S14: PASS — A pure refactor preserving all behavior can record a skip
  accepted with its Spec. A screen change merely lacking a demo cannot.
  The guide makes meaningful inspectable behavior the distinction.
- S15: PASS — The documented reader consumes the same preserved Markdown
  file. The executed count case returns 5; an altered expectation of 6
  is detected. [Build skill][build-skill] requires renewed confirmation
  or an accepted Spec revision before continuing with changed cases.
- S16: PASS — Walkthroughs reject data labelled as production secrets or
  real personal data and require synthetic replacements. No actual secret
  or personal data was used. Prototype skill and review policy agree.
- S17: PASS — Stage instructions and active diagrams target main and
  reject environment branches as deployment state. The actual Build PR
  merged into main; [delivery guidance][delivery] covers products too.
- S18: PASS — Manual trace distinguishes preview P, merged source M, and
  immutable staging artifact A. Proof tests A from M; Ship promotes A.
  For this source-only template, this Proof tests the exact merged source
  artifact named above, with matching tree identity.
- S19: PASS — Reviewed all 27 changed files, active workflow diagrams,
  entry points, and delivery instructions. Shared rules and stage-specific
  instructions agree; searches found no remaining old direct Intent-to-Spec
  sequence in active guidance. Historical feature chains stay unchanged.
- S20: PASS — A no-behavior case records a concrete skip, without an empty
  prototype. The guide rejects missing time or evidence as a substitute
  reason and keeps owner acceptance at the Spec gate.
- S21: PASS — A mixed screen/service case missing its trial fails readiness
  and cannot provide complete confirmation. The Spec template and review
  policy explicitly block acceptance for an omitted applicable form.
- S22: PASS — A record confirming commit A cannot authorize a presented
  version B. Spec skill and prototype skill require the exact version
  before substantive drafting, not a later repair of the confirmation.
- S23: PASS — A previously demonstrated version whose evidence cannot be
  preserved remains blocked at Spec acceptance. The guide and Spec template
  require accessible preserved evidence despite the earlier demonstration.
- S24: PASS — A provider failure case that cannot run keeps the version
  out of ready. The guide and prototype skill require every named case
  to run before readiness; there is no coverage gate instead.
- S25: PASS — Manual artifact comparison rejects B instead of proved A,
  or a claimed source N instead of merged Build M. [Proof skill][proof-skill]
  and template record both identity and source. This source checkout
  matched its actual named Build before testing.
- S26: PASS — Manual delivery review leaves shipment unsuccessful when A
  is unavailable or the destination requires a different rebuild.
  [Ship skill][ship-skill] requires the same proved artifact and renewed
  Build/Proof for corrections. No runtime shipment is claimed here.

## Verification

On 2026-09-16, the live entry gate for Task #29 passed after Build
Task #28 recorded PR #47 and its approved artifact permalink. The Proof
worktree started from the exact merged Build, not the former PR branch.

`make test` passed all 86 tests in that clean checkout, including existing
stage regressions, Python and shell syntax, and whitespace checks.
Those existing tests protect the current gates; they do not automate
the new confirmation rules. All ten added or updated skills passed
`quick_validate.py`; the existing `.claude/skills` symlink discovers the
prototype skill. All local link destinations in the Build diff resolve.

The full merged tree equals the approved PR head
`2d6aefe1ea0289fd61b6205941543f484457a1c1`. Both have tree
`5c93828b8166a57d3b5a82b84a6e31ea91e7bbf4`. Comparing the Build with
its parent shows exactly the 27 files declared by the approved Plan:
817 insertions and 59 deletions. No validator, CI, test, package,
accepted planning artifact, or historical feature change is hidden
in the merge. This PR adds only this Proof record.

### Executed evidence exercises

Repeated the [Build's reproduction procedure][build-record] against this
merged source using fresh temporary repositories:

1. The documented JSON reader loaded the four examples covering all
   three forms. The count inputs `[2, 3]` produced the expected `5`;
   changing that expectation to `6` produced the intended disagreement.
2. The existing `WorkflowTests` disposable-Git fixture accepted a phase
   Spec plus its byte-identical `design/prototype-examples.md` under full
   artifact history validation. Adding executable `design/demo.py` was
   rejected. The repository's production hooks were unchanged.
3. A separate temporary source repository committed the examples and
   then a clearly synthetic decision note naming the earlier commit.
   A retained tag reached both. After pushing to a local bare remote
   and deleting only the work branch, a fresh clone resolved the tag,
   the prototype ancestor, the decision, and the unchanged example bytes.

The example file SHA-256 before and after preservation was
`8ed8374fb53b8c2271cae8d1c05463d093061b34c8ae3997668306b803a71502`.
These exercises validate the file handoff and retention procedure, not
the truth of an owner decision or automatic remote tag protection.

Age fixtures used `2026-08-01T00:00:00+00:00` as creation time. At
`2026-08-30T23:59:59+00:00` the default warning is false; at
`2026-08-31T00:00:00+00:00` it is true and the Spec age decision applies.
For a seven-day setting, the warning changes at
`2026-08-08T00:00:00+00:00`; that override does not change the Spec's
30-day acceptance review rule. This is arithmetic plus manual review
of the documented behavior, not an installed expiry job.

### Review limits

The manual cases above were reapplied to the merged guide, templates,
skills, and review policy. No blocking finding remains within P1's
approved documentation scope. The [capability][capability] accurately
states the limits: no new prototype branch permission, sandbox checks,
automatic expiry, retention service, or background lifecycle automation.
An already permitted workspace is required until the lane is installed.

This template has no deployed runtime. Product artifact examples in
S18, S25, and S26 were procedure walkthroughs, not deployments to staging
or production. Existing accepted Specs, including P1's own, are not
retroactively assigned invented prototype confirmations.

## Human review

Suraj Chhetry [approved the Build][human-review] on 2026-09-16 at
05:49:08 UTC for exact head `2d6aefe1ea0289fd61b6205941543f484457a1c1`.
The review remains APPROVED and names that head. Both required
[Build CI checks][build-ci] passed. PR #47 merged into main at
05:49:18 UTC as the Build commit named above; its contents match the
reviewed version exactly.

The Plan's conversation approval and merged PR #46 remain recorded in
the [approved Plan][plan]. Agent walkthrough results here provide
technical evidence, not an invented human review. This separate Proof
PR still requires human review and merge before Ship may begin.

## Intent results

The shared Intent has six success criteria. Results are limited to P1:

1. **Confirmation before Spec:** the three forms, exact-version owner
   decision, reviewable evidence, and justified skip are implemented as
   contributor guidance and human review requirements. Synthetic cases
   passed; no claim is made about adoption by a real downstream product.
2. **Same examples in Build tests:** the preserved Markdown format and
   direct reader work, including the changed-data negative case. Skills
   and review require the same file rather than copied fixture data.
3. **Prototype branch and sandbox checks:** outside P1; P2 owns this
   outstanding criterion. No new branch permission is claimed here.
4. **One-command stage tracking:** outside P1; P3 owns this outstanding
   criterion. Capability R24 continues to state that automation is absent.
5. **Existing gates and human approval:** the 86 regressions pass; actual
   Intent, Spec, Plan, and Build approvals/merges remain linked. Prototype
   adds owner confirmation without another merged stage PR or fabricated
   approval, and current hooks remain in force.
6. **Adoption note:** P1 explains adoption for work not yet at Spec and
   retains accepted history. The final cross-phase adoption note remains
   due in P3's Ship, as required by the Intent.

P1's documented workflow is technically verified. Its Ship still follows
this Proof's review and merge. The parent outcome remains open for the
remaining phases and success criteria; passing this Proof is not shipment.

[build-commit]: https://github.com/kevalabs/ai-native-product-template/commit/3ee3aea5d08b4dacbc73d18baab7f4ceeb6519de
[build-ci]: https://github.com/kevalabs/ai-native-product-template/actions/runs/35060172740
[human-review]: https://github.com/kevalabs/ai-native-product-template/pull/47#pullrequestreview-5218937611
[build-record]: https://github.com/kevalabs/ai-native-product-template/blob/3ee3aea5d08b4dacbc73d18baab7f4ceeb6519de/features/004-prototype-first/P1-prototype-step/build.md#executed-evidence-handoff
[plan]: https://github.com/kevalabs/ai-native-product-template/blob/03c2171cddcce20b2f067c297f2d7571ebd6fcbc/features/004-prototype-first/P1-prototype-step/plan.md
[guide]: https://github.com/kevalabs/ai-native-product-template/blob/3ee3aea5d08b4dacbc73d18baab7f4ceeb6519de/docs/agentic-sdlc.md#prototype-before-spec
[delivery]: https://github.com/kevalabs/ai-native-product-template/blob/3ee3aea5d08b4dacbc73d18baab7f4ceeb6519de/docs/agentic-sdlc.md#branches-and-delivery
[prototype]: https://github.com/kevalabs/ai-native-product-template/blob/3ee3aea5d08b4dacbc73d18baab7f4ceeb6519de/.agents/skills/prototype/SKILL.md
[examples]: https://github.com/kevalabs/ai-native-product-template/blob/3ee3aea5d08b4dacbc73d18baab7f4ceeb6519de/templates/prototype-examples-template.md
[note]: https://github.com/kevalabs/ai-native-product-template/blob/3ee3aea5d08b4dacbc73d18baab7f4ceeb6519de/templates/prototype-template.md
[spec-template]: https://github.com/kevalabs/ai-native-product-template/blob/3ee3aea5d08b4dacbc73d18baab7f4ceeb6519de/templates/spec-template.md
[spec-skill]: https://github.com/kevalabs/ai-native-product-template/blob/3ee3aea5d08b4dacbc73d18baab7f4ceeb6519de/.agents/skills/spec/SKILL.md
[review-policy]: https://github.com/kevalabs/ai-native-product-template/blob/3ee3aea5d08b4dacbc73d18baab7f4ceeb6519de/REVIEW.md
[build-skill]: https://github.com/kevalabs/ai-native-product-template/blob/3ee3aea5d08b4dacbc73d18baab7f4ceeb6519de/.agents/skills/build/SKILL.md
[proof-skill]: https://github.com/kevalabs/ai-native-product-template/blob/3ee3aea5d08b4dacbc73d18baab7f4ceeb6519de/.agents/skills/proof/SKILL.md
[ship-skill]: https://github.com/kevalabs/ai-native-product-template/blob/3ee3aea5d08b4dacbc73d18baab7f4ceeb6519de/.agents/skills/ship/SKILL.md
[capability]: https://github.com/kevalabs/ai-native-product-template/blob/3ee3aea5d08b4dacbc73d18baab7f4ceeb6519de/product/capabilities/sdlc-workflow.md
