# <Outcome> — Ship

<!-- Runtime-artifact delivery only. A merged-source product ships by
     pushing an annotated shipped/<outcome>[-<Pn-name>] tag on the
     merged Build commit and writes no ship.md. Check the Delivery
     setting in AGENTS.md before using this file. -->

**Status:** delivered
**Stage:** ship
**Outcome:** <NNN-name>
**Phase:** <single or Pn-name>
**Parent issue:** <GitHub Intent issue URL>
**Stage issue:** <GitHub stage Task URL>
**Predecessor PR:** <merged previous-stage PR URL>
**Build commit:** <full proved Build SHA>
**Proof commit:** <full merged Proof SHA>
**Artifact identity:** <same immutable ID/digest as Proof; source SHA for this template>
**Artifact source:** <originating merged Build SHA, matching Proof and Build commit>
**Destination:** <delivery target>
**Result:** success
**Delivery evidence:** <link to successful delivery evidence>

<!-- Fill only with verified results. Do not claim passed/delivered while blocked. -->

## Delivery

<Evidence, exact version, and any relevant limits.>

<Compare the delivered identity with Proof and record the result and
destination. Unavailable artifacts or a destination requiring a different
rebuild leave shipment unsuccessful. Keep the confirmed prototype commit
and decision reachable through shipment; follow product retention policy
afterward. This template delivers the exact merged Build source.>

## Intent results

<Evidence, exact version, and any relevant limits.>
