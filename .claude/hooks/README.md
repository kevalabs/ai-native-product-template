# Hooks — deterministic enforcement

Populated per product. The two hooks every instance should configure
first (in `.claude/settings.json`):

1. **Protect main** — block `git commit`/`git push` targeting the
   default branch; work lands via PR only.
2. **Freeze contracts** — block edits under `packages/` from feature
   branches (contract changes come through their own intent chain).

Skills advise; hooks enforce. Anything REVIEW.md treats as blocking
and a machine can detect deterministically belongs here too.
