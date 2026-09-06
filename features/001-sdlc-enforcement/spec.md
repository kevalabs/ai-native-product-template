# Reliable SDLC gates — Spec

**Status:** accepted
**Intent:** [intent.md](intent.md)
**Phase:** single phase
**Personas served:** template owner, contributor, reviewer
**Capabilities affected:** product/capabilities/sdlc-workflow.md

## Flows

1. A contributor prepares intent and spec on an artifact branch.
2. The owner accepts each artifact before its next stage starts.
3. A reviewed artifact PR lands the accepted requirements.
4. A contributor creates a feature worktree from that base, records an
   approved plan in its first commit, then implements the change.
5. Local checks and PR checks validate the changes before human review.

## Requirements

- S1 An artifact branch accepts only the permitted planning files for
  its chain. It cannot carry application or enforcement code.
- S2 A feature change needs accepted intent and spec, and an approved
  plan for that exact chain and phase. Working-tree drafts do not count.
- S3 The first implementation commit contains only the approved plan.
  Later changes require that plan to have already been committed.
- S4 Unsupported branch names, detached local commits, default-branch
  commits, and deletion or rename changes cannot bypass these checks.
- S5 PR validation checks the commit history, including violations later
  hidden by follow-up commits, without trusting that local hooks ran.
- S6 Contributors can run all template verification with make test and
  install the hook with make setup. Failures return a nonzero exit code.
- S7 The instructions distinguish machine checks from human approvals,
  required repository settings, and future product-specific test jobs.

## States and transitions

Intent draft → accepted; spec draft → accepted; plan draft → approved.
Human acceptance permits the next stage. A status marker records the
approval; a script cannot prove that a human actually gave it.

## Permissions

Artifact branches carry planning documents only. Feature branches carry
implementation after a committed plan. Contract changes still need their
own contracts chain and an explicit declaration in its plan.

## Errors and edge cases

Checks name the failed rule and exit unsuccessfully. Missing history,
missing requirements, ambiguous chains, draft plans, sibling-phase plans,
code bundled with a first plan, and removed plans are rejected.

## UX

Command-line diagnostics name the needed correction. No product UI.

## Contract changes

No client-facing contracts change. Existing contributor instructions gain
an explicit artifact branch and PR handoff.

## Data changes

No existing production data is affected. Existing template history is
preserved; PR checks apply to commits introduced by the reviewed branch.

## Region variance

None.

## Acceptance criteria

- S1: artifact-only changes pass; unrelated and executable files fail.
- S2: approved matching plans pass; untracked, draft, and wrong-phase
  plans fail; staged approval does not authorize code in that commit.
- S3: plan-only first commit passes; bundled code or earlier changes fail.
- S4: tests exercise branch names, detached HEAD, deletions, and renames.
- S5: history tests accept a valid chain and reject a violation even if
  its final tree looks valid.
- S6: run the suite through make test; verify setup installs the hook.
- S7: review the README, conventions, stage skills, and hook guide against
  the actual checks and the artifact-to-implementation handoff.

## Out of scope

Deploying products, changing remote branch protection, proving real human
identity from Markdown, and choosing a future product's stack or tests.

## Open questions

None. These requirements implement the four findings the user asked to fix.
