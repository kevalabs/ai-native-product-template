# <Feature name> — Spec

**Stage:** spec
**Outcome:** <NNN-name>
**Phase:** <single or Pn-name>
**Parent issue:** <GitHub Intent issue URL>
**Stage issue:** <GitHub stage Task URL>
**Predecessor PR:** <merged previous-stage PR URL>

**Status:** draft | accepted
**Intent:** link to this feature's intent.md
**Personas served:** <from product/personas.md>
**Capabilities affected:** <files in product/capabilities/ this will
create or change>

The spec answers WHAT. Someone who knows the product should
understand every line without knowing how it is built. No tables,
endpoints, components, or services — those belong in `plan.md`.

## Flows

The paths through this phase, one per actor, as numbered steps in
plain words: what the actor does, what they see, what happens next.
User stories ("as a salon owner, I want …") are welcome here where
they help; they are not the unit of work.

## Requirements

Numbered, testable rules (these become capability rules on shipping).
Non-functional needs go here too, as rules with numbers in them —
"S5 search returns in under 300ms with 10k products", never "fast".
Only where this feature differs from the product-wide baselines in
`product/architecture.md`.

- S1 <actor> can <action> when <condition>.
- S2 …

## States and transitions

The states a thing in this phase can be in, which actor or event
moves it between them, and which states are final. Multi-phase
chains: the phase that introduces a state model defines it here;
later phases cite it and never redefine it.

<state> → <state> → <state> | <terminal states>

## Permissions

Who may do what, by persona. Say what happens when someone without
permission tries.

## Errors and edge cases

What the actor sees when a rule fails, a precondition is missing, or
input is invalid. Each is an S-rule too — silence about an error path
is a spec bug.

## UX

Reference committed mocks in this feature's `design/` directory
(low-fidelity is enough). State what each screen/flow must achieve,
not how it is implemented.

## Contract changes

What other systems or clients can newly see or do, and what changes
for them. Mark breaking vs additive. Additive-only while old mobile
binaries hold traffic. Shape and wire format are plan-level.

## Data changes

What the product must newly remember, or remember differently, and
how EXISTING records read under the new rules ("orders placed before
this ships count as `delivered` on their old date"). "No existing
data affected" must be an explicit claim. Tables and migrations are
plan-level.

## Region variance

Anything that differs per region — parameter values, providers,
feature-flag rollout order. Variance goes through the regions registry.

## Acceptance criteria

How we know it works: the tests that must exist and pass, keyed to
S-numbers above. Review proves the PR against this list.

## Out of scope

What this feature explicitly does not do.

## Open questions

Resolved before or during plan.

<!-- On owner approval, add **Accepted by:** with the person and actual approval source. -->
