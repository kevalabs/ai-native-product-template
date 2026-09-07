# SDLC workflow

The template checks linked stage outcomes. Build makes the implemented
checks available; an outcome counts as shipped only after its separate
Proof and Ship evidence lands and its success criteria hold.

## Actors & permissions

- R1 Contributors begin with a draft intent and a parent issue of type
  Intent. Stage sub-issues have type Task and link their governing
  Markdown. Each stage lands in a separate reviewed PR.
- R2 Owners accept intent/spec and approve plan. Conversation approval
  is recorded once. Reviewers verify the actual source and outcome;
  markers and a human merge alone do not prove independent review.

## Rules

- R10 Stage order is Intent → Spec → Plan → Build → Test + Review → Ship.
  A stage requires its same-phase approved predecessor on the base and
  verified GitHub merge evidence before advancement.
- R11 Plan enters history approved in a Plan-only PR. Build requires
  that Plan already merged and cannot amend its approved scope.
- R12 Local checks read the index and committed objects. Their success
  is local-only; remote handoff checks read GitHub evidence live.
- R13 Unsupported/default/detached branches, deletions, renames, and
  sibling-phase artifacts cannot skip prerequisite checks.
- R14 Artifact PRs contain one intent or exact-phase spec. Proof and
  Ship branches carry only their evidence; bootstrap keeps its narrow
  constitution document scope.
- R15 PR checks inspect every commit and reject mixed stages and early
  violations even after later corrections. PR history remains linear.
- R16 make test runs the offline regressions, syntax, and whitespace
  checks. Products add their own tests, lint, and build.
- R17 Contract changes require a contracts intent and approved touched
  surface. Build paths must match its committed plan.
- R18 Completed tasks retain approved commit permalinks and merged PRs.
  New artifacts link their stage task. Branch deletion does not erase
  completion evidence; legacy missing backlinks are recorded explicitly.
- R19 Proof covers every S-rule and names the exact merged Build. Ship
  requires passing proof and successful delivery of the proved version.
  Changed code or requirements invalidate old proof.

## Lifecycle and edge cases

- R20 A later revert does not hide an earlier history violation.
- R21 Missing Git objects, inaccessible APIs, stale versions, and wrong
  identities fail with an explanation; no offline remote-gate success.
- R22 Administrators configure required checks and human review. Setup
  reports classic protection and ruleset evidence without installing it.
- R23 Stage and work status are separate. The parent stays open until
  all phases ship and success criteria hold. Cancellation does not
  unlock dependent work. Reopened tasks require renewed evidence checks.
- R24 Stage skills look up existing identities before mutations and
  verify unknown write results before retrying. There is no background
  issue/PR lifecycle automation or automatic human approval.
- R25 An owner can record an explicit intent-label fallback where custom
  types are unavailable. It retains the same artifact and merge gates.

## Region availability

No region-specific behavior. Build checks are available on merge; formal
outcome completion requires the separate Proof and Ship stages.
