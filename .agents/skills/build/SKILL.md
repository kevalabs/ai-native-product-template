---
name: build
description: Implement an outcome or phase after its approved Plan PR has merged; verify changes and prepare the separate Build PR.
---

Build feature NNN or phase Pn under its accepted Spec and approved Plan.
Read those artifacts and AGENTS.md before editing code. Read
`.githooks/README.md` for record fields and gate commands.

1. Fetch the default branch. Find the existing Intent parent and Build
   Task, and run `make handoff` for that Task before coding. Verify the
   exact Plan PR is approved and merged. Start a feature worktree from
   the updated default branch; do not stack on an unmerged Plan.
2. Read the plan's touched surface and other active plans for collisions.
   Implement only approved scope. New requirements or changed scope go
   through their own accepted stage PR before dependent work continues.
3. Write `build.md` using `templates/build-template.md`. Link its Task,
   parent, merged Plan PR, and exact Plan commit. Record older missing
   backlinks under Transition when adopting a legacy chain, with real
   approval and merge links. Never claim historical compliance.
4. Implement and test the approved changes. Bug fixes start with a
   failing test. Update matching capability docs with current behavior
   and any release restrictions. New glossary terms land in this PR.
5. Run make test, staged checks, and full PR-history checks. Review the
   complete diff against the declared files and every S-rule. Record
   actual verification in build.md; incomplete work is not ready.
6. Commit, push, and open the separate Build PR ready for review with a
   Stage issue header and artifact link. Update the existing Task with
   that PR, then run live GitHub evidence checks. Look up identities
   before mutations and verify an unknown write result before retrying.
7. After human review and merge, record the approved artifact permalink
   and merged PR on the Build Task and close it as completed. Keep the
   parent open. Only then may `/proof` start. A Build merge is not Ship.

Do not create Proof or Ship evidence early. If proof later identifies
an in-scope correction, use another Build PR updating build.md, then
repeat proof for the corrected merged version. Stop if required evidence
is missing or remote verification is unavailable.
