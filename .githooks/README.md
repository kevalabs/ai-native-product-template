# Stage gates and GitHub evidence

Run `make setup` once per clone to install the local hook. `make test`
checks Python syntax, shell syntax, whitespace, and the offline tests.
Product repositories extend it with their tests, lint, and build.

## One outcome, one stage PR at a time

| Stage | Branch | Outcome artifact | Prerequisite |
|---|---|---|---|
| Intent | artifact/NNN-name | intent.md | Parent Intent issue |
| Spec | artifact/NNN-name | spec.md | Accepted Intent PR merged |
| Plan | feature/NNN[-Pn]-name | plan.md only | Accepted Spec PR merged |
| Build | feature/NNN[-Pn]-name | build.md and declared implementation | Approved Plan PR merged |
| Test + Review | proof/NNN[-Pn]-name | proof.md only | Build PR merged |
| Ship | ship/NNN[-Pn]-name | ship.md only | Passing Proof PR merged |

All paths live under the chain or exact phase directory. Artifact PRs
cannot combine Intent and Spec. Bootstrap keeps its existing narrow
constitution allowlist. Start each stage worktree from the updated
remote default branch. Local branch reuse after a reviewed merge is
fine once fast-forwarded; previous stage commits must not be replayed.

## Before work and before review

```sh
git fetch --prune origin
make handoff REPO=owner/repo ISSUE=123 BASE=origin/main
```

The task may still be a placeholder: handoff verifies its parent,
dependencies, predecessor merge, approved content, and completion links
before the next artifact exists. An inaccessible gate fails explicitly.
Then draft the stage artifact, recording approval when given. Plan's
first commit must already be approved and contain only plan.md.

For the PR itself:

```sh
python3 scripts/check_sdlc.py --base origin/main --head HEAD --branch feature/003-name
python3 scripts/check_github.py --repo owner/repo --base origin/main --head HEAD --branch feature/003-name --pr 456
```

Use the real branch, default branch, issue, and PR. The local hook reads
the index and Git objects, not unstaged approvals. Its success is
local-only. CI repeats each commit's checks and reads live GitHub
metadata. It uses the ordinary pull_request event with read-only
permissions. There is no supplied-snapshot or offline-success option.

## Tracking record

Use exact standalone Markdown headers, not fenced code, in issue bodies
and artifacts. New artifact templates include Stage, Outcome, Phase,
Parent issue, Stage issue, and Predecessor PR. Outcome is the numbered
folder name; Phase is `single` or the full `Pn-name` folder name. Stages
are lowercase `intent`, `spec`, `plan`, `build`, `proof`, and `ship`.
The PR body includes its Stage issue URL.

The parent has type Intent, Outcome, Status, Artifact (intent URL), and
an index of available artifacts. Each stage task has type Task, Outcome,
Stage, Phase, Parent issue, Owner, Status, Artifact, Completion criteria,
and Review PR when opened. Use actual sub-issue and blocked-by relations.
Statuses are Blocked, Ready, In progress, In review, and Done. The parent
stays open until successful shipment. A phased parent has one Intent
task plus phase groups (`Stage: phase`, `Phase: Pn-name`) containing
Spec-through-Ship tasks. Only complete, noncancelled dependencies unlock
work. Keep project Stage and Status fields separate if using a project.

After merge, set the task to Done, close it as completed, and record
Approved artifact as a full commit permalink and Review PR as the merged
PR URL. Verify content before closure. A cancelled issue uses a reason
and never counts as Done. Reopening requires checking evidence again.
Stage skills look up existing records before writing; after an unknown
write result, verify before retrying. GitHub issue forms provide the
record, but their required text boxes do not enforce the merge gate.

Older completed artifacts can lack backlinks. The first new stage must
record that gap in `## Transition`, link real merged PRs, and use complete
current tracking. Do not rewrite shipped history or claim old compliance.

## Setup and review limits

`make setup-check REPO=owner/repo` reads issue types, classic protection,
and branch rulesets. Missing or inaccessible setup is reported and exits
unsuccessfully. An administrator must configure both required job names,
human review, and renewed approval after changes. Inspect bypass rights
as part of that configuration review. Local setup never changes remote
policy. If Intent types are unavailable, the owner can explicitly choose
an `intent` label fallback: record `Issue type mode: label` and
`Fallback approved by` as bold headers on the parent. No silent fallback.

PR checks establish merges, identity, and content, not whether an
acceptance sentence or test proves the outcome. Conversation acceptance
is recorded and checked by a human under REVIEW.md; it is not fabricated
as a GitHub review. GitHub review records, when used, must be current and
not dismissed. Bot merges need a current human approving review. A human
merge alone does not prove an independent review happened. Required
repository policy and human review remain necessary.

Because a PR can replace its own validator, review the checks and test
changes as code. No skipped hooks, disabled jobs, or historical rewrites
are part of the validator transition.
