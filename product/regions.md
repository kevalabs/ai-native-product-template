# Regions — market strategy

**Status:** TEMPLATE. Delete this file if the product is
single-region — and remove region rules from CLAUDE.md/REVIEW.md.

## Model

<!-- template: the recommended multi-region shape (adapt or replace):
one product, one codebase, one mobile binary. Region is a first-class
runtime concept:
- client resolves region once, binds the account, talks to that
  region's backend
- all variance declared in the region registry (packages/regions/):
  currency, providers, locale, business-rule parameters, feature flags
- business logic never branches on region codes (blocking review rule)
- backends deploy per region — separate containers and database, so
  personal/financial data stays in-country
- accounts are regional in v1 unless cross-region identity is a real
  requirement
- per-region feature flags allow shipping to one market first -->

## {{REGION_CODE}} — launch region

- **Hosting:** <!-- provider + open due-diligence items (SLA, backups,
  SSL) -->
- **Currency / Timezone(s):** <!-- note oddities: 45-min offsets, DST -->
- **Payments / SMS:** <!-- provider shortlist, [TO CONFIRM] -->
- **Language:** <!-- launch locale; strings externalized regardless -->

## {{REGION_CODE_2}} — second region

<!-- same shape; note compliance regime (data residency laws) -->

## Phasing

<!-- 1. build with all regions in the registry from day one (money,
        timezone, provider interfaces, i18n are cheap now, brutal later)
     2. launch region 1; run region 2 as staging so portability is
        exercised, not assumed
     3. launch region 2: target date [TO CONFIRM] -->

`make deploy REGION=…` — same images, different target and config.
No long-lived version branches; `main` + tags + regional flags only.
