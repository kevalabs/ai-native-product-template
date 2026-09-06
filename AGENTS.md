# {{PRODUCT_NAME}} — Agent Conventions

This is the one conventions file for every coding agent working in
this repo. Codex, Antigravity, and Gemini CLI read it directly;
`CLAUDE.md` and `GEMINI.md` are one-line pointers to it; Antigravity
also gets a pointer in `.agents/rules/`. Skills (the stage commands)
live in `.agents/skills/`, which every agent reads (`.claude/skills`
is a symlink to it). Edit this file, never the pointers.

Read `product/intent.md` for what this product is. Every feature is
built from a committed artifact chain in `features/NNN-name/`:
`intent.md` (why) → `spec.md` (what) → `plan.md` (how) → code →
proof → ship. The model behind it is `docs/agentic-sdlc.md`. Do not
write feature code without an approved `plan.md` in that feature's
(or phase's) directory.

## Workflow rules (generic — keep)

- Never commit directly to `main`. All work happens on a
  `feature/NNN-name` branch (or `feature/NNN-Pn-name` for one phase
  of a multi-phase intent) in its own worktree; changes land via
  reviewed PR only.
- Work is cut by outcome, never by page or task. An intent too big
  for one reviewable PR is split into phases in its `intent.md`;
  each phase has its own `spec.md`, `plan.md`, branch, and PR under
  `features/NNN-name/Pn-name/`.
- Start every feature session with the feature's `spec.md` in
  context, in your agent's read-only planning mode if it has one.
  `plan.md` (including the list of files/apps it will touch) is the
  first commit on the branch; edit no code before it is committed.
- Keep the spec free of implementation: tables, endpoints, and
  components belong in `plan.md`. The spec's acceptance criteria are
  what tests and review prove against.
- Verify before handoff: `make test` (tests, lint, build) must pass.
  Never hand off failing work.
- Bug fixes: write the failing test first. Never edit an existing test
  to make it pass.
- Behavior changes update the matching `product/capabilities/` doc in
  the same PR.
- New domain vocabulary is added to `product/glossary.md` in the PR
  that introduces it.
- All artifacts (intent, spec, plan, capability docs) are written in
  plain everyday language — see `.agents/writing-style.md`. Glossary
  terms used exactly; everything else in words you'd say out loud.
- The hard rules above are enforced by `.githooks/pre-commit` and CI,
  not by any one agent's hook system. Run
  `git config core.hooksPath .githooks` once per clone.

## Code rules (product-specific — bootstrap fills this)

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
