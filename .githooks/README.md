# Git hooks — deterministic enforcement, for every agent

Skills advise; hooks enforce. These are plain git hooks so they bind
Claude Code, Codex, Antigravity, Gemini CLI, and humans alike —
nothing here depends on one agent's hook system.

Install once per clone (bootstrap adds this to `make setup`):

```bash
git config core.hooksPath .githooks
```

## What `pre-commit` blocks

1. **Commits on the default branch.** Work lands via reviewed PR
   only.
2. **Code on a feature branch with no `plan.md`.** `plan.md` is the
   first commit; artifacts under `features/`, `product/`, `docs/`,
   `.agents/`, and any Markdown are exempt so the plan itself can be
   committed.
3. **Edits under `packages/` from a feature branch** unless that
   chain's `plan.md` declares `packages/` in its touched surface —
   contracts change through their own chain, never as drive-bys.

`git commit --no-verify` skips the hook. That is for humans in an
emergency; CI and branch protection must repeat these checks so a
skipped hook never lands anything. Anything `REVIEW.md` treats as
blocking that a machine can detect deterministically belongs here or
in CI, not in a skill.

## Agent-native hooks (optional)

If an agent offers its own hooks (Claude Code's `settings.json`
hooks, for example), use them only to fail faster on the same rules —
never as the only enforcement. Per-machine settings files such as
`.claude/settings.local.json` are git-ignored.
