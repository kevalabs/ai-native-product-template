# Stage tracking takes one command, not many edits — Build

**Status:** ready
**Stage:** build
**Outcome:** 004-prototype-first
**Phase:** P3-stage-automation
**Parent issue:** https://github.com/kevalabs/ai-native-product-template/issues/22
**Stage issue:** https://github.com/kevalabs/ai-native-product-template/issues/40
**Predecessor PR:** https://github.com/kevalabs/ai-native-product-template/pull/83
**Plan commit:** 61080ff442f57a793bb15e53fd5f1267d70a961d
**Verification:** make test passed all 119 tests, lint, and template verification on this branch; 10 tests are new and each failed before its command existed.

<!-- Fill only with verified results. Do not claim passed/delivered while blocked. -->

## Requirement results

- S1: PASS — test_create_builds_the_graph_for_each_phase_shape builds a whole graph from one command.
- S2: PASS — test_create_builds_the_graph_for_each_phase_shape produces one parent and one task per tracked stage, for a single phase and a phased intent.
- S3: PASS — test_link_records_the_pr_and_status records the PR and sets the task to in review.
- S4: PASS — test_complete_records_the_merge_or_refuses records the permalink and merged PR, sets Done, and closes as completed.
- S5: PASS — test_repeated_run_creates_no_duplicate reads first and writes nothing when a graph exists.
- S6: PASS — test_dry_run_reports_without_writing reports the same change and makes no call.
- S7: PASS — test_no_command_writes_a_human_decision refuses each decision field by name.
- S8: PASS — test_complete_records_the_merge_or_refuses refuses an unmerged PR and writes nothing.
- S9: PASS — test_dry_run_reports_without_writing checks the change report names each write.
- S10: PASS — test_partial_and_unavailable_results_are_honest reports the writes that landed and omits the one that failed.
- S11: PASS — test_no_workflow_secret_or_bot_identity_is_installed finds no token, secret, or bot identity, and no workflow change.
- S12: PASS — test_cancelled_shipped_and_foreign_targets_refuse refuses a cancelled task.
- S13: PASS — test_no_command_writes_a_human_decision confirms the merge, review, and tag endpoints appear nowhere in the script.
- S14: PASS — test_guidance_describes_the_commands_and_refusals checks the conventions file states a command's success is not evidence; the 109 pre-existing tests prove the checks are unchanged.
- S15: PASS — test_guidance_describes_the_commands_and_refusals checks every guidance file names the commands and their refusals.
- S16: PASS — test_create_builds_the_graph_for_each_phase_shape refuses an intent that is not accepted.
- S17: PASS — test_repeated_run_creates_no_duplicate reports the existing graph instead of creating a second.
- S18: PASS — test_cancelled_shipped_and_foreign_targets_refuse refuses a task from another outcome.
- S19: PASS — test_partial_and_unavailable_results_are_honest reports an unavailable write as a failure, never as success.
- S20: PASS — test_repeated_run_creates_no_duplicate covers the read-before-write rule that makes a retry safe.

## Intent results

- TRUE — for work about screens, numbers, or an outside service, the owner confirms a prototype before its spec is accepted, or the spec says in one line why there is none. P1 delivered this and every spec written since has recorded a skip.
- TRUE — the Build's tests for that work load the same examples file the owner confirmed. P1 delivered the rule, the preserved file, and the reader.
- TRUE — starting a stage, creating the tracking issues for a merged intent, and recording a merged stage on its task each take one command. This phase delivers `make track-create`, `make track-link`, and `make track-complete`.
- TRUE — every existing gate and human approval still applies. No stage was removed, and the commands refuse to record any approval, by name.
- TRUE — products already built on the template can adopt the change by following a written adoption note. The note is below; the intent placed it in the last Ship record, which merged-source delivery no longer produces, and the owner approved moving it here on 2026-09-17.

## Changes

`scripts/track.py` adds three subcommands. `create` builds an outcome's
parent Intent issue and one Task per stage its delivery mode tracks,
for every phase the accepted intent declares. `link` records a stage PR
on its task and sets the status to in review. `complete` verifies the
merge with the existing evidence rules, then records the approved
permalink and merged PR, sets Done, and closes the task.

Every write passes through one `apply()` function, so the dry run and
the change report are one mechanism rather than three promises. A
denylist next to that function refuses Accepted by, Approved by,
Confirmed by, Blocking findings, and any completion without a merged PR
behind it. The merge, review, and tag endpoints appear nowhere in the
script, so no flag can reach them.

Reads go through `check_github.py`, which already knows how to resolve a
phase's stage path, check a merge, and compute the tracked stage set
from the delivery mode. Its behavior is unchanged, and the 109
pre-existing tests prove it.

Three Make targets expose the commands, each accepting
`DRY_RUN=--dry-run`. The conventions file, README, gate guide, four
stage skills, glossary, and capability doc describe them and say plainly
that a command's success is not evidence. Capability rules R42 and R43
record the commands and their refusals; R24 is replaced in place, keeping
its important half: nothing records a human approval automatically.

## Transition

Started from merged Plan PR #83 at the Plan commit above. The live entry
gate for Task #40 passed on 2026-09-17. Accepted Spec PR #82 and the
twice-revised Intent PR #78 are on the base.

No deviation from the approved Plan. All twelve changed files are inside
its declared surface, and each of its ten named tests exists.

This is the outcome's last phase. Its two cancelled siblings, P2 and the
optional-tracking phase of outcome 005, are recorded in their intents and
their issues are closed as not planned. The prototype step ships as P1
delivered it and stays manual, as the owner chose.

## Confirmed examples

The accepted Spec records a prototype skip: command-line tooling and
documentation only, with nothing to inspect before Build. There is no
confirmed examples file and no example reader. No example data is
invented here.

## Adoption note

A product already built on an earlier copy of this template adopts
everything in outcomes 004 and 005 by doing the following. Nothing here
rewrites shipped history.

Copy these files, which are template infrastructure rather than product
content: `scripts/check_sdlc.py`, `scripts/check_github.py`,
`scripts/track.py`, `tests/test_sdlc.py`, `tests/test_github.py`,
`tests/test_track.py`, `templates/` including the new prototype, fix,
and record templates, and `fixes/README.md`.

Merge these by hand, because a product has edited them: `AGENTS.md`,
`README.md`, `REVIEW.md`, `.githooks/README.md`, `features/README.md`,
`docs/agentic-sdlc.md`, `Makefile`, `product/glossary.md`, and
`product/capabilities/sdlc-workflow.md`. Take the new rules and keep the
product's own sections.

Fill these settings once. In `AGENTS.md`, add a `## Delivery settings`
section with `Delivery:` set to `merged source` or `runtime artifact`
and `Test paths:` listing the directories holding the product's tests.
A product that deploys a built artifact chooses `runtime artifact` and
keeps its Proof and Ship stages exactly as they were. A product whose
delivery is the reviewed default branch chooses `merged source`, closes
its open Proof and Ship tasks as not planned, and ships by tag from then
on. The `## Prototype settings` section keeps its expiry and sandbox
entries; the sandbox lane was cancelled and none is installed.

Set up a PR authoring identity if required review is configured. GitHub
ignores an approving review from a PR's author, so one person needs a
separate identity, a GitHub App or a machine account, to open PRs and
approve them as themselves. `make setup-check` prints this whenever it
finds required review.

A product with extra branch lanes such as `fix/`, `chore/`, or
`hotfix/` should know that `fix/` is now a defined lane with its own
rules: a failing test, one numbered record under `fixes/`, nothing under
`features/`, and a non-author approving review. Other lane names remain
unsupported and will be rejected by the branch check; either rename them
to `fix/` where they carry corrections, or open an intent to define them.

Nothing in an existing product's shipped chains needs back-filling. Old
`ship.md` records remain valid shipment evidence, and phases that
shipped under the six-stage rules keep their completed Proof and Ship
tasks.

## Delivery preparation

Delivery is `merged source`, so the reviewed merge of this PR is the
delivery. Shipment is one annotated tag,
`shipped/004-prototype-first-P3-stage-automation`, pushed on that merge
commit with a message naming this PR. No artifact is built, no Proof or
Ship PR opens, and tasks #41 and #42 are already closed as not planned.
After the tag lands, the parent Intent issue closes: every required
phase has shipped or been cancelled, and the success criteria above all
hold. The merge SHA is not yet known and is not invented here.
