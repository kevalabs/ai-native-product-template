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

**Stage 1 — Intent.** Copy `templates/intent-template.md` to
`features/NNN-short-name/intent.md`. State the problem and outcome,
not the solution. Product owner accepts it.

**Stage 2 — Spec.** Draft `spec.md` from the template with Claude,
attaching the intent + relevant `product/capabilities/` docs. Mocks
are exported into the feature's `design/` folder and referenced from
the spec. Product owner resolves flags, accepts.

**Stage 3 — Plan, then build.**

```bash
git worktree add ../wt-NNN -b feature/NNN-short-name
```

Open Claude Code there **in plan mode** with `spec.md` attached.
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
`product/capabilities/` doc — review blocks it otherwise. A human
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
Future: open intents. Never trust memory over these files — and if you
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
