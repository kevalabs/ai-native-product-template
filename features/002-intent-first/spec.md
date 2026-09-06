# Start every proposal with intent — Spec

**Status:** accepted
**Intent:** [intent.md](intent.md)
**Phase:** single phase
**Personas served:** template owner, contributor, reviewer
**Capabilities affected:** product/capabilities/sdlc-workflow.md

## Flows

1. A contributor describes a problem and why it matters.
2. The intent stage records it as a draft intent on an artifact branch.
3. The owner accepts the intent before the spec stage begins.
4. Status reports show draft intents as proposed work.

## Requirements

- S1 The template offers no separate idea capture command or inbox.
- S2 Current instructions and reports direct proposed work to draft
  intents and do not require a prior capture or graduation step.
- S3 The removed idea branch is unsupported in local and PR checks.
- S4 Numbered artifact branches accept only their planning files;
  they cannot change the removed inbox through a special exception.
- S5 Accepted requirements, approved plans, bootstrap documents, and
  all other SDLC checks keep their existing behavior.

## States and transitions

Intent draft → accepted → spec → plan → implement → prove → ship.
Draft means proposed; acceptance is still the gate to the next stage.

## Permissions

Owner approval rules stay the same. The proposal capture exception is
removed from branch validation.

## Errors and edge cases

The validator rejects the removed branch name and an inbox change on a
numbered artifact branch. Existing shipped records remain historical.

## UX

The product board has three sections: done, promised, and proposed.
The stakeholder report has no separate inbox section.

## Contract changes

No client-facing contracts change.

## Data changes

The empty inbox is removed. No captured proposals need migration.

## Region variance

None.

## Acceptance criteria

- S1–S2: inspect skills, README, conventions, and report instructions;
  search active guidance for stale command, inbox, and graduation links.
- S3–S4: test local and PR rejection of the removed branch and inbox
  exception, including a numbered artifact branch with valid documents.
- S5: make test passes the complete remaining workflow suite.

## Out of scope

Rewriting shipped feature history, changing human approval gates, and
replacing the removed inbox with another command or storage location.

## Open questions

None. These requirements reflect the owner's requested cleanup.
