# <Outcome> — Build

**Status:** ready
**Stage:** build
**Outcome:** <NNN-name>
**Phase:** <single or Pn-name>
**Parent issue:** <GitHub Intent issue URL>
**Stage issue:** <GitHub stage Task URL>
**Predecessor PR:** <merged previous-stage PR URL>
**Plan commit:** <full approved Plan commit SHA>
**Verification:** <test, lint, and build results>

<!-- Fill only with verified results. Do not claim passed/delivered while blocked. -->

## Requirement results

<!-- Merged-source delivery records Test + Review here. One line per
     S-rule of the accepted Spec, naming first the test that proves it.
     CI fails on a missing rule, a FAIL, or a test name that appears in
     no declared test path. A runtime-artifact product records these in
     proof.md against its immutable artifact instead. -->

- S1: PASS — <test identifier> <what it asserts>

## Intent results

<!-- Which Intent success criteria this phase makes true, one TRUE or
     OPEN line per criterion, in the intent's order. The outcome's last
     phase cannot leave one OPEN. -->

- TRUE — <criterion, and the evidence that it holds>

## Changes

<Evidence, exact version, and any relevant limits.>

## Transition

<Evidence, exact version, and any relevant limits.>

## Confirmed examples

<For a confirmed prototype: original commit permalink, preserved examples
file, byte comparison, test reader, and actual case results. The tests load
the same Markdown file. Record accepted skips or legacy scope honestly.>

## Delivery preparation

<For merged source: the reviewed merge of this PR is the delivery, and
shipment is an annotated `shipped/<outcome>[-<Pn-name>]` tag on that
merge commit whose message names this PR. Name the tag you will push;
do not invent the future merge SHA.

For a runtime artifact: the artifact recipe and intended staging
destination. Its actual identity or digest and originating merged Build
SHA are recorded in Proof after merge. Preview evidence is optional.>
