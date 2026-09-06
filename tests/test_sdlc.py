"""Exercise the contributor workflow in disposable Git repositories."""

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / ".githooks/pre-commit"
CHECK = ROOT / "scripts/check_sdlc.py"
CHAIN = "features/001-demo"
PLAN = f"{CHAIN}/plan.md"
APPROVED = "**Status:** approved\n\n## Touched surface\n\n- app.py\n"


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="sdlc-test-")
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.env = {
            key: value for key, value in os.environ.items()
            if not key.startswith("GIT_")
        }
        self.env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Workflow Test")
        self.git("config", "user.email", "test@example.invalid")
        self.write("app.py", "print('before')\n")
        self.write(f"{CHAIN}/intent.md", "**Status:** accepted\n**Kind:** change\n")
        self.write(f"{CHAIN}/spec.md", "**Status:** accepted\n")
        if CHECK.exists():
            self.write("scripts/check_sdlc.py", CHECK.read_text())
        self.commit("Fixture base")
        self.base = self.git("rev-parse", "HEAD").stdout.strip()
        self.git("checkout", "-b", "feature/001-demo")

    def git(self, *args):
        return subprocess.run(
            ["git", "-c", "core.hooksPath=/dev/null", *args],
            cwd=self.repo, env=self.env, capture_output=True, text=True, check=True,
        )

    def write(self, path, text):
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)

    def commit(self, message):
        self.git("add", "-A")
        self.git("commit", "-m", message)

    def plan(self, text=APPROVED, path=PLAN):
        self.write(path, text)
        self.commit("Approved plan")

    def change_code(self, path="app.py"):
        self.write(path, "print('after')\n")
        self.git("add", "--", path)

    def hook(self, allowed):
        result = subprocess.run(
            ["sh", str(HOOK)], cwd=self.repo, env=self.env,
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode == 0, allowed, result.stderr + result.stdout)

    def history(self, allowed, branch="feature/001-demo"):
        result = subprocess.run(
            ["python3", str(CHECK), "--base", self.base, "--head", "HEAD",
             "--branch", branch], cwd=self.repo, env=self.env,
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode == 0, allowed, result.stderr + result.stdout)

    def test_missing_plan_blocks_code(self):
        self.change_code()
        self.hook(False)

    def test_untracked_draft_does_not_authorize_code(self):
        self.write(PLAN, "**Status:** draft\n")
        self.change_code()
        self.hook(False)

    def test_committed_draft_does_not_authorize_code(self):
        self.plan("**Status:** draft\n")
        self.change_code()
        self.hook(False)

    def test_sibling_phase_does_not_authorize_code(self):
        self.git("branch", "-m", "feature/001-P2-next")
        self.plan(path=f"{CHAIN}/P1-first/plan.md")
        self.change_code()
        self.hook(False)

    def test_unsupported_branch_blocks_code(self):
        self.git("branch", "-m", "chore/demo")
        self.change_code()
        self.hook(False)

    def test_deletion_requires_plan(self):
        self.git("rm", "app.py")
        self.hook(False)

    def test_rename_requires_plan(self):
        self.git("mv", "app.py", "renamed.py")
        self.hook(False)

    def test_default_branch_is_blocked(self):
        self.git("checkout", "main")
        self.change_code()
        self.hook(False)

    def test_detached_commit_is_blocked(self):
        self.git("checkout", "--detach")
        self.change_code()
        self.hook(False)

    def test_first_plan_only_commit_is_allowed(self):
        self.write(PLAN, APPROVED)
        self.git("add", PLAN)
        self.hook(True)

    def test_plan_and_code_in_same_commit_are_blocked(self):
        self.write(PLAN, APPROVED)
        self.git("add", PLAN)
        self.change_code()
        self.hook(False)

    def test_staged_approval_does_not_authorize_code(self):
        self.plan("**Status:** draft\n")
        self.write(PLAN, APPROVED)
        self.git("add", PLAN)
        self.change_code()
        self.hook(False)

    def test_committed_approved_plan_allows_code(self):
        self.plan()
        self.change_code()
        self.hook(True)

    def test_plan_deletion_is_blocked(self):
        self.plan()
        self.git("rm", PLAN)
        self.hook(False)

    def test_unstaged_plan_edit_does_not_affect_committed_approval(self):
        self.plan()
        self.write(PLAN, "**Status:** draft\n")
        self.change_code()
        self.hook(True)

    def test_missing_accepted_spec_blocks_first_plan(self):
        self.git("checkout", "main")
        self.git("rm", f"{CHAIN}/spec.md")
        self.commit("Fixture without spec")
        self.git("checkout", "-B", "feature/001-demo")
        self.write(PLAN, APPROVED)
        self.git("add", PLAN)
        self.hook(False)

    def test_exact_phase_is_allowed(self):
        self.git("checkout", "main")
        self.write(f"{CHAIN}/P2-next/spec.md", "**Status:** accepted\n")
        self.commit("Accepted phase")
        self.base = self.git("rev-parse", "HEAD").stdout.strip()
        self.git("checkout", "-B", "feature/001-P2-next")
        self.plan(path=f"{CHAIN}/P2-next/plan.md")
        self.change_code()
        self.hook(True)
        self.commit("Implementation")
        self.history(True, "feature/001-P2-next")

    def test_artifact_branch_allows_its_requirements(self):
        self.git("branch", "-m", "artifact/001-demo")
        self.write(f"{CHAIN}/spec.md", "**Status:** accepted\nA clarified rule.\n")
        self.git("add", f"{CHAIN}/spec.md")
        self.hook(True)
        self.commit("Clarify requirement")
        self.history(True, "artifact/001-demo")

    def test_artifact_branch_blocks_unrelated_documents(self):
        self.git("branch", "-m", "artifact/001-demo")
        self.write("AGENTS.md", "Disable all checks\n")
        self.git("add", "AGENTS.md")
        self.hook(False)

    def test_artifact_branch_blocks_code_even_inside_feature_directory(self):
        self.git("branch", "-m", "artifact/001-demo")
        self.change_code(f"{CHAIN}/design/run.py")
        self.hook(False)

    def test_artifact_branch_cannot_add_a_plan(self):
        self.git("branch", "-m", "artifact/001-demo")
        self.write(PLAN, APPROVED)
        self.git("add", PLAN)
        self.hook(False)

    def test_removed_idea_branch_is_rejected(self):
        self.git("branch", "-m", "artifact/ideas")
        self.write("product/IDEAS.md", "- A new thought\n")
        self.git("add", "product/IDEAS.md")
        self.hook(False)
        self.commit("Try the removed entry point")
        self.history(False, "artifact/ideas")

    def test_artifact_branch_rejects_removed_inbox_exception(self):
        self.git("branch", "-m", "artifact/001-demo")
        self.write(f"{CHAIN}/spec.md", "**Status:** accepted\nA clarified rule.\n")
        self.write("product/IDEAS.md", "- A new thought\n")
        self.git("add", f"{CHAIN}/spec.md", "product/IDEAS.md")
        self.hook(False)
        self.commit("Try an inbox change with accepted requirements")
        self.history(False, "artifact/001-demo")

    def test_bootstrap_branch_cannot_change_enforcement(self):
        self.git("branch", "-m", "artifact/bootstrap")
        self.write("product/intent.md", "A product constitution\n")
        self.git("add", "product/intent.md")
        self.hook(True)
        self.change_code(".githooks/pre-commit")
        self.hook(False)

    def test_filename_with_newline_cannot_hide_deletion(self):
        self.git("checkout", "main")
        path = "odd\nname.py"
        self.write(path, "print(1)\n")
        self.commit("Fixture unusual filename")
        self.git("checkout", "-B", "feature/001-demo")
        self.git("rm", "--", path)
        self.hook(False)

    def test_valid_history_passes(self):
        self.plan()
        self.change_code()
        self.commit("Implementation")
        self.history(True)

    def test_history_rejects_code_before_plan_even_if_final_tree_is_valid(self):
        self.change_code()
        self.commit("Bypassed hook")
        self.plan()
        self.history(False)

    def test_history_rejects_a_plan_bundled_with_code(self):
        self.write(PLAN, APPROVED)
        self.change_code()
        self.commit("Bundled plan and code")
        self.history(False)

    def test_history_rejects_draft_later_marked_approved(self):
        self.plan("**Status:** draft\n")
        self.write(PLAN, APPROVED)
        self.commit("Late approval")
        self.history(False)

    def test_history_rejects_artifact_bypass_even_if_code_is_reverted(self):
        self.git("branch", "-m", "artifact/001-demo")
        self.change_code()
        self.commit("Forbidden code")
        self.write("app.py", "print('before')\n")
        self.commit("Revert forbidden code")
        self.history(False, "artifact/001-demo")

    def test_contract_change_requires_its_own_chain(self):
        self.plan(APPROVED + "- packages/types.py\n")
        self.change_code("packages/types.py")
        self.hook(False)

    def test_dedicated_contract_chain_is_allowed(self):
        self.git("checkout", "main")
        self.write(f"{CHAIN}/intent.md", "**Status:** accepted\n**Kind:** contracts\n")
        self.commit("Accepted contract intent")
        self.git("checkout", "-B", "feature/001-demo")
        self.plan(APPROVED + "- packages/types.py\n")
        self.change_code("packages/types.py")
        self.hook(True)

    def test_installed_hook_blocks_an_actual_commit(self):
        hook_dir = self.repo / ".githooks"
        hook_dir.mkdir()
        shutil.copy2(HOOK, hook_dir / "pre-commit")
        (hook_dir / "pre-commit").chmod(0o755)
        shutil.copy2(ROOT / "Makefile", self.repo / "Makefile")
        subprocess.run(["make", "setup"], cwd=self.repo, env=self.env,
                       capture_output=True, check=True)
        self.change_code()
        result = subprocess.run(["git", "commit", "-m", "Must be blocked"],
                                cwd=self.repo, env=self.env, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b"sdlc:", result.stderr)
        self.assertEqual(self.git("rev-parse", "HEAD").stdout.strip(), self.base)

    def test_missing_history_object_is_an_explicit_error(self):
        result = subprocess.run(
            ["python3", str(CHECK), "--base", "missing-ref", "--head", "HEAD",
             "--branch", "feature/001-demo"], cwd=self.repo, env=self.env,
            capture_output=True, text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("sdlc:", result.stderr)


if __name__ == "__main__":
    unittest.main()
