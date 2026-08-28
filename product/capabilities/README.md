# Capabilities — current behavior of the product

One file per capability (see `templates/capability-template.md`).
Each describes what the shipped product does **today**, as of `main`:

- Behavior, rules, states, and edge cases — not implementation.
- Rules are numbered (R1, R10…) so specs, tests, and review findings
  can cite them.
- Region availability noted where a feature flag differs.
- Updated **only** inside the PR that changes the behavior — never
  edited directly. REVIEW.md blocks behavior changes that skip the
  capability-doc update.

History lives in `features/` (the append-only ledger) and git.
Future behavior lives in intents and specs. This directory is only
ever the present tense.
