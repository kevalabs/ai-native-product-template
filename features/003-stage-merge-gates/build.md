# Review linked outcomes and merge each stage before advancing — Build

**Status:** ready
**Stage:** build
**Outcome:** 003-stage-merge-gates
**Phase:** single
**Parent issue:** https://github.com/kevalabs/ai-native-product-template/issues/10
**Stage issue:** https://github.com/kevalabs/ai-native-product-template/issues/14
**Predecessor PR:** https://github.com/kevalabs/ai-native-product-template/pull/9
**Plan commit:** 1e8fce64077f1b5c90fe344c20afe7236ef74bb5
**Verification:** make test passes 79 tests plus syntax and whitespace checks; skill and YAML validation passes; the live Plan-to-Build handoff passes.

## Changes

Separate stage scopes and merged prerequisites replace the old
plan-and-build PR rule. A read-only GitHub adapter checks linked tasks,
actual predecessor merges, approved artifact versions, and setup.
Stage skills and templates support Intent through Ship with readable
artifact links, proof freshness, and explicit shipment completion.

## Transition

Feature 003 adopts issue tracking at Build. The earlier Markdown
artifacts have no issue backlinks; their actual approval and merge
records remain unchanged. Newly created tasks record that history:

- Intent: [PR #6](https://github.com/kevalabs/ai-native-product-template/pull/6),
  commit f33a83dc12af7ababb214249e3fc8a8611132c69;
  [task #11](https://github.com/kevalabs/ai-native-product-template/issues/11).
- Spec: [PR #7](https://github.com/kevalabs/ai-native-product-template/pull/7)
  reviewed requirements; [PR #8](https://github.com/kevalabs/ai-native-product-template/pull/8) recorded their acceptance,
  commit 5c022e920eb5a45bbaf209618e4cedad258b5c41;
  [task #12](https://github.com/kevalabs/ai-native-product-template/issues/12).
- Plan: [PR #9](https://github.com/kevalabs/ai-native-product-template/pull/9),
  commit 1e8fce64077f1b5c90fe344c20afe7236ef74bb5;
  [task #13](https://github.com/kevalabs/ai-native-product-template/issues/13).

This Build began from the merged Plan. The old validator failed the
new regression for a Plan already on the PR base and allowed a bundled
Intent/Spec PR. Both failures were observed before changing it.
The replacement runs through the existing hook and required CI path;
no hook, job, or approval gate was disabled. Features 001 and 002 remain
unchanged historical records.

## Verification evidence

- Before implementation, the old validator rejected a Build with its
  Plan already on the base and allowed bundled Intent/Spec changes.
  Both regression failures were recorded before replacing the rules.
- make test passes 79 tests, Python/shell syntax, and whitespace checks.
  GitHub tests use controlled API responses; no test needs credentials.
- All ten stage skills pass skill validation; workflow and issue-form
  YAML parses and the issue forms retain exact Markdown tracking headers.
- The live handoff check passes for Build task #14 against Plan PR #9.
  Tracking includes one Intent parent and six stage tasks. Historical
  stages are linked to their real approvals, and Proof/Ship are blocked.
- All 37 changed files are declared in the approved Plan. Shipped
  feature 001/002 artifacts and the approved feature 003 Plan/Spec are
  unchanged. No application contracts or dependencies were introduced.
- The setup report finds Intent available, with required checks and
  human review still missing or inaccessible. The direct protection and
  ruleset inspection found no effective main protection. No administrator
  setting was changed and remote enforcement is not claimed.

Proof and Ship remain separate stages. A passing Build suite is not
recorded as completion of their human review or delivery outcomes.

## Release restrictions

The implemented checks become available when this Build merges. The
outcome remains unshipped until separate Proof and Ship PRs complete.
Repository administrators still need to configure required checks and
human review before enforcement can be claimed at the default branch.
