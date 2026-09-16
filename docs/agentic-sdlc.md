# Agentic SDLC — Intent-Driven Development

> **Reference.** This is the working model the loop in `README.md`
> (section 3) implements. Copied from
> `belisha-os/agentic-sdlc-intent-driven-development.md` on
> 2026-09-06; the repository mapping evolves with our workflow. When the process and this
> document disagree, fix one of them in the same PR — the process
> evolves through use, and so does this file.
>
> How it maps onto this repo:
>
> | Reference | Here |
> |-----------|------|
> | Intent (WHY) | `features/NNN-name/intent.md` — `/intent` on `artifact/NNN-name` |
> | Artifact handoff | the six stages each land through a reviewed PR; Prototype uses owner confirmation, not a merged PR |
> | Prototype (TRY) | `/prototype NNN [Pn]` after Intent merge; confirmation or a justified Spec skip |
> | Phases | `## Phases` in the intent; multi-phase chains put each phase in `features/NNN-name/Pn-name/` |
> | Spec (WHAT) | `spec.md` per chain or per phase — `/spec NNN [Pn]` |
> | Plan (HOW) | `plan.md`, approved first commit in its own PR before Build — `/plan NNN [Pn]` |
> | Implement | one worktree, one branch, one agent per phase |
> | Prove | `make test` + PR commit-history validation + `REVIEW.md` (spec compliance and outcome check); product repos extend the template checks with their build/tests |
> | Ship | delivery succeeds and its Ship evidence PR merges, after passing Proof; capability docs land with Build |
> | Human gates | intent `accepted` (includes the phase split), spec `accepted`, plan `approved`, PR approved |
> | GitHub structure | one Intent parent, Task sub-issues per stage, optional phase groups, and one reviewed PR per stage |

## 1. Core principle

We want the development process to be **outcome-driven rather than
task-driven**.

The fundamental flow is:

> **WHY → TRY → WHAT → HOW → BUILD → PROVE → SHIP**

Or, in artifact/process terms:

> **Intent → Prototype → Spec → Plan → Implement → Test & Review → Ship**

We can remember the overall approach as **STEPS**.

The important principle is that AI agents can perform much of the work,
but **humans remain responsible for important decisions, boundaries,
approvals, and review**.

------------------------------------------------------------------------

## Prototype before Spec

After the accepted Intent PR merges, demonstrate the behavior before
writing its Spec. Use a **screen walkthrough** for screens, a **worked
example** for rules or calculations, and an **integration trial** for
outside services. Mixed work needs every applicable form. The owner can
confirm them together when they share one exact version and evidence set.

This step is contributor guidance and human review. It adds no merged
stage PR and no mandatory seventh tracking task. The existing Intent,
Spec, Plan, Build, Proof, and Ship PRs keep their gates. A Spec tracking
Task can exist before confirmation; substantive Spec drafting cannot.

### Run and confirm

Use [the prototype skill](../.agents/skills/prototype/SKILL.md), the
[note template](../templates/prototype-template.md), and the
[examples template](../templates/prototype-examples-template.md).
First verify the accepted Intent merge and the product's permitted
prototype workspace. P1 does not install a prototype branch lane or
sandbox enforcement. If no permitted workspace exists, report that
limit and wait for P2 or a separately authorized product setup. Do not
bypass hooks or place prototype code on an artifact branch.

A prototype only needs to run its named examples well enough for feedback.
Add no unit, integration, or end-to-end tests to its code, and impose no
coverage gate. This exception applies to disposable prototype code;
Build still needs tests. Existing security and privacy rules apply.
Use synthetic data and test services, never real personal data or
production secrets. Reachable real users may give feedback; lack of
available users does not block the owner from making a decision.

Before marking a version `ready`, run every named case:

- Screen walkthrough: named scenarios and sample data.
- Worked example: named inputs and expected outputs.
- Integration trial: named success and failure cases.

Missing data, an omitted applicable form, or a failed named case keeps
the demonstration out of `ready`. Commit the runnable version and its
examples before asking the owner to decide. The note's `Prototype commit`
is that full SHA; record the decision afterward, avoiding a self-referencing
commit hash. Never claim an uncommitted version has been confirmed.

Only the product owner confirms or rejects. Record `Prototype form`,
`Prototype commit`, `Evidence`, `Examples`, `Confirmed by`, `Confirmed at`,
and `Confirmation source`. Every location must identify the exact version.
Record how available user feedback affected the decision. A conversation
source includes the person, dated decision, and enough attributable text
or a link for review. User feedback and an agent's assertion are not approval.

### State, age, and retention

Each version follows `draft → ready → confirmed | rejected`, with
`ready → expired → ready` for an unresolved version. The final two states
are immutable. A change after confirmation or rejection creates a new
version; only the latest explicitly confirmed version governs a new Spec.
Do not overwrite the old examples, commit, or decision record.

Read `Prototype settings` in AGENTS.md. The default unresolved-note age
limit is 30 days from `Created at`; a product may declare another period.
Use timestamps with UTC offsets. At the limit, report `expired` as a
warning, not a failing check. P1 makes this a manual warning, not a new
CI job. To return to `ready`, explicitly record a refresh and rerun the
cases. Preserve the original date; a refresh does not reset the age used
for Spec acceptance or silently extend a confirmation.

Before accepting a Spec whose note is at least 30 days old, the owner
reconfirms the version or explicitly accepts its age in the Spec with
a dated source. This review remains necessary even after a refresh.
Once the Spec is accepted, its frozen confirmation no longer expires.

Keep a remote ref reaching the confirmed commit until the phase ships.
Record repository and ref in `Retained ref`, and preserve the decision
record and confirmation source as well. If the working branch will be
deleted, retain a tag first; never retarget that tag to changed content.
Review access from a fresh fetch or clone. An old SHA link alone does
not establish retention. Prototype code and its working note never merge
to main; preserve their evidence through the Spec instead. P1 installs
no tag protection, cleanup job, or new branch naming scheme.

### Freeze the evidence in Spec

The prototype demonstration reads its examples Markdown file. That file
has one JSON code block containing cases with unique `id` and `form`
fields and the form-specific data described above. Products choose
domain fields before confirmation. Illustrative template cases are not
real owner-confirmed examples.

Copy the whole confirmed file byte for byte to the exact phase's
`design/prototype-examples.md`. Preserve supporting Markdown and images
in that directory, using the current allowed extensions: `.md`, `.png`,
`.jpg`, `.jpeg`, `.webp`, `.svg`, or `.pdf`. Review images and Markdown
for embedded executable code or sensitive data; an allowed extension
alone does not make the content safe or appropriate.

Fill the Spec template's `Prototype confirmation` section with the
confirmation fields, retained ref, original and preserved example
locations, evidence, and any age acceptance. Preserve the owner's
attributable decision in reviewable form. The Spec derives requirements
and acceptance cases from those examples. Copy no runnable prototype
source or working note. A confirmation for another commit, inaccessible
source, missing examples, or evidence that cannot be preserved blocks
Spec acceptance, even if a demonstration previously took place.

When there is nothing meaningful to inspect, replace that section's
fields with `Prototype skip:` and one concrete reason. A pure refactor
that preserves all behavior can qualify. A screen change with no demo
yet does not. Owner acceptance of the Spec accepts the skip. Do not make
an empty prototype to satisfy paperwork; lack of evidence is not itself
a reason to skip. Existing accepted Specs are not back-filled.

### Use the examples in Build

The Plan names the preserved file and the test reader. Build tests load
the same file's JSON block and assert the product's observed behavior;
do not transcribe it into a second fixture. Compare the original and
preserved bytes and record the source and destination in build.md.
For example, a Python product can read the single block as follows:

```python
import json
import re
from pathlib import Path

blocks = re.findall(r"^```json\n(.*?)^```\s*$",
                    Path(examples_path).read_text(), re.M | re.S)
assert len(blocks) == 1
cases = json.loads(blocks[0])
```

The product's tests supply `examples_path` and compare each case's
expected results with the real implementation. This example is a reader,
not a product test or a new common library. Changed case data needs
renewed prototype confirmation or an accepted Spec revision before
Build continues. Implement production behavior independently; never
promote the disposable prototype code into the product.

## Branches and delivery

All stage PRs target `main`. Do not use a long-lived `dev` or other
environment branch as deployment state. A feature-branch preview is
optional when early interaction helps. A merge into main identifies
integrated source; it is not by itself production delivery.

Build an immutable artifact from the merged Build commit for development
or staging. Record its identity or digest and source commit in Proof,
then test that exact version. The Build record can describe the artifact
recipe before merge; it cannot invent its future merge SHA or digest.
Proof rejects an artifact whose identity or source differs from the
named merged Build. A pre-merge preview is not that proved artifact.

After passing Proof merges, Ship promotes the same artifact to the
delivery destination. Compare the identity and record the successful
result. If the artifact is unavailable or the destination needs a
different rebuild, leave shipment unsuccessful. Do not rebuild and call
the result the proved version. A correction needs reviewed Build work
and renewed Proof. Preserve existing release approval and region rules.

For this template, which has no runtime deployment, the immutable
merged Build source is the artifact. Reviewed availability on main is
its delivery target. Separate Proof and Ship evidence still establish
outcome completion; no mandatory release tag or provider is introduced.

Adopt the prototype step for outcomes or phases not yet at Spec. Keep
accepted Specs and shipped history intact. P1 provides manual guidance;
P2 owns the new sandbox lane, and P3 owns tracking automation. A rollback
of guidance is reviewed and preserves already accepted evidence. The
final phase's Ship records the full adoption note for existing products.

## 2. Intent --- WHY

Every meaningful piece of work starts with an **Intent**.

An intent is not a list of coding tasks. It describes the **outcome we
want to achieve and why it matters**.

An intent can represent:

-   a product feature
-   an architectural improvement
-   a refactoring
-   infrastructure work
-   developer-experience improvement
-   performance/security improvement

The important requirement is that it has a **clear, verifiable
outcome**.

For example, instead of:

> Create salon tables, APIs and onboarding pages.

Use:

> A new salon owner can complete the required setup and get approved
> before going live.

### Intent structure

An intent should contain roughly:

``` text
Intent
├── Problem / Context
├── Desired Outcome
├── Actors
├── High-level Success Criteria
└── Phases
```

The intent should **not contain implementation details**.

------------------------------------------------------------------------

## 3. Phases --- breaking an intent into manageable outcomes

A large intent should be divided into **phases**.

We deliberately prefer the term **phase** rather than creating layers of
"sub-intents."

For example:

``` text
Intent: Salon Onboarding

Phase 1 — Account registration
Phase 2 — Contact verification
Phase 3 — Business profile
Phase 4 — Branch configuration
Phase 5 — Opening hours
Phase 6 — Staff setup
Phase 7 — Submit application
Phase 8 — Operator review
Phase 9 — Activation
```

These phases belong to the **same overall intent** because together they
produce one business outcome.

However, phases can have different actors.

``` text
Salon Owner
   ↓
Registration
   ↓
Business setup
   ↓
Branch / Hours / Staff
   ↓
Submit
   ↓
Operator
   ↓
Review / Approve
   ↓
System
   ↓
Activate Salon
```

Operator approval is therefore **not necessarily another parent
intent**. It can be a separate phase of the same onboarding intent.

------------------------------------------------------------------------

## 4. Don't divide work by pages

A key decision:

> **Do not define intent boundaries based on UI pages.**

Pages are an implementation/product-interface consequence.

Instead, divide work according to:

-   business outcomes
-   actors
-   state transitions
-   independently reviewable capabilities
-   dependencies

For example, `staff.html` is not an intent.

Instead:

> Salon owner can add the staff required to operate the salon.

The UI may later contain one page, three pages, an API, or a mobile
flow.

------------------------------------------------------------------------

## 5. Human reviewability determines phase size

This is especially important for agentic development.

AI agents can generate enormous amounts of code very quickly.

Therefore:

> **The unit of implementation should remain small enough for a human to
> meaningfully review.**

If implementing a phase produces a huge diff touching many unrelated
areas, that is a signal that the phase may need further decomposition.

A good phase should ideally produce:

> **one understandable capability → focused implementation → focused
> tests → reviewable PR**

Do not optimize for maximum agent output.

Optimize for:

> **maximum trustworthy human review.**

------------------------------------------------------------------------

## 6. Parallel agents

Independent phases may be implemented by different coding agents
simultaneously.

``` text
                 Salon Onboarding Intent
                          │
           ┌──────────────┼──────────────┐
           ↓              ↓              ↓
      Branch Setup    Staff Setup    Opening Hours
           │              │              │
        Agent A         Agent B         Agent C
```

But parallel execution should happen only when shared contracts are
sufficiently clear.

Examples include:

-   domain terminology
-   data ownership
-   status/state definitions
-   API contracts
-   naming conventions
-   authorization rules
-   shared models

Otherwise multiple agents can independently produce correct-looking
solutions that conflict when integrated.

------------------------------------------------------------------------

## 7. Spec --- WHAT

After the accepted Intent merges, the owner confirms the prototype
or the Spec records a concrete skip reason. The agent then produces
the **Specification** from that evidence.

The spec answers:

> **WHAT exactly should the system do?**

The intent is high-level. The spec expands each phase into detailed
expected behavior.

``` text
Intent accepted and merged
  ↓
Prototype confirmed (or justified skip)
  ↓
Specification
```

The spec should contain things such as:

-   actors
-   user/system flows
-   behavior
-   business rules
-   required information
-   validations
-   permissions
-   states and transitions
-   edge cases
-   error behavior
-   acceptance criteria
-   low-fidelity UI/UX designs where useful

For UI features, low-fidelity designs can be extremely valuable because
they give both humans and coding agents a shared understanding of the
expected experience.

------------------------------------------------------------------------

## 8. Keep technical implementation out of the product spec

We established a useful boundary:

### Intent

**WHY are we doing this?**

### Specification

**WHAT should happen?**

### Plan

**HOW are we going to build it?**

Therefore the product spec generally should not turn into:

``` text
Create PostgreSQL table X
Add endpoint POST /api/...
Create React component...
Modify service Y...
```

Those belong in the technical plan.

The spec should remain understandable to someone who understands the
product without needing to understand the implementation.

------------------------------------------------------------------------

## 9. Acceptance criteria belong in the spec

Acceptance criteria are especially important because they later become
the basis for **proof**.

For example:

``` text
Acceptance Criteria

- Owner can provide an email address or phone number.
- Verification code is sent to the selected channel.
- Invalid/expired verification codes are rejected.
- Verified owner can continue onboarding.
- Required business information must be completed before submission.
- Submitted applications become read-only where required.
- Operator can approve or reject the application.
- Salon becomes active only after approval.
```

This creates a critical connection:

> **Spec defines expected behavior → tests prove the behavior → review
> verifies the outcome.**

------------------------------------------------------------------------

## 10. Plan --- HOW

After the spec is approved, the coding/architecture agent creates the
technical plan.

The plan answers:

> **HOW will we implement the specification?**

This is where technical decisions belong.

For example:

-   architecture changes
-   domain model
-   database/schema changes
-   migrations
-   APIs
-   services
-   components
-   authorization
-   state management
-   dependencies
-   integration points
-   test strategy
-   implementation sequence
-   affected files/modules
-   compatibility concerns

Conceptually:

``` text
WHY        TRY           WHAT             HOW
Intent  →  Prototype  →  Specification  →  Technical Plan
```

The plan should be reviewed before significant code generation begins.

------------------------------------------------------------------------

## 11. Implementation

Once the plan is accepted, agents execute it.

``` text
Intent
   ↓
Prototype (or justified skip)
   ↓
Spec
   ↓
Plan
   ↓
Implement
```

Implementation should happen **phase by phase**, rather than asking an
agent to implement an enormous parent intent in one pass.

Each phase should preferably result in a focused PR.

Agents can use worktrees/branches to execute independent phases in
parallel where appropriate.

------------------------------------------------------------------------

## 12. Prove before shipping

Generated code is not considered complete merely because it compiles or
the agent says it is finished.

After implementation comes **Proof**.

Proof consists broadly of:

> **Testing + Verification + Review**

The agent should first perform its own automated verification.

Examples:

-   unit tests
-   integration tests
-   end-to-end tests
-   linting
-   type checking
-   security checks
-   acceptance tests
-   build verification

But tests alone aren't enough.

The implementation must also be checked against the **specification**.

The central review question becomes:

> **Did we actually build what the specification said we would build?**

And at the highest level:

> **Did this implementation achieve the original intent?**

This gives us traceability:

``` text
Intent
  ↓
Prototype (or justified skip)
  ↓
Spec
  ↓
Plan
  ↓
Implementation
  ↓
Tests
  ↓
Review
  ↓
Original Intent
```

------------------------------------------------------------------------

## 13. Ship

Only after the implementation has been proven and reviewed should it be
shipped.

``` text
Intent → Prototype (or justified skip) → Spec → Plan
                                                 ↓
                                               Build
                                                 ↓
                                         Test + Review
                                                 ↓
                                                Ship
```

That is the core Agentic SDLC loop.

------------------------------------------------------------------------

## 14. GitHub structure and stage handoffs

Track one parent issue of type Intent per outcome. Give every stage a
Task sub-issue with its owner, governing Markdown, predecessor, review
PR, and completion criteria. Larger outcomes group Spec-through-Ship
tasks under phase issues after their shared Intent is accepted.

The workflow is Intent → Prototype → Spec → Plan → Build → Test +
Review → Ship. Prototype has owner confirmation or a justified Spec skip,
not a merged stage PR. Each of the six stages commits its outcome
artifact and merges its reviewed PR before the next stage starts. Build
includes normal tests and human review before its merge; Proof checks the exact merged
version against every Spec rule and the Intent's success criteria.

Issues link readable draft artifacts. After merge, they retain exact
approved commit permalinks and merged PRs. Artifacts link back to their
stage tasks. Task closure, board movement, and local approval markers
cannot substitute for actual approval and merge evidence. Keep the
parent open until all required phases ship and its success criteria hold.

Milestones represent delivery targets. Small implementation tasks use
checklists or separately owned tasks that cite approved Spec/Plan
sections. Keep stage and work status separate on the project board.
The repository commands and evidence fields are defined in
[the gate guide](../.githooks/README.md).

------------------------------------------------------------------------

## 15. Relationship with Agile/user stories

Intent-driven development does not require throwing away user stories.

Instead, user stories become a tool **inside the specification** where
they are useful.

Traditional:

> As a salon owner, I want to add staff so that...

Intent-driven:

``` text
Intent
    ↓
Phase
    ↓
Prototype confirmed (or justified skip)
    ↓
Specification
    ├── User flows
    ├── User stories (when useful)
    ├── Business rules
    └── Acceptance criteria
```

This allows us to retain useful Agile techniques without making the user
story the top-level unit of the entire engineering process.

------------------------------------------------------------------------

## 16. Agent responsibility vs human responsibility

"Agentic" does **not** mean removing humans.

The agent can:

-   analyze an intent
-   propose phases
-   identify missing requirements
-   generate a specification
-   generate low-fi designs
-   propose architecture
-   create implementation plans
-   implement
-   write tests
-   self-review
-   identify inconsistencies

The human should control important gates:

``` text
Human defines/discusses Intent
            ↓
Agent proposes Phases
            ↓
       HUMAN APPROVES
            ↓
Agent demonstrates Prototype
            ↓
 OWNER CONFIRMS (or accepts Spec skip)
            ↓
Agent develops Spec
            ↓
       HUMAN APPROVES
            ↓
Agent develops Plan
            ↓
       HUMAN APPROVES
            ↓
Agents Implement
            ↓
Agents Test / Self-review
            ↓
       HUMAN REVIEWS
            ↓
           Ship
```

The goal is not human involvement in every keystroke.

The goal is **human judgment at high-leverage decision points**.

------------------------------------------------------------------------

## 17. Working mantra

The simplest mental model is:

> **WHY → TRY → WHAT → HOW → BUILD → PROVE → SHIP**

Which maps to:

> **Intent → Prototype → Spec → Plan → Implement → Test & Review → Ship**

The broader mnemonic is **STEPS**:

-   **S --- State the Intent**
-   **T --- Try the behavior, then Translate into Specification**
-   **E --- Execute the Plan**
-   **P --- Prove the Outcome**
-   **S --- Ship**

There is one subtlety: **planning happens between specification and
execution**, so STEPS is a mnemonic rather than a literal
artifact-for-letter mapping.

The actual operational sequence should remain:

> **Intent → Prototype → Spec → Plan → Implement → Prove → Ship**

------------------------------------------------------------------------

## Instruction for the coding agent

Use the above as the **current working model, not immutable doctrine**.

When improving our existing development process:

1.  Preserve the distinction between **Intent (Why), Spec (What), and
    Plan (How)**.
2.  Make work **outcome-driven rather than task-driven**.
3.  Introduce **phases** for large intents.
4.  Keep phases/PRs small enough for meaningful human review.
5.  Allow independent phases to run in parallel when contracts are
    clear.
6.  Make specifications the source of truth for acceptance and
    verification.
7.  Require implementation to be proven against the spec before
    shipping.
8.  Adapt GitHub issues toward **Intent → Phase/Sub-issue → Task → PR**.
9.  Add human approval gates at high-leverage points rather than
    requiring humans to supervise every agent action.
10. **Do not over-engineer the process.** Improve it incrementally based
    on what we learn from actually using it.

Most importantly:

> **This process itself should evolve through use.**

The Anthropic AI-native SDLC ideas are an inspiration and starting
point, but our goal is to develop a practical workflow based on our own
day-to-day experience with coding agents---not simply copy a playbook.
