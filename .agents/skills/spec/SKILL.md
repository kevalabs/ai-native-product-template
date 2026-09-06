---
name: spec
description: Stage 2 of the feature loop — interviews the owner against an accepted intent, then drafts spec.md (flows, rules, states, permissions, errors, acceptance criteria) for a feature chain or one phase of it. Use when the user asks to spec, specify, or write requirements for feature NNN.
---

Draft the Stage 2 spec.

**Arguments:** the feature number `NNN` (or directory name), and for
multi-phase intents the phase `Pn`, given when this skill is
invoked. If the feature is missing, ask for it before anything else.

The spec answers WHAT. It turns an accepted intent (or one phase of
it) into flows, states, permissions, error paths, and numbered,
testable requirements that a person who knows the product can read
without knowing how it will be built. Your job is to force precision:
every vague answer becomes either a sharp S-rule or an open question.
Do not draft `spec.md` until the interview is done.

## Step 0 — gates and context

- Work on `artifact/NNN-short-name` in its own worktree. For a later
  phase, create a fresh artifact branch from the updated default branch.
  Resolve `features/NNN-*/`. Its `intent.md` must exist with status
  `accepted`. If it is still `draft`, stop and say the Stage 1 gate is
  not passed (the owner can accept it right now if they mean to).
- Read the intent's `## Phases`. If it lists phases and no `Pn` was
  given, ask which phase this spec is for and stop until answered.
  If it says "Single phase" and a `Pn` was given, say so and stop.
  - Single phase: the spec lives at `features/NNN-*/spec.md`.
  - Phase Pn: the spec lives at `features/NNN-*/Pn-short-name/spec.md`
    (create the directory; short-name from the intent's phase list).
    Read every sibling phase's spec that already exists — the shared
    ground the intent names (state names, terms, data ownership) is
    defined once, in the phase that introduces it; this spec cites
    it and must not redefine it. Check the phase's dependencies:
    warn if a phase it depends on has no accepted spec yet.
- Read the intent, `product/glossary.md`, `product/personas.md`,
  `product/regions.md` (if present), and every
  `product/capabilities/` doc the intent could touch. List for the
  user which capabilities you believe are affected and confirm.
- If `spec.md` already exists, switch to revising it — show what
  exists and ask what changed.

## Step 1 — interview (requirements before design)

Run the interview per `.agents/interview-method.md` (read it first):
frontier rounds, a recommended answer with every question, facts
looked up rather than asked. For every answer, apply the test: *could
someone write a failing test from this sentence?* If not, ask again
more narrowly. And the other test: *would a product person understand
it without knowing the code?* If not, it is plan material — park it
for `/plan`.

1. **Flows.** Walk the outcome (the phase's, or the intent's) one
   actor at a time: what they do, what they see, what happens next,
   step by step. Where a user story helps ("as a salon owner, I want
   …"), use it — but the flow is what gets specified, the story is
   just a way in.
2. **Behavior rules.** From the flows, extract rules in the form
   `<actor> can <action> when <condition>`. Probe the conditions —
   "always?", "which persona exactly?", "what if the precondition
   fails?". These become S1, S2, … Required information and
   validations are rules too ("S4 a business profile needs a legal
   name and a tax number before submission").
3. **States and transitions.** What states can the thing be in, who
   or what moves it, which states are final, and which transitions
   are forbidden? Multi-phase: if an earlier phase defined the state
   model, cite it and only add what this phase introduces.
4. **Permissions.** Who may do what, by persona — and what happens to
   someone who tries without permission.
5. **Errors and edge cases.** For every rule: what does the actor see
   when it fails? Expired codes, duplicate submissions, half-finished
   input, the thing deleted underneath them. Each answer is an S-rule.
6. **Collisions with today.** For each affected capability doc, do any
   existing R-rules change or conflict? A changed R-rule must appear
   explicitly in the spec.
7. **UX.** What must each screen/flow achieve (not how it looks)? Are
   mocks available to commit under this spec's `design/` directory?
   Low-fidelity is enough and worth having — it gives humans and
   agents the same picture. If none exist yet, record that as an
   open question — don't invent flows.
8. **Contracts.** Do other systems or clients see or do anything new?
   For each: breaking or additive? Remember the standing rule:
   additive-only while old mobile binaries hold traffic — if the user
   proposes a breaking change, make them confront that rule out loud.
   Shape and wire format are plan-level; here it is only what changes
   for whom.
9. **Data.** What must the product newly remember, or remember
   differently? How does EXISTING production data read under the new
   rules? "No existing data affected" must be an explicit claim, not
   an omission. Tables and migrations are plan-level.
10. **Region variance.** Anything that differs per region? Variance
    goes through the regions registry — never region branches in
    logic. (Skip if single-region.)
11. **Non-functional needs.** Where does this feature differ from the
    product-wide baselines in `product/architecture.md` standing
    rules? Probe: how fast (latency budget), how many (expected volume
    and peak), what when it breaks (degraded mode, retry, data loss
    tolerance), who may see it (privacy/permissions beyond the
    obvious). Each answer becomes a testable S-rule with a number in
    it — "under 300ms at 10k products", never "fast". Baseline is
    fine as an answer; only deviations go in the spec.
12. **Out of scope.** What will people assume is included that is NOT?
    Force at least one real exclusion; "nothing" is rarely true.
    Multi-phase: other phases' outcomes are out of scope by default —
    say so explicitly.
13. **Vocabulary.** Any new domain terms? They must be added to
    `product/glossary.md` in the PR that introduces them. Actively
    model, don't just record: when the user's language conflicts with
    the glossary, surface it ("the glossary says X, you seem to mean
    Y — which changes?"); when a term is fuzzy, stress-test it with an
    invented edge case ("is a cancelled-then-refunded order still a
    'sale'?") until its boundary is precise.

## Step 2 — write the artifact

- Write in plain everyday language per `.agents/writing-style.md` —
  read it first. S-rules name the actor and use concrete numbers and
  states ("within 14 days", "while the order is `delivered`"), never
  "appropriate" or "timely". Plain but still testable as written.
- Follow `templates/spec-template.md` exactly, at the path from
  Step 0, status `draft`. Fill the `Phase:` header.
- Acceptance criteria are keyed to S-numbers — every S-rule gets at
  least one named test; an S-rule with no test is a spec bug. This
  list is what review proves the PR against.
- If a table, endpoint, component, or service name slipped in, move
  it to **Open questions** addressed to `/plan` — the spec stays
  readable by product people.
- Mark inferences `[ASSUMED]`; unresolved themes go to **Open
  questions** with a named owner (resolved before or during plan). If
  an owner isn't in this session, offer the questionnaire from the
  interview method.

## Step 3 — close

Show the draft and the list of affected capability docs (the shipping
PR must update them). The owner accepting the spec is the Stage 2
gate. Commit the accepted intent and spec on the artifact branch and
land their reviewed PR. Then create the implementation worktree from
the updated default branch and use `plan` (`/plan NNN [Pn]`). A plan
never belongs in the artifact PR. Do not start coding at this stage.
