---
name: idea
description: Captures a raw product idea as one line in product/IDEAS.md — ten-second capture, no interview, no evaluation. Use when the user says "idea:", "park this", "note for later", or wants to jot a thought without starting a feature chain.
---

Capture an idea in `product/IDEAS.md`.

**Arguments:** the idea, in one line, given when this skill is
invoked.

This is the ONE command with no interview. Capture must be
frictionless — the thinking happens later, at `/intent`, and only for
ideas that earn it. Do not evaluate the idea, ask clarifying
questions, or start a chain.

1. If the idea is missing or empty, ask for it in one line and stop
   there — that's the only question allowed.
2. Use the current artifact/feature worktree if its scope allows the
   inbox edit; otherwise create or reuse an `artifact/ideas` worktree.
   Never leave the change on main. Compress it to one plain-language
   line if needed (keep the user's
   words as much as possible). Add it to the top of the **Ideas**
   list in `product/IDEAS.md`:

   `- YYYY-MM-DD <idea> (from: <user>)`

3. If a very similar idea is already listed, or an open chain in
   `features/` already covers it, still add the line — but say so in
   one sentence so the user knows.
4. Confirm in one line and name the worktree if it differs from the
   user's starting directory. Do not commit; the edit lands through a
   reviewed PR on this branch when the user asks.

That's it. No number allocation, no directory, no draft intent.
