# Architecture — target layout and standing rules

**Status:** TEMPLATE. This records decisions and their reasons; the
layout is a destination, not commit one.

## Target layout

<!-- template: adapt. The invariant ideas: apps named by AUDIENCE, one
     singular domain core, contracts in packages/, artifacts beside
     code. -->

```
{{repo}}/
├── AGENTS.md               # agent conventions, read by every agent
│                           # (CLAUDE.md / GEMINI.md point here)
├── REVIEW.md               # PR review policy
├── product/                # constitution + capabilities/
├── features/               # append-only ledger of change chains
├── templates/              # artifact templates
├── docs/                   # process reference (agentic-sdlc.md)
├── .agents/                # skills + method docs (advisory),
│                           # read natively by Codex/Antigravity/
│                           # Gemini; .claude/skills symlinks here
├── .githooks/              # git hooks (enforced, every agent)
├── apps/                   # one directory per AUDIENCE
│   ├── core/               # the one domain API
│   ├── {{audience}}/       # frontend (+ bff/ when extracted)
│   └── docs/               # docs site rendering product/ + features/
├── packages/               # shared contracts, domain types, regions
└── Makefile                # make test / make deploy REGION=…
```

## Platform services (cross-product, outside this repo)

<!-- template: shared Kevalabs services this product consumes, e.g.
     the Ledger (Rust, own repo, per-region): core posts entries and
     queries balances via versioned API — never keeps local financial
     truth. -->

## Standing rules

<!-- template: candidates proven on prior products — keep, adapt, or
     delete with reasons. Numbered so PRs and reviews can cite them.
     Product-wide non-functional baselines belong here too —
     availability target, latency budget, accessibility standard,
     data retention — each with a number in it, so specs only state
     deviations and reviews can cite the rule. Bootstrap asks for
     these. -->

1. **Single language inside this repo** unless an intent chain states
   the forcing problem. (AI removes the cost of writing a second
   language, not of operating one: toolchains, CI, governance ×N.)
2. **Portability by construction.** Plain containers + vanilla
   database; no platform-proprietary APIs in `apps/core`.
3. **BFF belongs to its frontend** — one consumer, changes as a unit
   with its UI. The only multi-consumer contract lives in `packages/`.
4. **Contracts change serially, features in parallel.** `packages/`
   changes need their own intent with `Kind: contracts` and a plan
   that declares `packages/` in Touched surface. The hook and CI
   check those declarations; reviewers check the actual boundary.
5. **Critical invariants are database guarantees** (unique
   constraints, transactions) — not application-level checks.
6. **Client-facing contracts are additive** while old client versions
   hold traffic.
7. **Docs are generated, never hand-authored HTML.** Markdown is the
   reviewed source; `apps/docs` renders manual (capabilities) +
   changelog (features).
8. **One agent, one worktree, one branch.** Every stage starts from
   the updated default branch after its predecessor PR merges. Intent,
   Spec, and Plan each land separately; Build requires the merged
   approved Plan. Proof and Ship have their own evidence PRs. Review
   checks that the Build diff matches the approved touched surface.
9. **Apps are named by audience.** Adding an audience adds a
   directory, never a restructure. `core` stays singular.
10. **The repo is the unit of truth, never the unit of deployment.**
    CI builds/deploys only what a diff affects, computed from the
    workspace dependency graph — not naive path filters.
11. **Build once, deploy many.** SHA-tagged images; a region deploy
    points a region at a SHA; rollback = re-point. A versioned
    manifest records which SHA runs where.
12. **Mobile releases are a separate lane** (store review, own
    cadence) — the standing reason for rule 6.

## Build order (first chains)

<!-- template: 1. the ONE feature that proves the core loop
     2. minimal operator slice needed to onboard the first customer
     3. extractions (BFFs) when needs diverge
     4. apps/docs once there are artifacts to render -->

## Deployment (per region)

CI builds container images once; `make deploy REGION=…` targets the
region's host. Deploy/rollback/status are exposed to agents as tools
(Make targets / MCP with scoped tokens) — agents never hold raw
platform credentials. Preview environments per PR where the platform
supports it.
