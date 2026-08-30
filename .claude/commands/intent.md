---
description: "Stage 1 — interview the owner, then start a new feature chain with intent.md"
argument-hint: "<short-name or a one-line description of the problem>"
---

Start a new feature chain (Stage 1 — Intent) for: $ARGUMENTS

You are helping the product owner think clearly about a problem BEFORE
anything is written. Do not draft `intent.md` until the interview below
is done. Run it per `.claude/interview-method.md` (read it first):
frontier rounds, a recommended answer with every question, facts
looked up rather than asked. The themes below are the question bank —
a sharp question now is cheaper than a wrong feature.

## Step 0 — context (before asking anything)

- Read `product/intent.md`, `product/personas.md`, and skim
  `product/capabilities/` and existing `features/*/intent.md`.
- Check `product/IDEAS.md`: if this graduates a parked idea, note
  which line — you'll delete it in Step 2. Nearby ideas that might
  belong to the same chain are worth mentioning to the user.
- If an existing chain or capability already covers this, say so and
  stop — don't create a duplicate chain.

## Step 1 — interview (the why)

Work through these themes. Skip a question only if the user's opening
description already answered it explicitly.

1. **Problem, not solution.** What is broken or missing today, and for
   whom (which persona from `product/personas.md`)? If the user
   describes a solution ("add a button that…"), push back: what problem
   does that solve? Record the problem in their answer's words.
2. **Evidence.** How do we know this is real — support tickets,
   metrics, an incident, a contract requirement, or just a hunch? A
   hunch is allowed but must be labeled as one.
3. **Why now.** What happens if we do nothing for six months? This
   surfaces urgency and exposes nice-to-haves.
4. **Outcome.** What is observably true after this ships? Behavior a
   test or a user could verify — not implementation. How would we know
   it worked (a metric, a stopped complaint)?
5. **Scope check.** Is this ONE unit of work? If the answers span
   multiple independent outcomes, propose splitting into separate
   chains now.
6. **Blast radius & constraints.** Which deployables/regions it
   touches; compliance, dependencies on other chains.
7. **Due date — real or wish?** If a deadline comes up, ask what
   makes it real: a contract, a regulation, a launch event? A real
   date goes in the intent's `Due:` field with its reason in
   Constraints. "As soon as possible" is a wish — the field stays
   "—" and nobody gets a fake date to miss.

## Step 2 — write the artifact

- Write in plain everyday language per `.claude/writing-style.md` —
  read it first. Keep the owner's own words for the problem; if you
  wouldn't say a sentence out loud to a teammate, rewrite it.
- Allocate the next feature number: highest `NNN` in `features/` + 1,
  zero-padded (numbers never reuse).
- Copy the structure of `templates/intent-template.md` into
  `features/NNN-short-name/intent.md`.
- Status: `draft`. Originator: the user. Date: today.
- The **Problem** section must state the evidence from Q2. Anything
  you inferred rather than heard, mark `[ASSUMED]`.
- Unresolved themes go under **Open questions** — never silently
  dropped, each with a named owner. If an owner isn't in this session,
  offer the questionnaire from the interview method.
- If this graduates a parked idea, delete its line from
  `product/IDEAS.md` now — the chain replaces it.

## Step 3 — close

Show the draft, remind the owner that accepting it (flipping status to
`accepted`) is the Stage 1 gate, and that the next step is `/spec NNN`.
Do NOT proceed to spec or code — that is a different stage with its own
gate.
