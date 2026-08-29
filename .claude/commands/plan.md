---
description: "Stage 3 — interview on approach and touched surface, then draft plan.md (first commit on the feature branch)"
argument-hint: "<NNN or feature directory name>"
---

Draft the Stage 3 implementation plan for feature: $ARGUMENTS

`plan.md` is the first commit on the feature branch — no code before
it. Your job is to make the implementation strategy and its full blast
radius explicit BEFORE any code exists, and to record why this
approach won over the alternatives.

## Step 0 — gates and context

- Resolve `features/NNN-*/`. `spec.md` must exist with status
  `accepted`; if not, stop — Stage 2 gate not passed.
- Check the current branch: work must happen on `feature/NNN-short-name`
  in its own worktree, never `main`. If on `main`, give the user the
  `git worktree add ../wt-NNN -b feature/NNN-short-name` command and
  stop until they're in the worktree.
- Read the spec, `product/architecture.md` (standing rules), and every
  OTHER in-flight chain's `plan.md` (chains with a plan but no shipped
  capability update) — you need their touched-surface lists for the
  collision check.
- If `plan.md` already exists on this branch, revise instead of
  recreating.

## Step 1 — interview (design decisions, out loud)

Run the interview per `.claude/interview-method.md` (read it first):
frontier rounds, a recommended answer with every question, facts
looked up rather than asked.

1. **Approach.** Propose 2–3 implementation strategies with real
   trade-offs and ask the user to choose (AskUserQuestion). The plan
   records the chosen approach AND the rejected alternatives with the
   reason — future readers need the why, not just the what.
2. **Touched surface.** Enumerate every app/package/file this will
   create or modify. Walk the spec S-rule by S-rule to catch stragglers
   (i18n files, capability doc, glossary, migrations, test files).
   The merged diff must match this list — undeclared changes are a
   blocking review finding.
   - If anything lands in `packages/`, stop: contracts are frozen to
     feature branches and need their own chain. Make the user decide —
     split a contract chain out, or redesign to avoid it.
   - Report overlaps with other in-flight plans' touched surfaces and
     ask how to sequence around them.
3. **Steps.** Cut the work as tracer bullets: each step is a narrow
   VERTICAL slice through every layer it needs (schema → domain → API
   → UI → tests) that is demoable on its own — not "all models, then
   all endpoints, then all UI". Order steps by their blocking edges
   (which steps genuinely gate which), every step ends with
   `make test` passing, and the first slice should prove the riskiest
   assumption from the approach discussion. Bug-fix rule applies:
   failing test before fix.
   - Exception — a wide mechanical change (rename, contract shape,
     mass migration) uses expand–contract instead: add the new form
     alongside the old, migrate call sites in batches with CI green,
     remove the old form last.
4. **Migrations.** Ordering and reversibility; what is the rollback if
   the deploy halts mid-way?
5. **Tests.** Map every spec S-number to the test(s) that prove it,
   and which tests are written first.
6. **Rollout.** Feature flags, region order, and the capability-doc
   update (which files, in this same PR).

## Step 2 — write and commit

- Write in plain everyday language per `.claude/writing-style.md` —
  read it first. The Approach section should read like you're
  explaining the decision to a teammate at a whiteboard: what we're
  doing, why, and what we turned down.
- Follow `templates/plan-template.md` in `features/NNN-*/plan.md`,
  status `approved` only after the user approves it in review.
- Once approved, commit it as the FIRST commit on the branch (nothing
  else in that commit).

## Step 3 — close

After the plan commit, implementation may start — in this same
session if the user says go. Restate the handoff bar: `make test`
green, diff matches the touched-surface list, capability docs updated
in the same PR.
