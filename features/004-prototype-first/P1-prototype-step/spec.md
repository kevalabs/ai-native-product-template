# Confirm a prototype before writing its spec — Spec

**Stage:** spec
**Outcome:** 004-prototype-first
**Phase:** P1-prototype-step
**Parent issue:** https://github.com/kevalabs/ai-native-product-template/issues/22
**Stage issue:** https://github.com/kevalabs/ai-native-product-template/issues/26
**Predecessor PR:** https://github.com/kevalabs/ai-native-product-template/pull/43

**Status:** accepted
**Accepted by:** Suraj Chhetry, confirmed in the owner conversation on 2026-09-16.
**Intent:** [Try an idea as a prototype and get feedback before its spec](../intent.md)
**Personas served:** product owner, contributors, reviewers, and reachable real users named by the Intent; `product/personas.md` does not yet define product-specific personas
**Capabilities affected:** `product/capabilities/sdlc-workflow.md`

The spec answers WHAT. Someone who knows the product should
understand every line without knowing how it is built. No tables,
endpoints, components, or services belong here.

## Flows

### Try an idea

1. After an Intent is accepted and merged, the contributor identifies
   whether the outcome concerns screens, rules or calculations, outside
   services, or more than one of these.
2. The contributor prepares the matching prototype forms and named
   examples. The prototype contains no automated product tests.
3. The contributor makes a runnable prototype version ready for feedback.
4. Reachable real users may try it and give feedback.
5. The product owner reviews the prototype and its examples. The owner
   confirms or rejects that exact version.
6. If the owner rejects it or requests a change, the contributor creates
   a new version and asks for confirmation again.

### Freeze the confirmed behavior in a Spec

1. The Spec author cites the exact confirmed prototype commit,
   confirmation source, and confirmed examples.
2. The Spec PR keeps the accepted evidence and examples reviewable. It
   does not carry the disposable prototype code.
3. The Spec turns the confirmed examples into requirements and acceptance
   cases.
4. If there was nothing meaningful to prototype, the Spec gives a
   one-line reason. Owner acceptance of the Spec also accepts that skip.
5. Review blocks acceptance when the confirmation or evidence cannot be
   reviewed.

### Build, prove, and ship the confirmed behavior

1. The Build implements the accepted Spec independently of the disposable
   prototype code.
2. Build tests load the same confirmed examples. A behavior change needs
   renewed prototype confirmation or an accepted Spec revision.
3. Each stage branch merges through a reviewed PR into `main`. A merge to
   `main` does not by itself mean production delivery.
4. A product may deploy a feature-branch preview before merge when human
   interaction would find useful problems early.
5. The merged Build commit produces an immutable artifact for the
   development or staging environment.
6. Proof tests that exact merged Build version.
7. Ship promotes the same proved artifact to the product's delivery
   destination. For this template, which has no deployed runtime, the
   reviewed merge to the default branch remains its delivery.

## Requirements

- S1 A contributor can begin prototype work only after the outcome's
  accepted Intent PR has merged.
- S2 A contributor uses a screen walkthrough for screen behavior, worked
  examples for rules or calculations, and an integration trial for
  outside-service behavior.
- S3 A contributor uses every applicable prototype form when an outcome
  combines screens, rules or calculations, and outside-service behavior.
  The owner may confirm the forms together when they share one exact
  version and evidence set.
- S4 A contributor does not add unit, integration, or end-to-end tests for
  prototype code. The prototype has no coverage gate and needs only to run
  well enough to demonstrate its named examples.
- S5 Every screen walkthrough has named scenarios and sample data. Every
  worked example has named inputs and expected outputs. Every integration
  trial has named success and failure cases.
- S6 Reachable real users may give prototype feedback, but only the product
  owner can confirm or reject a prototype version. The owner records how
  available user feedback affected the decision.
- S7 A prototype confirmation records the prototype form, exact commit,
  evidence and examples location, confirmer, confirmation date, and an
  attributable confirmation source.
- S8 A confirmed or rejected prototype version is immutable. Any change
  creates a new version, and only the latest explicitly confirmed version
  governs the Spec.
- S9 The confirmed prototype commit remains reachable until its phase
  ships. The Spec PR preserves the confirmed evidence and examples, but
  never merges the disposable prototype code.
- S10 A contributor starts substantive Spec drafting only after the owner
  confirms the prototype or the Spec records a one-line skip reason.
  Creating the Spec tracking task before that decision is allowed.
- S11 An unresolved prototype becomes `expired` 30 days after its note is
  created unless the product declares another period. Expiry warns and
  does not fail a check. An expired version can return to `ready` after it
  is refreshed.
- S12 When 30 days pass before Spec acceptance, the owner reconfirms the
  prototype or explicitly accepts its age in the Spec. An accepted Spec
  freezes its confirmed prototype and that confirmation no longer expires.
- S13 A reviewer blocks Spec acceptance when the prototype commit,
  confirmation source, evidence, or examples cannot be reviewed. The only
  alternative is an owner-accepted skip reason in the Spec.
- S14 The owner accepts a prototype skip only when the outcome has no
  behavior a person can meaningfully inspect before Build. A pure refactor
  is one valid example.
- S15 Build tests load the confirmed examples without silently changing
  them. Changed examples require a newly confirmed prototype version or an
  accepted Spec revision before Build continues.
- S16 Prototype work follows the product's existing security, privacy, and
  secret-handling rules. Real personal data and production secrets are
  never used to make a prototype quick.
- S17 Every stage branch merges through a reviewed PR into `main`. Products
  do not use environment branches such as a long-lived `dev` branch to
  represent deployment state.
- S18 A merge into `main` establishes the integrated source version, not a
  production release. Preview deployment before merge is optional. Proof
  tests the immutable artifact built from the merged Build commit, and
  Ship promotes that same proved artifact.
- S19 Contributor guidance explains the branch, preview, staging, Proof,
  and Ship policy in one consistent way. The same Build change removes or
  updates any conflicting repository guidance.

## States and transitions

Each prototype version follows this state model:

`draft` → `ready` → `confirmed` | `rejected`

`ready` → `expired` → `ready`

- `draft` means the version is not ready for feedback.
- `ready` means the version and its examples are available for feedback.
- `confirmed` means the owner accepted that exact version. It is final.
- `rejected` means the owner declined that exact version. It is final.
- `expired` means the version remained unresolved beyond the configured
  period. Refreshing it returns that version to `ready`.
- Further work after `confirmed` or `rejected` creates a new version rather
  than changing the final version.

## Permissions

- Contributors can create, refresh, and demonstrate prototype versions.
- Reachable real users can give feedback. Their feedback is not approval.
- Only the product owner can confirm, reject, accept an aged confirmation,
  or accept a prototype skip.
- Spec reviewers block acceptance when the required prototype evidence is
  absent or inaccessible.
- Build reviewers block implementation that promotes prototype code or
  changes confirmed examples without the required acceptance.

## Errors and edge cases

- S20 When no prototype form matches an outcome, the Spec names the skip
  reason rather than creating an empty prototype.
- S21 When a mixed outcome omits an applicable prototype form, review lists
  the missing form and blocks Spec acceptance.
- S22 When a confirmation points to a changed or different commit, the
  version is not confirmed and substantive Spec drafting remains blocked.
- S23 When confirmed evidence cannot be preserved in the Spec PR, review
  blocks acceptance even if the prototype was previously demonstrated.
- S24 When a prototype cannot run one of its named examples, it cannot move
  to `ready` for that evidence set.
- S25 When Proof receives an artifact that differs from the merged Build
  version, Proof fails and Ship remains blocked.
- S26 When a production destination cannot receive the exact proved
  artifact, shipment fails rather than rebuilding a different artifact.

## UX

This phase introduces no product screen. It standardizes three feedback
experiences:

- A screen walkthrough lets a person follow the important screen scenarios
  with sample data.
- A worked example lets a person compare named inputs with expected
  outputs.
- An integration trial lets a person observe named success and failure
  cases for an outside service.

No design mock is required for this process-only phase.

## Contract changes

No external product or client contract changes. P1 changes the repository's
contributor workflow. It does not change `packages/` contracts.

## Data changes

The repository newly remembers prototype confirmation details, preserved
evidence, confirmed examples, accepted age exceptions, and skip reasons in
reviewed artifacts. Existing shipped chains remain unchanged. A chain that
has not reached Spec may adopt this process; nothing is back-filled.

Prototype code remains outside the default branch and is not production
data or product code.

## Region variance

No region-specific behavior. Products may choose their own deployment
destinations, but the same proved artifact is promoted without region
branches in business logic.

## Acceptance criteria

- T1 (S1) A prototype attempt before its Intent merge is rejected; the same
  attempt after the merge can begin.
- T2 (S2, S3) Screen, calculation, integration, and mixed examples select
  the required prototype forms, including every applicable form for mixed
  work.
- T3 (S4) Review of a prototype containing an automated product test asks
  for the test to be removed, while a runnable test-free demonstration is
  allowed.
- T4 (S5) Each prototype form is rejected as incomplete when one of its
  required named example parts is absent.
- T5 (S6) Real-user feedback is recorded without granting confirmation;
  owner confirmation records how the feedback affected the decision.
- T6 (S7) Confirmation is incomplete when any required identity, version,
  evidence, date, or source field is absent.
- T7 (S8) Changing a confirmed or rejected version creates a new version
  and does not alter the final record.
- T8 (S9) The confirmed commit remains reachable through phase shipment,
  the Spec PR preserves its evidence and examples, and the Spec PR contains
  no prototype code.
- T9 (S10) A Spec with substantive requirements but neither confirmation
  nor a skip reason is blocked; a tracking-only task is allowed.
- T10 (S11, S12) An unresolved 30-day-old note warns without failing. Spec
  acceptance then requires reconfirmation or explicit acceptance of age,
  while an already accepted Spec does not expire.
- T11 (S13, S14) Missing evidence blocks acceptance unless the owner accepts
  a one-line reason showing there was nothing meaningful to prototype.
- T12 (S15) Build tests load the confirmed examples unchanged. A changed
  example blocks Build until the required acceptance exists.
- T13 (S16) Review rejects prototype evidence containing real personal data
  or production secrets.
- T14 (S17) Stage PRs target `main`; documentation does not instruct teams
  to use a long-lived environment branch as deployment state.
- T15 (S18) A scenario distinguishes integration into `main`, optional
  preview, staging of the merged Build artifact, Proof, and promotion of
  the same artifact at Ship.
- T16 (S19) Contributor guidance contains one consistent branch and
  deployment policy, with no conflicting repository instruction left by
  the Build.
- T17 (S20) An outcome with nothing meaningful to demonstrate records a
  concrete skip reason and creates no empty prototype.
- T18 (S21) A mixed outcome missing one applicable form is blocked with the
  missing form named.
- T19 (S22) A confirmation for another commit does not unlock substantive
  Spec drafting.
- T20 (S23) A demonstrated prototype with inaccessible preserved evidence
  does not unlock Spec acceptance.
- T21 (S24) A prototype that cannot run a named example cannot become
  `ready` for that evidence set.
- T22 (S25) Proof rejects an artifact that differs from the merged Build
  version and keeps Ship blocked.
- T23 (S26) Shipment fails instead of rebuilding when the production
  destination cannot receive the proved artifact.

## Out of scope

- Enforcing sandbox paths or creating the prototype branch lane. P2 owns
  that outcome.
- Automating stage startup, issue creation, or merge recording. P3 owns
  that outcome.
- Promoting prototype code into product code.
- Requiring automated tests, production quality, performance tuning, or
  coverage for a prototype.
- Making real-user feedback a mandatory gate.
- Changing existing shipped feature chains.
- Defining a product-specific hosting provider or deployment platform.

## Open questions

- Plan owner: choose the exact reviewed artifact fields and repository
  documents that present this behavior without duplicating conflicting
  guidance.
- P2 Spec owner: define how prototype branches and sandbox boundaries are
  enforced, and where an unmerged prototype note's final outcome is found.
