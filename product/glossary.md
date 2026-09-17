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
  and Intent. For merged-source delivery it is recorded in the Build
  record and its approving review; for a runtime artifact it has its own
  artifact and PR.
- **Ship** — delivery of the proved version and its recorded evidence.
- **Fix** — a change that makes the product do what a shipped Spec or
  capability rule already says. It adds and changes no rule.
- **Fix lane** — the one reviewed PR a fix lands in, on a
  `fix/short-name` branch, with no intent, spec, plan, or shipment
  record.
- **Fix record** — the numbered Markdown file under `fixes/` naming a
  fix's failing test, the outcome it corrects, and the rule it restores.
- **Delivery mode** — a product's declared `merged source` or
  `runtime artifact` setting, which decides where Test + Review and Ship
  evidence lands and which stage tasks exist.
- **S-rule result** — one line in a Build record giving a Spec rule's
  PASS or FAIL and naming the test that proves it.
- **Shipped tag** — an annotated `shipped/<outcome>[-<Pn-name>]` tag on
  a merged Build commit. It is the Ship record for merged-source
  delivery, never moves, and freezes its phase.
- **Stage task** — a Task sub-issue tracking one stage, its artifact,
  owner, dependencies, approval, and merged PR.
- **Artifact branch** — a branch reviewing one Intent or exact-phase Spec.
- **Feature** — one numbered outcome directory, immutable after Ship.
- **Capability** — current implemented behavior, updated with the Build
  that changes it and stating any remaining release restrictions.
- **Prototype** — disposable demonstration of an accepted Intent's
  behavior before Spec. Its code never becomes production code.
- **Sandbox** — the product's explicitly permitted place for prototype
  work. A declaration alone does not install branch or path enforcement.
- **Screen walkthrough** — prototype form with named screen scenarios
  and sample data that a person can follow.
- **Worked example** — prototype form with named inputs and expected
  outputs for a rule or calculation.
- **Integration trial** — prototype form with named success and failure
  cases for an outside service.
- **Prototype note** — versioned working record of a prototype's cases,
  evidence, state, age, feedback, and decision; it stays outside main.
- **Prototype confirmation** — the owner's attributable, dated acceptance
  of an exact committed prototype, its forms, evidence, and examples.
  Real-user feedback alone is not confirmation.
