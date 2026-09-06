# Review linked outcomes and merge each stage before advancing — Intent

**Status:** accepted
**Accepted by:** Suraj Chhetry, confirmed in the owner conversation on 2026-09-06.
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

The owner also wants an `Intent` issue type in GitHub and a direct link
from every issue or task to its Markdown artifact. Reviewers need to
find the outcome, the content under review, and the exact approved
version from the work they are tracking.

## Outcome

For each feature or phase, contributors can start the next stage only
after the previous stage's outcome artifacts are committed, approved,
and merged through its own reviewed PR. Reviewers can follow each
outcome from its GitHub issue to the artifacts and merge evidence that
authorize the next stage.

The sequence is Intent → Spec → Plan → Build → Test + Review → Ship.

## Actors

- The owner accepts intent, spec, and plan.
- Contributors and coding agents prepare each stage's outcome artifacts.
- Reviewers verify those outcomes and approve their PRs.
- The organization owner manages the `Intent` issue type in GitHub.
- Repository checks block transitions that lack the required evidence.

## Success criteria

- Spec waits for the accepted intent's merged PR; Plan waits for the
  accepted spec's merged PR; Build waits for the approved plan's merged PR.
- Test + Review starts only after the Build outcome's PR is merged;
  Ship starts only after the Test + Review outcome's PR is merged.
- Each outcome has one parent issue of type `Intent`, with stage
  sub-issues of type `Task`. The parent stays open until the outcome
  ships and its success criteria are met.
- Every issue or task links to its governing artifact. Completed stages
  link to the exact approved artifact version and merged PR. Reviewers
  can navigate back from each artifact to the issue that tracks it.
- A local commit, approval marker, closed issue, open PR, or unmerged
  predecessor branch does not unlock the next stage. Agents stop at
  that gate.
- Conventions, stage skills, status reports, and automated checks agree
  on the sequence and identify the next missing approval or merge.

## Phases

Single phase — one outcome: each stage waits for the previous stage's
merged outcome. Each stage has its own PR within this phase.

## Affected systems

Repository conventions, workflow guidance, stage skills, artifact
templates, status reports, review policy, Git checks, and CI.
GitHub issue types, issue templates, parent and task relationships,
dependencies, and project tracking are also affected.

## Constraints

- Keep intent about why, spec about what, and plan about how.
- Keep approved content in repository artifacts. GitHub issues track
  ownership, discussion, dependencies, and progress, and link to that
  content rather than maintaining another copy of the requirements.
- The parent `Intent` issue links to the intent and an index of the
  stage artifacts. Its Intent-stage task closes after the accepted
  intent PR merges; that merge does not close the parent outcome.
- Stage tasks identify their outcome, owner, parent, stage, governing
  artifact, review PR, predecessor, and completion criteria. Larger
  outcomes may group the Spec-through-Ship tasks under phases after
  the shared intent is accepted and merged.
- Drafts link to readable Markdown in the working branch. Completed
  stages retain commit permalinks to the approved content and links to
  their merged PRs, so later edits cannot change the review record.
- Smaller implementation tasks link to the relevant approved spec
  requirement or plan section and implementation PR. They do not need
  duplicate Markdown files. Test + Review and Ship each record their
  own outcome evidence in a linked artifact.
- Future-stage issues may exist as placeholders. Their work remains
  blocked until the predecessor's approval and merge are verified.
  Issue dependencies and board status alone do not enforce that gate.
- Track lifecycle stage separately from work status. An issue can be
  in the Spec stage while blocked, ready, in progress, or in review.
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

- Owner, during spec: define the evidence that closes Test + Review
  and Ship, including how Ship completion is recorded when there is
  no deployment. Ship is the final stage, so it has no next-stage gate.
- Owner, during spec: settle how the revised process applies to any
  in-flight work and to the founding bootstrap workflow.
- Owner, during spec: define setup when a repository cannot use custom
  issue types or the contributor cannot configure the organization.
  Any fallback must be visible and preserve artifact and merge gates.
