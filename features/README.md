# Features — the append-only change ledger

One numbered directory per intent (one unit of outcome, not one page
or one task):

```
features/NNN-short-name/
├── intent.md    # WHY: problem, outcome, actors, success criteria,
│                #   phases (Stage 1)
├── spec.md      # WHAT: flows, rules, states, acceptance (Stage 2)
├── design/      # committed mocks the spec references
└── plan.md      # HOW: approach, touched files, steps (Stage 3)
```

An intent whose outcome is too big for one reviewable PR is cut into
**phases** (in `intent.md`). Each phase gets its own spec, plan,
branch, and PR under the same intent:

```
features/NNN-short-name/
├── intent.md                # lists P1, P2, … and their dependencies
├── P1-short-name/
│   ├── spec.md
│   ├── design/
│   └── plan.md
└── P2-short-name/
    ├── spec.md
    └── plan.md
```

- Numbers allocate in commit order and never reuse. Phase numbers
  are fixed once the intent is accepted.
- A directory is **immutable once its feature ships** — changes to
  shipped behavior are a NEW feature chain that links back, never an
  edit here. Current behavior lives in `product/capabilities/`.
  A shipped phase is immutable even while later phases are open.
- Incidents and maintenance findings (Stage 6) re-enter as new
  entries here.
- Draft intent and spec on `artifact/NNN-short-name` in a worktree.
  Accept each before its next stage. Merge the reviewed artifact PR,
  then create the implementation worktree from the updated default
  branch. For later phases, another artifact PR adds the phase's spec.
  A plan never lands in an artifact PR.
- Implementation branch naming: `feature/NNN-short-name`, or
  `feature/NNN-Pn-short-name` per phase — one branch, one worktree,
  one agent per chain or phase. Independent phases may run in
  parallel once the intent's shared ground (state names, terms, data
  ownership, contracts) is settled.
