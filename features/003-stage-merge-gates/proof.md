# Review linked outcomes and merge each stage before advancing — Proof

**Status:** passed
**Stage:** proof
**Outcome:** 003-stage-merge-gates
**Phase:** single
**Parent issue:** https://github.com/kevalabs/ai-native-product-template/issues/10
**Stage issue:** https://github.com/kevalabs/ai-native-product-template/issues/15
**Predecessor PR:** https://github.com/kevalabs/ai-native-product-template/pull/18
**Build commit:** 54764fe2237ca9098360acc99b13a2fdc0d9df57
**Blocking findings:** none

This evidence checks the corrected Build merged by PR #18. It does not
mark the outcome shipped. This Proof PR must receive human review and
merge before Ship starts.

## Requirement results

The named tests below are in the [Git workflow tests][local-tests] and
[GitHub evidence tests][remote-tests]. Guided actions and human decisions
also use the walkthroughs and attributed evidence below. Tests with
controlled GitHub responses do not prove real administrator policy;
the live policy readback supplies that evidence.

- S1: PASS — The live handoff reads parent Intent #10 and its six native Task sub-issues #11–#16. The parent remains open; duplicate and missing stage tests reject incorrect graphs.
- S2: PASS — `test_phase_group_uses_its_exact_stage_artifacts` checks grouped phase tasks. Wrong-phase and extra-dependency tests reject mismatched or unmet prerequisites. The stage skills require checking accepted Intent dependencies before phase work.
- S3: PASS — The live graph and task records identify the outcome, owner, parent, stage, artifact, and completion criteria. Build task #14 records PR #18; Proof task #15 tracks this review. Future Ship task #16 remains a blocked placeholder.
- S4: PASS — The parent indexes the artifacts, and active tasks link readable Markdown. The Build record links back to #14, and this record links #15. Backlink and section-link tests reject mismatches. Legacy planning backlinks are covered by the explicit transition under S21.
- S5: PASS — Build task #14 retains the full approved commit permalink and merged PR #18 after its remote branch was deleted. Intent, Spec, and Plan tasks retain their own permalinks. `test_branch_link_is_not_completion_evidence` rejects a mutable completion link.
- S6: PASS — The real sequence is Intent PR #6, Spec PRs #7/#8, Plan PR #9, Build PRs #17/#18, then this Proof. The Plan-on-base, unmerged-Plan, bundled-stage, and complete-Proof tests enforce separate handoffs. The live Ship gate rejects advancement before this Proof merges.
- S7: PASS — The live Build-to-Proof handoff passed before this worktree was created from main at the named Build. Closed-issue, wrong-default-branch, wrong-phase, and extra-dependency regressions reject substitute or incomplete evidence.
- S8: PASS — Existing Intent, Spec, and Plan artifacts retain the owner's attributed approvals. Stage skills record conversation acceptance without requesting it again. Changed, stale, and dismissed review tests reject invalid GitHub approval evidence; human confirmation is recorded separately below.
- S9: PASS — Plan PR #9 changed only the approved Plan. Tests reject Plan bundled with code, Intent bundled with Spec, and a Build that edits its Plan. The reviewed validator transition did not combine Plan and Build.
- S10: PASS — Both Build PR checks passed, and the owner confirmed reviewing #17 and #18. Build includes tests and matching capability rules with shipment restrictions. Required checks and fresh human approval are now enforced on main, as verified below; this does not claim that protection existed before those merges.
- S11: PASS — This record names the exact merged Build, covers all 24 S-rules, and records tests, human review, Intent results, and remaining stage work. Disposable checks reject a missing result, a failed S-rule, a blocking finding, and an empty Human review section.
- S12: PASS — Review found the additional-dependency gap in the initial Build. Six regressions failed before PR #18 corrected it; this Proof tests the corrected merge. Stale-Build tests reject earlier evidence, and no passing Proof was recorded for the initial Build.
- S13: PASS — The live Ship entry gate rejects unfinished Proof task #15. The current-proof shipment test accepts a complete record; a disposable failed-delivery check rejects Result: failed. The Ship skill records the template's delivered default-branch version and final evidence PR.
- S14: PASS — Parent #10 and Ship task #16 remain open after both Build merges. The Ship skill checks every required phase and final Intent result before closure, then records its own merge on the task. This is guided completion, not automatic issue closure.
- S15: PASS — Build task #14 is Done only after its merge, approved permalink, and confirmed review were recorded. Proof task #15 is In progress during verification and becomes In review with its PR; Ship stays Blocked. Status skills report stage and work status separately and name missing gates.
- S16: PASS — Cancelled-parent and cancelled-dependency tests reject advancement. Closed-active-task tests reject invalid active state, and fresh dependency checks run for reopened tasks. The status and Ship skills keep cancellation separate from shipment and require a recorded reason.
- S17: PASS — Staged and full-history tests reject uncommitted approvals, bundled stages, and early violations even after later corrections. The seven added dependency regressions cover every dependency's merge and artifact evidence. The installed CI job runs both local history and live GitHub checks.
- S18: PASS — Timeout, malformed-response, wrong-repository, unavailable-dependency, and stale-artifact tests fail explicitly. Live retries looked up existing #10/#14/#15/#16 records before updating them; no replacement parent, stage task, or PR was created because a response was uncertain.
- S19: PASS — Intent type is available. Live setup first reported missing policy and then configured policy after the owner's explicit configuration approval. Readback verifies the installed checks, review requirements, and admin enforcement; local setup did not silently install them.
- S20: PASS — Explicit-fallback and no-silent-fallback tests require an owner-attributed label mode while preserving merge gates. A controlled inaccessible-setup check reports unverifiable. This repository continues using its existing Intent type.
- S21: PASS — Git comparison against the merged Plan shows no changes to shipped features 001/002 or feature 003's accepted planning artifacts. The Build transition records earlier missing backlinks and actual merged PRs without inventing historical compliance.
- S22: PASS — Bootstrap's document allowlist remains narrow. `test_bootstrap_branch_cannot_change_enforcement` rejects hook or CI changes there; the bootstrap skill directs later feature work into the six-stage sequence.
- S23: PASS — The approved Plan records how to replace the conflicting validator only after its separate merge. The Build record preserves the failing-before evidence and real predecessor merges. PR #18 is an in-scope correction under the same Plan; this Proof began after that correction merged.
- S24: PASS — All 86 tests pass, including unsupported/default branches, wrong-phase plans, deletions, renames, contracts, and history regressions. Current conventions, stage skills, status guidance, glossary, templates, and review policy describe the same six stages. A disposable check also rejects rewriting an already shipped outcome.

## Verification

On 2026-09-08, `make test` passed all 86 tests in the Proof worktree at
Build `54764fe2237ca9098360acc99b13a2fdc0d9df57`, before adding this
artifact. The target also passed Python syntax, shell syntax, and
whitespace checks. [PR #18's CI run][ci] passed both `SDLC history` and
`Template verification` on the correction before merge.

Additional checks used disposable repositories with the same fixture
helpers from the committed tests. Starting from `land_build()`, changing
Blocking findings from none, changing S1 from PASS to FAIL, or emptying
Human review each caused the staged hook to reject Proof. After a valid
fixture Proof commit, a Ship record with Result: failed was rejected.
After a successful fixture Ship commit reached the fixture's main,
changing build.md was rejected as rewriting a shipped outcome. A
controlled API that denied access to setup endpoints returned
unverifiable for every setting. These checks changed no repository code
and are additional walkthrough evidence, not extra permanent tests.

The real `make handoff` for #15 passed after Build task #14 was completed.
The same command for Ship task #16 failed because its Proof dependency is
unfinished. That failure is the expected gate, not a test-suite failure.
No implementation or planning file differs from the named Build in
this Proof worktree; this PR adds only proof.md. Ship must repeat the
freshness and live merge checks after this PR merges.

## Human review

Suraj Chhetry confirmed in the owner conversation on 2026-09-08 that
he personally reviewed both initial Build PR #17 and correction PR #18.
The confirmation and exact approved artifact are recorded on
[Build task #14][build-task]. GitHub's review lists for those PRs were
empty: the evidence is the owner's attributed conversation confirmation,
not a fabricated GitHub approving-review event. Confirmation was
recorded after the merges; no earlier review timestamp is asserted.

Agent review reproduced the initial dependency defect and verified its
correction. That review supplies technical findings, not human approval.
The owner also approved the concrete main-protection configuration in
the same conversation. GitHub readback now confirms:

- Required SDLC history and Template verification checks from the
  GitHub Actions app, with the branch current against main.
- One approving review, stale approval dismissed on changes, and
  approval of the latest push by someone other than its pusher.
- Enforcement for administrators, required linear history, and disabled
  force pushes and deletion of main.

`make setup-check` now reports all four requirements configured.
Protection was installed during this stage; it is not retroactive
review evidence. The approved PR requirements also apply to this Proof
PR. Its eventual review and merge are recorded through [task #15][task].

## PR identity

This Proof was first proposed in [PR #19](https://github.com/kevalabs/ai-native-product-template/pull/19)
using the owner's GitHub credentials. GitHub therefore treated the owner
as its author and prevented his approval from satisfying the review rule.
The replacement uses the `keva-builder[bot]` installation identity for
the latest push and PR creation. Earlier commits and PR #19 remain in
history; the bot identity does not supply human approval. The tested
Build and requirement results remain the same. Task #15 links the
current review PR.

## Intent results

The six success criteria describe stage behavior. They are checked here
without claiming that feature 003 has already completed Ship:

1. Spec, Plan, and Build wait for their approved merged predecessors:
   covered by the merged planning chain and rejected early-stage tests.
2. Proof waits for Build and Ship waits for Proof: verified by this
   worktree's base, its passing entry gate, and the rejected Ship gate.
3. One Intent parent has the six Task stages: verified by the live graph;
   the parent remains open while delivery is unfinished.
4. Reviewers can navigate artifacts and approved versions: active-stage
   backlinks and immutable completion links are present. Legacy planning
   gaps remain explicitly recorded in the Build transition.
5. Local commits, markers, closed issues, and unmerged PRs cannot stand
   in for a completed predecessor: the local and remote negative cases
   pass, including the corrected additional-dependency cases.
6. Guidance, reports, and checks agree on the sequence and missing gate:
   the next gate is review and merge of this Proof, followed by Ship.

No blocking technical finding remains for the corrected Build. Actual
shipment, its evidence PR, and the final parent success check remain
required next-stage work. They have not been marked complete here.

[local-tests]: https://github.com/kevalabs/ai-native-product-template/blob/54764fe2237ca9098360acc99b13a2fdc0d9df57/tests/test_sdlc.py
[remote-tests]: https://github.com/kevalabs/ai-native-product-template/blob/54764fe2237ca9098360acc99b13a2fdc0d9df57/tests/test_github.py
[ci]: https://github.com/kevalabs/ai-native-product-template/actions/runs/34095537798
[build-task]: https://github.com/kevalabs/ai-native-product-template/issues/14
[task]: https://github.com/kevalabs/ai-native-product-template/issues/15
