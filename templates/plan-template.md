# <Feature name> — Plan

**Status:** approved (this file is the first commit on the feature
branch — no code before it)
**Spec:** link to this feature's spec.md

## Approach

The implementation strategy in a few paragraphs: key design decisions
and why, alternatives rejected.

## Touched surface (collision check)

Exhaustive list of apps/packages/files this plan will create or
modify. Reviewed against other in-flight plans before build starts.
The merged diff must match this list — undeclared changes are a
blocking review finding.

## Steps

Ordered, verifiable steps. Each ends in a state where `make test`
passes. Prefer tracer-bullet slices — narrow vertical cuts through
every layer, each demoable — over layer-by-layer sequencing; put the
riskiest slice first.

1. …
2. …

## Migrations

Database/data migrations, ordering, and reversibility.

## Test plan

Tests to be written per spec acceptance criteria (S-numbers), incl.
which are written first (bug-fix rule: failing test precedes fix).

## Rollout

Feature flags, region order, capability-doc update, anything needed
at deploy time.
