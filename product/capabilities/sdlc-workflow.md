# SDLC workflow

The template checks linked stage outcomes. Build makes the implemented
checks available; an outcome counts as shipped only after every phase
records its shipment evidence and its success criteria hold.

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
  Spec skip, without a merged stage PR. Intent, Spec, Plan, and Build
  each retain their own reviewed PR and gate. A stage requires its
  same-phase approved predecessor on the base and verified GitHub merge
  evidence before advancement.
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
- R19 Proof covers every S-rule and names the exact merged Build. For
  runtime-artifact delivery it is a separate record and PR, and Ship
  requires passing proof and successful delivery of the proved version.
  Changed code or requirements invalidate old proof.
- R34 A product declares `Delivery: merged source` or
  `Delivery: runtime artifact` with its test paths in the Delivery
  settings section of its conventions file. A missing or unrecognized
  value fails the Build check and names both accepted values.
- R35 A merged-source Build record carries one result line per Spec
  S-rule, each naming a test that appears under the declared test
  paths, and an Intent results line per success criterion. The check
  fails on a missing rule, a FAIL result, an absent test name, or a
  criterion count that does not match. The outcome's last phase cannot
  leave a criterion OPEN.
- R36 A Build PR merges only with a current approving review from
  someone other than its author, whoever performs the merge. That
  review is the Test + Review step.
- R37 Merged-source shipment is an annotated `shipped/<outcome>` or
  `shipped/<outcome>-<Pn-name>` tag on the merged Build commit. The
  checks require it to reach a default-branch commit holding that
  phase's ready Build record. The tag freezes its phase; a later change
  starts a new intent.
- R38 A merged-source outcome tracks Intent, Spec, Plan, and Build
  tasks per phase. A task for a stage the mode does not track is
  accepted whenever it is closed, whether as not planned or as
  completed under the previous rules, and a cancelled task unlocks no
  dependent work. An open task for an untracked stage is an error.
- R39 A fix to shipped behavior lands in one reviewed PR on a
  `fix/short-name` branch. The checks require a changed file under the
  declared test paths, exactly one record at `fixes/NNN-short-name.md`,
  no change under `features/`, an unused fix number, and an unedited
  record. A fix has no stage artifact and no tracking issue.
- R40 A fix PR merges only with a current approving review from someone
  other than its author. The reviewer judges whether the change
  restores behavior a shipped rule already states; a change that adds
  or alters a rule is new work and needs its own intent. Size does not
  decide, and no check makes that judgement.
- R41 Fix numbers never reuse and a merged fix record is immutable. A
  fix needs no shipped tag, and the outcome it corrects keeps the tag it
  already has.

## Lifecycle and edge cases

- R20 A later revert does not hide an earlier history violation.
- R21 Missing Git objects, inaccessible APIs, stale versions, and wrong
  identities fail with an explanation; no offline remote-gate success.
- R22 Administrators configure required checks and human review. Setup
  reports classic protection and ruleset evidence without installing it.
  When required review is configured, the report also states that PRs
  need an authoring identity other than the approver, because GitHub
  ignores an approval from a PR's author. The report cannot verify
  which identity a repository uses.
- R23 Stage and work status are separate. The parent stays open until
  all phases ship and success criteria hold. Cancellation does not
  unlock dependent work. Both handoff and PR checks verify every
  dependency's merged stage PR and current approved artifact for its
  declared outcome and phase. A closed task alone cannot unlock work.
  Reopened tasks require renewed evidence checks.
- R24 Stage skills and tracking commands look up existing identities
  before mutations and verify unknown write results before retrying.
  Tracking runs only when a contributor invokes it; there is no
  background automation and no automatic human approval.
- R42 `track-create` builds an outcome's parent Intent issue and one
  Task per tracked stage and phase from its accepted intent, and
  refuses when a graph already exists. `track-link` records a stage PR
  and sets its task to in review. `track-complete` verifies the merge,
  records the approved permalink and merged PR, and closes the task as
  completed, refusing an unmerged PR or a changed artifact.
- R43 Every tracking write reports what it changed and supports a dry
  run that writes nothing. A command refuses to record Accepted by,
  Approved by, Confirmed by, or Blocking findings, and never merges a
  PR, approves a review, or pushes a tag. A command's success is not
  evidence: the handoff and PR checks verify the graph independently.
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
outcome completion requires the shipment evidence its delivery mode
names. This template declares `merged source`, so its own outcomes
record Test + Review in the Build PR and ship by tag. Pushing that tag
and closing tracking records remain manual.
Prototype rules are manual instructions and human review checks. The
new prototype branch lane and sandbox enforcement are not installed;
work requires an already permitted workspace. There is no automated
expiry, retention, confirmation, or lifecycle service. Existing accepted
Specs and shipped chains retain their recorded history without back-fill.
