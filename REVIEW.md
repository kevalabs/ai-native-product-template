# PR Review Policy

Applied identically to every PR. Findings cite file:line and state
severity. Do not review formatting or style — linters own that.

## Passes (generic — keep)

1. **Correctness** — logic errors, unhandled edge cases, race
   conditions, broken error paths.
2. **Security** — injection, authorization gaps, secrets in the diff,
   unsafe handling of personal data.
3. **Spec compliance** — does the diff match this feature's committed
   `plan.md` and `spec.md`? Flag files touched that the plan never
   declared.

## Severity (generic — keep)

- **Blocking:** security findings, spec deviations, any
  product-specific rule below.
- **Comment-only:** improvement suggestions with working alternatives.
- Do not raise speculative findings you cannot ground in the diff.

## Process checks (generic — keep)

- Behavior change without a matching update to the capability doc in
  `product/capabilities/`.
- Changes under `packages/` without a linked contracts intent in the
  PR description.
- Test files modified in a bug-fix PR — flag for human attention.
- Breaking (non-additive) change to a client-facing contract while
  old client versions hold traffic (mobile apps especially).

## {{PRODUCT_NAME}}-specific checks (blocking — bootstrap fills this)

<!-- template: derive from the product's constitution. Examples from
     a prior product: PII in logs; float money; naive datetimes in
     scheduling; region branching outside the regions registry;
     platform-proprietary APIs in the portable core. -->
- {{PRODUCT_SPECIFIC_CHECKS}}

## Non-goals (generic — keep)

- Formatting, import order, naming taste on working code.
- Rewrites of code the plan didn't touch.
