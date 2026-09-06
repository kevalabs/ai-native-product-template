# Git hooks and PR verification

Run `make setup` once per clone. It sets `core.hooksPath` to the
relative `.githooks` directory, so each worktree uses its own version.
Git, Make, and Python 3.9+ are required. Run `make test` for the template
regression suite, whitespace checks, shell syntax, Python syntax, and
required entry points. Product repos add their tests, lint, and build.

## Artifact handoff

1. Create `artifact/NNN-name` in a worktree from the updated default
   branch. Draft the intent; the owner accepts it before spec starts.
2. Draft the spec in that worktree. Once accepted, commit the documents
   and land the reviewed artifact PR. For a later phase, another
   artifact PR adds that phase's spec under the existing intent.
3. Create `feature/NNN-name` or `feature/NNN-Pn-name` from the updated
   default branch. The accepted documents are already committed there.
4. Review the plan, set its standalone status line to
   `**Status:** approved`, and commit only that file. Then implement.

Keep implementation history linear. Rebase onto the target branch
instead of merging it. Preserve the plan-only first commit until the
PR checks and human review pass; the final reviewed merge may squash.
If the artifact PR was squashed, rebase only the implementation commits
onto the updated main; do not replay the old artifact commit too.

## Allowed branches

| Branch | Allowed changes |
|--------|-----------------|
| `artifact/NNN-name` | This chain's intent, specs, design exports (`md`, `png`, `jpg`, `jpeg`, `webp`, `svg`, `pdf`), and `questions-for-<role>.md` |
| `artifact/bootstrap` | Founding product intent, glossary, personas, regions, architecture; root AGENTS, REVIEW, README, LICENSE; bootstrap skill document |
| `feature/NNN-name` | Implementation after that chain's committed approved plan |
| `feature/NNN-Pn-name` | Implementation after that exact phase's committed approved plan |

Numbers have at least three digits; names use lowercase words, digits,
and hyphens. Bootstrap documents still need review. Artifact branches
cannot change hooks, scripts, workflows, application files, or plans.
Other branch names and local detached HEAD commits are rejected.

## What the checks enforce

The shell hook calls `scripts/check_sdlc.py --staged`. It reads the Git
index and committed objects, including deletions, both sides of renames,
and filenames containing whitespace. There are no broad Markdown or
directory exemptions on implementation branches.

For feature changes it requires accepted intent/spec files in HEAD,
an approved plan in the proposed commit, and an already committed
approved plan before implementation. It checks that the plan was
introduced alone with approval. Missing, untracked, draft, deleted,
or sibling-phase plans fail. `packages/` changes also need
`**Kind:** contracts` in the committed intent and `packages/` under
`## Touched surface` in the previously committed approved plan.

CI's `SDLC history` job calls the same validator for every PR commit.
It additionally requires the accepted requirements to exist at the PR
merge base and the first implementation commit to contain only the plan.
It rejects merge commits within the PR and rejects violations even if
a later commit fixes or reverts them. Full history is fetched; the
validator fails if a required Git object is missing.

For local history verification:

```bash
python3 scripts/check_sdlc.py --base origin/main --head HEAD \
  --branch feature/007-refund-requests
```

Use the actual default branch and feature name. This is separate from
`make test`, which also runs on main and on the CI merge checkout.

## Human review and repository settings

The scripts check paths, status markers, and history. They cannot
establish that a human actually approved an artifact, that a test proves
an outcome, or that capability docs describe the behavior correctly.
`REVIEW.md` remains responsible for those checks and the touched-file
list. Review changes to this validator, its tests, and the workflow:
a PR can modify the checks that run against it.

In default-branch protection, require `SDLC history`,
`Template verification`, a human approving review, and renewed approval
after changes. Apply the rules to administrators and restrict bypasses.
For another default-branch name, also update the workflow's push branch.
These are administrator settings; `make setup` cannot install them.

The workflow uses the ordinary
[pull_request event](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#pull_request),
read-only repository permissions, and explicit PR head/base commits for
history validation. Template tests run on GitHub's proposed merge tree.
It does not use pull_request_target to execute contributor code.

`git commit --no-verify` can skip a local hook. Required CI and human
review must still pass before merge. Agent-native hooks may call the
same validator to fail earlier; they are never the only check.
