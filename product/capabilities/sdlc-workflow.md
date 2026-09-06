# SDLC workflow

Current template behavior as of main. These rules ship with the change
to the contributor workflow; they describe the template, not a product UI.

## Actors & permissions

- R1 Contributors start each proposal with a draft intent that states
  the problem, why it matters, and the desired outcome. They prepare
  intent and spec on an artifact branch and land accepted requirements
  through a reviewed PR before implementation.
- R2 Owners approve intent, spec, and plan; reviewers approve PRs.
  Status markers record these decisions but do not prove human approval.

## Rules

- R10 A feature change requires its committed accepted intent and spec
  and an approved plan for the same chain and phase.
- R11 A plan enters implementation history in an approved, plan-only
  commit. Code requires that plan to already be committed.
- R12 Local checks inspect staged and committed files. An untracked
  plan, staged approval, or sibling-phase plan cannot authorize code.
- R13 Unsupported branches, default-branch commits, detached local
  commits, and deletions or renames cannot skip plan checks.
- R14 Artifact branches only carry their allowed planning documents.
  The bootstrap branch has its own narrow document scope.
- R15 PR validation checks each commit since the merge base and requires
  a plan-only first implementation commit. PR history stays linear.
- R16 make test runs the template regression suite and syntax checks.
  Product repositories extend it with their own tests, lint, and build.
- R17 Contract changes require a dedicated contracts intent and a
  committed plan that declares packages/ in its touched surface.

## Lifecycle

Intent accepted → spec accepted → artifact PR merged → plan approved
and committed → implement → verify → human review → implementation PR merged.

## Edge cases

- R20 A later correction or revert does not hide an earlier PR history
  violation. The contributor corrects the branch history before review.
- R21 Missing required Git objects cause verification to fail.
- R22 A repository administrator configures required checks and human
  review. Local setup does not configure remote branch protection.

## Region availability

The template has no region-specific behavior.
