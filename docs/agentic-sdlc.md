# Agentic SDLC — Intent-Driven Development

> **Reference.** This is the working model the loop in `README.md`
> (section 3) implements. Copied from
> `belisha-os/agentic-sdlc-intent-driven-development.md` on
> 2026-09-06; the body below is verbatim. When the process and this
> document disagree, fix one of them in the same PR — the process
> evolves through use, and so does this file.
>
> How it maps onto this repo:
>
> | Reference | Here |
> |-----------|------|
> | Intent (WHY) | `features/NNN-name/intent.md` — `/intent` |
> | Phases | `## Phases` in the intent; multi-phase chains put each phase in `features/NNN-name/Pn-name/` |
> | Spec (WHAT) | `spec.md` per chain or per phase — `/spec NNN [Pn]` |
> | Plan (HOW) | `plan.md`, first commit on the branch — `/plan NNN [Pn]` |
> | Implement | one worktree, one branch, one agent per phase |
> | Prove | `make test` + `REVIEW.md` (spec compliance and outcome check) |
> | Ship | reviewed PR merges; `/capability` updates `product/capabilities/` in the same PR |
> | Human gates | intent `accepted` (includes the phase split), spec `accepted`, plan `approved`, PR approved |
> | GitHub structure | one issue per intent, one sub-issue per phase, one PR per plan — see README section 3 |

## 1. Core principle

We want the development process to be **outcome-driven rather than
task-driven**.

The fundamental flow is:

> **WHY → WHAT → HOW → BUILD → PROVE → SHIP**

Or, in artifact/process terms:

> **Intent → Spec → Plan → Implement → Test & Review → Ship**

We can remember the overall approach as **STEPS**.

The important principle is that AI agents can perform much of the work,
but **humans remain responsible for important decisions, boundaries,
approvals, and review**.

------------------------------------------------------------------------

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

Once the human approves the intent, the agent produces the
**Specification**.

The spec answers:

> **WHAT exactly should the system do?**

The intent is high-level. The spec expands each phase into detailed
expected behavior.

``` text
Intent
  ↓
Approved
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
WHY          WHAT         HOW
Intent  →  Specification  →  Technical Plan
```

The plan should be reviewed before significant code generation begins.

------------------------------------------------------------------------

## 11. Implementation

Once the plan is accepted, agents execute it.

``` text
Intent
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
WHY          WHAT         HOW
 │            │            │
Intent ───→ Spec ───→ Plan
                         │
                         ↓
                       Build
                         │
                         ↓
                       Prove
                  ┌──────┴──────┐
                 Test          Review
                  └──────┬──────┘
                         ↓
                        Ship
```

That is the core Agentic SDLC loop.

------------------------------------------------------------------------

## 14. GitHub structure

GitHub should shift from traditional **task-driven tracking** toward
**outcome-driven tracking**.

Instead of creating issues such as:

> Add staff CRUD

create an outcome-oriented issue such as:

> Salon owner can add and manage staff required for salon operations.

The hierarchy can be:

``` text
Milestone
   │
   └── Intent Issue
          │
          ├── Phase / Sub-Issue
          │      ├── Task
          │      ├── Task
          │      └── PR
          │
          ├── Phase / Sub-Issue
          │      └── PR
          │
          └── Phase / Sub-Issue
                 └── PR
```

So:

-   **Milestone** = delivery/release target
-   **Intent issue** = desired business/system outcome
-   **Phase/sub-issue** = independently manageable part of the intent
-   **Task/checklist** = implementation action
-   **PR** = reviewable implementation unit

This prevents GitHub from becoming a giant collection of disconnected
technical tasks.

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

> **WHY → WHAT → HOW → BUILD → PROVE → SHIP**

Which maps to:

> **Intent → Spec → Plan → Implement → Test & Review → Ship**

The broader mnemonic is **STEPS**:

-   **S --- State the Intent**
-   **T --- Translate into Specification**
-   **E --- Execute the Plan**
-   **P --- Prove the Outcome**
-   **S --- Ship**

There is one subtlety: **planning happens between specification and
execution**, so STEPS is a mnemonic rather than a literal
artifact-for-letter mapping.

The actual operational sequence should remain:

> **Intent → Spec → Plan → Implement → Prove → Ship**

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
