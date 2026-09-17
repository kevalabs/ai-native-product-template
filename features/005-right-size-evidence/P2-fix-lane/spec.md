# A fix to shipped behavior lands in one reviewed PR — Spec

**Stage:** spec
**Outcome:** 005-right-size-evidence
**Phase:** P2-fix-lane
**Parent issue:** https://github.com/kevalabs/ai-native-product-template/issues/51
**Stage issue:** https://github.com/kevalabs/ai-native-product-template/issues/60
**Predecessor PR:** https://github.com/kevalabs/ai-native-product-template/pull/77

**Status:** accepted
**Accepted by:** Suraj Chhetry, who accepted this Spec and its recorded prototype skip in the working conversation on 2026-09-17.
**Intent:** [Keep every gate, drop the paperwork the gates do not need](../intent.md)
**Personas served:** product owner, solo developer, contributors and coding agents, reviewers
**Capabilities affected:** `product/capabilities/sdlc-workflow.md`

The spec answers WHAT. Someone who knows the product should
understand every line without knowing how it is built. No tables,
endpoints, components, or services belong here.

## Prototype confirmation

**Prototype skip:** process rules, checks, and documentation only.
There is no screen, calculation, or outside service to inspect before
Build. The S-rules below and the tests named for them are the
inspectable behavior. The owner chose this skip in the working
conversation on 2026-09-17; accepting this Spec accepts it.

## Flows

### Ship a fix

1. A contributor finds the product doing something a shipped Spec rule
   or capability rule already says it should not do.
2. They start a fix branch from the updated default branch.
3. They write a test that fails because of the defect.
4. They make the smallest change that makes the test pass.
5. They write a short fix record naming the failing test, the outcome
   the fix corrects, and the capability rule it restores.
6. They update the capability doc when its text described the broken
   behavior rather than the promised one.
7. They open one PR carrying the test, the change, and the record.
8. A person other than the author reviews it. The reviewer's job is to
   decide whether the change restores already stated behavior, or
   whether it changes what the product promises.
9. On approval it merges. There is no intent, spec, plan, or shipped
   tag for a fix.

### Refuse a fix that is really new work

1. The reviewer finds the change adds a rule, changes a rule, or makes
   the product promise something new.
2. They reject it as new work rather than a fix.
3. The contributor opens an intent, and the change follows the full
   sequence.

### Correct the delivery-mode tracking defect

1. A phase that shipped under the previous six-stage rules has Proof
   and Ship tasks closed as completed, with real merged PRs behind them.
2. A merged-source product's checks read those historical tasks.
3. The checks accept them as the record of what happened, and continue.

## Requirements

- S1 A fix branch is named `fix/<short-name>` and targets the default
  branch, like every other branch in the workflow.
- S2 A fix PR contains the failing test, the change that makes it pass,
  its fix record, and any capability doc correction. It needs no
  intent, spec, plan, proof, or ship record.
- S3 A fix restores behavior a shipped Spec rule or a capability rule
  already states. A change that adds a rule, changes a rule, or makes
  the product promise something new is not a fix and its PR is
  rejected as new work.
- S4 Size alone never decides whether something is a fix. A one-line
  change that alters a promise is new work; a wide change that only
  restores stated behavior is a fix.
- S5 A fix record lives at `fixes/NNN-short-name.md`, numbered in its
  own sequence, and names the failing test, the outcome directory it
  corrects, the capability rule it restores, and the date.
- S6 A fix never edits a shipped feature directory. Those stay
  immutable, and the fix record carries the correction instead.
- S7 A fix PR merges only with a current approving review from someone
  other than its author, and only when the full test suite passes.
- S8 The checks reject a fix PR that carries no new or changed test,
  because a fix starts from a failing test.
- S9 The checks reject a fix PR that changes a file under `features/`,
  or that adds an intent, spec, plan, build, proof, or ship artifact.
- S10 A fix PR may change `packages/` only when the product's contract
  rule already allows it; the existing contracts rule is unchanged.
- S11 Fix numbers never reuse, and a merged fix record is immutable.
  A later correction is another fix or a new intent.
- S12 A fix needs no shipped tag. Its merge is its delivery, and the
  outcome it corrects keeps the tag it already has.
- S13 The checks accept a historical Proof or Ship task that is closed
  as completed on a merged-source product, because it records a phase
  that shipped under the previous rules. Only an open task for a stage
  the delivery mode does not track is an error.
- S14 Contributor guidance, the review policy, the gate guide, and the
  capability doc describe the fix lane in one consistent way, including
  when to refuse a fix and open an intent instead.

## States and transitions

A fix moves through:

`written` → `reviewed` → `merged`

- `written`: the branch carries a failing test, the change, and the
  record.
- `reviewed`: a non-author approving review exists on the current head.
- `merged`: the PR merged into the default branch. The record is final.
- There is no shipped state. A fix delivers on merge.

## Permissions

- Any contributor or coding agent can open a fix PR.
- Any person who is not the PR's author can give the approving review.
  A coding agent or bot cannot.
- The reviewer decides whether a change is a fix or new work. That
  judgement is not delegated to a check.
- Nobody edits a merged fix record or a shipped feature directory.

## Errors and edge cases

- S15 When a fix PR carries no new or changed test, the check names the
  missing test and blocks the merge.
- S16 When a fix PR changes anything under `features/`, the check names
  the file and blocks the merge.
- S17 When a fix record is missing, misnumbered, or reuses a number, the
  check says which and blocks the merge.
- S18 When a fix PR has no current non-author approving review, it
  cannot merge, exactly as a Build PR cannot.
- S19 When a reviewer judges a change to be new work, the PR closes
  unmerged and the contributor opens an intent. The fix record, if one
  was written, is not committed.
- S20 When the defect is in the checks themselves, the same rules apply
  and the reviewer reads the check change as code.

## UX

This phase introduces no product screen. It adds one branch lane, one
record type, and one review judgement. No design mock is required.

## Contract changes

No external product or client contract changes. This phase changes the
repository's contributor workflow only.

## Data changes

The repository newly remembers fix records under `fixes/`. Shipped
feature directories, their tags, and chains 001 to 004 are unchanged.
No existing record is rewritten or renumbered.

## Region variance

No region-specific behavior.

## Acceptance criteria

- T1 (S1, S2) A `fix/` branch carrying a test, a change, and a record
  passes; the same content on an unsupported branch name is rejected.
- T2 (S3, S4, S19) The review policy states the restore-only rule and
  that size does not decide; a change that alters a promise is named as
  new work.
- T3 (S5, S17) A correctly numbered record passes; a missing,
  misnumbered, or reused number is rejected with the reason named.
- T4 (S6, S9, S16) A fix PR touching a shipped feature directory or
  adding a stage artifact is rejected with the file named.
- T5 (S7, S18) A fix PR merges with a current non-author approving
  review and is blocked without one.
- T6 (S8, S15) A fix PR with no new or changed test is rejected.
- T7 (S10) A fix touching `packages/` follows the existing contracts
  rule unchanged.
- T8 (S11, S12) A merged fix record cannot be edited, and no shipped tag
  is required or created for a fix.
- T9 (S13) A merged-source outcome whose historical Proof and Ship tasks
  are closed as completed validates; an open task for an untracked stage
  is still rejected.
- T10 (S14, S20) Guidance describes the fix lane once and consistently,
  including the refusal case and check changes.

## Out of scope

- Changing how intents, specs, plans, or builds work.
- Automating stage tracking. Outcome 004 phase P3 owns that.
- A rollback or revert lane. A revert is an ordinary fix if it restores
  stated behavior.
- Emergency or hotfix deployment procedures. This template has no
  runtime.
- Making stage issues optional. That phase is cancelled.

## Open questions

- Plan owner: whether a fix gets a tracking issue at all, and if so
  whether it is a Task under no parent or an untyped issue.
- Plan owner: how the check detects "a new or changed test" for a
  product whose tests are not Python.
