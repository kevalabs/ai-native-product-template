---
description: "Stage 2 — interview against the intent, then draft spec.md for a feature chain"
argument-hint: "<NNN or feature directory name>"
---

Draft the Stage 2 spec for feature: $ARGUMENTS

The spec turns an accepted intent into numbered, testable requirements.
Your job is to force precision: every vague answer becomes either a
sharp S-rule or an open question. Do not draft `spec.md` until the
interview is done.

## Step 0 — gates and context

- Resolve `features/NNN-*/`. Its `intent.md` must exist with status
  `accepted`. If it is still `draft`, stop and say the Stage 1 gate is
  not passed (the owner can accept it right now if they mean to).
- Read the intent, `product/glossary.md`, `product/personas.md`,
  `product/regions.md` (if present), and every
  `product/capabilities/` doc the intent could touch. List for the
  user which capabilities you believe are affected and confirm.
- If `spec.md` already exists, switch to revising it — show what
  exists and ask what changed.

## Step 1 — interview (requirements before design)

Run the interview per `.claude/interview-method.md` (read it first):
frontier rounds, a recommended answer with every question, facts
looked up rather than asked. For every answer, apply the test: *could
someone write a failing test from this sentence?* If not, ask again
more narrowly.

1. **Behavior rules.** Walk the outcome from the intent and extract
   rules in the form `<actor> can <action> when <condition>`. Probe
   the conditions — "always?", "which persona exactly?", "what if the
   precondition fails?". These become S1, S2, …
2. **Collisions with today.** For each affected capability doc, do any
   existing R-rules change or conflict? A changed R-rule must appear
   explicitly in the spec.
3. **UX.** What must each screen/flow achieve (not how it looks)? Are
   mocks available to commit under `features/NNN-*/design/`? If none
   exist yet, record that as an open question — don't invent flows.
4. **Contracts.** Any API surface change? For each: breaking or
   additive? Remember the standing rule: additive-only while old
   mobile binaries hold traffic — if the user proposes a breaking
   change, make them confront that rule out loud.
5. **Data.** New/changed entities? How does EXISTING production data
   map to the new semantics? "No migration needed" must be an explicit
   claim, not an omission.
6. **Region variance.** Anything that differs per region? Variance
   goes through the regions registry — never region branches in logic.
   (Skip if single-region.)
7. **Out of scope.** What will people assume is included that is NOT?
   Force at least one real exclusion; "nothing" is rarely true.
8. **Vocabulary.** Any new domain terms? They must be added to
   `product/glossary.md` in the PR that introduces them. Actively
   model, don't just record: when the user's language conflicts with
   the glossary, surface it ("the glossary says X, you seem to mean
   Y — which changes?"); when a term is fuzzy, stress-test it with an
   invented edge case ("is a cancelled-then-refunded order still a
   'sale'?") until its boundary is precise.

## Step 2 — write the artifact

- Follow `templates/spec-template.md` exactly, in
  `features/NNN-*/spec.md`, status `draft`.
- Acceptance criteria are keyed to S-numbers — every S-rule gets at
  least one named test; an S-rule with no test is a spec bug.
- Mark inferences `[ASSUMED]`; unresolved themes go to **Open
  questions** with a named owner (resolved before or during plan). If
  an owner isn't in this session, offer the questionnaire from the
  interview method.

## Step 3 — close

Show the draft and the list of affected capability docs (the shipping
PR must update them). The owner accepting the spec is the Stage 2
gate; next is a worktree + `/plan NNN` in plan mode. Do not start
planning or coding now.
