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
- For work adopting the prototype step, use the
  [shared review rules](docs/agentic-sdlc.md#prototype-before-spec).
  Before Spec, require every applicable prototype form, successful named
  cases, the exact committed version, and attributable owner confirmation.
  Check retained-ref reachability, evidence access, age acceptance when
  needed, and byte-for-byte preserved examples. Missing evidence or a
  different commit blocks acceptance. The alternative is a concrete
  owner-accepted skip for nothing meaningful to inspect, not an empty demo.
  Do not demand retroactive confirmation for existing accepted Specs.
- Prototype code has no automated product tests or coverage gate. Reject
  prototype tests and any real personal data or production secrets.
  Build tests must load the confirmed examples file unchanged; altered
  cases require renewed confirmation or an accepted Spec revision.
  Prototype code and its working note never merge into the product.
- Read the `Delivery` setting in `AGENTS.md` before judging evidence.
  For `merged source`, the Build record must carry a PASS for every
  Spec S-rule naming a test that exists, and say which Intent success
  criteria the phase makes true; judge whether each named test actually
  proves its rule, because the check only proves the name is real.
  Shipment is a `shipped/` tag on the merged Build commit; a moved or
  retargeted tag is a blocking finding. For `runtime artifact`, check
  the immutable artifact's identity and originating merged Build commit
  in Proof, then require Ship to deliver that same artifact. A mismatch
  blocks Proof; an unavailable artifact or a required rebuild prevents
  successful Ship. Optional previews do not replace this evidence.
- Every Build PR needs a current approving review from someone other
  than its author, whoever merges it. That review is the Test + Review
  step. A self-approved PR, or a protection bypass used in place of a
  separate PR authoring identity, is a blocking finding.
- Confirm each predecessor stage has its own approved, merged PR
  before the next stage starts. Plan must already be merged before
  Build. A dependent phase starts only after its predecessor phase is
  shipped: a `shipped/` tag for merged source, a merged Ship PR for a
  runtime artifact. Verify the exact phase and the approved artifact permalink.
  `SDLC history` and `Template verification` must pass. Inspect changes to the workflow, validator, and tests:
  a PR can change its own checks, so a green job is not enough.
- For planning PRs, review only the current stage and its human gate.
  Intent, Spec, and Plan must not share one PR. Check that explicit
  conversation approval is recorded before merge; do not request it
  again or confuse a ready-for-review PR with artifact acceptance.
- Verify issue-to-artifact links and backlinks, exact completed
  versions, stage dependencies, and the parent staying open until Ship.
  A merged-source outcome tracks Intent, Spec, Plan, and Build tasks;
  an untracked stage's task is closed as not planned and unlocks nothing.
  Check every proof result and shipment evidence; generated PASS text
  and a human merge alone do not prove independent review or success.
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
