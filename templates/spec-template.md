# <Feature name> — Spec

**Status:** draft | accepted
**Intent:** link to this feature's intent.md
**Personas served:** <from product/personas.md>
**Capabilities affected:** <files in product/capabilities/ this will
create or change>

## Requirements

Numbered, testable rules (these become capability rules on shipping).
Non-functional needs go here too, as rules with numbers in them —
"S5 search returns in under 300ms with 10k products", never "fast".
Only where this feature differs from the product-wide baselines in
`product/architecture.md`.

- S1 <actor> can <action> when <condition>.
- S2 …

## UX

Reference committed mocks in this feature's `design/` directory.
State what each screen/flow must achieve, not how it is implemented.

## Contract changes

New/changed API surface (core contract, BFF contract). Mark breaking
vs additive. Additive-only while old mobile binaries hold traffic.

## Data changes

New/changed entities and migrations, incl. how existing production
data maps to new semantics.

## Region variance

Anything that differs per region — parameter values, providers,
feature-flag rollout order. Variance goes through the regions registry.

## Acceptance criteria

How we know it works: the tests that must exist and pass, keyed to
S-numbers above.

## Out of scope

What this feature explicitly does not do.

## Open questions

Resolved before or during plan.
