# Writing style for artifacts (intent, spec, plan, capability docs)

These documents are read by new teammates, non-engineers, and future
you. Write them the way you would explain the feature to a colleague
at a whiteboard — plain, everyday language.

## The rules

- **Short sentences, one idea each.** If a sentence needs a second
  read, split it.
- **Name the actor and the action.** "The customer taps Refund and
  gets their money back within 5 days" — not "a refund may be
  initiated by the user, which will be processed in a timely manner".
- **Concrete beats abstract.** Numbers, states, and examples:
  "within 14 days", "only while the order is `delivered`" — never
  "appropriate", "timely", "as needed".
- **Glossary words exactly, everything else simple.** Domain terms
  from `product/glossary.md` are precise on purpose — use them
  as written. Every other word should be one you'd say out loud.
- **No filler words.** Banned: leverage, utilize, robust, seamless,
  comprehensive, streamline, facilitate, holistic, "enable users to",
  "in order to". If a word only makes the sentence sound smarter,
  cut it.
- **Say who decides and who benefits.** "Support asked for this
  because they get ~40 emails a week" beats "this addresses a
  significant operational pain point".

## The two tests

1. **Read it aloud.** Would you actually say this sentence to a
   teammate? If not, rewrite it the way you'd say it.
2. **New-hire test.** Could someone on day one understand it without
   asking a question (except glossary lookups)? If not, add the
   missing plain words.

Plain does not mean vague: S-rules and R-rules must still be testable
as written. "The customer can cancel an order until it ships" is both
plain and testable — that is the target.
