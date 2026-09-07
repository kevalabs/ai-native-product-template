---
name: product-status
description: Stakeholder status report — every feature with status, started/due/completed dates, dependencies, and open questions, computed from the artifacts and git history. Read-only. Use when the user asks for a status report, an update for stakeholders, or what is overdue or blocked.
---

Build the stakeholder status report.

**Arguments:** optionally the word `save`, given when this skill is
invoked, to also write the report to a file.

The audience is stakeholders, not the team: people who want to know
where things are without learning the repo. Plain everyday language
per `.agents/writing-style.md` — no stage numbers, no gate jargon,
no file paths in the report body. Read-only: computes everything from
files and git history; never asks anyone to maintain a status file.

## Gather (all computed, never asked)

For every chain in `features/NNN-*/` plus every shipped capability:

- **Status**, in stakeholder words:
  - `Proposed` — intent is draft.
  - `Committed` — intent accepted, requirements or Plan in progress.
  - `In build` — approved Plan PR merged; Build underway.
  - `In review` — Build or Proof being reviewed; identify which.
  - `In delivery` — passing Proof PR merged; Ship not complete.
  - `Shipped` — successful delivery and Ship evidence PR merged,
    every required phase complete, and Intent success criteria checked.
  - `Cancelled` — explicitly cancelled, never counted as shipment.
  - Multi-phase: one row per parent outcome, with completed phase count.
    Keep stage separate from work status. Inspect linked issues and
    actual merged PRs; markers, task closure, or capability text alone
    do not prove advancement. Name inaccessible evidence as unverified.
  - Legacy shipped records keep their real historical evidence; active
    adoption records missing backlinks rather than inventing old proof.
- **Started** — the intent's Date field; fall back to the first git
  commit that touched the feature directory
  (`git log --reverse --format=%as -- features/NNN-*` | first line).
- **Due** — the intent's `Due:` field. Blank if "—" or absent; never
  invent one. If a due date is past and the chain isn't shipped, mark
  the date `⚠ overdue` in the table and name it in the summary —
  overdue is news, not something to bury in a column.
- **Completed** — for shipped chains, the verified shipment completion date, after delivery and the Ship
  evidence merge. Legacy records retain their historical completion
  date. Blank otherwise — never estimate a future date.
- **Depends on** — read the intent's Constraints and the plan's
  touched-surface list: named dependencies on other chains, plus
  collisions (two in-flight plans touching the same files means one
  waits — report it as a dependency).
- **Open questions** — count the bullets under "Open questions" in
  the chain's intent and spec. This number is the honesty column:
  a chain "In build" with 4 open questions is a risk stakeholders
  deserve to see.

## Report format

```
# {{Product}} — status report ({{today}})

One paragraph, three sentences max: how many features shipped, how
many in flight, the single most important thing currently blocked or
at risk. Write it last, from the table.

| # | Feature | Status | Started | Due | Completed | Depends on | Open Qs |
|---|---------|--------|---------|-----|-----------|------------|---------|

Newest first within each status; Shipped chains last (they are the
track record, not the news). Feature names in plain words — the
intent's problem line, not the directory slug.

**Needs a decision** — only if open questions exist: one bullet per
chain naming the question and who owes the answer. This is the
section stakeholders can actually act on.

```

## Delivery

Print the report. If the argument contains `save`, also write it to
`reports/status-YYYY-MM-DD.md` (create `reports/` if needed; use
today's date) so it can be shared or attached — but don't commit;
the user decides what lands in git.

Do not pad: no executive-summary boilerplate, no RAG colors unless a
chain genuinely is blocked, no percentages invented from step counts.
If there is nothing in flight, say so in one sentence.
