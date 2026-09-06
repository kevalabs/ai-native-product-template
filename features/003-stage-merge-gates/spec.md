# Review linked outcomes and merge each stage before advancing — Spec

**Status:** draft
**Intent:** [intent.md](intent.md)
**Intent PR:** [#6](https://github.com/kevalabs/ai-native-product-template/pull/6), merged
**Phase:** single phase
**Personas served:** template owner, contributor, coding agent, reviewer, organization owner
**Capabilities affected:** product/capabilities/sdlc-workflow.md

## Flows

1. The contributor starts an outcome with an Intent issue and a linked
   draft intent. Its Intent-stage task tracks review of that artifact.
2. The owner accepts the intent. The contributor commits that acceptance
   and submits an intent-only PR. Required checks and human review pass,
   then the PR merges into the default branch.
3. The contributor verifies the merge and approved artifact version,
   records them on the stage task, and closes that task. The parent
   Intent stays open. The contributor starts Spec from the updated
   default branch.
4. Spec and Plan each follow the same approval, commit, review, and merge
   handoff in their own PR. Build starts after the Plan PR merges.
5. Build delivers the approved changes, tests, and matching capability
   updates. Required checks and human review pass before its PR merges.
   The contributor then starts the separate Test + Review stage.
6. The reviewer checks the merged Build outcome against the spec and
   intent. The contributor records the tested version and acceptance
   evidence in an artifact. Unresolved findings block Ship.
7. After the Test + Review PR merges, the contributor performs the
   agreed shipment and records its result. The Ship task closes after
   shipment succeeds and its evidence PR merges. The parent closes
   when all required phases have shipped and its success criteria hold.

## Requirements

- S1 Every outcome has one parent GitHub issue of type `Intent`. It has
  one `Task` sub-issue for each stage: Intent, Spec, Plan, Build,
  Test + Review, and Ship. The parent stays open through all six stages.
- S2 A phased intent has one shared Intent-stage task. Each phase has
  its own Spec-through-Ship tasks grouped under that phase. A phase
  cannot start work blocked by an unmet dependency in the accepted intent.
- S3 Each stage task names its outcome, owner, parent, stage, governing
  artifact, completion criteria, and predecessor where one exists. It
  links its review PR once opened. Future tasks may be placeholders;
  creating or assigning one does not authorize stage work.
- S4 Every issue or task has a readable link to its governing Markdown
  artifact or relevant section. The parent links to the intent and an
  index of available stage artifacts. Each artifact links back to its
  tracking issue. Smaller Build tasks reuse approved spec requirements
  or plan sections instead of duplicating the requirements.
- S5 During drafting, an artifact link shows the content being reviewed.
  Before a stage is complete, its task records the exact approved
  artifact version through a commit permalink and the merged PR URL.
  Deleting the working branch does not break the completion record.
- S6 Stage order is Intent → Spec → Plan → Build → Test + Review → Ship.
  Each stage delivers its outcome through a separate PR. Contributors
  and agents must verify the previous stage's approval and merge into
  the default branch before drafting or performing the next stage.
- S7 Each stage begins from the updated default branch containing the
  previous outcome. Unmerged stacked branches, local commits, open PRs,
  draft approvals, board status, and manually closed issues do not pass
  the handoff. Each gate applies to the same outcome and exact phase.
- S8 The owner accepts intent and spec and approves plan. Contributors
  record those decisions in the corresponding committed artifacts.
  Explicit owner approval in the working conversation counts as owner
  acceptance; an agent must not ask for the same approval again. PR
  review and merge remain separate checks. Agents cannot invent approval
  by setting a status marker or approving their own work.
- S9 Intent, Spec, and Plan PRs contain only the outcome documents for
  their stage and directly related review material. Plan has its own
  approved, plan-only first commit and PR; code follows in the separate
  Build PR after that Plan PR merges.
- S10 Every PR passes the required checks and human review before merge.
  Build includes the tests needed to verify its changes and runs
  `make test` before handoff. A later Test + Review stage does not defer
  those checks. Behavior changes include matching capability updates;
  capability text states any release restrictions that still apply.
- S11 Test + Review records the exact Build version checked, a result
  for every spec requirement, the intent's success criteria, test and
  build results, human review evidence, and unresolved findings. It
  passes only when every requirement has evidence and no blocking
  finding remains. [ASSUMED: completion policy pending owner review.]
- S12 Failed proof keeps Ship blocked. A code correction lands through
  a reviewed Build correction PR under the approved scope, then proof
  is repeated for the corrected version. A changed intent, spec, or
  plan must be reapproved and merged before dependent work resumes.
  Earlier evidence stays available and does not approve a new version.
- S13 Ship starts only after the passing Test + Review outcome merges.
  Its artifact identifies the delivered version, delivery destination,
  result, and completion evidence. Failed delivery leaves Ship and the
  parent open. For a template with no deployment, delivery means the
  approved version is available on the default branch and the shipment
  evidence PR has merged; a release tag is optional. [ASSUMED: completion
  policy pending owner review.]
- S14 A Build merge alone never marks an outcome shipped or closes its
  parent. The parent closes only after all required phase shipments and
  the final intent success check. Ship is the last stage; its own PR
  URL is recorded on its task after merge, without requiring an endless
  sequence of evidence PRs about previous evidence PRs.
- S15 Work status is separate from lifecycle stage. Tasks use Blocked,
  Ready, In progress, In review, and Done. A stage becomes Ready only
  when its prerequisites are verified and Done only when its outcome
  and merge evidence satisfy the gate. Reports show the missing approval,
  merge, artifact, or delivery result when blocked.
- S16 A cancelled outcome is recorded as cancelled, with a reason. It
  does not count as shipped or unlock dependent work. Reopening a task
  requires its evidence and dependencies to be checked again.
- S17 Local checks reject staged stage combinations and missing
  committed prerequisites. PR checks validate each commit, predecessor
  merge evidence, and required artifact links. They reject an early
  violation even when a later commit fixes or reverts it. Starting work
  is also governed by the agent instructions and human review; checks
  cannot prevent a person from typing an uncommitted draft.
- S18 Missing, inaccessible, stale, or mismatched evidence blocks the
  affected gate with a message naming what must be verified. Retrying a
  handoff after a network failure does not create duplicate outcome
  issues, stage tasks, or PRs. Approval cannot be inferred from an
  unavailable GitHub response.
- S19 Organization owners manage the custom issue type; repository
  administrators configure required checks and human review. Setup
  reports whether those requirements are configured, missing, or cannot
  be verified. A local setup command does not claim to install remote
  policy merely because it completed successfully.
- S20 If custom issue types are unavailable, setup may use an explicit
  `intent` label fallback only when the owner chooses and records that
  mode. All artifact, approval, and merge gates still apply. Insufficient
  permission is reported; setup does not silently change modes.
  [ASSUMED: fallback policy pending owner review.]
- S21 Shipped feature history remains unchanged. Active chains adopt
  the gates at their next unfinished stage, with existing evidence
  reviewed and any missing prerequisite recorded before advancement.
  No past approval or merge is fabricated. [ASSUMED: transition policy
  pending owner review.]
- S22 Bootstrap remains a separate reviewed constitution PR, with its
  existing narrow document scope and no application, hook, or CI changes.
  The six-stage feature sequence applies after bootstrap. [ASSUMED:
  bootstrap policy pending owner review.]
- S23 Feature 003 follows the accepted stage sequence itself. Its
  accepted Intent PR #6 precedes this Spec PR, and its Plan PR must merge
  before Build starts. If existing checks conflict with that handoff,
  contributors report the conflict and obtain a reviewed transition
  decision before proceeding; they do not bypass or disable the checks.
- S24 Existing protection against unsupported branches, direct default
  branch commits, wrong-phase plans, deletions, renames, and contract
  changes without a dedicated contracts intent remains in force. Stage
  guidance, templates, review policy, glossary, and status reports must
  describe the same revised lifecycle.

## States and transitions

The parent outcome is proposed while its intent is draft, accepted when
the owner accepts it, and shipped only after S14. Cancellation is a
separate terminal result. Closing the Intent-stage task does not close
the parent.

Each stage follows Blocked → Ready → In progress → In review → Done.
Intent starts Ready once its tracking issue and draft artifact exist.
A review finding returns the affected stage to In progress. Missing or
invalidated prerequisites return it to Blocked. Done requires the stage
outcome and reviewed merge, with delivery also required for Ship.

GitHub PR draft status describes readiness for review; it is separate
from artifact acceptance. A draft spec may have a PR ready for review.
Owner acceptance does not itself merge the PR.

## Permissions

Contributors and agents prepare artifacts, tasks, tests, and evidence
within their repository access. The owner decides intent, spec, and
plan acceptance. Human reviewers judge PRs and the proof of the outcome.
Organization and repository administrators manage remote policy under
S19. Missing permission blocks the affected action with the explanation
required by S18; it grants no substitute approval.

## Errors and edge cases

S5 covers branch deletion after merge. S7 covers the wrong phase, an
open predecessor, and a manually closed task. S12 covers failed proof
and changes after approval. S13 covers failed shipment. S16 covers
cancellation and reopening. S18 covers inaccessible or stale evidence
and interrupted retries. S20–S23 cover setup and transition conflicts.

## UX

Reviewers can open each artifact directly from its issue, reach its
review PR, and identify the approved version after merge. Contributors
can see the current stage, owner, work status, and unmet prerequisite
without comparing duplicate copies of the requirements. Existing GitHub
issue, PR, and project views provide this flow; no new product UI or
design mocks are needed.

## Contract changes

No application or client-facing contracts change. The contributor
workflow changes: combining planning stages or starting Build from an
unmerged Plan no longer passes. GitHub issue classification and artifact
links become part of the review record. No `packages/` changes are needed.

## Data changes

New tracking records retain parent and stage relationships, owners,
artifact links, approval evidence, merged PRs, exact approved versions,
and proof and shipment results. Existing shipped records are preserved.
Active records follow the proposed transition in S21. Existing unrelated
GitHub issues and organization issue types are not renamed or deleted.

## Region variance

None. These are repository workflow rules.

## Acceptance criteria

- S1–S3: **Outcome and phase tracking** — verify one parent, the correct
  stage tasks, phase dependencies, required information, and blocked
  placeholders. Parent remains open after the Intent task completes.
- S4–S5: **Artifact navigation** — follow issue-to-artifact and return
  links, section links, and approved commit permalinks; delete the
  merged branch and verify the completion links still resolve.
- S6–S9: **Separate stage handoffs** — exercise each adjacent gate with
  accepted and unaccepted artifacts, merged and open PRs, stacked
  branches, wrong-phase evidence, and a manually closed issue. Confirm
  owner acceptance is recorded once and Plan merges before Build.
- S10: **Checks before Build merge** — reject failing checks and missing
  human review; verify behavior changes include accurate capability
  updates with any remaining release restrictions stated.
- S11–S12: **Proof and corrections** — require every requirement and
  outcome check, reject unresolved blocking findings, and show that a
  corrected Build version requires renewed proof.
- S13–S14: **Shipment completion** — block early or failed shipment;
  close a template shipment only with delivery evidence and its merged
  PR, then close the parent only when every phase and success check pass.
- S15–S16: **Honest status** — report stage independently from status,
  name missing evidence, and never count cancellation as shipment or
  allow a reopened issue to reuse invalid evidence.
- S17–S18: **Enforcement and unavailable evidence** — reject bundled
  stages, early history violations, missing links, and unavailable or
  mismatched predecessors. Retry without duplicate tracking records.
- S19–S20: **Setup visibility** — cover configured, missing, and
  inaccessible remote policy; require an explicit owner decision for
  fallback and preserve all gates in that mode.
- S21–S23: **Transition without invented history** — preserve shipped
  records, check active-chain prerequisites, retain narrow bootstrap
  scope, and identify feature 003's old-check conflict before Build.
- S24: **Existing protections and consistent guidance** — run the full
  regression suite and `make test`; review every current lifecycle
  reference against this spec and retain unrelated protections.

## Out of scope

Application features, client contract changes, a new tracking UI,
automatic human approval, automatic production deployment, rewriting
shipped history, and creating a Markdown document for every small task.
This Spec PR does not implement checks or modify organization settings.

## Open questions

- Owner: accept or change the proposed completion evidence in S11 and
  S13, transition and bootstrap policy in S21–S22, and explicit fallback
  in S20. The three interview questions remain pending; these rules are
  marked assumptions until answered or accepted in review.
- Plan author and owner: decide how feature 003's separate Plan and
  Build PRs can pass the old check that requires a new plan as the first
  commit of every implementation PR. The plan must include a concrete,
  reviewed transition before Build; S23 forbids bypassing the check.
- Plan author: choose evidence artifact names and how local and PR
  checks obtain and validate merge and approval evidence. Keep S18's
  explicit failure behavior when evidence cannot be verified.

The affected capability is `product/capabilities/sdlc-workflow.md`.
R1 and R10–R12 change to separate intent, spec, and plan merges. R14–R15
change to stage-specific PR scopes and predecessor checks. The lifecycle
gains explicit proof and shipment completion. New rules cover tracking
and artifact links. R2, R13, R16–R17, and R20–R22 retain their protections,
with wording aligned to the new stage names and evidence requirements.
