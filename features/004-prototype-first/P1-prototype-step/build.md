# Confirm a prototype before writing its spec — Build

**Status:** ready
**Stage:** build
**Outcome:** 004-prototype-first
**Phase:** P1-prototype-step
**Parent issue:** https://github.com/kevalabs/ai-native-product-template/issues/22
**Stage issue:** https://github.com/kevalabs/ai-native-product-template/issues/28
**Predecessor PR:** https://github.com/kevalabs/ai-native-product-template/pull/46
**Plan commit:** 03c2171cddcce20b2f067c297f2d7571ebd6fcbc
**Verification:** make test passed all 86 tests; evidence handoff exercises and manual S1–S26 walkthroughs completed; all 10 changed skills passed quick_validate.py.

## Changes

Implement the shared prototype guide, skill, evidence templates, and
stage instructions under the approved P1 Plan. P2 owns sandbox and
branch enforcement; P3 owns lifecycle automation.

The guide owns confirmation, state, age, retention, preserved examples,
and delivery rules. Stage skills link to it and describe their own work.
New prototype note and examples templates supply the records; Spec keeps
the confirmed examples as Markdown with a single JSON block. Plan and
Build name the same file and reader. Proof and Ship record immutable
artifact identity and originating Build source.

Conventions, review policy, architecture, bootstrap, status skills, and
workflow diagrams use the same sequence. Capability R10 now includes the
prototype step; R26–R33 describe its manual review behavior and delivery
rules. R24 still states that background lifecycle automation is absent.
All changes stay within the Plan's 27 Build files. There are no changes
to validators, regression tests, CI, packages, or historical artifacts.

## Transition

Started from merged Plan PR #46 at the Plan commit above. The live entry
gate for Task #28 passed on 2026-09-16. Accepted Spec PR #45 and Intent
PR #43 are on the base. Their current tasks retain completion evidence.
No historical artifact or existing accepted Spec is back-filled.

P1 installs no prototype branch lane or sandbox enforcement. The new
skill requires an already permitted workspace and reports missing setup
instead of bypassing the current gates. Expiry, retention, confirmation,
and evidence review remain manual. The completed behavior is guidance;
P1 shipment still requires separate Proof and Ship. The parent remains
open for P2, P3, and the final adoption note.

## Verification exercises

These are Build verification, not the later Proof record or human PR
approval. Cases below use synthetic inputs and synthetic owner decisions;
none records an actual prototype confirmation. The current template's
accepted Spec predates this feature and needs no retroactive prototype.

### Executed evidence handoff

Used the examples template's four cases: empty screen list, count inputs
`[2, 3]` with total `5`, and provider success/failure cases. The documented
JSON reader loaded all four cases from the same Markdown file. A changed
expectation of `6` disagreed with the computed total and was detected.

Using the existing disposable-Git fixture from `tests/test_sdlc.py`, added
an accepted synthetic P1 Spec and its copied `design/prototype-examples.md`
on an artifact branch. The unchanged full history validator accepted it.
Adding `design/demo.py` produced the expected rejection. The copied
examples matched the source bytes exactly. No production hook was skipped
or changed; the fixture's isolated Git history was used only for this test.

In a separate temporary source repository, committed those example bytes,
then a synthetic decision note citing the earlier commit. Retained a tag
on the decision commit, pushed to a temporary bare remote, and deleted the
working branch. A fresh clone resolved the retained tag, the earlier
prototype commit, and the same examples bytes. This proves the proposed
retention procedure without relying on an unreachable SHA. No tag
protection or automatic retention service is claimed.

Reproduction: use the existing `WorkflowTests` fixture to commit the
phase Spec and copied Markdown, then invoke its `history` helper with
`artifact/001-demo`; repeat after adding executable source and expect
failure. In another temporary Git repository, commit examples and a
synthetic decision, tag the latter, push both branch and tag to a local
bare remote, delete only the branch, and clone again. Compare
`git show <prototype-sha>:examples.md` with the original bytes and run
the reader shown in the shared guide. Temporary harnesses and logs are
not repository dependencies; Proof can repeat these steps independently.

### Manual procedure walkthroughs

Applied the shared guide, skill steps, templates, and review policy to
each case below. “Blocked” means the written procedure and reviewer
decision block advancement, not a new automated validator. Every expected
disposition was present and usable in the completed guidance.

| Case / rules | Synthetic input and expected result | Observed disposition and evidence |
|---|---|---|
| T1 / S1 | Unmerged Intent, then accepted merged Intent | First blocks startup; second permits the workspace check. Prototype skill step 1. |
| T2 / S2, S3 | Screen, sum, provider, and mixed behavior | Selected walkthrough, worked example, trial, and all three respectively. Guide “Run and confirm”; examples template. |
| T3 / S4 | Runnable demo with a unit test, then no product tests | Review requires the test removed; the runnable test-free demo can proceed. REVIEW.md prototype exception. |
| T4 / S5 | Omit screen sample data, expected calculation output, or provider failure case | Each omission prevents ready; the template identifies the missing data. Guide readiness list. |
| T5 / S6 | User feedback alone; then synthetic owner confirmation | Feedback does not confirm; the owner decision records its effect. Note Feedback and Decision sections. |
| T6 / S7 | Omit form, commit, evidence, examples, owner, date, or source one at a time | Every incomplete record blocks confirmation/Spec. Guide confirmation list and Spec skill entry instructions. |
| T7 / S8 | Edit a confirmed version; edit a rejected version | Both require a new version and retain the old record unchanged. Guide state rules and note Refresh section. |
| T8 / S9 | Retained tag, deleted working branch, copied examples, and copied source | Fresh clone and byte comparison pass; executable source fails the existing check. Executed exercise above. |
| T9 / S10 | Tracking placeholder versus substantive Spec with neither confirmation nor skip | Placeholder is allowed; drafting is blocked. Spec skill and confirmation section. |
| T10 / S11, S12 | Note dated 2026-08-01T00:00:00Z, evaluated at 29 and 30 days; 7-day override at 6 and 7 days | UTC arithmetic gives warnings at each configured limit, not before. Refresh preserves age. A 30-day-old Spec needs reconfirmation or explicit age acceptance; an accepted Spec has no expiry. Guide age rules. |
| T11 / S13, S14 | Unavailable evidence; pure refactor preserving all behavior | Missing evidence blocks. A concrete no-behavior skip is available and needs owner Spec acceptance. Guide Spec rules. |
| T12 / S15 | Preserved sum case expects 5; altered copy expects 6 | Reader consumes the same file; changed data is detected and needs renewed confirmation or Spec revision. Executed exercise and Build skill. |
| T13 / S16 | Examples labelled as containing production secrets or real personal data | Review rejects the proposed data and requires synthetic replacements. No real secret or personal data was used. Prototype skill step 3 and REVIEW.md. |
| T14 / S17 | Stage PR and a proposed long-lived environment branch | Stage instructions target main; environment branch proposal is rejected as deployment state. Delivery guide and architecture. |
| T15 / S18 | Optional preview P, merged Build M, staging artifact A; then template source M | Preview does not satisfy Proof. Proof tests A from M; Ship promotes A. Template uses source M as its artifact. Delivery guide and evidence templates. |
| T16 / S19 | All active entry points and diagrams | Updated sequence and delivery language agree. Six merged stage PRs remain; prototype uses confirmation or skip. Historical chains excluded from edits. |
| T17 / S20 | Pure refactor with nothing to demonstrate; screen change lacking a demo | Refactor records a concrete skip without an empty prototype; missing screen demo does not justify skipping. Guide Spec rules. |
| T18 / S21 | Mixed screen/service case omits the trial | Missing integration form prevents ready and cannot produce complete confirmation. Prototype skill steps 2–3. |
| T19 / S22 | Confirmation cites commit A while the presented version is B | Spec remains blocked. Guide confirmation and Spec skill checks. |
| T20 / S23 | Prior demonstration succeeded but preserved evidence is inaccessible | Prior confirmation is insufficient; Spec acceptance is blocked. Guide “Freeze the evidence in Spec”. |
| T21 / S24 | One named provider failure case cannot run | Version stays out of ready. Guide readiness check and prototype skill step 3. |
| T22 / S25 | Proof receives artifact B instead of A, or A names source N instead of M | Both mismatches block Proof; identity and source fields make the comparison explicit. Proof skill and template. |
| T23 / S26 | Destination cannot accept A without rebuilding, or A is unavailable | Ship remains unsuccessful; a rebuilt artifact needs reviewed Build work and renewed Proof. Ship skill and template. |

## Confirmed examples

The exercised examples are synthetic template data, not an owner-confirmed
prototype for this already accepted Spec. Their source is
`templates/prototype-examples-template.md`; their destination was the
temporary fixture's `features/001-demo/P1-example/design/prototype-examples.md`.
The byte comparison and test-side reader passed as described above.

## Delivery preparation

This is a source-only template change. The eventual merged Build SHA is
the immutable artifact identity; no runtime deployment or new provider
is introduced. Proof records and verifies that actual merged version.
Ship follows passing merged Proof and records delivery to main.
