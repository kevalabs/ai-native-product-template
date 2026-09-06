# Reliable SDLC gates — Plan

**Status:** approved
**Spec:** [spec.md](spec.md)
**Phase:** single phase
**Branch:** feature/001-sdlc-enforcement

## Approach

Implement the four fixes authorized by the user's “improve the gaps”
request after the review. Keep accepted requirements on an artifact
branch; stack the implementation branch on that commit for local work.
The artifact PR must land before the implementation PR targets main.

Use one Python standard-library validator from the shell hook and CI.
Read Git's index and committed objects rather than working-tree plan
files. Resolve the exact chain and phase, verify status markers, and
check that the first implementation commit contains only its plan.
Replay each PR commit so a later correction cannot hide an earlier bypass.

Allow narrowly scoped artifact branches for numbered requirements,
bootstrap documents, and the idea inbox. Require feature branches for
all implementation, including executable governance files. Keep review
responsible for actual human approval and semantic spec compliance.

A shell-only validator was rejected because robust path handling and
history tests are harder to maintain. Separate hook and CI logic was
rejected because their rules would drift. No third-party dependencies.

## Touched surface (collision check)

No other feature plans exist. This change creates or modifies:

- .githooks/pre-commit
- .githooks/README.md
- scripts/check_sdlc.py
- scripts/verify_template.py
- tests/test_sdlc.py
- Makefile
- .github/workflows/verify.yml
- .gitignore
- AGENTS.md
- README.md
- REVIEW.md
- docs/agentic-sdlc.md (repository mapping only)
- features/README.md
- templates/intent-template.md
- templates/plan-template.md
- .agents/skills/intent/SKILL.md
- .agents/skills/spec/SKILL.md
- .agents/skills/plan/SKILL.md
- .agents/skills/idea/SKILL.md
- .agents/skills/bootstrap-product/SKILL.md
- .agents/skills/feature/SKILL.md
- .agents/skills/product-status/SKILL.md
- product/architecture.md
- product/glossary.md
- product/capabilities/sdlc-workflow.md
- features/001-sdlc-enforcement/plan.md

## Steps

1. Commit this plan alone, then write regression tests and demonstrate
   that the existing hook fails them before changing enforcement code.
2. Implement the shared validator, hook, verification entry point, and
   PR workflow. Run the meaningful branch, index, and history cases.
3. Update the handoff instructions and capability rules. Run make test,
   validate both branch histories, and review the diff against this list.

## Migrations

No production migration. Existing history stays intact. New PR checks
start at the PR's merge base. Feature branches keep linear history and
rebase on main; the reviewed merge may still be squashed.

## Test plan

Use isolated temporary Git repositories with local fixture identities.
S1: artifact allowlist. S2: missing/draft/untracked/wrong-phase plans and
accepted requirements. S3: first plan-only commit and bundled code.
S4: default/unsupported/detached branches, deletion, rename, and unusual
filenames. S5: valid and invalid PR histories. S6: make test, syntax
checks, setup, and hook invocation. S7: compare docs with enforcement.
Write the reproduced bypass tests first and retain their expectations.

## Rollout

Merge the artifact PR first, then review and merge implementation.
Run make setup per clone. Repository administrators require the SDLC
and template verification jobs plus human review on the default branch.
Future product bootstraps extend make test with their tests, lint, and
build. No remote settings are changed by this implementation.

## Verification evidence

- Before changing enforcement, the original hook failed 20 of the 30
  initial workflow tests, including all five bypasses from the review.
- After the changes, make test passes all 33 regression tests, shell
  syntax, whitespace checks, and Python syntax/entry-point checks.
- S1: artifact scope, idea scope, and bootstrap scope tests pass.
- S2: draft, untracked, staged approval, missing spec, and exact/sibling
  phase tests pass.
- S3: first-plan-only, bundled code, and late approval history tests pass.
- S4: unsupported/default/detached branches, deletion, rename, and
  newline-filename tests pass.
- S5: valid history and bypass-then-revert history tests pass. Both
  local branches validate against their intended predecessor.
- S6: make setup installs a hook that blocks an actual invalid commit
  in a disposable repository. Missing Git history fails explicitly.
- S7: conventions, README, skills, hook guide, and capability rules were
  checked against the validator. The workflow YAML parses successfully.
- The touched-file list covers the complete implementation diff.

The requirements branch is artifact/001-sdlc-enforcement; implementation
is stacked on its accepted requirements commit. Review and merge that
artifact PR first, then rebase the implementation commits onto main if
needed. Remote Actions runs and branch-protection settings have not been
verified. No application build is claimed by the template checks.
