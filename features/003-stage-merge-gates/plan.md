# Review linked outcomes and merge each stage before advancing — Plan

**Status:** approved
**Approved by:** Suraj Chhetry, in the owner conversation on 2026-09-07.
**Spec:** [spec.md](spec.md)
**Spec acceptance PR:** [#8](https://github.com/kevalabs/ai-native-product-template/pull/8), merged
**Phase:** single phase
**Branch:** feature/003-stage-merge-gates

## Approach

Extend the existing Python validator and keep the shell hook as its
entry point. Add one read-only GitHub adapter for PR, issue, review,
and setup evidence. Stage skills guide contributors through finding,
creating, and updating issues and PRs using their existing GitHub tools.
No background service or automatic merge agent is needed.

This is the recommended approach discussed with the owner before their
instruction to continue. A command suite that also creates and advances
every issue and PR would need a second state-management system, write
permissions, and recovery logic. Leave that automation for a separate
outcome. A documentation-only change would not meet the Spec's enforced
merge and artifact-link requirements.

Keep Markdown as the reviewed source. Parse a small set of exact,
standalone headers shared by the artifact and issue templates: Outcome,
Stage, Parent issue, Stage issue, Predecessor PR, and Artifact. Existing
intent/spec/plan status headers retain their meanings. Completion
records on issues add the approved artifact permalink and merged PR.
Artifact names are `intent.md`, `spec.md`, `plan.md`, `build.md`,
`proof.md`, and `ship.md`, under the chain or exact phase directory.

Build records the approved plan version, stage task, predecessor PR,
change summary, and verification results. Proof records the exact Build
commit and PR, results keyed to every S-rule, intent success results,
human review evidence, and unresolved findings. Ship records the proved
version, destination, delivery result, and evidence. Current PR numbers
live in the issue and PR body once assigned; an artifact need not predict
its own PR number or final commit hash.

### Stage and branch checks

Keep `artifact/NNN-name` for Intent or Spec, selecting one stage from the
PR's changed artifact paths. Reject a PR combining both stages. Keep
`feature/NNN[-Pn]-name` for Plan or Build: a Plan PR changes only its
approved plan; a Build PR requires that plan on the default branch and
includes `build.md`. Add `proof/NNN[-Pn]-name` and `ship/NNN[-Pn]-name`
with narrow, exact-phase evidence-file scopes. Keep bootstrap's existing
document allowlist. Shared review notes and design files belong only
to their declared planning stage, never a second outcome.

Determine the PR stage once, then validate every commit against that
scope and the merge-base prerequisites. Locally, validate the Git index
and committed objects, including deletion and both ends of a rename.
Do not let a working-tree approval, an arbitrary Markdown file, or a
sibling-phase artifact authorize changes. A Plan-only correction stays
a Plan PR; Build cannot amend its own approved scope.

### GitHub evidence and approval

Implement `scripts/check_github.py` with Python's standard library and
read-only `gh api` calls. Use argument arrays, fixed GitHub endpoints,
bounded timeouts, and pagination. Validate repository identity, stage,
phase, and full commit IDs; do not send credentials to URLs copied from
an artifact. Do not print authentication values or raw private content
in failures. Tests inject API responses and never need network access.

The gate checks that the predecessor PR actually merged into the
repository's default branch, that its merge result is in the current
base, and that the referenced approved artifact matches that result.
For squash and rebase merges, compare the relevant file content and
verify the resulting default-branch commit; do not require the old head
SHA to remain an ancestor. Check that all commits in the current PR
were based on the predecessor's merged outcome. A later rebase cannot
prove when somebody first typed a draft; instructions and human review
remain responsible for that limit.

Resolve parent and sub-issue relationships and dependencies through
GitHub, and validate the corresponding artifact and PR links. Do not
trust an issue being closed, an editable label, or a user-supplied JSON
snapshot as proof of merge. Completion permalinks must resolve after
branch deletion. Reject missing, stale, wrong-phase, or inaccessible
evidence with the affected stage and required remedy.

Owner acceptance and PR review are separate. Require committed status
and an attributed acceptance source, and show that source to the human
reviewer. Conversation acceptance is a valid source under S8; software
must not pretend to authenticate a conversation it cannot access.
Where GitHub review evidence is used, fetch it and check reviewer
identity, dismissal, changes requested, and the reviewed version.
Current-PR human approval is enforced at merge through repository
policy; do not make a running CI check depend on its own eventual merge.

Add a `--handoff` mode for agents before opening the next stage. It
requires live GitHub evidence. Keep local staged validation useful
without network access, but clearly label that result local-only.
The required PR job runs local history and live GitHub checks. There
is no offline-success fallback for a remote gate. Add `--setup-check`
to report configured, missing, or unverifiable issue types, required
checks, and review policy, inspecting both protection and rulesets.
Expose these checks through Make targets; keep `make test` offline.

### Resolve the old validator conflict

1. Obtain owner approval of this file, set `Status: approved`, and
   commit only this plan as the first commit on the feature branch.
   The old validator already accepts an approved Plan-only PR.
2. Merge that reviewed Plan PR before writing implementation. Start
   the Build worktree from the updated default branch. Keep the approved
   plan's original commit and the accepted requirements in history.
3. After that merge, write regression tests showing that the old PR
   check rejects a valid Build whose plan is already on main, and
   that the old checks permit bundled Intent/Spec stages.
4. The first Build commit replaces those rules with the new stage and
   merged-predecessor checks, their tests, `build.md`, and the matching
   capability update. The existing hook executes the working-tree
   validator; CI executes the validator checked out from the PR. Both
   therefore use the reviewed replacement when validating this commit.
5. Run the updated staged check and full PR-history check before that
   commit and handoff. Verify the real merged Plan PR, accepted Spec
   PRs #7/#8, Intent PR #6, and their committed artifacts. No skipped
   hook, disabled job, hardcoded feature-003 exemption, fake merge, or
   altered historical plan is part of this transition.

This is an ordinary change to the validator under an approved, merged
plan. Since a PR can change its own checks, the reviewer must inspect
the replacement predicates and regression evidence before merging it.
If this sequence does not pass the checks, stop and revise the Plan
through review; do not widen the permitted paths to make it pass.

## Touched surface (collision check)

Features 001 and 002 are shipped. No other in-flight plan exists in
the fetched default branch. Their artifacts stay unchanged. No app or
`packages/` files are in scope. One outcome is covered: a contributor
can complete each linked stage and pass its enforced handoff.

Plan PR:

- features/003-stage-merge-gates/plan.md

Build PR creates or updates only the following repository files:

- scripts/check_sdlc.py
- scripts/check_github.py
- scripts/verify_template.py
- tests/test_sdlc.py
- tests/test_github.py
- .github/workflows/verify.yml
- .github/ISSUE_TEMPLATE/intent.yml
- .github/ISSUE_TEMPLATE/stage-task.yml
- .github/pull_request_template.md
- Makefile
- .githooks/README.md
- AGENTS.md
- REVIEW.md
- README.md
- docs/agentic-sdlc.md (repository workflow and GitHub mapping)
- features/README.md
- templates/intent-template.md
- templates/spec-template.md
- templates/plan-template.md
- templates/build-template.md
- templates/proof-template.md
- templates/ship-template.md
- templates/capability-template.md
- .agents/skills/intent/SKILL.md
- .agents/skills/spec/SKILL.md
- .agents/skills/plan/SKILL.md
- .agents/skills/build/SKILL.md
- .agents/skills/proof/SKILL.md
- .agents/skills/ship/SKILL.md
- .agents/skills/capability/SKILL.md
- .agents/skills/feature/SKILL.md
- .agents/skills/product-status/SKILL.md
- .agents/skills/bootstrap-product/SKILL.md
- product/architecture.md (standing workflow rule 8)
- product/glossary.md (process vocabulary)
- product/capabilities/sdlc-workflow.md
- features/003-stage-merge-gates/build.md

The separate Proof PR adds `features/003-stage-merge-gates/proof.md`;
the separate Ship PR adds `features/003-stage-merge-gates/ship.md`.
The shell hook and agent pointer files need no changes.

External surface: feature 003's Intent issue, phase/stage tasks,
relationships, artifact links, stage PR descriptions, and the repository
project's stage/status fields if a project is in use. Inspect existing
records before creating any. Configure the custom Intent type only if
missing and permitted; it already exists here. Setup verification reads
repository rules and review requirements. Changes to those administrator
settings require a concrete configuration review before application.

Keep executable changes in the two validators and their tests. Most
other edits replace the same old lifecycle wording or add short
templates. If execution expands into a large automation framework or
cannot be reviewed in one sitting, return to the accepted phase split
before adding that work.

## Steps

1. **Prove the Plan-to-Build handoff.** After this Plan merges, implement
   the replacement checks and transition tests described above. Record
   feature 003's real predecessor evidence in `build.md`. Update the
   matching R-rules in the capability doc and run `make test`.
2. **Make a tracked stage reviewable.** Add the issue/artifact/PR fields
   and GitHub relationship checks together. Update Intent, Spec, and
   Plan skills to look up existing tracking records before mutation,
   maintain readable links, record approval before merge, and verify
   handoffs. Test broken links, duplicates found during lookup, deleted
   branches, wrong parents, wrong phases, and unavailable evidence.
   Run `make test`.
3. **Complete the lifecycle.** Add Build, Proof, and Ship skills and
   evidence templates, narrow branch scopes, proof freshness, correction
   handling, cancellation, and shipment completion checks. Update status
   skills to distinguish stage from status and report actual missing
   gates. Run `make test` and the lifecycle acceptance scenarios.
4. **Check setup and align guidance.** Add the setup report and explicit
   owner-selected label fallback guidance. Update current conventions,
   glossary, architecture workflow rule, capability text, and examples.
   Retain bootstrap's narrow scope and historical outcomes. Extend CI's
   read permissions only for the metadata checks it actually uses.
   Run `make test`, full PR history validation, and live handoff checks.
5. **Review, prove, and ship separately.** Inspect the full Build diff
   against this list and every S-rule before handoff. After Build merges,
   run Proof against that exact merged version and land its evidence PR.
   After Proof merges, complete the template shipment and its evidence
   PR. Record their final links on tasks and close the parent only after
   the intent success criteria are checked.

## Migrations

Adopt the new gate at the next unfinished stage. Completed legacy stages
retain their actual approval and merge history. Link their existing
artifacts and PRs in the first new stage's transition record; explicitly
identify older missing issue backlinks rather than fabricating past
compliance or rewriting shipped artifacts. For feature 003, this is
the Build record referring to PRs #6–#8 and the new Plan PR. New stages
must have their complete issue and artifact links.

No application data changes. New issue creation and stage updates remain
guided, reversible operations. Before retries, fetch the parent, stage,
and PR identity; if a prior write's result is unknown, verify it before
creating anything else. Never silently fall back from the custom type.
Record an owner's chosen label fallback on the parent issue, and keep
the same relationship and evidence checks in that mode.

Current setup inspection on 2026-09-07 found the Intent type available,
no open issues in the repository response, no classic branch protection
for main, and no effective main ruleset rules. Recheck before rollout;
these observations are not a substitute for required remote policy.

If the new checks fail operationally, keep the affected gate blocked
and land a reviewed correction under this plan while it is active.
Do not disable checks or claim delivery success. After shipment, fixes
start a new intent as required by the append-only feature history.

## Test plan

Write the changed-behavior tests before the validator change and show
their failures against the old implementation. Existing tests whose
expected permission changes under S6–S9 must be updated explicitly as
behavior changes, not removed to hide failures. Keep the unrelated
regressions for branches, paths, approvals, and contracts.

- S1–S3: fake GitHub responses cover parent type, six stage tasks,
  phased outcomes, owner fields, predecessor relationships, duplicate
  identities, and placeholders. Manually exercise guided retry lookup
  with a pre-existing issue and PR, confirming no duplicates are added.
- S4–S5: verify readable file and section links, backlinks, repository
  identity, approved commit content, and surviving branch deletion.
- S6–S9: disposable Git histories test every adjacent stage, separate
  Plan merge, single-stage scope, wrong phase, staged approval, stacked
  work, squash/rebase merges, and manually closed predecessor issues.
  Review the skills' explicit conversation-approval handling by hand.
- S10: verify Build tests and capability coverage, required CI checks,
  and administrator review policy in the setup report. Keep current-PR
  merge requirements separate from predecessor evidence checks.
- S11–S12: require results for every S-rule, reviewed version, and
  success criterion; reject blocking findings, a different Build SHA,
  and proof made stale by a reviewed correction or changed requirement.
- S13–S14: require delivered version, destination, successful result,
  and merged proof. Exercise failed shipment, optional template tags,
  multi-phase parent completion, and final issue links without a
  recursive requirement for another evidence PR.
- S15–S16: report stage/status separately; block invalid reopen and
  cancelled predecessors; never count cancellation as shipment.
- S17–S18: exercise local index and every PR commit, missing or changed
  prerequisite blobs, reverted earlier violations, API timeouts,
  forbidden access, pagination, malformed responses, and false snapshots.
- S19–S20: cover classic protection, rulesets, missing and inaccessible
  settings, absent Intent type, explicit label fallback, and no silent
  success when remote evidence cannot be verified.
- S21–S23: test adoption from recorded real legacy merges, narrow
  bootstrap scope, and feature 003's first Build commit with its plan
  already on the base; keep the rejected early-Build counterpart.
- S24: run `make test`, compare the declared touched surface with the
  diff, and search all current docs and skills for conflicting lifecycle
  guidance. Historical features 001 and 002 are excluded from rewrites.

GitHub behavior is based on the official [PR API](https://docs.github.com/en/rest/pulls/pulls),
[review API](https://docs.github.com/en/rest/pulls/reviews),
[sub-issue API](https://docs.github.com/en/rest/issues/sub-issues), and
[dependency API](https://docs.github.com/en/rest/issues/issue-dependencies).
Keep API adapters thin and review live behavior once during Proof.

## Rollout

Approval of this Plan is required before its first commit. Commit it
alone, run the existing checks, and open a Plan-only PR ready for review.
Merge that PR before Build. Do not publish a draft plan commit that the
current validator would reject, or rely on a later status repair.

Keep the existing `SDLC history` and `Template verification` job names.
The history job runs both local and remote predecessor validation with
read-only metadata permissions. It never executes contributor code with
an administrator token. Local setup verifies external settings without
silently changing them; it must report missing administrator policy.

Before claiming the new workflow enforced, review and install the
required checks and human review through repository policy and verify
the effective result. Complete the separate Proof and Ship PRs for
feature 003. For this template, record the delivered default-branch
version; no deployment service or mandatory release tag is introduced.
