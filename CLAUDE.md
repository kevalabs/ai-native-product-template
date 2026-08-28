# {{PRODUCT_NAME}} — Agent Conventions

<!-- template: if this file still contains {{PLACEHOLDER}} markers,
     stop and tell the user to run the bootstrap-product skill. -->

Read `product/intent.md` for what this product is. Every feature is
built from a committed artifact chain in `features/NNN-name/`:
`intent.md` → `spec.md` → `plan.md` → code. Do not write feature code
without an approved `plan.md` in that feature's directory.

## Workflow rules (generic — keep)

- Never commit directly to `main`. All work happens on a
  `feature/NNN-name` branch in its own worktree; changes land via
  reviewed PR only.
- Start every feature session in plan mode with the feature's `spec.md`
  attached. `plan.md` (including the list of files/apps it will touch)
  is the first commit on the branch.
- Verify before handoff: `make test` (tests, lint, build) must pass.
  Never hand off failing work.
- Bug fixes: write the failing test first. Never edit an existing test
  to make it pass.
- Behavior changes update the matching `product/capabilities/` doc in
  the same PR.
- New domain vocabulary is added to `product/glossary.md` in the PR
  that introduces it.

## Code rules (product-specific — bootstrap fills this)

<!-- template: candidate rules that apply to most commerce/SaaS
     products — keep, adapt, or delete during bootstrap: -->
- Money is integer minor units + ISO currency code. No float
  arithmetic on money.
- Domain times carry an explicit IANA timezone. Never use server-local
  time for domain logic.
- Personal data never appears in logs, error messages, or analytics
  events.
- All user-facing strings are externalized (i18n) — no hardcoded copy.
- Region variance goes through the regions registry and provider
  interfaces only — business logic must not branch on region codes.
  (Delete if single-region.)
- `packages/` is contract territory: changes there require their own
  intent chain, not drive-by edits from feature branches.
- {{PRODUCT_SPECIFIC_RULES}}
