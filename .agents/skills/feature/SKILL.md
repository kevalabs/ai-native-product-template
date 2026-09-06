---
name: feature
description: The product board — reports what is shipped, promised, proposed, and just an idea, plus the stage and health of each feature chain. Read-only. Use when the user asks what the product does, what is in flight, where feature NNN stands, or what the next step for a chain is.
---

Report product status.

**Arguments:** optionally a feature number `NNN`, given when this
skill is invoked. With no argument, show the whole board.

This is a read-only status command — it never creates or edits
artifacts. It computes everything live from the files, so it is
always current: `product/capabilities/` for what's done, `features/`
for what's promised, `product/IDEAS.md` for what's just an idea.

For each chain in scope, inspect `features/NNN-*/` and report:

1. **Stage reached.**
   - `intent.md` missing → not a chain yet.
   - intent `draft` → Stage 1 open; gate: owner accepts intent.
   - intent `accepted`, no/`draft` spec → Stage 2; gate: owner accepts
     spec (`/spec NNN` to draft or revise).
   - spec `accepted`, no plan → Stage 3; gate: worktree +
     `/plan NNN`.
   - plan committed → building/in review; gate: `make test` green,
     PR merged with capability docs updated.
   - Shipped (check: does a `product/capabilities/` doc reflect the
     spec's rules, and is the branch merged in `git log`?) →
     immutable. Any further change is a NEW chain that links back.

   Multi-phase intents (the intent's `## Phases` lists `Pn` entries):
   apply the same ladder to each `features/NNN-*/Pn-*/` directory and
   report the chain as "phase k of n shipped, Pm at <stage>". A phase
   with no directory yet is "not started". The chain is shipped only
   when every phase is.
2. **Health flags**, if any: spec open questions still unresolved at
   plan stage; a branch `feature/NNN-*` existing with code commits but
   no committed plan.md (rule violation); touched-surface overlaps
   between in-flight plans (sibling phases included); a shipped chain
   whose capability doc was never updated; a phase being built while
   a phase it depends on has no accepted spec; an intent accepted
   more than a month ago with phases still not started.

With no argument, output the board in four sections — done first,
because "what does the product do today" is the most common question:

1. **✅ Done (shipped)** — one line per `product/capabilities/` doc:
   capability name + a one-sentence plain-language summary of what it
   does. This is what the system provides today.
2. **🔨 Promised (in flight)** — chains with an accepted intent that
   haven't shipped: number, name, stage, next gate. An accepted
   intent is a commitment; this is what the system will provide.
3. **🤔 Proposed (draft)** — chains whose intent is still `draft`:
   someone is thinking about it, nothing is promised yet.
4. **💡 Ideas** — how many lines wait in `product/IDEAS.md`, with
   the oldest one's date (a stale inbox is worth noticing). List the
   lines themselves only if there are ten or fewer.

After the board, detail only the chains with health flags. With a
specific NNN, skip the board and give the full picture of that chain
including its open questions.

Point the user at the right next command (`/intent`, `/spec NNN`,
`/plan NNN`, `/capability NNN`) instead of offering to do the next
stage's work here.
