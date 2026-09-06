---
name: capability
description: Stage 5 of the feature loop — drafts or updates the product/capabilities/ doc(s) for a feature that is shipping, converting shipped spec rules into present-tense capability rules. Use inside the feature's PR, on the feature branch, when the user asks to update capabilities or document shipped behavior for feature NNN.
---

Update capability docs for a shipping feature.

**Arguments:** the feature number `NNN`, and for multi-phase intents
the phase `Pn`, given when this skill is invoked. If missing, derive
it from the current branch name (`feature/NNN[-Pn]-…`) or ask.

Capabilities are units of BEING: current shipped behavior, present
tense only, updated ONLY inside the PR that changes the behavior. This
command runs on the feature branch as part of that PR — never on
`main` and never for unshipped speculation.

## Step 0 — gates and context

- Must be on the `feature/NNN-*` (or `feature/NNN-Pn-*`) branch with
  the implementation done (or nearly done). If on `main`, stop.
- Read this chain's or phase's `spec.md` (its "Capabilities affected"
  header names the target files) and the current text of each
  affected `product/capabilities/` doc. Follow
  `templates/capability-template.md` for any new file. Multi-phase:
  only this phase's S-rules ship now; later phases' behavior stays
  out of the capability doc until their own PR.

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

Edit/create the capability doc(s) in plain everyday language per
`.agents/writing-style.md` — read it first. Every statement present
tense, every rule testable as written, every rule a sentence you
could say out loud ("A customer can cancel an order until it
ships"). No history, no future — history lives
in `features/`, future lives in open intents.

## Step 3 — close

Summarize which R-rules were added/changed and remind the user: these
edits ship in THIS PR (review blocks behavior changes without them),
and after merge the feature (or phase) directory is immutable —
subsequent changes start a new chain with `/intent`. If this is the
last phase of an intent, walk the intent's `## Success criteria` and
say which are now true; any that aren't are a finding for the PR.
