# {{PRODUCT_NAME}} — Agent Conventions

This is the one conventions file for every coding agent working in
this repo. Codex, Antigravity, and Gemini CLI read it directly;
`CLAUDE.md` and `GEMINI.md` are one-line pointers to it; Antigravity
also gets a pointer in `.agents/rules/`. Skills (the stage commands)
live in `.agents/skills/`, which every agent reads (`.claude/skills`
is a symlink to it). Edit this file, never the pointers.

Read `product/intent.md` for what this product is. Every feature is
built from a committed artifact chain in `features/NNN-name/`:
`intent.md` (why) → `spec.md` (what) → `plan.md` (how) → code →
proof → ship. The model behind it is `docs/agentic-sdlc.md`. Do not
write feature code without an approved `plan.md` in that feature's
(or phase's) directory.

## Workflow rules (generic — keep)

- Every outcome follows Intent → Spec → Plan → Build → Test + Review
  → Ship. Commit each stage's artifacts, obtain the required human
  approval, and merge its own PR before starting the next stage.
- Never commit directly to the default branch. Start every stage in
  its own worktree from the updated default branch. Artifact branches
  carry one intent or exact-phase spec; feature branches carry a
  Plan-only PR or a Build PR with an already merged Plan. Proof and
  Ship use their own branches and evidence PRs. No stacked-stage work.
- Every proposal begins with a draft intent. Owner acceptance of
  intent/spec and approval of plan are recorded before merging their
  PRs. Explicit approval in the working conversation counts: record
  it, do not ask for it again. Agents cannot invent human approval.
- The parent GitHub issue has type Intent; stage sub-issues have type
  Task. Every issue links to its governing Markdown artifact or section;
  each new artifact links back. Completed tasks retain an approved
  commit permalink and merged PR. Closing an issue is not a merge gate.
- Before stage work, fetch the default branch and run `make handoff`
  for its task. Missing or inaccessible evidence blocks that handoff.
  Local index checks are useful offline but do not establish remote
  approval. See `.githooks/README.md` for commands and evidence fields.
- Cut work by outcome. A large intent has fixed phases and dependencies;
  each phase follows Spec through Ship after the shared Intent merge.
  Independent phases may run in parallel only when their prerequisites
  and shared contracts are settled. Keep PR history linear.
- Begin Build with the accepted spec in context. The approved plan,
  including touched files, lands alone in its first commit and its own
  PR before code. Build cannot amend its own approved scope.
- Keep spec about behavior; implementation detail belongs in Plan.
  Artifacts use `.agents/writing-style.md` and exact glossary terms.
- `make test` must pass before handoff, including before Build merges.
  Bug fixes start with a failing test; never edit an existing test just
  to make a fix pass. Behavior changes update matching capability docs
  in the Build PR, describing any remaining release restrictions.
- Proof names the exact merged Build, results for every S-rule, intent
  success results, and human review. Blocking findings prevent Ship.
  Corrections need reviewed Build changes and renewed proof.
- Ship follows merged proof. Record the delivered version and result;
  close the parent only after all phases and success criteria pass.
  Cancellation is not shipment. Shipped artifacts remain immutable.
- Add new process/domain vocabulary to `product/glossary.md` in the PR
  introducing it. Keep shipped history unchanged; record legacy gaps
  honestly when adopting the next stage's gates.
- `artifact/bootstrap` remains a separate reviewed constitution PR,
  limited to its existing document allowlist. No application, hook,
  or CI changes belong there.
- Run `make setup` once per clone. `make setup-check` reports remote
  setup separately; configure required `SDLC history`, `Template
  verification`, and human review in repository policy. A local command
  cannot install or attest administrator settings it cannot access.
- Hooks and CI check stage scope, prerequisites, paths, history, and
  links. Human review verifies actual approval and semantic evidence
  under `REVIEW.md`. Review changes to the checks themselves.

## Code rules (product-specific — bootstrap fills this)

- Money is integer minor units + ISO currency code. No float
  arithmetic on money.
- Domain times carry an explicit IANA timezone. Never use server-local
  time for domain logic.
- Personal data never appears in logs, error messages, or analytics
  events.
- All user-facing strings are externalized (i18n) — no hardcoded copy.
- Region variance goes through the regions registry and provider
  interfaces only — business logic must not branch on region codes.
  (Delete if single-region.)
- `packages/` is contract territory: changes require their own intent
  with `Kind: contracts` and `packages/` declared in the approved
  plan's Touched surface section. No drive-by contract edits.
- {{PRODUCT_SPECIFIC_RULES}}
