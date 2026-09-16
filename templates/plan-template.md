# <Feature name> — Plan

**Stage:** plan
**Outcome:** <NNN-name>
**Phase:** <single or Pn-name>
**Parent issue:** <GitHub Intent issue URL>
**Stage issue:** <GitHub stage Task URL>
**Predecessor PR:** <merged previous-stage PR URL>

**Status:** draft
<!-- Change to exactly "approved" only after owner approval. Keep the
     status on its own line. Commit this file alone as the first commit
     on the feature branch, before any implementation changes. -->
**Spec:** link to this feature's spec.md
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

When the Spec confirms a prototype, name its preserved examples file,
case IDs, and how tests read the JSON block directly from that same file.
Record how to compare the original and preserved bytes. Changed cases
need renewed confirmation or an accepted Spec revision. For an accepted
skip or legacy Spec, record that fact without inventing example data.

## Rollout

Feature flags, region order, capability-doc update, anything needed
at deploy time.

Stage PRs target main; previews are optional. Describe how the merged
Build produces an immutable staging artifact, how Proof records and
tests its identity, and how Ship promotes that same artifact without
rebuilding. For this template, use the merged source version as the
artifact. Do not invent a future merge SHA or require environment branches.

<!-- On owner approval, add **Approved by:** with the person and actual approval source. -->
