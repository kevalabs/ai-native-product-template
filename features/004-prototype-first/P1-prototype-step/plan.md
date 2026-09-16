# Confirm a prototype before writing its spec — Plan

**Stage:** plan
**Outcome:** 004-prototype-first
**Phase:** P1-prototype-step
**Parent issue:** https://github.com/kevalabs/ai-native-product-template/issues/22
**Stage issue:** https://github.com/kevalabs/ai-native-product-template/issues/27
**Predecessor PR:** https://github.com/kevalabs/ai-native-product-template/pull/45

**Status:** approved
**Approved by:** Suraj Chhetry, explicitly approved in the owner conversation on 2026-09-16: "yea approve".
**Spec:** [spec.md](spec.md)
**Branch:** feature/004-P1-prototype-step

## Approach

Put the shared prototype rules in `docs/agentic-sdlc.md`. Add a
`prototype` skill, a prototype-note template, and an examples template.
Each existing stage skill explains its own actions and links to the
shared rules. Contributors should find one explanation of confirmation,
preserved evidence, and delivery, without maintaining the same full
instructions in every skill.

The owner approved this approach. Repeating the
whole workflow in each skill would make each file self-contained, but
would make conflicting instructions more likely. A new validator or
automation command would make some checks automatic, but would cross
the accepted phase boundary: P1 changes docs, skills, and templates only.

The Plan starts from `e384371a2d7bdb2209db811e0fe8eb5ab8acf33b`, the
merged Spec from PR #45. The live entry gate for Task #27 passed on
2026-09-16. The accepted Intent came through PR #43. P1 has no phase
dependency. P2 and P3 depend on P1 and retain their own Specs and Plans.

### A reviewable prototype record

The new note template uses standalone bold Markdown headers, matching
the repository's existing artifact style. It defines these fields:

- `Outcome`, `Phase`, and `Intent`: the governing accepted outcome,
  exact phase, and merged Intent permalink.
- `Version`, `State`, `Created at`, and `Expiry days`: the version
  label, Spec state, timestamp with UTC offset, and default 30-day age.
- `Prototype form`: one or more of `screen walkthrough`, `worked
  example`, and `integration trial`.
- `Prototype commit`, `Retained ref`, `Evidence`, and `Examples`: the
  full demonstrated commit, a retained remote ref, and exact locations
  of the demonstration evidence and named examples.
- `Confirmed by`, `Confirmed at`, and `Confirmation source`: the
  owner's identity, dated decision, and attributable source. Leave
  these unfilled until confirmation actually happens.

Short sections describe what to run, the named cases, available user
feedback and its effect on the decision, the decision or rejection,
and any refresh. A failed named case prevents `ready`. A missing form
or confirmation field prevents treating the version as confirmed.
User feedback never supplies the owner's approval.

Commit the runnable version and examples before asking for confirmation.
The confirmation cites that earlier full commit; it does not try to
contain its own commit hash. Record the decision separately afterward.
Keep the confirmed or rejected version and decision unchanged. A change
after either decision receives a new version and new confirmation.

Keep a remote ref reaching the confirmed commit until the phase ships,
and record that ref. Preserve the confirmation record as well. Do not
depend on an unreferenced commit remaining available after branch
deletion. The guide recommends retaining a tag if the working branch
will be removed; never move an existing retained tag to another version.
Review verifies reachability and access. P1 adds no tag protection or
automatic retention service, and chooses no prototype branch naming rule.

Compute age from the note's recorded creation time and the product's
declared expiry period. Show expiry as a warning, not a failed check.
An expired version needs an explicit refresh before returning to ready;
do not erase the original dates or silently renew a confirmation.
Before accepting an aged Spec, record renewed confirmation or the
owner's explicit acceptance of its age. Spec acceptance freezes that
confirmation and ends its expiry requirement.

### Preserve examples without promoting prototype code

Use the existing exact-phase `design/` allowance for preserved evidence.
The examples template produces a Markdown file with named cases in one
JSON code block. Each case has an `id` and `form`, with the relevant
scenario and sample data, inputs and expected outputs, or service
success and failure expectations. The same file can carry several forms.
Products add their domain fields without changing confirmed case data.

The prototype uses that examples file as input to its demonstration.
During Spec preparation, copy the confirmed file byte for byte to
`design/prototype-examples.md`. Preserve supporting Markdown and images
under `design/` using the formats the current artifact validator allows.
Do not copy runnable prototype source or its working note into main.

Add a `Prototype confirmation` section to the Spec template. It records
the form, full commit, retained ref, evidence and examples locations,
confirmer, date, source, and any age acceptance. Alternatively it holds
one concrete skip reason for an outcome with nothing meaningful to
inspect. Owner acceptance of the Spec also accepts that skip.

The Plan template names the exact preserved examples file and how Build
tests will load it. Build tests read that file's JSON block directly;
they do not silently rewrite it as separate fixture data. Build records
the original and preserved locations and verifies identical content.
Changed examples require renewed confirmation or an accepted Spec
revision before Build continues. No common loader library or new file
extension allowance is introduced in P1.

This fits the current checks: Spec PRs already permit Markdown and
images in the same phase's `design/` directory. A plain JSON fixture in
that directory is currently rejected. Keeping structured data inside
Markdown avoids changing enforcement in this documentation phase.

### Carry the same version through Proof and Ship

Update current workflow diagrams and instructions together. Intent,
Spec, Plan, Build, Proof, and Ship retain their separate reviewed PRs.
Prototype sits between Intent and Spec with owner confirmation; it
does not add a merged stage PR or another mandatory tracking task.

Every stage PR targets main. Describe a feature preview as optional,
and a main merge as integration of the source. Products build an
immutable artifact from the merged Build commit for staging. Proof
records its identity, tests that version, and compares it with the
merged Build. Ship promotes the same artifact without rebuilding it.

Build, Proof, and Ship templates add space for the artifact identity
or digest, originating Build commit, destination, and result evidence.
If the artifact is produced after Build merges, its actual identity
is first recorded in Proof; the Build record cannot predict its future
merge SHA. A mismatch blocks Proof. An unavailable proved artifact
or a destination requiring a different rebuild blocks Ship.

This template has no deployed runtime. Its immutable source version is
the delivery artifact, and reviewed availability on the default branch
remains delivery. Its separate Proof and Ship records still apply.
P1 does not configure a deployment provider or change remote policy.

### Release limits and adoption

P1 supplies instructions and human review checks. It does not teach
contributors to skip hooks, bypass an approved Plan, or commit prototype
code on today's artifact branches. This repository's new prototype
branch lane and sandbox enforcement become available only through P2.
Until then, the new skill must state this limitation if a requested
prototype has no already authorized place to run. Templates and review
exercises can be used without claiming that the future lane exists.

The glossary defines prototype, sandbox, worked example, screen
walkthrough, integration trial, prototype note, and prototype
confirmation. Add a short `Prototype settings` section to AGENTS.md
for the default expiry period and the planned sandbox declaration.
Leave sandbox paths and exemption rules to P2; an unconfigured section
does not grant permission to write prototype code anywhere.

Bootstrap preserves the shared rules, asks about a different expiry
period, and records unresolved sandbox setup rather than inventing a
path. Capability rules describe P1's manual behavior and these release
limits. Keep R24's lack of background lifecycle automation; P3 owns
that change. Existing accepted Specs and shipped chains are not
back-filled. P1's own already accepted Spec retains its real history.

## Touched surface (collision check)

No other active Plan is present on fetched main. Plans 001 and 002
record completed historical work; feature 003 records them as shipped
and has its own delivered Ship record. Their old broad path lists are
not active reservations. P2 and P3 have no Plans yet. Recheck this at
Build entry; sequence any new overlap through review before editing.

The Plan PR changes only this file:

- features/004-prototype-first/P1-prototype-step/plan.md

The Build creates these files:

- .agents/skills/prototype/SKILL.md
- templates/prototype-template.md
- templates/prototype-examples-template.md
- features/004-prototype-first/P1-prototype-step/build.md

The Build updates these files:

- docs/agentic-sdlc.md
- AGENTS.md
- README.md
- REVIEW.md
- features/README.md
- .githooks/README.md
- product/architecture.md
- product/glossary.md
- product/capabilities/sdlc-workflow.md
- .agents/skills/intent/SKILL.md
- .agents/skills/spec/SKILL.md
- .agents/skills/plan/SKILL.md
- .agents/skills/build/SKILL.md
- .agents/skills/proof/SKILL.md
- .agents/skills/ship/SKILL.md
- .agents/skills/bootstrap-product/SKILL.md
- .agents/skills/feature/SKILL.md
- .agents/skills/product-status/SKILL.md
- templates/spec-template.md
- templates/plan-template.md
- templates/build-template.md
- templates/proof-template.md
- templates/ship-template.md

These are 27 Build files serving one workflow. Most changes are short
links, fields, or corrections to the same stage sequence. Target about
800–1,100 changed lines and stay below the Intent's roughly 1,500-line
limit. If the change grows beyond one review sitting, stop and revise
the phase split rather than expanding this Plan during Build.

Architecture changes cover the workflow and delivery wording only;
leave product architecture placeholders intact. Do not modify scripts,
tests, CI, Makefile, packages, pointer files, or historical feature
artifacts. The separate Proof and Ship PRs later create their own
phase records; those files are not part of this Build.

External tracking is limited to the existing P1 stage tasks, PR links,
and completion evidence. No new issue automation or administrator
settings are part of this Plan. P2 and P3 must reuse the settled terms
and evidence fields and declare their own touched files.

## Steps

1. **Prove the evidence handoff.** Add the note and examples templates,
   the shared guide's evidence rules, and the Spec instructions. Use a
   disposable fixture to copy one confirmed Markdown examples file
   into an exact phase's design directory. Verify that the existing
   artifact validator accepts it and that a test-side JSON reader
   consumes identical case data. Check rejection of copied executable
   prototype source. Record actual results in build.md and update the
   capability's implemented behavior and limits. Run `make test`.
2. **Make confirmation usable.** Add the prototype skill and remaining
   note lifecycle guidance, glossary terms, expiry settings, bootstrap
   instructions, and review checks. Walk screen, calculation, service,
   and mixed examples through ready, confirmed, rejected, and expired
   states. Include missing fields, unavailable evidence, a changed
   commit, and a justified skip. Run `make test`.
3. **Carry examples and delivery evidence forward.** Update Plan,
   Build, Proof, and Ship skills and templates as one path. Demonstrate
   tests loading the preserved examples and rejecting changed data.
   Walk a product artifact through staging, Proof, and Ship, including
   mismatched and unavailable artifact cases. Also walk the template's
   source-only delivery. Run `make test`.
4. **Align every entry point.** Update conventions, newcomer guidance,
   the ledger guide, gate guide, architecture, and status skills.
   Make the optional prototype skip and the P1 release limits visible.
   Check all active workflow diagrams and commands for conflicting
   instructions. Complete build.md, compare the full diff with this
   touched surface, and run `make test` and stage history checks before
   opening the separate Build PR.

## Migrations

There is no database or product-data migration. Adopt at the next
outcome or phase that has not begun its Spec. Keep existing accepted
Specs, confirmed evidence, and shipped history unchanged. Record any
remaining adoption limit without inventing older confirmations.

Preserve the reviewed examples when changing stages; do not rename or
rewrite them as part of adoption. Products retain the prototype commit
and its confirmation until shipment, then follow their retention policy.
P3's final Ship supplies the full cross-phase adoption note required by
the Intent; P1 documents its own prerequisites and manual steps now.

Before release, correct a failed scenario through a reviewed Build
change and repeat its verification. If a rollback is needed after
adoption, restore the previous guidance through reviewed changes and
keep already accepted evidence reachable. Do not delete evidence,
rewrite shipped artifacts, or disable checks to complete a rollout.

## Test plan

The change is documentation behavior. Use named manual acceptance
exercises, temporary files, and the existing checks; add no product
tests to prototype code and no tests that merely search for wording.
Record each exercise's inputs, expected result, observed result, and
evidence in build.md. Proof repeats the relevant exercises against
the exact merged Build. Example owner decisions in exercises are
clearly marked synthetic and never recorded as real approval.

Run the evidence handoff exercise first because the allowed file
formats are the highest-risk assumption. Every Spec rule has this
verification:

- S1 / T1: attempt startup with an unmerged Intent, then a verified
  merged Intent; the written procedure blocks only the first.
- S2, S3 / T2: classify screen, calculation, service, and mixed cases;
  require every applicable form.
- S4 / T3: review a test-bearing prototype and a test-free runnable
  demonstration; require removal of prototype tests only in the first.
- S5 / T4: remove one required example element from each form and
  verify that the readiness review identifies the missing part.
- S6 / T5: user feedback alone leaves the version unconfirmed; an
  owner decision records how that feedback affected confirmation.
- S7 / T6: omit each confirmation field in turn; none of the resulting
  records is sufficient to unlock Spec drafting.
- S8 / T7: propose changes to both confirmed and rejected versions;
  both require a new version without modifying the prior record.
- S9 / T8: resolve the retained ref from a fresh clone, compare the
  preserved examples byte for byte, and inspect the Spec diff for
  prototype code. Repeat after deleting only the disposable work ref.
- S10 / T9: a placeholder Task is allowed; substantive Spec drafting
  needs confirmation or the concrete skip reason.
- S11, S12 / T10: use dates just before and at 30 days, plus a declared
  alternate period. Exercise refresh, warning, reconfirmation, explicit
  age acceptance, and an already accepted Spec whose age is irrelevant.
- S13, S14 / T11: unavailable evidence blocks review; a pure-refactor
  skip with nothing meaningful to inspect can be accepted by the owner.
- S15 / T12: a temporary test-side reader consumes the preserved file;
  changing a case requires renewed confirmation or a Spec revision.
- S16 / T13: review synthetic examples marked as forbidden production
  data or secrets, and require replacement; use no actual private data.
- S17 / T14: inspect stage commands and diagrams for main-targeted PRs
  and the absence of environment branches as deployment state.
- S18 / T15: trace optional preview, merged Build source, immutable
  staging artifact, Proof, and promotion of that same artifact. Repeat
  for this template's source-only delivery.
- S19 / T16: search all active docs, skills, and templates for conflicting
  sequences, preview rules, and delivery claims; inspect each match.
  Exclude immutable historical feature chains from rewrites.
- S20 / T17: a no-form case records a concrete skip without an empty
  prototype; an ordinary screen change cannot claim that skip.
- S21 / T18: omit the integration form from a mixed case; review names
  the omission and blocks confirmation of incomplete evidence.
- S22 / T19: a confirmation for a different commit cannot unlock Spec.
- S23 / T20: losing access to preserved evidence blocks Spec acceptance
  even when a prior demonstration and confirmation are recorded.
- S24 / T21: a failed named scenario prevents ready status.
- S25 / T22: Proof rejects an artifact whose source or identity differs
  from the merged Build record.
- S26 / T23: Ship remains unsuccessful when the destination cannot
  receive the exact proved artifact; rebuilding does not cure the case.

`make test` remains the regression gate for existing enforcement.
Its current 86 tests do not prove the new manual prototype rules.
Do not describe the P1 instructions as automated validation. Inspect
relative links, template field agreement, the new skill's discovery
path, and the complete changed-file list during review.

## Rollout

Owner approval is recorded above. Commit this file alone as the
branch's first commit. Open its Plan-only PR and record that PR on
Task #27.
Human review and merge precede Build task #28 and its fresh worktree.

The Build updates the capability in the same PR and records the manual
enforcement limits. After its merge, Proof task #29 verifies the exact
merged content. Ship task #30 follows the merged passing Proof. Only
then does P1 unlock its dependent phases. No feature flags, regional
rollout, runtime deployment, or changes to repository policy are needed.

The parent Intent remains open: P2's sandbox lane, P3's automation, and
the final adoption note are still required for the full outcome.
