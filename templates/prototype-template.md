# <Outcome / phase / version> — Prototype note

**Outcome:** <NNN-name>
**Phase:** <single or Pn-name>
**Intent:** <accepted Intent commit permalink and merged PR>
**Version:** <version label>
**State:** draft
**Created at:** <ISO 8601 timestamp with UTC offset>
**Expiry days:** 30
**Prototype form:** <screen walkthrough, worked example, integration trial; include all that apply>
**Prototype commit:** <full runnable commit SHA; fill after committing the demonstration>
**Retained ref:** <remote repository and ref retaining that commit through phase shipment>
**Evidence:** <exact version's evidence locations>
**Examples:** <exact commit permalink to the examples Markdown file>
**Confirmed by:**
**Confirmed at:**
**Confirmation source:**

<!-- Keep this working note outside main. The Spec preserves confirmation
     fields and evidence, not this note or runnable prototype code.
     Empty confirmation fields never mean approval. -->

## Run and inspect

<How a reviewer runs the demonstration and checks every named case.
Link the examples created from prototype-examples-template.md.
Use sample data, never production secrets or real personal data.
Do not add unit, integration, or end-to-end tests to prototype code.>

## Feedback

<Available real-user feedback and how it affected the owner's decision.
Record when no user feedback was available; it is not a required gate.>

## Decision

<Only the owner confirms or rejects the exact committed version.
Record the person, timestamp, source, and accepted forms and examples.
For rejection, record the owner's reason without filling confirmation fields.
Preserve the decision record and its source alongside the retained commit.>

## Refresh

<For an expired unresolved version, record the refresh date, rerun cases,
and result before returning to ready. Keep the original creation date.
Confirmed and rejected records are final; changes create a new version.>

See [the shared prototype rules](../docs/agentic-sdlc.md#prototype-before-spec)
in the template repository; when copying this note, keep a usable link
to that guide in your product.
