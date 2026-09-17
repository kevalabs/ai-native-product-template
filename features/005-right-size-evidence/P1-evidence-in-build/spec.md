# Test + Review and Ship evidence land where they are produced — Spec

**Stage:** spec
**Outcome:** 005-right-size-evidence
**Phase:** P1-evidence-in-build
**Parent issue:** https://github.com/kevalabs/ai-native-product-template/issues/51
**Stage issue:** https://github.com/kevalabs/ai-native-product-template/issues/54
**Predecessor PR:** https://github.com/kevalabs/ai-native-product-template/pull/72

**Status:** accepted
**Accepted by:** Suraj Chhetry, who accepted the Spec and its recorded prototype skip in the working conversation on 2026-09-17.
**Intent:** [Keep every gate, drop the paperwork the gates do not need](../intent.md)
**Personas served:** product owner, solo developer, contributors and coding agents, reviewers; `product/personas.md` does not yet define product-specific personas
**Capabilities affected:** `product/capabilities/sdlc-workflow.md`

The spec answers WHAT. Someone who knows the product should
understand every line without knowing how it is built. No tables,
endpoints, components, or services belong here.

## Prototype confirmation

**Prototype skip:** process rules, templates, and documentation only.
There is no screen, calculation, or outside service to inspect before
Build. The S-rules below and the tests named for them are the
inspectable behavior. The owner chose this skip in the working
conversation on 2026-09-17; accepting this Spec accepts it.

## Flows

### Declare how the product delivers

1. The product's conventions file carries a delivery setting with one
   of two values: merged source or runtime artifact.
2. This template ships with merged source. Bootstrap asks the product
   owner which value applies and fills it once.
3. A product with a deployed runtime chooses runtime artifact and keeps
   the separate Proof and Ship stages exactly as they work today.

### Build, review, and ship a merged-source phase

1. After the Plan PR merges, the contributor implements the phase under
   the approved Plan, as today.
2. The Build record lists every S-rule of the phase's Spec with a
   result and the name of the test that proves it.
3. The Build record says which Intent success criteria this phase makes
   true and which remain open. The last phase of an outcome walks every
   criterion.
4. The contributor opens the Build PR. CI fails when an S-rule has no
   result, names a test that does not exist, or does not pass, or when
   the test suite fails.
5. A person other than the PR's author reviews the diff, the S-rule
   results, and the Intent results, and records an approving review.
   That review is the Test + Review step.
6. The owner or reviewer merges the Build PR. The merge is the delivery
   for a merged-source product.
7. The contributor pushes a shipped tag on the merged Build commit. The
   tag names the phase and the merged PR. The phase now counts as
   shipped and its record is immutable.
8. When the last phase's tag lands and every Intent success criterion is
   recorded true, the outcome is shipped and its parent closes.

### Start the next stage or phase

1. The next phase's Spec handoff checks that the phase it depends on has
   a shipped tag on its merged Build commit.
2. Tracking, when a product uses stage issues, has Intent, Spec, Plan,
   and Build tasks per phase for a merged-source product. The Build task
   closes when its tag lands. Proof and Ship tasks exist only for
   runtime-artifact products.

### Set up as one person

1. The README's setup says that GitHub ignores an approval from a PR's
   author, and that required review therefore needs a separate
   authoring identity, such as a GitHub App, that opens every PR.
2. A solo developer follows that setup, approves the PRs the identity
   opens, and merges under required review without a bypass.

## Requirements

- S1 A product declares its delivery mode in its conventions file as
  exactly `merged source` or `runtime artifact`. The template ships
  with `merged source`. A missing or other value fails the Build PR
  check with an explanation; there is no silent default.
- S2 For a runtime-artifact product, the Proof and Ship stages, their
  PRs, their records, and their checks keep their current behavior.
- S3 For a merged-source product, the Build record contains one result
  line per S-rule of the phase's accepted Spec. Each line names the
  S-rule, a result of PASS or FAIL, and the identifier of the test that
  proves it.
- S4 The Build PR check fails when any S-rule of the accepted Spec has
  no result line, when any result is FAIL, when a named test identifier
  does not appear in the repository's tests, or when the test suite
  does not pass on the PR head.
- S5 For a merged-source product, the Build record has an Intent
  results section. It names each Intent success criterion the phase
  makes true and each one it leaves open. The outcome's last phase
  records every criterion as true or the outcome is not shipped.
- S6 A Build PR merges only with a current approving review on its head
  commit from a person who is not the PR's author. A human merge
  without such a review does not count as Test + Review.
- S7 For a merged-source product, Ship is a shipped tag on the merged
  Build commit named after the outcome and, for a phased outcome, its
  phase. The tag's message names the merged Build PR.
- S8 A phase or single-phase outcome counts as shipped only when its
  shipped tag points at a commit on the default branch whose Build
  record has Status ready and passing results. A tag elsewhere is
  invalid and does not ship anything.
- S9 A shipped tag never moves. A correction after shipment starts a new
  intent or, once P2 ships, a fix; it never retargets the tag.
- S10 The next stage or phase handoff treats a merged-source predecessor
  as shipped when S8 holds, and treats a runtime-artifact predecessor
  as shipped when its Ship PR has merged, as today.
- S11 After a phase ships, its directory is immutable, exactly as a
  Ship record made it immutable before.
- S12 Each tracking fact appears once per chain. The Build record names
  its Plan commit and predecessor PR. No record repeats a commit hash in
  more than one field, and no record restates another record's
  success-criteria walk.
- S13 For a merged-source product that uses stage issues, each phase has
  Intent, Spec, Plan, and Build tasks. The Build task completes when
  the Build PR has merged and the shipped tag exists. The tracking check
  accepts that four-task shape and still requires the six-task shape for
  a runtime-artifact product.
- S14 The parent Intent issue closes only after every phase has its
  shipped tag and the last phase's Build record shows every Intent
  success criterion true.
- S15 The README's setup section states that a self-authored PR cannot
  satisfy required review, and describes the separate authoring
  identity that opens PRs so one person can approve and merge.
- S16 The setup check's report names the authoring-identity requirement
  when it finds required review configured, so a solo developer learns
  it before their first PR.
- S17 Contributor guidance, stage skills, templates, review policy, the
  gate guide, and the capability doc describe the merged-source and
  runtime-artifact paths in one consistent way. The Build change removes
  or updates every conflicting instruction.
- S18 Shipped chains keep their records. An in-flight phase that has not
  merged its Build adopts this behavior; its existing Proof and Ship
  placeholder tasks close as not planned with a note, and their closure
  is not a completed dependency.
- S19 No human gate is removed. Intent acceptance, Spec acceptance, Plan
  approval, and an approving review of every Build PR remain required.

## States and transitions

A phase, or a single-phase outcome, moves through:

`accepted` → `specified` → `planned` → `built` → `shipped`

- `accepted`: the Intent PR merged with owner acceptance.
- `specified`: the Spec PR merged with owner acceptance.
- `planned`: the Plan PR merged with owner approval.
- `built`: the Build PR merged with passing S-rule results and an
  approving non-author review.
- `shipped`: for merged source, the shipped tag points at the merged
  Build commit; for runtime artifact, the Ship PR merged after a passing
  Proof PR, adding `proved` between `built` and `shipped` as today.
- `shipped` is final. Later change starts a new intent or, once P2
  ships, a fix.

## Permissions

- The owner accepts the Spec, approves the Plan, and may be the
  reviewer or the merger of a Build PR, but not both author and
  approver.
- Any person who is not the Build PR's author can give the approving
  review. A coding agent or bot cannot.
- A contributor or the repository's automation pushes the shipped tag,
  and only after the Build PR has merged.
- Nobody moves a shipped tag. An attempt is a blocking review finding.
- An administrator sets the delivery mode at bootstrap; changing it
  later is a reviewed change to the conventions file.

## Errors and edge cases

- S20 When the delivery setting is missing or misspelled, the Build PR
  check fails and names the two accepted values.
- S21 When an S-rule result names a test that the repository does not
  contain, the check names the S-rule and the missing test.
- S22 When the accepted Spec gains or changes an S-rule after the Build
  record was written, the Build PR check fails until the record covers
  the current rules.
- S23 When a shipped tag points at a commit that is not on the default
  branch, or whose Build record is absent, the handoff and PR checks
  report the tag as invalid and the phase as not shipped.
- S24 When a Build PR is merged without a current approving non-author
  review, the next handoff reports the phase as built without review
  and blocks the dependent stage until a review is recorded on that
  merged head or a corrected Build PR merges with one.
- S25 When a runtime-artifact product opens a Build PR whose record
  carries S-rule results, the check accepts them but still requires the
  separate Proof and Ship PRs.
- S26 When an in-flight phase under the old rules has an open Proof or
  Ship task, closing it as not planned does not unlock any dependent
  work; the shipped tag does.

## UX

This phase introduces no product screen. It changes what a contributor
writes in the Build record, what a reviewer reads in the Build PR, and
what one person reads in the README setup. No design mock is required.

## Contract changes

No external product or client contract changes. This phase changes the
repository's contributor workflow only. It does not change `packages/`.

## Data changes

The repository newly remembers a delivery setting in its conventions
file, S-rule results and Intent results in Build records, and shipped
tags. For a merged-source product it stops creating Proof and Ship
records and tasks. Existing shipped chains, including their Proof and
Ship records and tags, remain unchanged and readable under the old
rules. Chains 001 to 004 are not back-filled.

## Region variance

No region-specific behavior.

## Acceptance criteria

- T1 (S1, S20) A conventions file with `merged source` passes; with
  `runtime artifact` passes; with the setting missing or misspelled the
  Build PR check fails and names both accepted values.
- T2 (S2, S25) A runtime-artifact product's Proof and Ship PRs pass and
  fail under exactly the existing tests, and a Build PR carrying S-rule
  results still needs them.
- T3 (S3, S4, S21, S22) A merged-source Build record with one PASS line
  per S-rule naming an existing test passes. A missing rule, a FAIL, a
  test name absent from the repository, and a Spec rule added after the
  record each fail with the rule named.
- T4 (S5, S14) A last-phase Build record with every Intent success
  criterion true allows the parent to close; a record leaving one open
  keeps the parent open.
- T5 (S6, S24) A Build PR merged with a current non-author approving
  review counts as reviewed; one merged by a human without that review
  is reported as built without review and blocks the dependent handoff.
- T6 (S7, S8, S23) A shipped tag on a merged Build commit on the default
  branch counts as shipped; a tag on any other commit is invalid.
- T7 (S9) A moved shipped tag is a blocking finding in review policy.
- T8 (S10, S11) A dependent Spec handoff passes when the predecessor
  phase has a valid shipped tag and fails without one; changes under a
  shipped phase directory are rejected as immutable.
- T9 (S12) The Build record template and the record in this outcome's
  own Build carry each tracking fact once; no field repeats a hash.
- T10 (S13, S18, S26) A merged-source phase with Intent, Spec, Plan, and
  Build tasks passes the tracking check; a runtime-artifact phase still
  needs six tasks; a Proof task closed as not planned is not a completed
  dependency.
- T11 (S15, S16) The README setup section states the self-authored PR
  limit and the authoring identity, and the setup check's report names
  that requirement when required review is configured.
- T12 (S17, S19) Repository guidance contains one consistent merged-
  source and runtime-artifact policy, and every human gate named in S19
  still appears in the conventions file and review policy.

## Out of scope

- A one-PR fix lane for shipped outcomes. P2 owns that outcome.
- Making stage issues optional or deriving them. P3 owns that outcome.
- Trimming the prototype note and its lifecycle. Outcome 004 P2 owns it.
- Automating tag pushes, task closure, or issue creation. Outcome 004
  P3 owns automation.
- Changing how runtime-artifact products prove and promote an artifact.
- Rewriting chains 001 to 004 or their Proof and Ship records.

## Open questions

- Plan owner: the exact test identifier form the check matches in a
  product's test files, and how a product with a non-Python stack
  declares its test file locations.
- Plan owner: how the shipped tag is verified from a fresh clone in CI,
  given that the ordinary pull request event does not carry tags.
