# Try an idea as a prototype and get feedback before its spec — Intent

**Stage:** intent
**Outcome:** 004-prototype-first
**Phase:** single
**Parent issue:** https://github.com/kevalabs/ai-native-product-template/issues/22
**Stage issue:** https://github.com/kevalabs/ai-native-product-template/issues/23

**Status:** draft
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

## Outcome

Before a spec is written, a team can show the owner a cheap, thrown-away
prototype and get it confirmed. The spec then freezes exactly what the
owner accepted, and the Build is tested against the same examples the
owner confirmed. Every existing gate stays, while the mechanical steps
around the gates take one command instead of many manual edits.

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
- A team can try an idea on a prototype branch without writing an
  intent, spec, plan, proof, or ship record. The checks reject any
  change outside the product's declared sandbox and the prototype note.
- Starting a stage, creating the tracking issues for a merged intent,
  and recording a merged stage on its task each take one command or
  happen on merge, and never create duplicate issues.
- Every existing gate and human approval still applies. No stage is
  removed, and no agent records an approval it did not receive.
- Products already built on the template can adopt the change by
  following a written adoption note.

## Phases

- P1 prototype-step — contributors and agents can run the prototype
  step, in one of its three forms, between Intent and Spec; the spec
  freezes the accepted prototype; the plan and review use its examples
  as test data. Docs, skills, and templates only. Depends on: —
- P2 proto-lane — a team can work on a prototype branch that needs no
  stage artifacts, and the checks keep it inside the product's declared
  sandbox. Depends on: P1 (can run alongside P3)
- P3 stage-automation — contributors can start a stage, create an
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
- A prototype is thrown away. Its code is never promoted into product
  code. Promotion means a new intent that cites the prototype.
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
2026-09-15:

- The prototype step is required for screen, rule, and integration
  work. Skipping it needs a one-line reason in the spec.
- A prototype branch never merges to the default branch. That covers
  its code and its prototype note. A demo that must stay up becomes
  its own intent.
- A prototype note expires 30 days after it is written unless the
  product sets another length. An expired note makes CI warn, not fail.
- Stage automation stays in this outcome as P3.
- A product declares its sandbox paths in a section of `AGENTS.md`.
  Bootstrap fills it, and the existing bootstrap PR may already
  change that file.

## Open questions

- Owner, during P1's spec: a spec links the exact accepted prototype
  commit. Prototype branches never merge and may be deleted, so how
  does that commit stay reachable?
- Owner, during P2's spec: the prototype note never reaches the
  default branch. Where is its outcome (promoted to intent NNN, or
  dropped) recorded so the team can find it later?
