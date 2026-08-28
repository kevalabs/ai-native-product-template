# Features — the append-only change ledger

One numbered directory per unit of work:

```
features/NNN-short-name/
├── intent.md    # problem + outcome (Stage 1)
├── spec.md      # requirements + design (Stage 2)
├── design/      # committed mocks the spec references
└── plan.md      # implementation plan (Stage 3)
```

- Numbers allocate in commit order and never reuse.
- A directory is **immutable once its feature ships** — changes to
  shipped behavior are a NEW feature chain that links back, never an
  edit here. Current behavior lives in `product/capabilities/`.
- Incidents and maintenance findings (Stage 6) re-enter as new
  entries here.
- Branch naming: `feature/NNN-short-name` — one branch, one worktree,
  one agent per chain.
