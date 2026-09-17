# Fixes — corrections to shipped behavior

One numbered Markdown file per fix, `fixes/NNN-short-name.md`, copied
from `templates/fix-template.md`. Numbers run in their own sequence, never
reuse, and a merged record is immutable.

A fix makes the product do what a shipped Spec rule or a capability rule
already says it does. It lands in one reviewed PR on a `fix/short-name`
branch carrying three things: a test that fails without the change, the
smallest change that makes it pass, and the record. No intent, spec,
plan, or shipped tag.

Anything that adds a rule, changes a rule, or makes the product promise
something new is not a fix. It starts with an intent and follows Intent
→ Prototype → Spec → Plan → Build → Test + Review → Ship. Size does not
decide: a one-line change that alters a promise is new work, and a wide
change that only restores stated behavior is a fix. The reviewer makes
that call, and it is the point of the review.

A fix never edits a shipped feature directory. Those stay immutable, and
this record carries the correction instead. Update the matching
capability doc in the same PR when its text described the broken
behavior rather than the promised one.
