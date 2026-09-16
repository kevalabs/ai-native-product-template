---
name: prototype
description: Demonstrate screens, rules, or outside-service behavior after an accepted Intent merges, and record owner confirmation of the exact prototype before Spec. Use when asked to prototype a named outcome or phase; this does not authorize a new branch lane or production Build.
---

Prepare the prototype for the named outcome and exact phase. Derive them
from context when clear; otherwise ask. Read its accepted Intent, phase
dependencies, AGENTS.md, and the
[shared prototype rules](../../../docs/agentic-sdlc.md#prototype-before-spec).
The shared guide defines forms, confirmation fields, age, retention, and
the evidence that Spec preserves. Use it rather than inventing a second
record format.

1. Verify the accepted Intent PR merged and required phase prerequisites
   passed. Use the existing stage tracking and live evidence commands;
   do not create a seventh stage task or pretend the note is a stage PR.
   Before writing prototype code, identify an already permitted workspace
   under the product's policy. P1 does not install a prototype branch
   lane or sandbox enforcement. If none exists, report that limit and
   stop code work until P2 or separately authorized product setup. Never
   bypass hooks, the approved-Plan rule, or artifact branch restrictions.
2. Select every applicable form: screen walkthrough, worked example,
   integration trial. If there is nothing meaningful to inspect, propose
   a concrete one-line Spec skip; the owner accepts it with the Spec.
   Do not use missing time, evidence, or a demo as a skip reason.
3. Use [the note template](../../../templates/prototype-template.md) and
   [examples template](../../../templates/prototype-examples-template.md)
   outside main. Make the demonstration read the examples file. Use
   synthetic data and test services. Add no automated product tests or
   coverage requirement to the disposable prototype. Run all named cases
   manually; missing data, an omitted form, or a failed case blocks ready.
4. Commit the runnable version and examples, then invite available user
   feedback and the owner's decision about that exact full SHA. Only the
   owner confirms or rejects; record the real source, person, date, and
   how available user feedback affected the decision. Never fill approval
   fields from a guessed answer or from an agent's own review.
5. Preserve final versions and decisions. A change after confirmation or
   rejection needs a new version and new confirmation. Apply the guide's
   age warning and explicit refresh rules without rewriting original dates.
   Keep a recorded remote ref reaching the commit and preserve the decision
   source until shipment. Do not delete the only ref when tidying branches.
6. Hand Spec the exact commit, confirmation, retained ref, evidence, and
   original examples file. Spec preserves permitted evidence and the file
   byte for byte, without merging the working note or prototype source.
   An incomplete or inaccessible record does not unlock substantive Spec.

Keep this work disposable. Production behavior is implemented independently
under the later approved Plan. Do not promote prototype code to main.
