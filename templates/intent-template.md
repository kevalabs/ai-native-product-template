# <Feature name> — Intent

**Status:** draft | accepted
**Originator:** <who>
**Date:** <yyyy-mm-dd>
**Due:** <yyyy-mm-dd only if someone committed to a date and can say
why (contract, regulation, event) — otherwise "—". A wish is not a
due date.>

The intent answers WHY. It names the outcome we want and how we will
know we got it. No screens, no tables, no endpoints — those are spec
and plan.

## Problem

What is broken or missing today, for whom, and how do we know?
State the problem, not the solution.

## Outcome

What is true after this ships? One outcome, stated as something a
person can do or a state the system reaches — "a new salon owner can
finish setup and get approved before going live", never "build the
onboarding pages".

## Actors

Who acts in this outcome and who benefits (personas from
`product/personas.md`, plus "the system" where it acts on its own).
An outcome with several actors usually has several phases below.

## Success criteria

How we know the intent is achieved, in three to six lines a person
could check. These are the questions the final review asks after the
last phase ships — not the detailed rules (those are S-rules in the
spec).

- <the owner can … and sees …>
- <the metric / complaint / incident that goes away>

## Phases

The outcome, cut into pieces a human can review one PR at a time.
Cut by outcome, actor, or state change — never by page or screen.
Most intents are one phase; write "Single phase" and stop. When
there are several, list them in order with their actor and what each
depends on. Accepting this intent also accepts this split.

- Single phase — this intent ships as one spec, one plan, one PR.

<!-- multi-phase form:
- P1 <short-name> — <actor> can <outcome>. Depends on: —
- P2 <short-name> — <actor> can <outcome>. Depends on: P1
- P3 <short-name> — <actor> can <outcome>. Depends on: P1 (can run
  alongside P2)

Shared ground — settled before phases run in parallel, and where:
- <the state names every phase uses> → defined in P1's spec
- <the terms> → product/glossary.md
- <who owns which data> → P1's spec
- <any contract in packages/> → its own contracts chain, NNN
-->

## Affected systems

Which deployables/regions this touches (core / console / customer app /
regions registry / contracts).

## Constraints

Deadlines, regional differences, compliance, dependencies on other
chains.

## Open questions

What must be resolved before or during spec.
