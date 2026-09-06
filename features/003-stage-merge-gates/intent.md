# Merge each stage before starting the next — Intent

**Status:** draft
**Kind:** change
**Originator:** Suraj Chhetry
**Date:** 2026-09-06
**Due:** —

## Problem

The owner wants contributors and coding agents to finish each stage,
commit its outcome artifacts, and merge its reviewed PR before starting
the next stage. Today, intent and spec can share an artifact PR. Build
can start after a plan is committed, before that plan has a merged PR.
Those rules allow work to advance before the previous outcome has landed.

The evidence is the current workflow guidance and checks, together with
the owner's request: "after each outcome artifacts force to commit and
merged PR then only next step start."

## Outcome

For each feature or phase, contributors can start the next stage only
after the previous stage's outcome artifacts are committed, approved,
and merged through its own reviewed PR.

The sequence is Intent → Spec → Plan → Build → Test + Review → Ship.

## Actors

- The owner accepts intent, spec, and plan.
- Contributors and coding agents prepare each stage's outcome artifacts.
- Reviewers verify those outcomes and approve their PRs.
- Repository checks block transitions that lack the required evidence.

## Success criteria

- Spec starts only after the accepted intent's PR is merged.
- Plan starts only after the accepted spec's PR is merged.
- Build starts only after the approved plan's PR is merged.
- Test + Review starts only after the Build outcome's PR is merged;
  Ship starts only after the Test + Review outcome's PR is merged.
- A local commit, approval marker, open PR, or unmerged predecessor
  branch does not unlock the next stage. Agents stop at that gate.
- Conventions, stage skills, status reports, and automated checks agree
  on the sequence and identify the next missing approval or merge.

## Phases

Single phase — one outcome: each stage waits for the previous stage's
merged outcome. Each stage has its own PR within this phase.

## Affected systems

Repository conventions, workflow guidance, stage skills, artifact
templates, status reports, review policy, Git checks, and CI.

## Constraints

- Keep intent about why, spec about what, and plan about how.
- Preserve human approval. Agents cannot approve their own artifacts
  by changing status markers or count their own review as human review.
- Keep required checks and human review before every merge. The later
  Test + Review stage does not defer tests needed to safely merge Build.
- Do not treat a Build merge as permission to release. Ship remains
  gated by the merged Test + Review outcome.
- Apply the sequence to this change: land this accepted intent before
  starting its spec. Do not prepare later stages on stacked branches.
- Preserve shipped feature artifacts as history. This change builds
  on features 001 and 002; it does not rewrite their past approvals.
- [ASSUMED] No deadline or external compliance requirement applies;
  the reason to act now is the owner's requested workflow change.

## Open questions

- Owner: confirm separate Build and Test + Review PRs when accepting
  this intent. This draft follows the requested stage-by-stage sequence;
  ordinary checks and human review still precede the Build merge.
- Owner, during spec: define the evidence that closes Test + Review
  and Ship, including how Ship completion is recorded when there is
  no deployment. Ship is the final stage, so it has no next-stage gate.
- Owner, during spec: settle how the revised process applies to any
  in-flight work and to the founding bootstrap workflow.
