# PR Review Policy

Applied identically to every PR. Findings cite file:line and state
severity. Do not review formatting or style — linters own that.

## Passes (generic — keep)

1. **Correctness** — logic errors, unhandled edge cases, race
   conditions, broken error paths.
2. **Security** — injection, authorization gaps, secrets in the diff,
   unsafe handling of personal data.
3. **Spec compliance** — does the diff match this feature's committed
   `plan.md` and `spec.md`? Walk the spec's acceptance criteria: each
   S-rule has a test in the diff that proves it, or the finding says
   which does not. Flag files touched that the plan never declared.
4. **Outcome** — does the PR deliver the phase's outcome as stated in
   the intent's `## Phases` (or, single phase, the intent's
   `## Outcome`)? On the last phase of an intent, walk the intent's
   `## Success criteria` and say which are now true. Code that passes
   its tests but leaves the outcome unmet is a finding.

## Severity (generic — keep)

- **Blocking:** security findings, spec deviations, any
  product-specific rule below.
- **Comment-only:** improvement suggestions with working alternatives.
- Do not raise speculative findings you cannot ground in the diff.

## Process checks (generic — keep)

- Verify actual owner approval of intent, spec, and plan. Markdown
  status values alone are not approval evidence.
- Confirm the accepted intent/spec artifact PR landed before the
  implementation branch. `SDLC history` and `Template verification`
  must pass. Inspect changes to the workflow, validator, and tests:
  a PR can change its own checks, so a green job is not enough.
- For artifact PRs, review only the permitted planning scope and the
  relevant human gates; there is no implementation plan yet.
- Require these jobs and human review through branch protection.
  The repository files cannot install or attest remote settings.

- Behavior change without a matching update to the capability doc in
  `product/capabilities/`.
- Changes under `packages/` without a linked contracts intent in the
  PR description.
- Test files modified in a bug-fix PR — flag for human attention.
- PR too large to review meaningfully in one sitting, or touching
  several unrelated areas — flag for human attention: the phase
  needs splitting, not a longer review.
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
