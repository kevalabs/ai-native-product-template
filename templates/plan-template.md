# <Feature name> — Plan

**Status:** draft
<!-- Change to exactly "approved" only after owner approval. Keep the
     status on its own line. Commit this file alone as the first commit
     on the feature branch, before any implementation changes. -->
**Spec:** link to this feature's spec.md
**Phase:** <Pn short-name, or "single phase">
**Branch:** feature/NNN[-Pn]-short-name

The plan answers HOW. This is where tables, endpoints, components,
and services belong. The whole plan must fit one PR a human can
review in one sitting; if it doesn't, go back and split the phase.

## Approach

The implementation strategy in a few paragraphs: key design decisions
and why, alternatives rejected.

## Touched surface (collision check)

Exhaustive list of apps/packages/files this plan will create or
modify. Reviewed against other in-flight plans before build starts —
including sibling phases of the same intent. The merged diff must
match this list — undeclared changes are a blocking review finding.

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
