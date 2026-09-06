# Start every proposal with intent — Plan

**Status:** approved
**Spec:** [spec.md](spec.md)
**Phase:** single phase
**Branch:** feature/002-intent-first

## Approach

Carry out the owner's request to remove the idea command and begin all
proposals with intent. Delete the empty inbox and skill, remove their
branch exceptions, and use draft intents for proposed-work reporting.
Keep the existing stages and approval gates. A replacement inbox would
retain the extra entry point the owner asked to remove.

Stack this local implementation branch on the requirements branch for
review. The artifact PR lands first; the implementation PR then targets
main. This plan is the first implementation commit and contains no code.

## Touched surface (collision check)

No other in-flight plans exist. Create, modify, or delete only:

- features/002-intent-first/plan.md
- .agents/skills/idea/SKILL.md
- .agents/skills/intent/SKILL.md
- .agents/skills/feature/SKILL.md
- .agents/skills/product-status/SKILL.md
- .githooks/README.md
- AGENTS.md
- README.md
- product/IDEAS.md
- product/capabilities/sdlc-workflow.md
- scripts/check_sdlc.py
- tests/test_sdlc.py

## Steps

1. Replace the obsolete idea-branch permission test with tests for the
   requested rejection behavior; add local and PR coverage for removing
   the inbox exception. Demonstrate these fail before changing the code.
2. Remove the skill, empty inbox, validator exceptions, and current
   documentation/report references. Update the existing capability rules.
3. Run make test, inspect the complete diff, and search current guidance
   for stale entry points. Validate both branch histories before handoff.

## Migrations

The inbox contains no proposals. Git retains the deleted files and
shipped feature 001 remains untouched. No production data changes.

## Test plan

S1–S2: review current guidance and command files, including the Claude
skills symlink, and search for stale references. S3–S4: local and PR
checks reject the removed branch and numbered-branch inbox exception.
The old permission test changes because this request changes behavior.
S5: run the complete make test suite, retaining all unrelated assertions.

## Rollout

Review the artifact PR first, then the implementation PR. No remote
settings or new dependencies are needed. Update the existing SDLC
capability doc in the implementation PR.

## Verification evidence

- Both new rejection tests failed against the old permissions before
  changing the validator.
- make test passes all 34 tests plus the template syntax and whitespace
  checks. Local and PR validation reject the removed entry points.
- Active guidance has no command, inbox, branch, or graduation references.
  The skill is also absent through the Claude skills symlink.
- All 12 implementation files match the touched-surface list. Shipped
  feature 001 is unchanged; its references remain part of the history.
- The artifact history and plan-only implementation history validate
  against their intended bases.
