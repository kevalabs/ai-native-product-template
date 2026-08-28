---
description: "Draft or update the product/capabilities/ doc(s) for a shipping feature — run inside the feature's PR"
argument-hint: "<NNN of the feature being shipped>"
---

Update capability docs for shipping feature: $ARGUMENTS

Capabilities are units of BEING: current shipped behavior, present
tense only, updated ONLY inside the PR that changes the behavior. This
command runs on the feature branch as part of that PR — never on
`main` and never for unshipped speculation.

## Step 0 — gates and context

- Must be on the `feature/NNN-*` branch with the implementation done
  (or nearly done). If on `main`, stop.
- Read the feature's `spec.md` (its "Capabilities affected" header
  names the target files) and the current text of each affected
  `product/capabilities/` doc. Follow
  `templates/capability-template.md` for any new file.

## Step 1 — interview (shipped truth only)

The danger here is aspirational documentation. For each spec S-rule,
establish with the user (or by reading the code/tests when the diff is
in this worktree):

1. **Did it actually ship in this PR?** Rules cut during
   implementation must NOT enter the capability doc — flag them as
   spec/plan drift instead, and note they need a follow-up chain or a
   spec revision before merge.
2. **Rewrite as being, not becoming.** Convert each shipped S-rule to
   a present-tense R-rule, testable as written. Keep numbering stable:
   never renumber existing R-rules; changed behavior edits the rule
   text in place, new behavior takes fresh numbers.
3. **Region reality.** Is the behavior live in all regions, or flagged
   off somewhere? Flags currently off go under Region availability;
   inline variance is recorded on the rule (`NP: …, AU: …`).
4. **Lifecycle & edge cases.** Did states or edge-case behavior
   change? Update those sections; silence about a changed edge case is
   a documentation bug.
5. **Vocabulary.** Any glossary terms introduced by this feature must
   already be in `product/glossary.md` in this same PR — verify, don't
   assume.

## Step 2 — write

Edit/create the capability doc(s). Every statement present tense,
every rule testable as written. No history, no future — history lives
in `features/`, future lives in open intents.

## Step 3 — close

Summarize which R-rules were added/changed and remind the user: these
edits ship in THIS PR (review blocks behavior changes without them),
and after merge the feature directory is immutable — subsequent
changes start a new chain with `/intent`.
