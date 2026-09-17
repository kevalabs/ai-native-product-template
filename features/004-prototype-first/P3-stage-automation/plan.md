# Stage tracking takes one command, not many edits — Plan

**Stage:** plan
**Outcome:** 004-prototype-first
**Phase:** P3-stage-automation
**Parent issue:** https://github.com/kevalabs/ai-native-product-template/issues/22
**Stage issue:** https://github.com/kevalabs/ai-native-product-template/issues/39
**Predecessor PR:** https://github.com/kevalabs/ai-native-product-template/pull/82

**Status:** approved
**Approved by:** Suraj Chhetry, who approved this plan as written in the working conversation on 2026-09-17, including placing the adoption note in this phase Build record.
**Spec:** [Stage tracking takes one command, not many edits](spec.md)
**Branch:** feature/004-P3-stage-automation

The plan answers HOW. This is where tables, endpoints, components,
and services belong. The whole plan must fit one PR a human can
review in one sitting; if it doesn't, go back and split the phase.

## Approach

One new script, `scripts/track.py`, with three subcommands: `create`,
`link`, and `complete`. One file keeps the shared pieces together, the
GitHub client, the field writer, and the refusal rules, and gives the
reader one place to judge every write this repository can make.

It reuses `check_github.py` rather than duplicating it. That module
already knows how to read issues, resolve a phase's stage path, check a
merge, and compute the tracked stage set from the delivery mode. The new
script imports it for every read and for the evidence it checks before
writing. What it adds is a small write layer: `gh api --method POST` and
`PATCH` calls, each returning what it changed.

Writes go through one `apply()` function that takes a description and a
call. In dry-run mode it prints the description and returns without
calling. Outside dry run it prints the description, makes the call, and
prints the result. Every write in the script goes through it, so the
dry-run guarantee and the change report are one mechanism rather than a
promise repeated in three places. A partial failure prints the writes
that already succeeded before it re-raises.

The refusal rules are a denylist of field names checked in the writer:
Accepted by, Approved by, Confirmed by, and Blocking findings, plus any
attempt to set Status to Done without a merged PR behind it. The script
never calls the merge, review, or tag endpoints at all, so those cannot
be reached by a flag. The rules live next to the writer and are tested
directly.

Duplicate safety comes from reading first. `create` fetches the parent's
sub-issues before creating anything and refuses when a graph already
exists, which makes a repeated run a report rather than a second graph.
After an unknown write result, the script re-reads the issue and checks
whether its write landed before retrying, so a timeout cannot produce a
duplicate.

The rejected alternative was three separate scripts. One script with
subcommands keeps the refusal rules and the write layer in a single
reviewable place, which matters more here than command granularity,
because the risk in this phase is a tool that writes something a human
did not decide.

## Touched surface (collision check)

- scripts/track.py
- scripts/check_github.py
- tests/test_track.py
- Makefile
- AGENTS.md
- README.md
- .githooks/README.md
- .agents/skills/intent/SKILL.md
- .agents/skills/spec/SKILL.md
- .agents/skills/plan/SKILL.md
- .agents/skills/build/SKILL.md
- product/capabilities/sdlc-workflow.md
- product/glossary.md
- features/004-prototype-first/P3-stage-automation/build.md

Fourteen files, about 750 changed lines, roughly half of them the new
script and its tests, plus the adoption note in the Build record.
`check_github.py` gains only what the new script needs to import; its
existing behavior does not change, and its existing tests prove that.

No other plan is in flight: outcome 004 phase P2 and outcome 005 phase
P3 are cancelled, and outcome 005 phases P1 and P2 have shipped. Nothing
under `packages/`, `.github/workflows/`, `fixes/`, or any shipped
feature directory changes.

## Steps

1. **The write layer and its refusals.** Failing tests first: a write
   in dry-run mode reports and does not call; a write outside dry run
   calls and reports; a write naming an approval field refuses and
   names it; a partial failure reports the writes that landed. Then add
   `scripts/track.py` with its client, `apply()`, and the denylist.
   (S6, S7, S9, S10, S13)
2. **Create an outcome's graph.** Failing tests first: a single-phase
   and a phased intent each produce the right parent, tasks, relations,
   and dependencies for the delivery mode; a missing, unaccepted, or
   unmerged intent refuses; a second run creates nothing. Then add the
   `create` subcommand, reading the intent and the tracked stage set
   from `check_github.py`. (S1, S2, S5, S16, S17)
3. **Link a stage task to its PR.** Failing tests first: the command
   records the PR and sets the status to in review; a task from another
   outcome refuses. Then add the `link` subcommand. (S3, S18)
4. **Complete a merged stage.** Failing tests first: the command
   records the permalink and merged PR, sets Done, and closes as
   completed; an unmerged PR, an absent artifact, and an artifact whose
   content differs from the permalink each refuse. Then add the
   `complete` subcommand, reusing the existing merge and artifact
   checks. (S4, S8)
5. **Refuse unsafe targets and unavailable evidence.** Failing tests
   first: a cancelled or shipped outcome refuses; an API failure is
   reported as unavailable, never as success; an unknown write result is
   verified before any retry. Then add those guards. (S12, S19, S20)
6. **Commands, guidance, and capability.** Add `make track-create`,
   `track-link`, and `track-complete`. Update the conventions file,
   README, the gate guide, the four stage skills that tell contributors
   to edit issues by hand, the glossary, and
   `product/capabilities/sdlc-workflow.md`, including what the commands
   refuse to do and that their success is not evidence. (S11, S14, S15)
7. **The adoption note.** The intent's last success criterion is that a
   product already built on this template can adopt everything by
   following a written note. The intent placed that note in the last
   Ship record, which merged-source delivery no longer produces, so it
   goes in this Build record instead. It lists the files to copy or
   merge, the settings each product must fill, and what changes for a
   product with extra branch lanes. Written and reviewed as part of this
   PR, not invented afterwards.

## Migrations

No data migration and no change to any existing issue. The commands
write the same fields contributors write today, in the same shapes the
gate guide already defines.

Reversibility: every step is a reviewed commit on one branch. Reverting
the Build removes the script and its Make targets; tracking returns to
manual edits and no recorded issue becomes invalid.

## Test plan

Written first, per the new-check rule. `tests/test_track.py` uses the
same fake-API technique as `tests/test_github.py`: a dictionary of
canned responses and a recording writer, so no test needs credentials
or a network.

| Spec | Test |
|---|---|
| T1 (S1, S2, S16) | `test_create_builds_the_graph_for_each_phase_shape` |
| T2 (S3) | `test_link_records_the_pr_and_status` |
| T3 (S4, S8) | `test_complete_records_the_merge_or_refuses` |
| T4 (S5, S17, S20) | `test_repeated_run_creates_no_duplicate` |
| T5 (S6, S9) | `test_dry_run_reports_without_writing` |
| T6 (S7, S13) | `test_no_command_writes_a_human_decision` |
| T7 (S10, S19) | `test_partial_and_unavailable_results_are_honest` |
| T8 (S11) | `test_no_workflow_secret_or_bot_identity_is_installed` |
| T9 (S12, S18) | `test_cancelled_shipped_and_foreign_targets_refuse` |
| T10 (S14, S15) | `test_guidance_describes_the_commands_and_refusals` |

The accepted Spec records a prototype skip, so there is no confirmed
examples file and no example reader.

## Rollout

No feature flag and no region order. `product/capabilities/sdlc-workflow.md`
gains rules for the three commands and their refusals, and R24, which
currently states there is no lifecycle automation, is replaced in place
by a rule that keeps its important half: nothing records a human
approval automatically.

Delivery follows this repository's `merged source` setting. The Build PR
carries its S-rule results and Intent results, receives a non-author
approving review, and merges. Shipment is an annotated tag
`shipped/004-prototype-first-P3-stage-automation` on that merge commit,
whose message names the Build PR. No Proof or Ship PR is opened, and
tasks #41 and #42 are already closed as not planned.

This is the outcome's last phase, so its Build record walks all five
remaining Intent success criteria and none may be left open. The sixth,
about prototype branches, was withdrawn with the cancelled proto lane.
The parent closes after the tag lands.

<!-- On owner approval, add **Approved by:** with the person and actual approval source. -->
