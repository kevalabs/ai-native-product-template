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


def conventions(mode="runtime artifact", test_paths="tests/"):
    return ("# Demo — Agent Conventions\n\n## Delivery settings\n\n"
            f"- **Delivery:** {mode}\n- **Test paths:** {test_paths}\n")


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
        self.write("AGENTS.md", conventions())
        self.write("tests/test_demo.py", "def test_outcome():\n    assert True\n")
        self.write(f"{CHAIN}/intent.md", "**Status:** accepted\n**Kind:** change\n")
        self.write(f"{CHAIN}/spec.md", "**Status:** accepted\n- S1 A checkable outcome.\n")
        if CHECK.exists():
            self.write("scripts/check_sdlc.py", CHECK.read_text())
        self.commit("Fixture base")
        self.base = self.fixture = self.git("rev-parse", "HEAD").stdout.strip()
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

    def land_plan(self, path=PLAN):
        self.base = self.git("rev-parse", "HEAD").stdout.strip()
        self.git("branch", "-f", "main", "HEAD")
        directory = path.rsplit("/", 1)[0]
        phase = "single" if directory == CHAIN else directory.rsplit("/", 1)[1]
        self.write(f"{directory}/build.md", self.record("build", phase) +
                   "**Plan commit:** " + self.base + "\n**Verification:** make test passed\n")
        self.git("add", f"{directory}/build.md")

    def record(self, stage, phase="single"):
        status = {"build": "ready", "proof": "passed", "ship": "delivered"}[stage]
        return (f"**Status:** {status}\n**Stage:** {stage}\n**Outcome:** 001-demo\n"
                f"**Phase:** {phase}\n**Parent issue:** https://github.com/example/repo/issues/1\n"
                "**Stage issue:** https://github.com/example/repo/issues/5\n"
                "**Predecessor PR:** https://github.com/example/repo/pull/4\n")

    def land_build(self):
        self.plan()
        self.land_plan()
        self.change_code()
        self.commit("Build")
        self.base = self.git("rev-parse", "HEAD").stdout.strip()
        self.git("branch", "-f", "main", "HEAD")
        self.git("checkout", "-b", "proof/001-demo")
        self.write(f"{CHAIN}/proof.md", self.record("proof") +
                   f"**Build commit:** {self.base}\n**Blocking findings:** none\n"
                   "## Requirement results\n- S1: PASS — test_outcome\n"
                   "## Verification\nmake test passed\n## Human review\nOwner review recorded\n"
                   "## Intent results\nAll success criteria met\n")
        self.git("add", f"{CHAIN}/proof.md")

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

    def staged_build(self, conventions_text):
        """Stage a Build under the given conventions file, starting from main."""
        self.git("checkout", "main")
        self.git("reset", "--hard", self.fixture)
        self.write("AGENTS.md", conventions_text)
        self.git("add", "-A")
        self.git("commit", "--allow-empty", "-m", "Conventions")
        self.git("checkout", "-B", "feature/001-demo")
        self.plan()
        self.land_plan()
        self.change_code()

    def hook_error(self):
        result = subprocess.run(
            ["sh", str(HOOK)], cwd=self.repo, env=self.env,
            capture_output=True, text=True,
        )
        self.assertNotEqual(result.returncode, 0, result.stdout)
        return result.stderr

    def test_delivery_setting_modes_and_errors(self):
        """T1 (S1, S20): a declared mode is accepted; absent or misspelled fails."""
        self.staged_build(conventions("runtime artifact"))
        self.hook(True)
        self.staged_build("# Demo — Agent Conventions\n\nNo settings here.\n")
        self.assertIn("Delivery settings", self.hook_error())
        self.staged_build(conventions("merged sources"))
        message = self.hook_error()
        self.assertIn("merged source", message)
        self.assertIn("runtime artifact", message)

    def merged_source_build(self, results="- S1: PASS — test_outcome\n",
                            intent_results="- TRUE — the outcome is reachable\n",
                            criteria="- the outcome is reachable\n", rules="- S1 A checkable outcome.\n"):
        """Stage a merged-source Build whose record carries its evidence sections."""
        self.git("checkout", "main")
        self.git("reset", "--hard", self.fixture)
        self.write("AGENTS.md", conventions("merged source"))
        self.write(f"{CHAIN}/intent.md",
                   "**Status:** accepted\n**Kind:** change\n\n## Success criteria\n\n" + criteria)
        self.write(f"{CHAIN}/spec.md", "**Status:** accepted\n\n## Requirements\n\n" + rules)
        self.commit("Merged-source conventions")
        self.git("checkout", "-B", "feature/001-demo")
        self.plan()
        self.land_plan()
        record = (self.repo / CHAIN / "build.md").read_text()
        self.write(f"{CHAIN}/build.md", record +
                   "\n## Requirement results\n\n" + results +
                   "\n## Intent results\n\n" + intent_results)
        self.git("add", f"{CHAIN}/build.md")
        self.change_code()

    def test_build_record_requires_result_per_s_rule(self):
        """T3 (S3, S4, S21, S22): every rule needs a passing result naming a real test."""
        self.merged_source_build()
        self.hook(True)
        self.merged_source_build(rules="- S1 A checkable outcome.\n- S2 A second rule.\n")
        self.assertIn("S2", self.hook_error())
        self.merged_source_build(results="- S1: FAIL — test_outcome\n")
        self.assertIn("S1", self.hook_error())
        self.merged_source_build(results="- S1: PASS — test_absent_from_the_suite\n")
        self.assertIn("test_absent_from_the_suite", self.hook_error())

    def test_last_phase_records_every_intent_criterion(self):
        """T4 (S5, S14): the last phase reports every criterion; an open one blocks."""
        self.merged_source_build(
            criteria="- the outcome is reachable\n- the complaint stops\n",
            intent_results="- TRUE — the outcome is reachable\n- TRUE — the complaint stops\n")
        self.hook(True)
        self.merged_source_build(
            criteria="- the outcome is reachable\n- the complaint stops\n",
            intent_results="- TRUE — the outcome is reachable\n")
        self.assertIn("Intent results", self.hook_error())
        self.merged_source_build(
            criteria="- the outcome is reachable\n- the complaint stops\n",
            intent_results="- TRUE — the outcome is reachable\n- OPEN — the complaint stops\n")
        self.assertIn("OPEN", self.hook_error())

    def test_runtime_artifact_path_is_unchanged(self):
        """T2 (S2, S25): a runtime-artifact Build needs no S-rule results."""
        self.staged_build(conventions("runtime artifact"))
        self.hook(True)

    def test_shipped_tag_freezes_the_phase(self):
        """T8 (S11): a shipped tag makes its phase immutable, as ship.md did."""
        self.merged_source_build()
        self.commit("Build")
        self.git("tag", "-a", "shipped/001-demo", "-m", "Shipped in PR #1")
        self.git("branch", "-f", "main", "HEAD")
        self.change_code()
        self.assertIn("shipped", self.hook_error())

    def test_records_carry_each_tracking_fact_once(self):
        """T9 (S12): no record repeats one commit hash across header fields."""
        self.merged_source_build()
        self.hook(True)
        record = (self.repo / CHAIN / "build.md").read_text()
        plan_commit = record.split("**Plan commit:** ")[1].split("\n")[0]
        self.write(f"{CHAIN}/build.md",
                   record.replace("**Verification:** make test passed",
                                  f"**Artifact source:** {plan_commit}\n**Verification:** make test passed"))
        self.git("add", f"{CHAIN}/build.md")
        self.assertIn("once", self.hook_error())

    def test_guidance_states_one_consistent_policy(self):
        """T12 (S15, S17, S19): one delivery policy and every human gate."""
        conventions = (ROOT / "AGENTS.md").read_text()
        readme = (ROOT / "README.md").read_text()
        review = (ROOT / "REVIEW.md").read_text()
        # S15: the solo-developer path is written down, not folklore.
        setup = readme.split("## 1. Read this first")[0]
        self.assertIn("authoring identity", setup)
        self.assertIn("ignores an approving review", setup)
        # S17: anything that still instructs Proof or Ship work says which
        # delivery mode it belongs to.
        guidance = ["AGENTS.md", "README.md", "REVIEW.md", "docs/agentic-sdlc.md",
                    ".githooks/README.md", "features/README.md",
                    "templates/proof-template.md", "templates/ship-template.md",
                    "templates/build-template.md", "templates/plan-template.md",
                    "product/capabilities/sdlc-workflow.md",
                    ".agents/skills/proof/SKILL.md", ".agents/skills/ship/SKILL.md",
                    ".agents/skills/build/SKILL.md", ".agents/skills/capability/SKILL.md",
                    ".agents/skills/bootstrap-product/SKILL.md"]
        for name in guidance:
            text = (ROOT / name).read_text()
            if "proof.md" in text or "Proof PR" in text or "ship.md" in text:
                self.assertTrue("merged source" in text or "runtime artifact" in text
                                or "Delivery" in text, name)
        # S19: no human gate was dropped.
        for gate in ("intent", "spec", "plan"):
            self.assertIn(gate, conventions)
        self.assertIn("approving review", conventions)
        self.assertIn("approving review", review)

    def staged_fix(self, branch="fix/broken-rule", record="fixes/001-broken-rule.md",
                   test="tests/test_fix.py", code=True):
        """Stage a fix: a changed test, the change itself, and its record."""
        self.git("checkout", "main")
        self.git("reset", "--hard", self.fixture)
        self.write("AGENTS.md", conventions("merged source"))
        self.git("add", "-A")
        self.git("commit", "--allow-empty", "-m", "Conventions")
        self.git("checkout", "-B", branch)
        if test:
            self.write(test, "def test_restores_stated_behavior():\n    assert True\n")
            self.git("add", "--", test)
        if record:
            self.write(record, "# Fix\n\n**Failing test:** test_restores_stated_behavior\n"
                               "**Corrects:** features/001-demo\n**Restores:** R1\n"
                               "**Date:** 2026-09-17\n")
            self.git("add", "--", record)
        if code:
            self.change_code()

    def test_fix_branch_carries_test_change_and_record(self):
        """T1 (S1, S2): a fix branch needs no stage artifact."""
        self.staged_fix()
        self.hook(True)
        self.staged_fix(branch="chore/broken-rule")
        self.assertIn("unsupported branch", self.hook_error())

    def test_fix_requires_a_changed_test(self):
        """T6 (S8, S15): a fix starts from a failing test."""
        self.staged_fix(test=None)
        self.assertIn("test", self.hook_error())

    def test_fix_cannot_touch_features_or_add_stage_artifacts(self):
        """T4 (S6, S9, S16): shipped outcomes stay immutable."""
        self.staged_fix()
        self.write(f"{CHAIN}/spec.md", "**Status:** accepted\n- S1 Changed.\n")
        self.git("add", f"{CHAIN}/spec.md")
        self.assertIn("features/", self.hook_error())

    def test_fix_record_numbering_is_checked(self):
        """T3 (S5, S17): one numbered record per fix, never reused."""
        self.staged_fix(record=None)
        self.assertIn("fixes/", self.hook_error())
        self.staged_fix(record="fixes/broken-rule.md")
        self.assertIn("fixes/", self.hook_error())
        self.git("checkout", "main")
        self.git("reset", "--hard", self.fixture)
        self.write("AGENTS.md", conventions("merged source"))
        self.write("fixes/001-earlier.md", "# Earlier fix\n")
        self.commit("Earlier fix")
        self.git("checkout", "-B", "fix/broken-rule")
        self.write("tests/test_later.py", "def test_later():\n    assert True\n")
        self.write("fixes/001-broken-rule.md", "# Fix\n")
        self.git("add", "-A")
        self.assertIn("001", self.hook_error())

    def test_merged_fix_record_is_immutable(self):
        """T8 (S11, S12): a merged record is final and needs no tag."""
        self.staged_fix()
        self.commit("Fix")
        self.git("branch", "-f", "main", "HEAD")
        self.git("checkout", "-B", "fix/second-try")
        self.write("fixes/001-broken-rule.md", "# Fix\n\nEdited after merge.\n")
        self.write("tests/test_fix.py", "def test_two():\n    assert True\n")
        self.git("add", "-A")
        self.assertIn("immutable", self.hook_error())

    def test_review_policy_states_the_restore_only_rule(self):
        """T2 (S3, S4, S19): the reviewer's judgement is written down."""
        review = (ROOT / "REVIEW.md").read_text()
        self.assertIn("restore", review.lower())
        self.assertIn("Size never decides", review)
        self.assertIn("new work", review)
        self.assertIn("intent", review)

    def test_guidance_describes_the_fix_lane_once(self):
        """T10 (S14, S20): every guidance file tells the same fix story."""
        for name in ("AGENTS.md", "README.md", "REVIEW.md", ".githooks/README.md",
                     "docs/agentic-sdlc.md", "fixes/README.md",
                     "product/capabilities/sdlc-workflow.md",
                     "product/glossary.md", "templates/fix-template.md"):
            text = (ROOT / name).read_text()
            self.assertIn("fix", text.lower(), name)
        for name in ("AGENTS.md", "README.md", ".githooks/README.md", "fixes/README.md"):
            text = (ROOT / name).read_text()
            self.assertIn("fix/", text, name)
            self.assertIn("fixes/", text, name)

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
        self.land_plan()
        self.change_code()
        self.hook(True)

    def test_plan_deletion_is_blocked(self):
        self.plan()
        self.git("rm", PLAN)
        self.hook(False)

    def test_unstaged_plan_edit_does_not_affect_committed_approval(self):
        self.plan()
        self.land_plan()
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
        self.land_plan(path=f"{CHAIN}/P2-next/plan.md")
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
        self.land_plan()
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
        self.land_plan()
        self.change_code("packages/types.py")
        self.hook(False)

    def test_dedicated_contract_chain_is_allowed(self):
        self.git("checkout", "main")
        self.write(f"{CHAIN}/intent.md", "**Status:** accepted\n**Kind:** contracts\n")
        self.commit("Accepted contract intent")
        self.git("checkout", "-B", "feature/001-demo")
        self.plan(APPROVED + "- packages/types.py\n")
        self.land_plan()
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

    def test_build_history_accepts_plan_already_on_base(self):
        self.plan()
        self.base = self.git("rev-parse", "HEAD").stdout.strip()
        self.write(f"{CHAIN}/build.md", "**Status:** ready\n**Stage:** build\n"
                   "**Outcome:** 001-demo\n**Phase:** single\n"
                   "**Parent issue:** https://github.com/example/repo/issues/1\n"
                   "**Stage issue:** https://github.com/example/repo/issues/5\n"
                   "**Predecessor PR:** https://github.com/example/repo/pull/4\n"
                   "**Plan commit:** " + self.base + "\n"
                   "**Verification:** make test passed\n")
        self.change_code()
        self.commit("Build after merged plan")
        self.history(True)

    def test_artifact_history_rejects_bundled_intent_and_spec(self):
        self.git("branch", "-m", "artifact/001-demo")
        self.write(f"{CHAIN}/intent.md", "**Status:** accepted\nChanged intent\n")
        self.write(f"{CHAIN}/spec.md", "**Status:** accepted\nChanged spec\n")
        self.commit("Bundle two stages")
        self.history(False, "artifact/001-demo")

    def test_build_rejects_unmerged_plan(self):
        self.plan()
        self.change_code()
        self.hook(False)
        self.commit("Code on unmerged plan")
        self.history(False)

    def test_build_rejects_undeclared_file(self):
        self.plan()
        self.land_plan()
        self.change_code("undeclared.py")
        self.hook(False)

    def test_build_cannot_edit_its_plan(self):
        self.plan()
        self.land_plan()
        self.write(PLAN, APPROVED + "- extra.py\n")
        self.git("add", PLAN)
        self.change_code()
        self.hook(False)

    def test_proof_allows_complete_evidence(self):
        self.land_build()
        self.hook(True)
        self.commit("Proof")
        self.history(True, "proof/001-demo")

    def test_proof_rejects_missing_requirement_result(self):
        self.land_build()
        text = (self.repo / f"{CHAIN}/proof.md").read_text()
        self.write(f"{CHAIN}/proof.md", text.replace("- S1: PASS — test_outcome", ""))
        self.git("add", f"{CHAIN}/proof.md")
        self.hook(False)

    def test_proof_rejects_code_changes(self):
        self.land_build()
        self.change_code("extra.py")
        self.hook(False)

    def test_ship_requires_current_proof_and_success(self):
        self.land_build()
        build = self.base
        self.commit("Proof")
        self.base = self.git("rev-parse", "HEAD").stdout.strip()
        self.git("branch", "-f", "main", "HEAD")
        self.git("checkout", "-b", "ship/001-demo")
        self.write(f"{CHAIN}/ship.md", self.record("ship") +
                   f"**Build commit:** {build}\n**Proof commit:** {self.base}\n"
                   "**Destination:** main\n**Delivery evidence:** verified version\n**Result:** success\n")
        self.git("add", f"{CHAIN}/ship.md")
        self.hook(True)
        self.commit("Ship")
        self.history(True, "ship/001-demo")

    def test_proof_rejects_stale_build(self):
        self.land_build()
        self.git("reset")
        self.write("app.py", "print('changed after test')\n")
        self.git("add", "app.py")
        self.git("commit", "-m", "Changed code")
        self.base = self.git("rev-parse", "HEAD").stdout.strip()
        self.git("branch", "-f", "main", "HEAD")
        self.git("add", f"{CHAIN}/proof.md")
        self.hook(False)

    def test_spec_requires_accepted_intent_on_base(self):
        self.git("checkout", "main")
        self.write(f"{CHAIN}/intent.md", "**Status:** draft\n")
        self.commit("Draft intent")
        self.base = self.git("rev-parse", "HEAD").stdout.strip()
        self.git("checkout", "-b", "artifact/001-demo")
        self.write(f"{CHAIN}/spec.md", "**Status:** draft\n")
        self.git("add", f"{CHAIN}/spec.md")
        self.hook(False)

    def test_proof_wrong_phase_is_rejected(self):
        self.land_build()
        text = (self.repo / f"{CHAIN}/proof.md").read_text().replace("**Phase:** single", "**Phase:** P2-other")
        self.write(f"{CHAIN}/proof.md", text)
        self.git("add", f"{CHAIN}/proof.md")
        self.hook(False)


if __name__ == "__main__":
    unittest.main()
