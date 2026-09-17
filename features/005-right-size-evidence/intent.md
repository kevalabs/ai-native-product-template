# Keep every gate, drop the paperwork the gates do not need — Intent

**Stage:** intent
**Outcome:** 005-right-size-evidence
**Phase:** single
**Parent issue:** https://github.com/kevalabs/ai-native-product-template/issues/51
**Stage issue:** https://github.com/kevalabs/ai-native-product-template/issues/52

**Status:** draft
**Kind:** change
**Originator:** Suraj Chhetry
**Date:** 2026-09-17
**Due:** —

The intent answers WHY. It names the outcome we want and how we will
know we got it. No screens, no tables, no endpoints — those are spec
and plan.

## Problem

The loop Intent → Prototype → Spec → Plan → Build → Test + Review →
Ship is followed and enforced in this template. The order is right and
every human gate sits where it should. The cost is on the sides of that
spine: the process pays twice for evidence it already has, and it has
no cheap path for small work or for one person working with an agent.

The evidence is this repository's own chain 004, phase P1, audited on
2026-09-17:

- Build merged at 11:34, Proof at 17:35, and Ship at 22:04 on the same
  day. Proof reran the same 86 tests on the same commit that Build CI
  had already run. Its human review section restates the Build PR
  approval. Ship repeats one commit hash in three header fields and
  records no new decision. That is two PRs, two issues, two worktrees,
  and two human reviews for no new information. `REVIEW.md` already
  makes the Build reviewer walk every S-rule.
- One outcome needs a parent issue plus six task issues, each with
  eight bold fields, blocked-by links, and after every merge a
  permalink, a PR link, a status change, and a close. The checks fail
  unless the graph has exactly that shape. The Markdown artifacts
  already carry status, acceptance, and predecessor PR.
- Tracking headers, permalink definitions, transition notes, and
  restated success criteria are about 230 of the 1,170 non-blank lines
  across the six P1 files. Proof and Ship each restate the same six
  success criteria.
- The checks accept only artifact, feature, proof, and ship branches.
  A typo fix or a hotfix therefore needs six PRs and seven issues.
  Chain 004's intent records that a menu-name change in a product on
  this template took 4 PRs and 1,343 lines of Markdown before Proof.
  Products answer this with unofficial `fix/` and `chore/` lanes the
  template never defines.
- GitHub ignores an approval from a PR's author, and setup requires an
  approving review. The only working path for one person is a bot
  identity that opens every PR. No file in the repository says so. A
  new solo user either fails setup or grants themselves bypass, which
  `REVIEW.md` tells reviewers to treat as a finding.
- The rules that say an S-rule passed are free text. Build's
  verification header only has to be filled. Proof's PASS lines match a
  pattern with no link to a real test. An agent can write PASS for
  every rule and only the human catches it.

## Outcome

One person with a coding agent, or a team, completes an outcome through
the same seven steps and the same human gates with only the evidence
that adds information. When the merged source is the delivery, Test +
Review evidence lands in the Build PR and Ship is a recorded result on
the merged Build, not two more PRs. Every S-rule names the test that
proves it and the checks fail when one is missing. A bug fix to a
shipped outcome lands in one reviewed PR. A product decides whether
stage issues exist. A solo developer can follow the README and merge
under the required branch protection without a bypass.

## Actors

- The owner accepts intents and specs, approves plans, and reviews the
  Build PR. Their gates do not change.
- A solo developer follows the written setup and gets their PRs
  approved and merged as one person.
- Contributors and coding agents write artifacts, run the stage
  commands, and ship fixes.
- Reviewers check S-rule evidence in the Build PR and the linked fix
  in a fix PR.
- The system (hooks, CI, and scripts) checks S-rule coverage, the
  combined evidence, the fix lane, and the optional tracking graph.
- Products with a runtime artifact keep separate Proof and Ship
  evidence for the staging test and the promotion.

## Success criteria

- For a product whose delivery is the merged source, one outcome takes
  four merged PRs after Intent acceptance: Spec, Plan, Build, and
  nothing else. Products that name a runtime artifact keep separate
  Proof and Ship PRs.
- Every Spec S-rule has a named test and a recorded result against the
  merged Build, and CI fails when one is missing or does not pass.
- A bug fix or small correction to a shipped outcome lands in one
  reviewed PR that starts with a failing test and links the outcome it
  corrects. It needs no new intent, spec, plan, proof, or ship record.
- A product can turn stage issues off. The checks then read approval
  and merge evidence from the artifacts and PRs alone.
- A solo developer following the README can get a PR approved and
  merged under the required branch protection without a bypass.
- Every existing human gate still applies: intent acceptance, spec
  acceptance, plan approval, and human review of every PR. No stage
  order changes and no agent records an approval it did not receive.

## Phases

- P1-evidence-in-build — contributors record Test + Review evidence,
  with a named test per S-rule, in the Build PR, and record Ship as a
  result on the merged Build when the merged source is the delivery.
  Each tracking fact appears once per chain. The README documents the
  solo-developer setup. Depends on: —
- P2-fix-lane — a contributor ships a bug fix or small correction to a
  shipped outcome in one reviewed PR that links the outcome it corrects.
  Depends on: P1
- P3-optional-tracking — a product chooses whether stage issues exist;
  when they do not, the checks verify approval and merge evidence from
  the artifacts and PRs alone. Depends on: P1 (can run alongside P2)

Shared ground — settled before P2 and P3 run in parallel, and where:

- what a Build record must contain for Test + Review and Ship
  evidence, and when a product must keep separate Proof and Ship →
  P1's spec
- the words evidence in build, fix lane, and tracking mode →
  `product/glossary.md`, in P1's Build PR
- the fields the checks read from artifacts and PRs when tracking
  issues are off → P1's spec names them; P3's spec uses them
- what counts as a small correction and what forces a new intent →
  P2's spec
- stage automation in outcome 004 phase P3 automates whatever tracking
  remains required after P3 here; its spec starts after P3's spec is
  accepted

## Affected systems

Repository conventions (`AGENTS.md`, `README.md`), the process model,
review policy, the gate guide, the stage skills and status skills, the
artifact templates, the glossary, the SDLC workflow capability doc, the
local and GitHub checks, their offline tests, and the CI workflow. No
`packages/` contracts change in this template.

## Constraints

- The seven steps and their order do not change. No human gate is
  removed. Intent, Spec, and Plan keep their own artifact PRs.
- Test + Review and Ship remain steps with recorded evidence. They lose
  their separate PRs only when the merged source is the delivery. A
  product declares a runtime artifact to keep the separate PRs.
- Shipped chains stay frozen. Chains 001 to 004 are not rewritten.
  Outcome 004 phase P2 owns the prototype note and its trim; this
  intent does not touch prototype rules.
- Every new check starts with a failing test. `make test` and
  `scripts/verify_template.py` stay green.
- Each phase's Build PR stays under about 1,500 changed lines.
- Every PR in this repository is opened by the `keva-builder[bot]`
  identity so the owner's approval counts. The README documents this
  as the solo-developer path for products.
- Nothing committed carries a tool signature: no "Generated with" line
  and no co-author line naming an AI.
- [ASSUMED] No deadline applies. The reason to act now is that every
  outcome after this one pays the cost the audit measured.

## Open questions

- Owner, during P1's spec: does a fix PR update the capability doc in
  place, or does the shipped outcome directory gain a short correction
  record?
- Owner, during P1's spec: when tracking issues are on, is the parent
  Intent issue enough, or do stage tasks stay for phased outcomes?
- Owner, during P2's spec: the size limit for a small correction, in
  changed lines or touched files, above which a new intent is required.
