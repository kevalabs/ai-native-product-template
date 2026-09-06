# Start every proposal with intent — Intent

**Status:** accepted
**Kind:** change
**Originator:** Suraj Chhetry
**Date:** 2026-09-06
**Due:** —

## Problem

The owner wants every proposal to start by explaining why it matters.
A separate idea command and inbox create another entry point that the
owner no longer wants. The inbox currently contains no captured entries.

## Outcome

Contributors begin proposed work with a draft intent, and the commands,
status reports, and branch rules all describe that same starting point.

## Actors

The owner proposes work; contributors draft intents; reviewers accept
requirements and review implementation.

## Success criteria

- The separate idea skill and inbox are removed.
- Current guidance and status reports start with draft intents.
- The removed idea branch and inbox exception no longer pass checks.
- Existing intent/spec/plan approval gates still work.

## Phases

Single phase — one focused cleanup of the proposal entry point.

## Affected systems

Stage skills, workflow guidance, capabilities, and branch validation.

## Constraints

The owner explicitly requested removal of the idea command and an
intent-first workflow. Preserve shipped feature artifacts as history.
The existing inbox is empty; no user proposals need migration.

## Open questions

None within the requested scope.
