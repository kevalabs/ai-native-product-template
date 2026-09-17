# Stage tracking takes one command, not many edits — Spec

**Stage:** spec
**Outcome:** 004-prototype-first
**Phase:** P3-stage-automation
**Parent issue:** https://github.com/kevalabs/ai-native-product-template/issues/22
**Stage issue:** https://github.com/kevalabs/ai-native-product-template/issues/38
**Predecessor PR:** https://github.com/kevalabs/ai-native-product-template/pull/78

**Status:** accepted
**Accepted by:** Suraj Chhetry, who accepted this Spec and its recorded prototype skip in the working conversation on 2026-09-17.
**Intent:** [Try an idea as a prototype and get feedback before its spec](../intent.md)
**Personas served:** product owner, solo developer, contributors and coding agents
**Capabilities affected:** `product/capabilities/sdlc-workflow.md`

The spec answers WHAT. Someone who knows the product should
understand every line without knowing how it is built. No tables,
endpoints, components, or services belong here.

## Prototype confirmation

**Prototype skip:** command-line tooling and documentation only. There
is no screen, calculation, or outside service to inspect before Build.
The S-rules below and the tests named for them are the inspectable
behavior. The owner chose this skip in the working conversation on
2026-09-17; accepting this Spec accepts it.

## Flows

### Create an outcome's tracking issues

1. The contributor has an accepted intent merged on the default branch.
2. They run the create command, naming the outcome.
3. The command reads the intent's phases and delivery mode, then reports
   what it would create.
4. On confirmation it creates the parent Intent issue and one Task per
   tracked stage and phase, with their fields, sub-issue relations, and
   blocked-by dependencies.
5. If the graph already exists, it says so and creates nothing.

### Link a stage task to its PR

1. The contributor opens a stage PR.
2. They run the link command, naming the stage task and the PR.
3. The command records the PR on the task and sets the task's status to
   in review, then reports what it changed.
4. The stage's checks now pass on their first run.

### Record a merged stage

1. A stage PR merges.
2. The contributor runs the complete command, naming the stage task.
3. The command reads the merge, records the approved artifact permalink
   and merged PR on the task, sets it Done, and closes it as completed.
4. If the PR is not merged, or its artifact is missing, it refuses and
   says why.

### Refuse to invent a human decision

1. A command is asked to set an acceptance, approval, or review that no
   human gave.
2. It refuses, names the field, and changes nothing.

## Requirements

- S1 A contributor creates an outcome's whole tracking graph with one
  command, from its accepted intent on the default branch.
- S2 The create command builds the parent Intent issue and one Task per
  stage the product's delivery mode tracks, for every phase the intent
  declares, with sub-issue relations and blocked-by dependencies that
  match the intent's phase order.
- S3 A contributor records a stage PR on its task with one command,
  which also sets the task's status to in review.
- S4 A contributor completes a merged stage with one command, which
  records the approved artifact permalink and the merged PR, sets the
  task Done, and closes it as completed.
- S5 Every command reads existing issues before writing and refuses to
  create a duplicate parent, phase group, or stage task.
- S6 Every command has a dry-run mode that reports exactly what it would
  change and writes nothing.
- S7 No command writes an acceptance, approval, review, or status that a
  human did not give. It refuses, names the field, and changes nothing.
- S8 The complete command refuses when the named PR is not merged, when
  its artifact is absent from the merge, or when the artifact's content
  differs from the approved permalink.
- S9 A command reports what it changed, naming each issue it touched, so
  the contributor can check the result.
- S10 A command that fails partway reports which writes succeeded and
  which did not. It never leaves the graph in a state it does not name.
- S11 Commands use the contributor's existing GitHub authentication.
  The template installs no workflow, no secret, and no bot identity.
- S12 A command refuses to act on a cancelled or shipped outcome.
- S13 The commands never merge a PR, never approve a review, and never
  push a shipped tag. Those stay human actions.
- S14 The existing checks are unchanged. A command's success is not
  evidence: the handoff and PR checks still verify the graph.
- S15 Contributor guidance, the gate guide, the stage skills, and the
  capability doc describe the commands in one consistent way, including
  what they refuse to do.

## States and transitions

A stage task moves through the states the gate guide already defines:

`Blocked` → `Ready` → `In progress` → `In review` → `Done`

- The create command writes `Blocked` for future stages and `Ready` for
  the first unblocked one.
- The link command moves a task to `In review`.
- The complete command moves it to `Done` and closes it as completed.
- `Cancelled` is set by a human, never by a command.

## Permissions

- Any contributor or coding agent can run the commands with their own
  GitHub authentication.
- Only a human sets acceptance, approval, cancellation, or a review.
- The commands act only on issues in the repository they are run
  against.

## Errors and edge cases

- S16 When the intent is missing, not accepted, or not merged, the
  create command refuses and says which.
- S17 When the graph already exists, the create command reports it and
  creates nothing, whether run once or many times.
- S18 When a named task does not exist or belongs to another outcome,
  the command refuses and names the mismatch.
- S19 When GitHub is unavailable or authentication fails, the command
  reports it as unavailable rather than as success, and writes nothing
  it cannot confirm.
- S20 When a write result is unknown, the command verifies before
  retrying, so a timeout never creates a duplicate issue.

## UX

These are command-line tools. Their output is plain text a person can
read: what will change, what changed, and what was refused. No product
screen and no design mock.

## Contract changes

No external product or client contract changes. This phase adds
contributor tooling only.

## Data changes

The repository newly remembers nothing. The commands write GitHub
issues, which are already the tracking record. No artifact, no shipped
directory, and no tag changes.

## Region variance

No region-specific behavior.

## Acceptance criteria

- T1 (S1, S2, S16) The create command builds the full graph for a single
  phase and a phased intent, and refuses on a missing or unaccepted one.
- T2 (S3) The link command records the PR and sets the status.
- T3 (S4, S8) The complete command records the permalink and PR and
  closes the task; it refuses on an unmerged PR or a missing artifact.
- T4 (S5, S17, S20) A repeated create makes no duplicate, and an unknown
  write result is verified rather than retried blindly.
- T5 (S6, S9) Dry run reports the same changes it would make and writes
  nothing.
- T6 (S7, S13) A command asked to write an approval, a review, a merge,
  or a tag refuses and names the field.
- T7 (S10, S19) A partial failure and an unavailable API are both
  reported honestly, never as success.
- T8 (S11) The commands use existing authentication and the template
  installs no workflow, secret, or bot identity.
- T9 (S12, S18) A cancelled or shipped outcome, and a task from another
  outcome, are both refused.
- T10 (S14, S15) The existing checks still pass unchanged, and guidance
  describes the commands and their refusals once.

## Out of scope

- Any GitHub Actions workflow or bot identity. The owner chose local
  commands only.
- Merging PRs, approving reviews, and pushing shipped tags.
- Creating or editing Markdown artifacts.
- The prototype step's records, which stay manual and unchanged.
- Project boards, milestones, and labels.

## Open questions

- Plan owner: whether the commands live in one script with
  subcommands or three, and which Make targets expose them.
- Plan owner: how a product without GitHub issues, once that is
  possible, is told these commands do not apply.
