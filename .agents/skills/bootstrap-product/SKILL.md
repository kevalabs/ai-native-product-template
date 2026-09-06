---
name: bootstrap-product
description: Instantiate this product template — interview the product owner, then generate the product constitution (intent, glossary, personas, regions, architecture) and fill all template placeholders. Use when the user asks to bootstrap, initialize, set up, or start a new product in a repo created from the Kevalabs product template.
---

# Bootstrap a new product from this template

You are running Stage 1 of the AI-native SDLC for a brand-new product.
The repo was created from the Kevalabs product template; files contain
`{{PLACEHOLDER}}` markers and `<!-- template: … -->` instructions.

Start in an `artifact/bootstrap` worktree from the default branch.
Create it if needed before editing; never commit the constitution on
main. This branch allows founding documents only, not code or CI.

## 1. Interview the product owner

Ask conversationally (not as a form), and follow up on what they say.
You need, minimally:

1. **Product name** and one-line description.
2. **Problem** — what's broken today, for whom, how do they know?
3. **Users** — every audience, including internal operators. Each
   audience becomes an `apps/` directory and a persona.
4. **Outcome & success metrics** — what's true in 6–12 months?
5. **Markets/regions** — single or multi-region? Which first?
   (Currency, timezone, payment/SMS providers, residency per region.)
6. **Constraints** — team, budget, platform preferences, compliance,
   stack opinions, shared Kevalabs services to consume (e.g. the
   Ledger for financial truth).
7. **Deployables** — web/mobile/API; mobile implies the additive-
   contracts rule and a separate release lane.
8. **Non-functional baselines** — how available ("down for an hour on
   Sunday night — who cares?"), how fast (a latency budget users
   would notice breaking), accessibility standard, data retention.
   Each answer needs a number in it; each becomes a standing rule in
   `product/architecture.md` so specs only state deviations.

Don't interrogate past usefulness: draft with explicit `[ASSUMED]`
markers where answers are thin — the owner corrects drafts faster
than they answer questionnaires.

## 2. Generate the constitution

Rewrite each `product/` file from its template, following the
inline `<!-- template -->` instructions, in this order:

1. `product/intent.md` — problem, outcome, users, constraints, open
   questions. Constraints state WHY.
2. `product/glossary.md` — resolve noun synonyms explicitly (pick one
   canonical term per concept). Keep the Process section verbatim.
3. `product/personas.md` — one per audience; deferred personas noted.
4. `product/regions.md` — fill per region, or DELETE if single-region
   (also remove region rules from AGENTS.md and REVIEW.md).
5. `product/architecture.md` — layout with real audience names; keep,
   adapt, or delete each candidate standing rule WITH the reason.

## 3. Fill the governance files

- `AGENTS.md` — replace `{{PRODUCT_NAME}}`; keep generic workflow
  rules verbatim; keep/adapt/delete candidate code rules; add rules
  specific to this product's constraints. Leave `CLAUDE.md`,
  `GEMINI.md`, and `.agents/rules/` alone — they only point here.
- `REVIEW.md` — same; derive the product-specific blocking checks
  from the constitution (every hard constraint should have a matching
  review check).
- `README.md` — it is already the newcomer's guide; retitle the H1 to
  the product name, fill the `{{PLACEHOLDERS}}` (product paragraph,
  apps/ map lines, regions & deployment paragraph, status), delete the
  "How to instantiate" section, and trim the day-one rules digest to
  match this product's actual rules.

## 4. Finish

- Verify no `{{PLACEHOLDER}}` or `<!-- template -->` markers remain
  anywhere (grep for `{{` and `template:`).
- Delete `.agents/skills/bootstrap-product/` — the instance doesn't
  carry the bootstrap skill; it lives only in the template.
- Run `make setup` to install the hook and `make test` to verify the
  template. Keep the existing Makefile, validator, tests, and CI.
- Record that the first implementation chain introducing the stack
  must extend `make test` with product tests, lint, and build. Bootstrap
  does not silently treat the template checks as an application build.
- Tell the owner to require `SDLC history`, `Template verification`,
  and human review in default-branch protection. These remote settings
  are not installed by `make setup`.
- Check for an inherited `LICENSE` file: the template's license does
  NOT apply to the product. Delete it (proprietary default) or replace
  it with the product's own license — ask the owner.
- Tell the owner: review the `[ASSUMED]` sections, then land the
  constitution through a reviewed bootstrap PR. Each product feature
  starts its own intent/spec artifact PR, then its implementation branch.
  Preserve existing feature numbers; allocate the next unused number.
