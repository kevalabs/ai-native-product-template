---
name: plan
description: Stage 3 of the feature loop — interviews on implementation approach and touched files, then drafts plan.md as the first commit on the feature branch. Use when the user asks to plan feature NNN, is on a feature branch with an accepted spec and no plan, or wants to start building.
---

Draft the Stage 3 implementation plan.

**Arguments:** the feature number `NNN` (or directory name), and for
multi-phase intents the phase `Pn`, given when this skill is
invoked. If the feature is missing, ask for it before anything else.

Work in your agent's read-only planning mode if it has one. Either
way: edit no code until `plan.md` is approved and committed.

The plan answers HOW — this is where tables, endpoints, components,
and services finally belong. `plan.md` is the first commit on the
feature branch — no code before it. Your job is to make the
implementation strategy and its full blast radius explicit BEFORE any
code exists, and to record why this approach won over the
alternatives.

## Step 0 — gates and context

- Resolve `features/NNN-*/` and the phase: single-phase chains plan
  at `features/NNN-*/plan.md`; phase `Pn` plans at
  `features/NNN-*/Pn-short-name/plan.md`. If the intent lists phases
  and no `Pn` was given, ask which and stop.
- The reviewed artifact PR must have landed the accepted intent and
  this directory's accepted spec on the default branch. Check committed
  objects, not just local files. If they have not landed, prepare that
  artifact PR before starting the implementation branch.
- That directory's `spec.md` must exist with status `accepted`; if
  not, stop — Stage 2 gate not passed. Multi-phase: if this phase
  depends on a phase that hasn't shipped, say so — planning may
  proceed, but the build must wait for or stub the dependency, and
  the plan must say which.
- Check the current branch: work must happen on
  `feature/NNN-short-name` (or `feature/NNN-Pn-short-name`) in its
  own worktree, never `main`. If needed, create the worktree from the
  updated default branch with
  `git worktree add ../wt-NNN[-Pn] -b feature/NNN[-Pn]-short-name main`
  and continue there. Preserve unrelated local edits.
- Read the spec, the intent (outcome and success criteria — the plan
  serves those, not just the S-rules), `product/architecture.md`
  (standing rules), and every OTHER in-flight plan (chains or phases
  with a plan but no shipped capability update), sibling phases of
  this intent included — you need their touched-surface lists for
  the collision check.
- If `plan.md` already exists on this branch, revise instead of
  recreating.

## Step 1 — interview (design decisions, out loud)

Run the interview per `.agents/interview-method.md` (read it first):
frontier rounds, a recommended answer with every question, facts
looked up rather than asked.

1. **Approach.** Propose 2–3 implementation strategies with real
   trade-offs and ask the user to choose (a multiple-choice question,
   per the interview method). The plan
   records the chosen approach AND the rejected alternatives with the
   reason — future readers need the why, not just the what.
2. **Touched surface.** Enumerate every app/package/file this will
   create or modify. Walk the spec S-rule by S-rule to catch stragglers
   (i18n files, capability doc, glossary, migrations, test files).
   The merged diff must match this list — undeclared changes are a
   blocking review finding.
   - If anything lands in `packages/`, this must be its own contracts
     chain with `Kind: contracts` in the accepted intent, and the plan
     must declare `packages/` under Touched surface. Otherwise split
     the contract work into its own chain or avoid the contract change.
   - Report overlaps with other in-flight plans' touched surfaces and
     ask how to sequence around them. Sibling phases running in
     parallel that touch the same files are a sign the intent's
     shared ground wasn't settled — say so.
   - **Reviewability check.** Look at the list as a reviewer would:
     can one human read this whole diff in one sitting and judge it?
     If it spans several unrelated areas or would run to thousands
     of lines, stop and propose splitting the phase (a revision to
     the intent's `## Phases`) before planning further. Optimise for
     a review someone can trust, not for how much an agent can
     produce.
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

- Write in plain everyday language per `.agents/writing-style.md` —
  read it first. The Approach section should read like you're
  explaining the decision to a teammate at a whiteboard: what we're
  doing, why, and what we turned down.
- Follow `templates/plan-template.md` at the path from Step 0, with
  the `Phase:` and `Branch:` headers filled, status `approved` only
  after the user approves it in review.
- Once approved, commit it as the FIRST commit on the branch (nothing
  else in that commit).

## Step 3 — close

After the plan commit, implementation may start — in this same
session if the user says go. Restate the handoff bar: `make test`
green, every spec S-rule named against the test that proves it, the
outcome from the intent checked by hand once more, diff matches the
touched-surface list, capability docs updated in the same PR.
