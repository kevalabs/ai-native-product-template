# Glossary — one vocabulary for all agents and humans

Every artifact, schema, API, and test uses these terms exactly. If a
session needs a word that isn't here, adding it to this file is part
of that feature's PR.

## Core domain

<!-- template: one entry per domain noun. Resolve synonyms explicitly —
     pick THE canonical noun and ban the alternatives from schemas and
     APIs (e.g. "appointment is the noun, book is the verb; 'booking'
     never appears as a noun"). Define entities, states, and units. -->

- **{{TERM}}** — {{definition}}

## Roles

<!-- template: user-facing roles and their permission boundaries. Note
     whether one person can hold multiple roles. -->

## Platform roles & surfaces

<!-- template: internal operator roles; one named surface per audience
     (e.g. System console = apps/system, Customer app = apps/customer). -->

## Process (AI-native SDLC — generic, keep as-is)

- **Intent** — problem + desired outcome for one unit of work
  (Stage 1 artifact).
- **Spec** — requirements and design for one feature (Stage 2).
- **Plan** — implementation plan incl. files/apps touched (Stage 3;
  first commit on the feature branch).
- **Feature** — a unit of *change*: one numbered directory in
  `features/`, immutable once shipped.
- **Capability** — a unit of *being*: current shipped behavior, one
  file in `product/capabilities/`, present tense only, updated only by
  shipping PRs.
