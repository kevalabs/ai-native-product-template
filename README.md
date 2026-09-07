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

1. Create a new repo with GitHub's "Use this template", then clone it.
   Keep its initial template commit as the base for the bootstrap PR.
2. Run `make setup`, then create a bootstrap worktree:
   `git worktree add ../wt-bootstrap -b artifact/bootstrap`.
   Open your coding agent there — Claude Code, Codex,
   Antigravity, or Gemini CLI — and say: **"bootstrap this
   product"** — the bootstrap skill interviews the product owner,
   generates the constitution (`product/`), fills every
   `{{PLACEHOLDER}}`, and deletes itself.
3. Review the drafts, correct the `[ASSUMED]` sections, and land them
   through a reviewed bootstrap PR. That closes the founding intent.
4. Require `SDLC history`, `Template verification`, and human review
   in branch protection. Git, Make, and Python 3.9+ run the template
   checks. Extend `make test` with the product's tests, lint, and build
   when introducing its stack. The template checks remain in place.

## 1. Read this first (in this order)

| # | File | What it tells you |
|---|------|-------------------|
| 1 | `product/intent.md` | Why the product exists: problem, outcome, constraints |
| 2 | `product/glossary.md` | The vocabulary. Use these words exactly — in code, schemas, APIs, tests |
| 3 | `product/personas.md` | Who we build for, including internal operators |
| 4 | `product/regions.md` | Market/region model (absent if single-region) |
| 5 | `product/architecture.md` | Target layout + the numbered standing rules every decision cites |
| 6 | `AGENTS.md` | How agent sessions must work in this repo — read by every coding agent |
| 7 | `REVIEW.md` | What every PR is judged against (blocking checks included) |
| 8 | `docs/agentic-sdlc.md` | The process model behind section 3 — why → what → how → build → prove → ship, phases, human gates |

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
                       Big intents split into phases: NNN-name/Pn-name/
                       holds that phase's spec, design/, and plan.
                       Immutable once shipped — this is the history.
templates/             copy these to start any artifact:
                       intent, spec, plan, capability
docs/agentic-sdlc.md   the process model this loop implements
                       (why → what → how → build → prove → ship)
AGENTS.md              agent conventions — the one file every coding
                       agent reads (CLAUDE.md, GEMINI.md, and
                       .agents/rules/ just point at it)
.agents/               skills (the stage commands, one SKILL.md each)
                       + the interview and writing-style method docs.
                       Read natively by Codex, Antigravity, Gemini
                       CLI; .claude/skills is a symlink to it
.githooks/             git hooks that check branches, artifact scope,
                       and committed plans for every agent and human
apps/                  one directory per AUDIENCE — a singular domain
                       core plus one frontend (+ bff/) per audience,
                       and docs/ generated from product/ + features/
packages/              shared contracts, domain types, region registry —
                       changed through dedicated contracts chains
Makefile               make setup installs hooks; make test verifies
                       the template (extend for the product's stack)
scripts/               shared SDLC validator and template verification
tests/                 workflow regression tests in temporary Git repos
.github/workflows/     template verification and PR history checks
```

<!-- template: bootstrap replaces the apps/ line with the product's
     real audience directories, one line each. -->

### Which agent reads what

The process is agent-neutral: one conventions file, one skills
directory, one set of git hooks. Nothing in the loop depends on a
particular tool.

| Agent | Conventions | Skills | Invoke a stage |
|-------|-------------|--------|----------------|
| Claude Code | `CLAUDE.md` → imports `AGENTS.md` | `.claude/skills` (symlink to `.agents/skills`) | `/intent`, `/spec 007` … |
| Codex | `AGENTS.md` | `.agents/skills` | `$intent`, `$spec 007` … |
| Antigravity | `AGENTS.md` + `.agents/rules/` | `.agents/skills` | name the skill: "run the spec skill for 007" |
| Gemini CLI | `GEMINI.md` → imports `AGENTS.md` | `.agents/skills` | name the skill, or `/skills` |

Every agent also picks a skill on its own when the request matches
its description, so "spec feature 007" works everywhere. If your
platform can't follow the `.claude/skills` symlink (some Windows
setups), replace it with a copy and keep the two in sync.

## 3. How a feature gets built (the loop)

Every unit of work starts with a draft Intent explaining the problem
and desired outcome. One outcome is one numbered feature directory;
large outcomes have fixed phases in the accepted Intent.

```
Intent → Spec → Plan → Build → Test + Review → Ship
   Each arrow requires approved artifacts committed and a reviewed PR merged.
```

| Command | Produces | Entry gate |
|---|---|---|
| `/intent` | intent.md and Intent parent issue | Proposed outcome |
| `/spec NNN [Pn]` | spec.md | Accepted Intent PR merged |
| `/plan NNN [Pn]` | plan.md, alone in its PR | Accepted Spec PR merged |
| `/build NNN [Pn]` | build.md, code, tests, capabilities | Approved Plan PR merged |
| `/proof NNN [Pn]` | proof.md | Reviewed Build PR merged |
| `/ship NNN [Pn]` | ship.md | Passing Proof PR merged |

The parent issue has type Intent; stage sub-issues have type Task. Each
issue links to its governing Markdown and each new artifact links back.
Completed tasks record approved commit permalinks and merged PRs, so
branch deletion never removes the review record. Small implementation
tasks cite the relevant Spec requirement or Plan section. The parent
stays open until every phase ships and the Intent success criteria hold.

Start each stage worktree from the updated default branch. Run the live
entry gate before drafting or executing the next stage:

```sh
git fetch --prune origin
make handoff REPO=owner/repo ISSUE=123 BASE=origin/main
```

Use the real stage task. Its predecessor must be merged and approved;
a local commit, open PR, closed issue, or board status cannot unlock it.
Read [.githooks/README.md](.githooks/README.md) for branch names and the
full tracking record. The stage skills retain their owner interviews.
Explicit conversation approval is recorded before merge, without asking
for the same approval again. Plan is approved before its first commit.

Build includes tests, lint, and build verification before merge. The
separate Proof stage names the exact merged Build, tests every Spec
rule, checks the Intent, and records human review and remaining findings.
Ship requires merged passing proof and successful delivery evidence.
For this template, delivery is the approved version on the default
branch; a release tag is optional. A Build merge alone does not close
the parent outcome. Cancelled work is never counted as shipped.

`/capability` updates current behavior in the Build PR, stating any
remaining release restrictions. `/feature` reports stage and the next
missing gate. `/product-status` gives stakeholder status based on actual
artifacts, links, merges, and shipment evidence. Neither report advances
work or treats a status label as proof.

Run `make setup` once per clone and `make test` before handoff. Run
`make setup-check REPO=owner/repo` to inspect issue types and required
remote policy. An administrator configures SDLC history, Template
verification, human review, and renewed approval after changes. Local
setup does not install those settings. A recorded, owner-selected
`intent` label fallback is available where custom types are unavailable.

Shipped feature directories are immutable. Incidents and later behavior
changes start new intents linking back to the original outcome.


## 4. Rules you will hit on day one

The full numbered list with reasons is in `product/architecture.md` —
these are the ones that bite newcomers:

- Never commit to `main` — everything lands by reviewed PR. Run
  `make setup` once per clone. Use a separate artifact PR for each requirements stage
  and feature branches for implementation. See `.githooks/README.md`
  for allowed paths and the exact automated checks.
- Contract changes use their own `Kind: contracts` intent and declare
  `packages/` in the plan's Touched surface section.
- Money = integer minor units + currency code; never floats. Domain
  times carry an explicit IANA timezone (see `AGENTS.md`).
- No region branching in business logic — variance lives in the
  region registry only. (If multi-region.)
- Personal data never goes in logs, errors, or analytics events.
- All user-facing strings externalized (i18n) from the first commit.
- Client-facing contracts are additive while old client versions hold
  traffic — mobile releases ride store review, not our deploys.

<!-- template: bootstrap trims/extends this digest to match the
     product's actual AGENTS.md and standing rules. -->

## 5. Regions & deployment in one paragraph

{{REGIONS_AND_DEPLOYMENT: one paragraph — region model, hosting per
region, build-once-deploy-many, affected-only CI, and any shared
Kevalabs platform services consumed (e.g. the Ledger for financial
truth). Details: product/regions.md, product/architecture.md. Delete
the regions sentence if single-region.}}

## 6. Where to ask "what does the product do today?"

`product/capabilities/` — always current, rule-numbered (R1, R10…) so
specs, tests, and reviews cite them. History: `features/` + git log.
Future: draft intents describe proposed work; accepted intents describe
committed work. Never trust memory over these files — and if you
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
