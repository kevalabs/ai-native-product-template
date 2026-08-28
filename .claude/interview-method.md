# Interview method (shared by /intent, /spec, /plan)

How to run the interview step of any stage command. The stage command
supplies the question themes; this file supplies the technique.
(Adapted from mattpocock/skills "grilling".)

## Frontier rounds

Map the open decisions as a tree — answers to early questions change
which later questions exist. Work in rounds:

1. Present only the **frontier**: questions whose prerequisites are
   already settled. Number them, one line of context each.
2. For every question, state your **recommended answer** and why —
   via AskUserQuestion when options are enumerable (recommended option
   first, labeled "(Recommended)"), free-form otherwise. A question
   with no recommendation usually means you haven't done Step 0's
   reading.
3. Wait for the answers, then compute the next frontier. Never ask a
   question whose premise depends on an unanswered one.

The interview is done when the frontier is empty — every branch either
answered, or explicitly parked as an open question with a named owner.

## Facts vs decisions

Never ask the user something you can look up. Code, git history,
`product/` docs, existing chains, external docs — fetch or read them
yourself (in parallel with the conversation where possible). The user
gets **decisions and unwritten context only**: priorities, intent,
tolerance for risk, facts that live in their head.

## Pressure, applied politely

- Answer vague → narrow the question, don't move on. ("Always? Which
  persona exactly? What happens when the precondition fails?")
- Answer conflicts with a committed artifact → surface it immediately:
  "the glossary says X, you seem to mean Y — which changes?"
- Answer is a solution when you asked for a problem → push back once,
  clearly, then record whichever the user insists on.

## Parked questions

An open question the present user cannot answer gets a named owner. If
that owner isn't in the session, offer to generate
`features/NNN-*/questions-for-<role>.md`: purpose and deadline up top,
themed questions ordered by importance, each with a one-line "why this
matters" and an answer stub. Async answers feed the next revision.
