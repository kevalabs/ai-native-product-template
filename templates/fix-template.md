# <What was broken, in one line>

**Failing test:** <the test that fails without this change>
**Corrects:** <features/NNN-name, the outcome whose behavior broke>
**Restores:** <the capability rule or Spec rule this brings back, e.g. R12>
**Date:** <yyyy-mm-dd>

## What was wrong

<What the product did, and what the named rule says it should do. Two or
three sentences. If you cannot name a rule it already breaks, this is not
a fix: open an intent.>

## The change

<The smallest change that makes the failing test pass, in plain words.
Say what you did not change, if a reader might expect more.>

<!-- One file per fix, at fixes/NNN-short-name.md, numbered in its own
     sequence. Numbers never reuse and a merged record is immutable: a
     later correction is another fix or a new intent. A fix never edits a
     shipped feature directory and needs no shipped tag. -->
