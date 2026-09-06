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
2. Open your coding agent in the new repo — Claude Code, Codex,
   Antigravity, or Gemini CLI — and say: **"bootstrap this
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
| 6 | `AGENTS.md` | How agent sessions must work in this repo — read by every coding agent |
| 7 | `REVIEW.md` | What every PR is judged against (blocking checks included) |
| 8 | `docs/agentic-sdlc.md` | The process model behind section 3 — why → what → how → build → prove → ship, phases, human gates |

`product/` is the **constitution** — slow-changing, always true.
(One deliberate exception: `product/IDEAS.md`, the fast-changing
idea inbox — see the map below.) Don't skip it: agents load these
files as context, and so should you.

## 2. Repository map

```
product/               the constitution (files above)
product/IDEAS.md       the idea inbox — any raw product thought, not
                       just features. The ONE fast-changing file in
                       product/: ideas wait here until /intent
                       graduates them to a chain (or a commit deletes
                       them, with the why in the message).
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
.githooks/             git hooks that enforce the hard rules for every
                       agent and human (git config core.hooksPath)
apps/                  one directory per AUDIENCE — a singular domain
                       core plus one frontend (+ bff/) per audience,
                       and docs/ generated from product/ + features/
packages/              shared contracts, domain types, region registry —
                       FROZEN to feature branches (see standing rules)
Makefile               make test = the whole verification loop
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

Every unit of work — new feature, change to shipped behavior, incident
fix, refactor, infrastructure — is a numbered chain in `features/`.
The chain is the same six questions every time, and the model behind
it is written up in `docs/agentic-sdlc.md`:

```
WHY        WHAT       HOW        BUILD       PROVE            SHIP
intent  →  spec   →   plan   →   code    →   make test     →  PR merges,
                                             + REVIEW.md      capability
                                                              doc updated
```

Never skip a stage. A human approves each artifact before the next
begins: the intent (including how it is cut into phases), the spec,
the plan, and finally the PR. Agents do the drafting, building,
testing, and self-review in between; humans judge at the gates.

Chains are cut by **outcome**, never by page, screen, or task. "Add
staff CRUD" is a task; "a salon owner can add the staff needed to run
the salon" is an outcome. When one outcome is too big to review in
one PR, the intent lists **phases** — each phase is one reviewable
capability with its own spec, plan, branch, and PR under the same
intent directory. Phases that don't depend on each other can run in
parallel, one agent per worktree, once the intent's shared ground
(state names, terms, data ownership, contracts) is settled.

Each stage is a skill in `.agents/skills/`, invoked by name in
whichever agent you use (the `/name` form below is Claude Code's;
Codex uses `$name`, others take the name in plain words — see "Which
agent reads what"). Every skill interviews you *before* generating
its artifact — the questions are the point: the artifact only has
value if a human thought through the problem, and the answers
(evidence, alternatives rejected, exclusions) are recorded in it.

| Skill | Stage | Produces |
|-------|-------|----------|
| `/idea <one line>` | 0 | a line in `product/IDEAS.md` — no interview, ten-second capture |
| `/intent <name>` | 1 | `features/NNN-name/intent.md` — outcome, actors, success criteria, phases |
| `/spec NNN [Pn]` | 2 | `spec.md` (per chain, or per phase) |
| `/plan NNN [Pn]` | 3 | `plan.md` (first commit on the branch) |
| `/capability NNN [Pn]` | 5 | updated `product/capabilities/` doc, same PR |
| `/feature [NNN]` | — | the product board: done / promised / proposed / ideas |
| `/product-status [save]` | — | stakeholder report: every feature with status, dates, dependencies, open questions |

### One feature end to end (worked example)

Say customers keep emailing support to undo an order. The moment the
thought occurs, park it — no interview, no number:

```
> /idea customers keep emailing support to undo orders — some way to refund?
```

That's one line in `product/IDEAS.md`. Days later, when it's worth
doing, graduate it. In your agent, on `main`:

```
> /intent refund-requests
```

The agent checks no existing chain or capability already covers refunds,
then interviews you — what's broken and for whom, what evidence
(support tickets? metrics? a hunch?), why now, who acts and who
benefits, what's observably true after shipping, and whether it fits
one PR or needs phases — and writes
`features/007-refund-requests/intent.md`. You edit until it's right,
flip its status to `accepted`. Gate passed — including the phase
split, if any.

(Had this been bigger — say "a customer can request, a support agent
can approve, and the money comes back" — the intent would list
`P1-request`, `P2-approve`, `P3-payout`, and every command below
would take the phase too: `/spec 007 P1`, `/plan 007 P1`, branch
`feature/007-P1-request`. Same gates, same files, one directory per
phase.)

```
> /spec 007
```

Refuses to run if the intent is still `draft`. Then turns your answers
into flows, states, permissions, error paths, and numbered testable
rules ("S1 A customer can request a refund while the order is
`delivered` and within 14 days"), confronts you with conflicting
capability rules, and forces a real "out of scope" list. Nothing
about tables or endpoints — anyone who knows the product can read
it. Accept `spec.md` the same way.

```bash
git worktree add ../wt-007 -b feature/007-refund-requests
```

```
> /plan 007        # in the worktree, before any code
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
🤔 proposed (draft intents), 💡 ideas (the inbox). It also flags
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

**Stage 1 — Intent (why).** Run `/intent <short-name>`. The
interview makes you state the problem and outcome, not the solution,
records the evidence, names the actors and success criteria, and
proposes phases if the outcome is too big for one PR; the result is
`features/NNN-short-name/intent.md` (manual path: copy
`templates/intent-template.md`). Product owner accepts it — and with
it the phase split.

**Stage 2 — Spec (what).** Run `/spec NNN` (or `/spec NNN Pn` for
one phase) with the intent accepted. The interview extracts flows,
states, permissions, error paths, testable S-rules, and collisions
with current capabilities into `spec.md`. Mocks are exported into the
feature's `design/` folder and referenced from the spec. No
implementation detail — that is the plan's job. Product owner
resolves flags, accepts.

**Stage 3 — Plan (how), then build.**

```bash
git worktree add ../wt-NNN -b feature/NNN-short-name
# or, for one phase:
git worktree add ../wt-NNN-P1 -b feature/NNN-P1-short-name
```

Open your agent there — in its **read-only planning mode** if it has
one — and run the `plan` skill (`/plan NNN [Pn]`).
Iterate until the plan is right — including the exact list of files it
will touch (checked against other in-flight plans, sibling phases
included, for collisions). If the plan won't fit one reviewable PR,
go back and split the phase. Commit `plan.md` as the **first commit
on the branch**, then implement. No code before a committed plan.

**Stage 4 — Prove.** `make test` (tests, lint, build) must pass
before handoff — the agent fixes its own failures. Bug fixes write the
failing test *first*, and never edit an existing test to make it pass.
Green tests are not the bar: the agent then walks the spec's
acceptance criteria and says which S-rule each test proves, and
reads the intent's outcome once more to check the work actually
delivers it.

**Stage 5 — PR and review.** Push, open a PR linking the feature (or
phase) directory. AI review runs `REVIEW.md` (correctness, security,
spec compliance, outcome — undeclared file changes are blocking).
The two review questions, in order: *did we build what the spec
said?* and, on the last phase, *did this achieve the intent?* If your
change alters behavior, the same PR must update the matching
`product/capabilities/` doc (run `/capability NNN [Pn]`) — review
blocks it otherwise. A human approves; merge deletes the branch;
remove the worktree.

If you track work in GitHub issues, mirror the chain, not the tasks:
one issue per intent titled by its outcome ("a salon owner can add
the staff needed to run the salon", never "add staff CRUD"), one
sub-issue per phase, and a PR per plan linking its phase directory.
Milestones group intents by release. Task checklists live inside the
phase issue, not as issues of their own.

**Stage 6 — Maintain.** Monitoring findings and incidents re-enter the
loop as *new* intents in `features/`. Shipped chains are never edited.

## 4. Rules you will hit on day one

The full numbered list with reasons is in `product/architecture.md` —
these are the ones that bite newcomers:

- Never commit to `main` — everything lands by reviewed PR. Run
  `git config core.hooksPath .githooks` once so the hook stops you
  (and your agent) before you try.
- Don't edit `packages/` from a feature branch — contracts change
  through their own chain.
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
Future: raw ideas in `product/IDEAS.md`, vetted work in open
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
