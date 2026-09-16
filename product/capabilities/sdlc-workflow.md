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

- R10 The workflow is Intent → Prototype → Spec → Plan → Build →
  Test + Review → Ship. Prototype uses owner confirmation or a justified
  Spec skip, without a merged stage PR. The six stage PRs retain their gates.
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
  unlock dependent work. Both handoff and PR checks verify every
  dependency's merged stage PR and current approved artifact for its
  declared outcome and phase. A closed task alone cannot unlock work.
  Reopened tasks require renewed evidence checks.
- R24 Stage skills look up existing identities before mutations and
  verify unknown write results before retrying. There is no background
  issue/PR lifecycle automation or automatic human approval.
- R25 An owner can record an explicit intent-label fallback where custom
  types are unavailable. It retains the same artifact and merge gates.

## Prototype review

These checks are contributor instructions and human review requirements,
not automated prototype validation.

- R26 Spec preserves the confirmed examples byte for byte in its phase's
  design directory, alongside reviewable evidence and the exact prototype
  commit and owner decision. Runnable prototype code and its working
  note do not merge. Build tests load the same examples file directly;
  changed cases require renewed confirmation or an accepted Spec revision.
- R27 Prototype work requires its accepted Intent PR merged and an
  already permitted workspace. Screen behavior uses a screen walkthrough,
  rules use worked examples, and outside services use an integration trial.
  Mixed work uses every applicable form. A failed named case, missing
  example data, or omitted form prevents ready status.
- R28 Prototype code contains no automated product tests and has no
  coverage gate. Existing privacy and security rules still apply; real
  personal data and production secrets are excluded.
- R29 Only the owner confirms or rejects an exact committed version.
  Confirmation identifies its forms, commit, evidence, examples, owner,
  date, and attributable source, including how available user feedback
  affected the decision. Real-user feedback is optional, not approval.
- R30 Confirmed and rejected versions and decisions are immutable.
  Changes create a new version; the latest explicit confirmation governs
  Spec. A remote ref retains the commit through shipment, and the decision
  remains reviewable. Different commits or inaccessible evidence block
  Spec acceptance, even after a successful earlier demonstration.
- R31 An unresolved note expires after 30 days from creation unless the
  product declares another period. Expiry warns without failing a check.
  An explicit refresh can return an expired version to ready without
  erasing its age. When the note is at least 30 days old and Spec is not
  yet accepted, the owner reconfirms or accepts its age. Accepted Specs
  freeze confirmation without expiry.
- R32 Substantive Spec drafting needs confirmation or a one-line reason
  why nothing meaningful can be inspected. A tracking Task may exist
  earlier. Spec acceptance accepts a justified skip; missing evidence
  alone does not justify skipping, and no empty prototype is required.
- R33 Stage PRs target main; environment branches do not represent
  deployment state. A preview is optional. For runtime products, Proof
  tests the immutable artifact from the merged Build and rejects a source
  or identity mismatch. Ship delivers that same artifact without rebuilding;
  an unavailable or incompatible artifact keeps shipment unsuccessful.
  This template uses its merged Build source as its delivery artifact.

## Region availability

No region-specific behavior. Build checks are available on merge; formal
outcome completion requires the separate Proof and Ship stages.
Prototype rules are manual instructions and human review checks. The
new prototype branch lane and sandbox enforcement are not installed;
work requires an already permitted workspace. There is no automated
expiry, retention, confirmation, or lifecycle service. Existing accepted
Specs and shipped chains retain their recorded history without back-fill.
