# Try an idea as a prototype and get feedback before its spec — Intent

**Stage:** intent
**Outcome:** 004-prototype-first
**Phase:** single
**Parent issue:** https://github.com/kevalabs/ai-native-product-template/issues/22
**Stage issue:** https://github.com/kevalabs/ai-native-product-template/issues/23

**Status:** accepted
**Accepted by:** Suraj Chhetry, original Intent confirmed on 2026-09-15; prototype worktree and code-retaining promotion revision confirmed in the owner conversation on 2026-09-17 (see Revision below).
**Kind:** change
**Originator:** Suraj Chhetry
**Date:** 2026-09-15
**Due:** —

The intent answers WHY. It names the outcome we want and how we will
know we got it. No screens, no tables, no endpoints — those are spec
and plan.

## Problem

A team using this template learns what the owner really wants too
late. Owner feedback from looking at the thing arrives at Build,
stage 4 of 6, after the spec is already accepted. For work that is
mostly about what a person sees, what numbers a report shows, or how
an outside service behaves, the cheapest time to learn is before the
spec. Today the process has no place to try an idea out cheaply first.

The evidence comes from a salon product built on this template:

- One outcome was a new menu, some placeholder pages, and a sample
  calendar. It took 21 merged PRs, 2,684 lines of Markdown, and 1,203
  lines of app code.
- One of its phases was a static picture of a calendar with fake data.
  Nothing was clickable, and it was marked to be thrown away when the
  real calendar arrived. It still took 9 PRs, 30 spec rules with a test
  each, and its own Proof and Ship PRs: 1,413 lines of Markdown for 398
  lines of code.
- The owner first saw that screen after it was built and deployed. It
  "looked very bad" and was rebuilt. Then the owner's own mock-ups
  arrived during Proof, which forced a spec revision PR and a second
  correction Build PR. The spec was written three times and the screen
  was built three times.
- A later phase that only made menu names clearer took 4 PRs and 1,343
  lines of Markdown before Proof and Ship.

The cause is not too many gates. The cause is where feedback arrives.
The owner also spends time on typing that the gates do not need:
starting each stage, creating the issue for each stage, and recording
the approved link and merged PR on each task by hand.

On 2026-09-17, the owner asked to simplify prototype work: keep it in
the normal worktree location on its own branch, then let an approved
prototype become feature work without throwing its code away.

## Outcome

Before a spec is written, a team can show the owner a cheap prototype
in a normal worktree on a separate branch. Once the owner approves it,
that prototype becomes feature work and retains its code. It follows
Spec → Plan → Build → Test + Review → Ship. The spec freezes what the
owner accepted, and Build tests use the same confirmed examples. Each
stage keeps its approval and merge gate, while the mechanical tracking
steps take one command instead of many manual edits.

The sequence becomes Intent → Prototype → Spec → Plan → Build →
Test + Review → Ship. The prototype step is required for work about
screens, rules and calculations, or outside services. It is skipped
only with a one-line reason in the spec, for example when there is
nothing to show.

## Actors

- The owner accepts the intent, confirms the prototype, accepts the
  spec, approves the plan, and reviews every PR.
- Real users look at a prototype where the team can reach them.
- Contributors and coding agents build prototypes, write artifacts,
  and run the stage commands.
- Reviewers check that a spec cites its accepted prototype and that
  Build tests load the confirmed examples.
- The system (hooks, CI, and scripts) checks the prototype lane and
  does the tracking steps after each merge.
- Teams that adopt the template fill in their own sandbox setting.

## Success criteria

- For work about screens, numbers, or an outside service, the owner
  confirms a prototype before its spec is accepted. The spec cites the
  exact accepted version, or says in one line why there is none.
- The Build's tests for that work load the same examples file the
  owner confirmed.
- Starting a stage, creating the tracking issues for a merged intent,
  and recording a merged stage on its task each take one command or
  happen on merge, and never create duplicate issues.
- Every existing gate and human approval still applies. No stage is
  removed, and no agent records an approval it did not receive.
- Products already built on the template can adopt the change by
  following a written adoption note.

## Phases

- P1-prototype-step — contributors and agents can run the prototype
  step, in one of its three forms, between Intent and Spec; the spec
  freezes the accepted prototype; the plan and review use its examples
  as test data. Docs, skills, and templates only. Depends on: —
- P2-proto-lane — **cancelled on 2026-09-17, see the second Revision.**
  A team can work on a prototype branch that needs no stage artifacts, and the checks keep it inside the product's declared
  sandbox. Its worktree uses the normal worktree location. Owner
  approval allows the branch and code to become feature work, followed
  by the existing Spec-through-Ship gates. P2 updates the delivered
  guidance and checks for this promotion. Depends on: P1 (can run
  alongside P3 after the promotion contract is settled)
- P3-stage-automation — contributors can start a stage, create an
  outcome's tracking issues, and record a merged stage on its task
  without manual edits. Depends on: P1 (can run alongside P2)

Shared ground — settled before P2 and P3 run in parallel, and where:

- the words prototype, sandbox, worked example, prototype note, and
  prototype confirmation → `product/glossary.md`, in P1's Build PR
- the three prototype forms and what the owner confirms for each →
  P1's spec
- the header that records a prototype confirmation → P1's spec
- the shape of the prototype note (what it tests, who looks at it,
  expiry, outcome) → P1's spec
- where a product declares its sandbox → a section in `AGENTS.md`;
  its exact form in P2's spec
- the tracking fields the automation reads and writes → already set by
  feature 003; P3 reuses them and does not redefine them
- prototype-to-feature promotion, retained code, and its relationship
  to stage branches → P2's accepted Spec; settle this before dependent
  P3 automation is specified

## Affected systems

Repository conventions (`AGENTS.md`, `README.md`), the process model,
stage skills including a new prototype skill and the bootstrap skill,
artifact templates, review policy, the glossary, the SDLC workflow
capability doc, the local and GitHub checks, their offline tests, the
CI workflow, the Makefile, and the gate guide. No `packages/`
contracts change in this template.

## Constraints

- The template stays product-agnostic. The salon product appears only
  as evidence in this intent. Examples in skills and docs are generic.
- Shipped chains stay frozen. Chains that have not reached Spec may
  adopt the prototype step. Nothing is back-filled.
- Phases are still cut by outcome, never by layer. Build still does
  screens and back end together.
- A prototype starts in a separate branch and a worktree alongside the
  team's other worktrees. After owner approval, that branch can become
  feature work and keep its code. It follows Spec → Plan → Build →
  Test + Review → Ship. An accepted governing Intent is still required;
  a standalone experiment obtains one before Spec if none exists.
- Prototype approval does not approve a Spec or Plan, permit further
  feature implementation before Plan approval, or approve a release.
  Retained code must meet the approved scope and normal Build tests
  and review before merging as production implementation. Spec and
  Plan PRs remain artifact-only; prototype source enters main through
  the reviewed Build. Preserve the exact confirmed version as evidence.
- Human gates do not change. The prototype step adds one owner
  confirmation, recorded like other approvals with the person, date,
  and source. Agents never invent it.
- Every new check starts with a failing test. `make test` and
  `scripts/verify_template.py` stay green.
- Each phase's Build PR stays under about 1,500 changed lines.
- The change makes small work cheaper. It must not add a seventh stage
  to work with nothing to show, such as a pure refactor or
  infrastructure.
- The SDLC workflow capability currently says there is no background
  issue or PR automation (R24). P3 changes that rule on purpose, so
  P3's spec must replace it and keep the rule that nothing records a
  human approval automatically.
- Nothing committed carries a tool signature: no "Generated with" line
  and no co-author line naming an AI.
- The last Ship record includes an adoption note for products already
  on the template. It lists which files to copy or merge, which
  settings each product must fill (sandbox paths, coverage and
  translation exemptions), and what changes for products with extra
  branch lanes such as `fix/` and `chore/`.
- [ASSUMED] No deadline applies. The reason to act now is the rework
  the salon product shows.

The owner decided the following in the working conversation on
2026-09-15. The branch and code-retention decision was replaced on
2026-09-17 as recorded below:

- The prototype step is required for screen, rule, and integration
  work. Skipping it needs a one-line reason in the spec.
- Originally, prototype code and its working note never merged to the
  default branch. The 2026-09-17 revision allows approved code to enter
  through feature Build. The working note remains prototype evidence.
- A prototype note expires 30 days after it is written unless the
  product sets another length. An expired note makes CI warn, not fail.
- Stage automation stays in this outcome as P3.
- A product declares its sandbox paths in a section of `AGENTS.md`.
  Bootstrap fills it, and the existing bootstrap PR may already
  change that file.

## Revision

Suraj Chhetry requested on 2026-09-17 in the working conversation:

> Let's make it simple prototype is a also work tree so it be place
> where working tree are being keep and also make sure that prototype
> will be separate branch which once approved can be converted into feature.

Asked whether conversion keeps the prototype code, with Spec and Plan
approval required before further feature work, the owner confirmed:

> yea , prototype once approve will become feature and need to follow
> the patter as spec->plan ....

This revises the still-open Intent for P2 and dependent P3 work. It does
not rewrite shipped P1 artifacts or claim that promotion is implemented.
P1 shipped through [PR #49](https://github.com/kevalabs/ai-native-product-template/pull/49)
under the original [Intent PR #43](https://github.com/kevalabs/ai-native-product-template/pull/43).
Its original approved Intent remains available at commit
`d05540e142e83241f18a69ecb4813d0d1b99bbb4`.

P2's Spec must explicitly replace P1's independent-reimplementation
flow and the prohibition on merging approved prototype code, including
S9's code exclusion. P2's reviewed Build will update the active guide,
skills, capability rules, and checks consistently. Exact-version owner
confirmation, retained examples, human stage approvals, and immutable
shipped records continue to apply. P3 uses the settled promotion
contract for its automation rather than defining another one.

## Revision, 2026-09-17: P2 cancelled

Suraj Chhetry cancelled phase P2-proto-lane on 2026-09-17 in the working
conversation, after reviewing the work left across both open intents.

The reason is evidence, not doubt about the idea. The prototype step
shipped in P1 and has not been used once since. Every spec written after
it recorded a justified skip, including this template's own. Building a
sandbox lane, branch enforcement, and promotion machinery for a step
nobody has exercised is speculative, and the design will be easier to
get right after someone actually prototypes something.

The success criterion about trying an idea on a prototype branch without
stage artifacts is withdrawn with the phase, rather than left
permanently open. P1's shipped artifacts stay unchanged as the
historical record, and the prototype step itself remains in the
workflow: an owner can still confirm a prototype before a Spec, using a
workspace the product already permits.

This also supersedes the promotion decision recorded in the first
Revision above. Nothing implements prototype-to-feature promotion, and
no guidance claims it does. The phase entry stays listed under Phases so
the tracking graph still matches this intent; its issues are closed as
not planned. Cancellation is not shipment and unlocks no dependent work.

Phase P3-stage-automation is unaffected and still required. With P2
cancelled it has no promotion contract to consume, so its Spec covers
stage tracking only.

## Open questions

- P1 settled retention: preserve the confirmed commit through shipment
  using a recorded remote ref, retaining a tag before deleting its only
  branch. P2 must preserve this evidence when a branch becomes feature work.
- Owner, during P2's Spec: where is a prototype's final outcome
  (converted to feature work or dropped) recorded so the team can find it?
- P2 Spec and Plan owners: define the promotion handoff so the same
  worktree and retained code can continue as feature work while Spec
  and Plan keep their separate artifact-only PRs and the Build starts
  from the merged Plan. Settle how prototype history is retained and
  how carried code becomes subject to the normal Build checks.
