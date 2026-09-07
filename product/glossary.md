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

## Process (AI-native SDLC — generic)

- **Intent** — the problem and desired outcome. Its parent GitHub issue
  has type Intent and stays open until the whole outcome ships.
- **Spec** — testable behavior requirements for one outcome or phase.
- **Plan** — approved implementation approach and touched files. It
  lands in a Plan-only PR before Build starts.
- **Build** — implementation and its verification under a merged Plan.
- **Proof** — Test + Review of the exact merged Build against the Spec
  and Intent, recorded in its own artifact and PR.
- **Ship** — delivery of the proved version and merged delivery evidence.
- **Stage task** — a Task sub-issue tracking one stage, its artifact,
  owner, dependencies, approval, and merged PR.
- **Artifact branch** — a branch reviewing one Intent or exact-phase Spec.
- **Feature** — one numbered outcome directory, immutable after Ship.
- **Capability** — current implemented behavior, updated with the Build
  that changes it and stating any remaining release restrictions.
