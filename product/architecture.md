# Architecture — target layout and standing rules

**Status:** TEMPLATE. This records decisions and their reasons; the
layout is a destination, not commit one.

## Target layout

<!-- template: adapt. The invariant ideas: apps named by AUDIENCE, one
     singular domain core, contracts in packages/, artifacts beside
     code. -->

```
{{repo}}/
├── CLAUDE.md               # agent conventions (root)
├── REVIEW.md               # PR review policy
├── product/                # constitution + capabilities/
├── features/               # append-only ledger of change chains
├── templates/              # artifact templates
├── .claude/                # skills (advisory) + hooks (enforced)
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
     delete with reasons. Numbered so PRs and reviews can cite them. -->

1. **Single language inside this repo** unless an intent chain states
   the forcing problem. (AI removes the cost of writing a second
   language, not of operating one: toolchains, CI, governance ×N.)
2. **Portability by construction.** Plain containers + vanilla
   database; no platform-proprietary APIs in `apps/core`.
3. **BFF belongs to its frontend** — one consumer, changes as a unit
   with its UI. The only multi-consumer contract lives in `packages/`.
4. **Contracts change serially, features in parallel.** `packages/`
   is frozen to feature branches (hook-enforced).
5. **Critical invariants are database guarantees** (unique
   constraints, transactions) — not application-level checks.
6. **Client-facing contracts are additive** while old client versions
   hold traffic.
7. **Docs are generated, never hand-authored HTML.** Markdown is the
   reviewed source; `apps/docs` renders manual (capabilities) +
   changelog (features).
8. **One agent, one worktree, one branch.** No direct commits to
   main; plan.md is the first commit; merged diff matches the plan.
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
