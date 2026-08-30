# AI-Native Product Development Template

<!-- template: this README is the newcomer's map. Bootstrap retitles
     it to the product name, replaces the placeholders, and deletes
     the "How to instantiate" section; everything else survives into
     the product. -->

{{ONE_PARAGRAPH: what the product is, its audiences/surfaces, and its
markets/regions.}}

This repo runs on the **AI-native SDLC**: every change flows through
committed artifacts, agents build under committed rules, and humans
judge intent, risk, and policy — not every line. If you are new, this
file is your map; read it top to bottom once.

## How to instantiate (template only — delete after bootstrap)

1. Create a new repo from this template ("Use this template" on
   GitHub, or copy the tree and `git init`).
2. Open Claude Code in the new repo and say: **"bootstrap this
   product"** — the bootstrap skill interviews the product owner,
   generates the constitution (`product/`), fills every
   `{{PLACEHOLDER}}`, and deletes itself.
3. Review the drafts, correct the `[ASSUMED]` sections, and make the
   first commit. That commit closes Stage 1.

## 1. Read this first (in this order)

| # | File | What it tells you |
|---|------|-------------------|
| 1 | `product/intent.md` | Why the product exists: problem, outcome, constraints |
| 2 | `product/glossary.md` | The vocabulary. Use these words exactly — in code, schemas, APIs, tests |
| 3 | `product/personas.md` | Who we build for, including internal operators |
| 4 | `product/regions.md` | Market/region model (absent if single-region) |
| 5 | `product/architecture.md` | Target layout + the numbered standing rules every decision cites |
| 6 | `CLAUDE.md` | How agent sessions must work in this repo |
| 7 | `REVIEW.md` | What every PR is judged against (blocking checks included) |

`product/` is the **constitution** — slow-changing, always true.
Don't skip it: agents load these files as context, and so should you.

## 2. Repository map

```
product/               the constitution (files above)
product/capabilities/  CURRENT shipped behavior, one file per capability.
                       Present tense only. Updated ONLY by the PR that
                       changes the behavior. Start here to learn what
                       the product does today.
features/              append-only ledger of change chains:
                       NNN-name/{intent,spec,plan}.md + design/ (mocks).
                       Immutable once shipped — this is the history.
                       BACKLOG.md is the idea inbox: raw ideas wait
                       there until /intent graduates them to a chain.
templates/             copy these to start any artifact:
                       intent, spec, plan, capability
.claude/               skills (advisory knowledge) + hooks (hard blocks)
apps/                  one directory per AUDIENCE — a singular domain
                       core plus one frontend (+ bff/) per audience,
                       and docs/ generated from product/ + features/
packages/              shared contracts, domain types, region registry —
                       FROZEN to feature branches (see standing rules)
Makefile               make test = the whole verification loop
```

<!-- template: bootstrap replaces the apps/ line with the product's
     real audience directories, one line each. -->

## 3. How a feature gets built (the loop)

Every unit of work — new feature, change to shipped behavior, incident
fix — is a numbered chain in `features/`. Never skip a stage.

Each stage has a slash command in Claude Code. Every command
interviews you *before* generating its artifact — the questions are
the point: the artifact only has value if a human thought through the
problem, and the answers (evidence, alternatives rejected, exclusions)
are recorded in it.

| Command | Stage | Produces |
|---------|-------|----------|
| `/idea <one line>` | 0 | a line in `features/BACKLOG.md` — no interview, ten-second capture |
| `/intent <name>` | 1 | `features/NNN-name/intent.md` |
| `/spec NNN` | 2 | `spec.md` |
| `/plan NNN` | 3 | `plan.md` (first commit on the branch) |
| `/capability NNN` | 5 | updated `product/capabilities/` doc, same PR |
| `/feature [NNN]` | — | the product board: done / promised / proposed / ideas |
| `/product-status [save]` | — | stakeholder report: every feature with status, dates, dependencies, open questions |

### One feature end to end (worked example)

Say customers keep emailing support to undo an order. The moment the
thought occurs, park it — no interview, no number:

```
> /idea customers keep emailing support to undo orders — some way to refund?
```

That's one line in `features/BACKLOG.md`. Days later, when it's worth
doing, graduate it. In Claude Code, on `main`:

```
> /intent refund-requests
```

Claude checks no existing chain or capability already covers refunds,
then interviews you — what's broken and for whom, what evidence
(support tickets? metrics? a hunch?), why now, what's observably true
after shipping — and writes `features/007-refund-requests/intent.md`.
You edit until it's right, flip its status to `accepted`. Gate passed.

```
> /spec 007
```

Refuses to run if the intent is still `draft`. Then turns your answers
into numbered, testable rules ("S1 A customer can request a refund
while the order is `delivered` and within 14 days"), confronts you
with conflicting capability rules, and forces a real "out of scope"
list. Accept `spec.md` the same way.

```bash
git worktree add ../wt-007 -b feature/007-refund-requests
```

```
> /plan 007        # in the worktree, in plan mode
```

Stops if you're on `main`. Offers 2–3 implementation approaches and
records why the losers lost, lists every file the work will touch
(checked against other in-flight plans for collisions), then commits
`plan.md` as the first commit on the branch. Build follows in the
same worktree until `make test` is green.

```
> /capability 007  # on the feature branch, before opening the PR
```

Converts the *shipped* S-rules — and only those — into present-tense
R-rules in `product/capabilities/refunds.md`, in the same PR (review
blocks behavior changes without this).

```
> /feature
```

Any time you come back cold, or anyone asks "what does the product
do, and what's coming?": one board, four sections — ✅ done (from
`product/capabilities/`), 🔨 promised (accepted chains in flight),
🤔 proposed (draft intents), 💡 ideas (backlog). It also flags
anything unhealthy (code on a branch with no committed plan, spec
questions still open at plan stage).

```
> /product-status
```

The same facts, written for people *outside* the repo: one table with
every feature's status (Proposed / Committed / In build / In review /
Shipped), started, due, and completed dates, dependencies, and open
questions — plus a "needs a decision" list naming who owes which
answer. Everything is computed from the artifacts and git history, so
it is never stale: started = the intent's date, completed = the merge
that shipped it, due = the intent's `Due:` field (set only when
someone committed to a real date — a chain past its due date is
flagged in the opening summary). `/product-status save` also writes
the report to `reports/status-YYYY-MM-DD.md` for sharing.

**Stage 1 — Intent.** Run `/intent <short-name>`. The interview makes
you state the problem and outcome, not the solution, and records the
evidence; the result is `features/NNN-short-name/intent.md` (manual
path: copy `templates/intent-template.md`). Product owner accepts it.

**Stage 2 — Spec.** Run `/spec NNN` with the intent accepted. The
interview extracts testable S-rules and collisions with current
capabilities into `spec.md`. Mocks are exported into the feature's
`design/` folder and referenced from the spec. Product owner resolves
flags, accepts.

**Stage 3 — Plan, then build.**

```bash
git worktree add ../wt-NNN -b feature/NNN-short-name
```

Open Claude Code there **in plan mode** and run `/plan NNN`.
Iterate until the plan is right — including the exact list of files it
will touch (checked against other in-flight plans for collisions).
Commit `plan.md` as the **first commit on the branch**, then implement.
No code before a committed plan.

**Stage 4 — Verify.** `make test` (tests, lint, build) must pass
before handoff — the agent fixes its own failures. Bug fixes write the
failing test *first*, and never edit an existing test to make it pass.

**Stage 5 — PR and review.** Push, open a PR linking the feature
directory. AI review runs `REVIEW.md` (correctness, security, spec
compliance — undeclared file changes are blocking). If your change
alters behavior, the same PR must update the matching
`product/capabilities/` doc (run `/capability NNN`) — review blocks
it otherwise. A human
approves; merge deletes the branch; remove the worktree.

**Stage 6 — Maintain.** Monitoring findings and incidents re-enter the
loop as *new* intents in `features/`. Shipped chains are never edited.

## 4. Rules you will hit on day one

The full numbered list with reasons is in `product/architecture.md` —
these are the ones that bite newcomers:

- Never commit to `main` — everything lands by reviewed PR.
- Don't edit `packages/` from a feature branch — contracts change
  through their own chain.
- Money = integer minor units + currency code; never floats. Domain
  times carry an explicit IANA timezone (see `CLAUDE.md`).
- No region branching in business logic — variance lives in the
  region registry only. (If multi-region.)
- Personal data never goes in logs, errors, or analytics events.
- All user-facing strings externalized (i18n) from the first commit.
- Client-facing contracts are additive while old client versions hold
  traffic — mobile releases ride store review, not our deploys.

<!-- template: bootstrap trims/extends this digest to match the
     product's actual CLAUDE.md and standing rules. -->

## 5. Regions & deployment in one paragraph

{{REGIONS_AND_DEPLOYMENT: one paragraph — region model, hosting per
region, build-once-deploy-many, affected-only CI, and any shared
Kevalabs platform services consumed (e.g. the Ledger for financial
truth). Details: product/regions.md, product/architecture.md. Delete
the regions sentence if single-region.}}

## 6. Where to ask "what does the product do today?"

`product/capabilities/` — always current, rule-numbered (R1, R10…) so
specs, tests, and reviews cite them. History: `features/` + git log.
Future: raw ideas in `features/BACKLOG.md`, vetted work in open
intents. Never trust memory over these files — and if you
learn a fact the files don't state, adding it is part of your PR.

## Status

<!-- template: bootstrap sets this. Convention: state the phase
     plainly — pre-first-commit / constitution accepted / first
     feature chain in flight — and name the next gate. -->

{{STATUS}}

## License

This template is [CC0-1.0](LICENSE) — public domain. Take the method,
no attribution required. **Products created from this template are NOT
covered by this license**: the bootstrap skill removes the inherited
`LICENSE` file so your product starts with its own licensing (all
rights reserved by default).
