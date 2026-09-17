# Stage gates and GitHub evidence

Run `make setup` once per clone to install the local hook. `make test`
checks Python syntax, shell syntax, whitespace, and the offline tests.
Product repositories extend it with their tests, lint, and build.

## One outcome, one stage PR at a time

| Stage | Branch | Outcome artifact | Prerequisite |
|---|---|---|---|
| Intent | artifact/NNN-name | intent.md | Parent Intent issue |
| Spec | artifact/NNN-name | spec.md and preserved design evidence | Accepted Intent PR merged; prototype confirmation or justified skip reviewed by a human |
| Plan | feature/NNN[-Pn]-name | plan.md only | Accepted Spec PR merged |
| Build | feature/NNN[-Pn]-name | build.md and declared implementation | Approved Plan PR merged |
| Test + Review | the Build PR, or proof/NNN[-Pn]-name | S-rule and Intent results in build.md, or proof.md only | Implementation complete; a non-author approving review before merge |
| Ship | the merged Build commit, or ship/NNN[-Pn]-name | shipped/NNN[-Pn-name] tag, or ship.md only | Reviewed Build merged; passing Proof PR merged for a runtime artifact |

The last two rows follow the `Delivery` setting in `AGENTS.md`. With
`merged source`, Test + Review evidence lands in the Build record and
Ship is an annotated tag on the merged Build commit; there is no Proof
or Ship PR and no Proof or Ship task. With `runtime artifact`, both
stages keep their own branches, records, PRs, and tasks.

A fix to shipped behavior uses none of these rows. It lands on a
`fix/short-name` branch in one reviewed PR carrying a changed file under
the declared Test paths, the change, and one record at
`fixes/NNN-short-name.md`. It touches nothing under `features/`, has no
stage task, and needs no tag. Its only remote gate is a current
approving review from someone other than its author.

All paths live under the chain or exact phase directory. Artifact PRs
cannot combine Intent and Spec. Bootstrap keeps its existing narrow
constitution allowlist. Start each stage worktree from the updated
remote default branch. Local branch reuse after a reviewed merge is
fine once fast-forwarded; previous stage commits must not be replayed.

All stage PRs target main. Between Intent and Spec, follow the
[prototype rules](../docs/agentic-sdlc.md#prototype-before-spec). Prototype
does not add a merged stage PR or another required Task. Spec preserves
the examples Markdown file byte for byte and permitted evidence under
the exact phase's `design/`; source code and the working note stay out.
The current artifact check permits Markdown and images there, not raw
JSON fixtures. Human review checks confirmation, age, access, and content.

P1 adds no prototype branch permission, sandbox enforcement, expiry job,
or lifecycle automation. `make handoff` verifies the six existing stage
gates, not the new manual confirmation. Do not report its success as
proof of confirmation or bypass hooks to create a prototype. Products
need an already permitted workspace until the separate lane is installed.
See [delivery rules](../docs/agentic-sdlc.md#branches-and-delivery) for
optional previews and promotion of the same proved artifact.

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

The shipped tag is annotated, named `shipped/<outcome>` or
`shipped/<outcome>-<Pn-name>`, and its message names the merged Build
PR. The checks fetch tags and require it to point at a commit on the
default branch carrying that phase's ready Build record. A tag never
moves; a correction starts a new intent.

The parent has type Intent, Outcome, Status, Artifact (intent URL), and
an index of available artifacts. Each stage task has type Task, Outcome,
Stage, Phase, Parent issue, Owner, Status, Artifact, Completion criteria,
and Review PR when opened. Use actual sub-issue and blocked-by relations.
Statuses are Blocked, Ready, In progress, In review, and Done. The parent
stays open until successful shipment. A phased parent has one Intent
task plus phase groups (`Stage: phase`, `Phase: Pn-name`) containing
Spec-through-Ship tasks. Only complete, noncancelled dependencies unlock
work. Keep project Stage and Status fields separate if using a project.

A merged-source outcome tracks Intent, Spec, Plan, and Build tasks per
phase; a runtime-artifact outcome also tracks Proof and Ship. A task for
a stage the mode does not track is closed as not planned and unlocks
nothing. The Build task completes when its PR has merged and the phase's
shipped tag exists.

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
and branch rulesets. When it finds required review configured it also
prints the PR authoring identity requirement: GitHub ignores an approval
from a PR's author, so one person needs a separate identity to open PRs.
It cannot verify which identity a repository uses. Missing or inaccessible setup is reported and exits
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
