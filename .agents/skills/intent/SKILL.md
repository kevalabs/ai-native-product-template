---
name: intent
description: Stage 1 of the feature loop — interviews the product owner about a problem, then starts a new feature chain by writing features/NNN-name/intent.md (why, outcome, actors, success criteria, phases). Use when the user wants to start a feature, open an intent, or graduate an idea from product/IDEAS.md.
---

Start a new feature chain (Stage 1 — Intent).

**Arguments:** a short name, or a one-line description of the
problem, given when this skill is invoked. If none was given, ask
for it in one line before anything else.

You are helping the product owner think clearly about a problem BEFORE
anything is written. Do not draft `intent.md` until the interview below
is done. Run it per `.agents/interview-method.md` (read it first):
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
   test or a user could verify — not implementation. State it as one
   sentence someone can do or a state the system reaches ("a new
   salon owner can finish setup and get approved before going live"),
   never as work ("build the onboarding pages").
5. **Actors and success criteria.** Who acts and who benefits —
   personas, plus "the system" where it acts alone. Then three to
   six lines a person could check after the last PR merges: how
   would we know it worked (a metric, a stopped complaint, a thing
   someone can now do)? These are what the final review is judged
   against.
6. **Scope and phases.** Is this ONE outcome? If the answers span
   several *independent* outcomes, propose separate chains. If it is
   one outcome that several actors or state changes carry (owner
   registers → owner sets up → operator approves → system activates),
   propose **phases** — each one capability a human can review in one
   PR, cut by outcome, actor, or state transition, never by page or
   screen. Name each phase's actor and what it depends on; say which
   could run in parallel. Then name the shared ground those parallel
   phases need settled first (state names, terms, who owns which
   data, contracts in `packages/`) and where each will be defined.
   Most chains are a single phase — don't invent phases for a small
   outcome. The owner accepting the intent accepts this split.
7. **Blast radius & constraints.** Which deployables/regions it
   touches; compliance, dependencies on other chains.
8. **Due date — real or wish?** If a deadline comes up, ask what
   makes it real: a contract, a regulation, a launch event? A real
   date goes in the intent's `Due:` field with its reason in
   Constraints. "As soon as possible" is a wish — the field stays
   "—" and nobody gets a fake date to miss.

## Step 2 — write the artifact

- Write in plain everyday language per `.agents/writing-style.md` —
  read it first. Keep the owner's own words for the problem; if you
  wouldn't say a sentence out loud to a teammate, rewrite it.
- Allocate the next feature number: highest `NNN` in `features/` + 1,
  zero-padded (numbers never reuse).
- Copy the structure of `templates/intent-template.md` into
  `features/NNN-short-name/intent.md`.
- Status: `draft`. Originator: the user. Date: today.
- The **Problem** section must state the evidence from Q2. Anything
  you inferred rather than heard, mark `[ASSUMED]`.
- **Phases**: write "Single phase" unless Q6 produced a split. For a
  split, list `P1-short-name`, `P2-…` with actor, outcome, and
  dependencies, then the shared-ground list. Phase numbers are fixed
  once the intent is accepted — later phases get their own
  `features/NNN-*/Pn-short-name/` directory when their spec starts.
- No implementation detail anywhere in the intent: if a screen,
  table, or endpoint crept in, move it to open questions for the spec
  or plan.
- Unresolved themes go under **Open questions** — never silently
  dropped, each with a named owner. If an owner isn't in this session,
  offer the questionnaire from the interview method.
- If this graduates a parked idea, delete its line from
  `product/IDEAS.md` now — the chain replaces it.

## Step 3 — close

Show the draft, remind the owner that accepting it (flipping status to
`accepted`) is the Stage 1 gate — it also fixes the phase split — and
that the next step is `/spec NNN` (or `/spec NNN P1` for the first
phase).
Do NOT proceed to spec or code — that is a different stage with its own
gate.
