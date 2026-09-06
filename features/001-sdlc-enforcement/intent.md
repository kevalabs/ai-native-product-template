# Reliable SDLC gates — Intent

**Status:** accepted
**Originator:** Suraj Chhetry
**Date:** 2026-09-06
**Due:** —
**Kind:** change

## Problem

The repository review reproduced five ways to commit code without the
right approved plan. The worked example also leaves accepted intent and
spec files on main without a way to transfer them into a worktree.
The advertised verification command and CI checks do not exist.

## Outcome

A contributor can take approved requirements through an artifact PR,
then build in a feature worktree with plan checks that also run in CI.

## Actors

- The owner accepts the outcome, requirements, and implementation scope.
- Contributors and coding agents prepare artifacts, code, and evidence.
- Reviewers approve PRs and configure required repository checks.

## Success criteria

- The documented handoff preserves accepted requirements in git.
- Untracked, draft, and sibling-phase plans cannot authorize changes.
- Branch naming and file deletions cannot bypass the plan requirement.
- A fresh clone can run the template checks with make test.
- PR validation repeats the commit checks when local hooks were skipped.

## Phases

Single phase — one focused change to the template's SDLC checks.

## Affected systems

Repository conventions, stage skills, git hooks, template tests, and CI.

## Constraints

Use Git and Python's standard library so the template needs no package
installation. Keep human approval separate from checking status markers.
The user authorized the review's four proposed fixes with “improve the
gaps.” Artifact and implementation branches remain separate for review.

## Open questions

None within the authorized scope. Remote branch protection is configured
by a repository administrator and is not changed by this work.
