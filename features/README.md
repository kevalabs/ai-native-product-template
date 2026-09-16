# Features — the append-only change ledger

One numbered directory per outcome:

```
features/NNN-name/
├── intent.md
├── spec.md
├── design/
├── plan.md
├── build.md
├── proof.md
└── ship.md
```

The accepted intent fixes phase names and dependencies. A phased outcome
keeps intent.md at its root and places each phase's Spec-through-Ship
artifacts under `Pn-name/`. Cut phases by outcome, not by page or task.
Each stage has a Task sub-issue and a separate PR. The parent Intent
issue links the artifact index and remains open until every phase ships.

Intent → Prototype → Spec → Plan → Build → Test + Review → Ship.
Prototype has owner confirmation or a justified Spec skip, not a merged
stage PR. The six stages each commit and merge their approved outcome.
The Spec preserves confirmation and examples under its `design/`
directory; disposable prototype source and its working note stay outside
main. Use [the shared rules](../docs/agentic-sdlc.md#prototype-before-spec).
Use artifact branches for Intent/Spec, feature branches for Plan/Build,
and proof/ship branches for their respective evidence, all targeting main.
P1 does not install a prototype branch lane. Details and
commands are in [.githooks/README.md](../.githooks/README.md).

Keep approved permalinks on tasks after branches are deleted. Numbers
never reuse; shipped artifacts never change. Later corrections start a
new intent linking the shipped history. In-flight legacy stages retain
real history and record missing old backlinks when adopting new gates.
