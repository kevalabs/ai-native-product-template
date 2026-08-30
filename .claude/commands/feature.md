---
description: "Show feature-chain status — which stage each chain is at and what gate is next"
argument-hint: "[NNN — omit to list all chains]"
---

Report feature-chain status for: $ARGUMENTS (all chains if empty).

This is a read-only status command — it never creates or edits
artifacts. A feature is a unit of change: one numbered directory in
`features/`, immutable once shipped.

For each chain in scope, inspect `features/NNN-*/` and report:

1. **Stage reached.**
   - `intent.md` missing → not a chain yet.
   - intent `draft` → Stage 1 open; gate: owner accepts intent.
   - intent `accepted`, no/`draft` spec → Stage 2; gate: owner accepts
     spec (`/spec NNN` to draft or revise).
   - spec `accepted`, no plan → Stage 3; gate: worktree +
     `/plan NNN` in plan mode.
   - plan committed → building/in review; gate: `make test` green,
     PR merged with capability docs updated.
   - Shipped (check: does a `product/capabilities/` doc reflect the
     spec's rules, and is the branch merged in `git log`?) →
     immutable. Any further change is a NEW chain that links back.
2. **Health flags**, if any: spec open questions still unresolved at
   plan stage; a branch `feature/NNN-*` existing with code commits but
   no committed plan.md (rule violation); touched-surface overlaps
   between in-flight plans; a shipped chain whose capability doc was
   never updated.

When listing all chains, start with one line for the backlog: how
many ideas are waiting in `features/BACKLOG.md` (with the oldest
one's date — a stale inbox is worth noticing).

Output one line per chain — number, name, stage, next gate — then
detail only the chains with health flags. With a specific NNN, give
the full picture of that chain including its open questions.

Point the user at the right next command (`/intent`, `/spec NNN`,
`/plan NNN`, `/capability NNN`) instead of offering to do the next
stage's work here.
