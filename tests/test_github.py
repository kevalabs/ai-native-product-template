"""Evidence checks use fake GitHub responses; no credentials or network needed."""

import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import check_github as remote
import check_sdlc as local

REPO = "example/repo"
URL = "https://github.com/" + REPO
ROOT = "features/001-demo"
BASE, HEAD = "a" * 40, "b" * 40


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.data = {"": {"default_branch": "main"}}
        self.data["/issues/100"] = {
            "number": 100, "state": "open", "type": {"name": "Intent"},
            "body": f"**Outcome:** 001-demo\n**Status:** Accepted\n**Artifact:** {URL}/blob/{HEAD}/{ROOT}/intent.md\n",
        }
        children = []
        for number, stage in enumerate(local.STAGES, 1):
            done = number < 4
            ref = BASE if done else HEAD
            body = (f"**Outcome:** 001-demo\n**Stage:** {stage}\n**Phase:** single\n"
                    f"**Parent issue:** {URL}/issues/100\n**Owner:** Owner\n"
                    f"**Status:** {'Done' if done else 'In progress'}\n"
                    f"**Artifact:** {URL}/blob/{ref}/{ROOT}/{stage}.md\n"
                    "**Completion criteria:** approved outcome and merged evidence\n")
            if done:
                body += f"**Review PR:** {URL}/pull/9\n**Approved artifact:** {URL}/blob/{BASE}/{ROOT}/{stage}.md\n"
            elif stage == "build":
                body += f"**Review PR:** {URL}/pull/20\n"
            self.data[f"/issues/{number}"] = {"number": number, "id": number, "state": "closed" if done else "open",
                                             "state_reason": "completed" if done else None, "type": {"name": "Task"}, "body": body}
            children.append({"number": number})
        self.data["/issues/100/sub_issues"] = children
        self.data["/issues/4/dependencies/blocked_by"] = [{"number": 3}]
        self.pr = {"base": {"repo": {"full_name": REPO}, "ref": "main"}, "merged": True,
                   "merge_commit_sha": BASE, "head": {"sha": BASE}, "merged_by": {"type": "User"},
                   "user": {"login": "author"}}
        self.data["/pulls/9"] = self.pr
        self.data["/pulls/9/reviews"] = []
        self.data["/pulls/9/files"] = [{"filename": ROOT + "/plan.md"}]
        self.data["/pulls/20"] = {"base": {"repo": {"full_name": REPO}, "ref": "main"},
                                  "head": {"sha": HEAD}, "body": f"**Stage issue:** {URL}/issues/4"}
        self.document = (f"**Stage:** build\n**Phase:** single\n**Outcome:** 001-demo\n"
                         f"**Parent issue:** {URL}/issues/100\n**Stage issue:** {URL}/issues/4\n"
                         f"**Predecessor PR:** {URL}/pull/9\n**Plan commit:** {BASE}\n"
                         "## Transition\nOlder plan has no issue backlink; actual reviewed PR retained.\n")
        self.files = {ROOT + "/build.md": self.document, ROOT + "/plan.md": "**Status:** approved\n",
                      ROOT + "/spec.md": "**Status:** accepted\n",
                      ROOT + "/intent.md": "**Status:** accepted\n## Phases\nSingle phase\n",
                      "AGENTS.md": ("## Delivery settings\n- **Delivery:** runtime artifact\n"
                                    "- **Test paths:** tests/\n")}
        self.evidence = remote.Evidence(REPO, lambda endpoint, pages=False: copy.deepcopy(self.data[endpoint.removeprefix("repos/" + REPO)]))
        self.content = patch.object(local, "content", side_effect=lambda ref, path: self.files.get(path, ""))
        self.content.start()
        self.addCleanup(self.content.stop)
        self.ancestry = patch.object(remote, "ancestor")
        self.ancestry.start()
        self.addCleanup(self.ancestry.stop)

    def validate(self):
        self.evidence.validate(BASE, HEAD, ("build", ROOT, ROOT), 20, "feature/001-demo")

    def test_complete_build_evidence(self):
        self.validate()

    def test_unmerged_predecessor_is_blocked_even_with_closed_issue(self):
        self.pr["merged"] = False
        with self.assertRaisesRegex(local.Violation, "must merge"):
            self.validate()

    def test_wrong_default_branch_is_blocked(self):
        self.pr["base"]["ref"] = "other"
        with self.assertRaisesRegex(local.Violation, "default branch"):
            self.validate()

    def test_wrong_repo_is_blocked(self):
        self.pr["base"]["repo"]["full_name"] = "other/repo"
        with self.assertRaisesRegex(local.Violation, "another repository"):
            self.validate()

    def test_duplicate_stage_issue_is_blocked(self):
        self.data["/issues/100/sub_issues"].append({"number": 4})
        with self.assertRaisesRegex(local.Violation, "duplicate"):
            self.validate()

    def test_phase_group_uses_its_exact_stage_artifacts(self):
        directory = ROOT + "/P1-first"
        self.data["/issues/200"] = {"number": 200, "body": "**Stage:** phase\n**Phase:** P1-first\n"}
        self.data["/issues/100/sub_issues"] = [{"number": 1}, {"number": 200}]
        self.data["/issues/200/sub_issues"] = [{"number": n} for n in range(2, 7)]
        for n in range(2, 7):
            body = self.data[f"/issues/{n}"]["body"]
            self.data[f"/issues/{n}"]["body"] = body.replace("**Phase:** single", "**Phase:** P1-first").replace(ROOT + "/", directory + "/")
        self.files[ROOT + "/intent.md"] = "**Status:** accepted\n## Phases\n- P1-first — one outcome\n"
        self.files[directory + "/build.md"] = self.document.replace("**Phase:** single", "**Phase:** P1-first")
        self.files[directory + "/plan.md"] = self.files[ROOT + "/plan.md"]
        self.files[directory + "/spec.md"] = self.files[ROOT + "/spec.md"]
        self.data["/pulls/9/files"] = [{"filename": directory + "/plan.md"}]
        self.evidence.validate(BASE, HEAD, ("build", ROOT, directory), 20, "feature/001-P1-first")

    def test_missing_stage_issue_is_blocked(self):
        self.data["/issues/100/sub_issues"].pop()
        with self.assertRaisesRegex(local.Violation, "exactly one"):
            self.validate()

    def test_cancelled_parent_is_blocked(self):
        self.data["/issues/100"]["state"] = "closed"
        with self.assertRaisesRegex(local.Violation, "parent"):
            self.validate()

    def test_closed_active_task_is_blocked(self):
        self.data["/issues/4"]["state"] = "closed"
        with self.assertRaisesRegex(local.Violation, "active task"):
            self.validate()

    def test_unfinished_dependency_is_blocked(self):
        self.data["/issues/3"]["state"] = "open"
        with self.assertRaisesRegex(local.Violation, "dependency"):
            self.validate()

    def extra_dependency(self):
        path = "features/002-other/plan.md"
        self.data["/issues/99"] = {
            "number": 99, "state": "closed", "state_reason": "completed",
            "body": ("**Status:** Done\n**Outcome:** 002-other\n"
                     "**Stage:** plan\n**Phase:** single\n"
                     f"**Review PR:** {URL}/pull/30\n"
                     f"**Approved artifact:** {URL}/blob/{BASE}/{path}\n"),
        }
        self.data["/issues/4/dependencies/blocked_by"].append({"number": 99})
        self.data["/pulls/30"] = copy.deepcopy(self.pr)
        self.data["/pulls/30/reviews"] = []
        self.data["/pulls/30/files"] = [{"filename": path}]
        self.files[path] = "**Status:** approved\n"
        return path

    def test_extra_closed_dependency_requires_merge_evidence(self):
        self.extra_dependency()
        self.data["/issues/99"]["body"] = self.data["/issues/99"]["body"].replace(
            f"**Review PR:** {URL}/pull/30\n", "")
        with self.assertRaisesRegex(local.Violation, "Review PR"):
            self.validate()

    def test_extra_dependency_unmerged_pr_is_blocked(self):
        self.extra_dependency()
        self.data["/pulls/30"]["merged"] = False
        with self.assertRaisesRegex(local.Violation, "must merge"):
            self.validate()

    def test_extra_dependency_wrong_artifact_is_blocked(self):
        self.extra_dependency()
        self.data["/issues/99"]["body"] = self.data["/issues/99"]["body"].replace(
            "features/002-other/plan.md", ROOT + "/plan.md")
        with self.assertRaisesRegex(local.Violation, "permalink"):
            self.validate()

    def test_extra_dependency_stale_artifact_is_blocked(self):
        path = self.extra_dependency()
        merge = "c" * 40
        self.data["/pulls/30"]["merge_commit_sha"] = merge
        self.data["/issues/99"]["body"] = self.data["/issues/99"]["body"].replace(BASE, merge)
        with patch.object(local, "content", side_effect=lambda ref, name:
                          "**Status:** approved\nchanged" if ref == BASE and name == path else self.files.get(name, "")):
            with self.assertRaisesRegex(local.Violation, "dependency.*changed"):
                self.validate()

    def test_extra_dependency_unavailable_evidence_is_blocked(self):
        self.extra_dependency()
        original = self.evidence.api

        def unavailable(endpoint, pages=False):
            if endpoint.endswith("/pulls/30"):
                raise local.Violation("GitHub evidence unavailable")
            return original(endpoint, pages)

        self.evidence.api = unavailable
        with self.assertRaisesRegex(local.Violation, "unavailable"):
            self.validate()

    def test_verified_extra_dependency_passes_both_gates(self):
        self.extra_dependency()
        self.validate()
        self.evidence.handoff(4, BASE)

    def test_handoff_extra_dependency_wrong_artifact_is_blocked(self):
        self.extra_dependency()
        self.data["/issues/99"]["body"] = self.data["/issues/99"]["body"].replace(
            "features/002-other/plan.md", ROOT + "/plan.md")
        with self.assertRaisesRegex(local.Violation, "permalink"):
            self.evidence.handoff(4, BASE)

    def test_cancelled_dependency_is_blocked(self):
        self.data["/issues/3"]["state_reason"] = "not_planned"
        with self.assertRaisesRegex(local.Violation, "dependency"):
            self.validate()

    def test_missing_dependency_relationship_is_blocked(self):
        self.data["/issues/4/dependencies/blocked_by"] = []
        with self.assertRaisesRegex(local.Violation, "depend"):
            self.validate()

    def test_branch_link_is_not_completion_evidence(self):
        self.data["/issues/3"]["body"] = self.data["/issues/3"]["body"].replace(f"**Approved artifact:** {URL}/blob/{BASE}", f"**Approved artifact:** {URL}/blob/main")
        with self.assertRaisesRegex(local.Violation, "permalink"):
            self.validate()

    def test_missing_legacy_transition_is_blocked(self):
        self.files[ROOT + "/build.md"] = self.document.split("## Transition")[0]
        with self.assertRaisesRegex(local.Violation, "Transition"):
            self.validate()

    def test_backlink_to_wrong_task_is_blocked(self):
        self.files[ROOT + "/build.md"] = self.document.replace("**Stage issue:** " + URL + "/issues/4", "**Stage issue:** " + URL + "/issues/5")
        with self.assertRaisesRegex(local.Violation, "backlink"):
            self.validate()

    def test_changed_pr_head_is_blocked(self):
        self.data["/pulls/20"]["head"]["sha"] = "c" * 40
        with self.assertRaisesRegex(local.Violation, "head changed"):
            self.validate()

    def test_newer_artifact_does_not_reuse_old_approval(self):
        with patch.object(local, "content", side_effect=lambda ref, path: "changed" if ref == BASE and path.endswith("plan.md") else self.files.get(path, "")):
            with self.assertRaises(local.Violation):
                self.validate()

    def test_predecessor_cannot_bundle_plan_and_code(self):
        self.data["/pulls/9/files"].append({"filename": "app.py"})
        with self.assertRaisesRegex(local.Violation, "bundled"):
            self.validate()

    def test_changed_review_blocks_predecessor(self):
        self.data["/pulls/9/reviews"] = [{"state": "CHANGES_REQUESTED", "user": {"login": "reviewer", "type": "User"}, "commit_id": BASE}]
        with self.assertRaisesRegex(local.Violation, "changes-requested"):
            self.validate()

    def test_bot_merge_needs_current_human_review(self):
        self.pr["merged_by"]["type"] = "Bot"
        self.data["/pulls/9/reviews"] = [{"state": "APPROVED", "user": {"login": "reviewer", "type": "User"}, "commit_id": "c" * 40}]
        with self.assertRaisesRegex(local.Violation, "human approving review"):
            self.validate()

    def test_dismissed_review_does_not_approve_bot_merge(self):
        self.pr["merged_by"]["type"] = "Bot"
        self.data["/pulls/9/reviews"] = [{"state": "DISMISSED", "user": {"login": "reviewer", "type": "User"}, "commit_id": BASE}]
        with self.assertRaises(local.Violation):
            self.validate()

    def reviews(self, *entries):
        self.data["/pulls/9/reviews"] = list(entries)
        self.evidence.cache.clear()

    def approval(self, login="reviewer", commit=BASE):
        return {"state": "APPROVED", "user": {"login": login, "type": "User"}, "commit_id": commit}

    def test_build_merge_requires_non_author_approval(self):
        """T5 (S6, S24): Test + Review is a current approval by someone else."""
        self.reviews()
        self.evidence.merged(9, BASE)
        self.reviews()
        with self.assertRaisesRegex(local.Violation, "approving review"):
            self.evidence.merged(9, BASE, "build")
        self.reviews(self.approval(login="author"))
        with self.assertRaisesRegex(local.Violation, "approving review"):
            self.evidence.merged(9, BASE, "build")
        self.reviews(self.approval(commit="c" * 40))
        with self.assertRaisesRegex(local.Violation, "approving review"):
            self.evidence.merged(9, BASE, "build")
        self.reviews(self.approval())
        self.evidence.merged(9, BASE, "build")

    def shipped(self, phase="single", commit=BASE, record="**Status:** ready\n"):
        directory = ROOT if phase == "single" else ROOT + "/" + phase
        self.files[directory + "/build.md"] = record
        tag = "shipped/001-demo" + ("" if phase == "single" else "-" + phase)
        return patch.object(remote, "tagged_commit", side_effect=lambda name: commit if name == tag else "")

    def test_shipped_tag_must_be_on_merged_build(self):
        """T6 (S7, S8, S23): the tag names a merged Build on the default branch."""
        with self.shipped():
            self.assertTrue(self.evidence.shipment(ROOT, ROOT, BASE))
        with self.shipped(commit=""):
            self.assertFalse(self.evidence.shipment(ROOT, ROOT, BASE))
        with self.shipped(record=""):
            with self.assertRaisesRegex(local.Violation, "Build record"):
                self.evidence.shipment(ROOT, ROOT, BASE)

    def test_moved_shipped_tag_is_rejected(self):
        """T7 (S9): a tag pointing outside the default branch ships nothing."""
        with self.shipped(commit="c" * 40):
            with patch.object(remote, "ancestor", side_effect=local.Violation("not on the default branch")):
                with self.assertRaisesRegex(local.Violation, "default branch"):
                    self.evidence.shipment(ROOT, ROOT, BASE)

    def test_dependent_handoff_requires_shipped_tag(self):
        """T8 (S10, S11): a merged-source predecessor phase ships by tag."""
        self.data["/issues/99"] = {
            "number": 99, "id": 99, "state": "closed", "state_reason": "completed",
            "body": ("**Status:** Done\n**Outcome:** 001-demo\n**Stage:** build\n"
                     "**Phase:** P1-first\n"
                     f"**Review PR:** {URL}/pull/31\n"
                     f"**Approved artifact:** {URL}/blob/{BASE}/{ROOT}/P1-first/build.md\n"),
        }
        self.data["/issues/4/dependencies/blocked_by"].append({"number": 99})
        self.data["/pulls/31"] = copy.deepcopy(self.pr)
        self.data["/pulls/31/reviews"] = [self.approval()]
        self.data["/pulls/31/files"] = [{"filename": ROOT + "/P1-first/build.md"},
                                        {"filename": "app.py"}]
        self.files[ROOT + "/P1-first/build.md"] = "**Status:** ready\n"
        self.files["AGENTS.md"] = ("## Delivery settings\n- **Delivery:** merged source\n"
                                   "- **Test paths:** tests/\n")
        with self.shipped(phase="P1-first"):
            self.evidence.dependencies(4, BASE)
        with self.shipped(phase="P1-first", commit=""):
            with self.assertRaisesRegex(local.Violation, "shipped tag"):
                self.evidence.dependencies(4, BASE)

    def merged_source(self):
        self.files["AGENTS.md"] = ("## Delivery settings\n- **Delivery:** merged source\n"
                                   "- **Test paths:** tests/\n")

    def test_task_shape_follows_delivery_mode(self):
        """T10 (S13, S18, S26): merged source tracks four stages, not six."""
        self.merged_source()
        with self.assertRaisesRegex(local.Violation, "does not track"):
            self.evidence.graph(100, ROOT, BASE)
        self.data["/issues/100/sub_issues"] = [{"number": n} for n in (1, 2, 3, 4)]
        self.evidence.cache.clear()
        self.assertEqual({stage for _, stage in self.evidence.graph(100, ROOT, BASE)},
                         {"intent", "spec", "plan", "build"})
        # A cancelled Proof task stays out of the graph and unlocks nothing.
        self.data["/issues/5"]["state"] = "closed"
        self.data["/issues/5"]["state_reason"] = "not_planned"
        self.data["/issues/100/sub_issues"].append({"number": 5})
        self.evidence.cache.clear()
        self.assertEqual({stage for _, stage in self.evidence.graph(100, ROOT, BASE)},
                         {"intent", "spec", "plan", "build"})
        self.data["/issues/4/dependencies/blocked_by"] = [{"number": 5}]
        self.evidence.cache.clear()
        with self.assertRaisesRegex(local.Violation, "dependency"):
            self.evidence.dependencies(4, BASE)

    def test_historical_stage_tasks_still_validate(self):
        """T9 (S13): a phase that shipped under the old rules keeps its tasks."""
        self.merged_source()
        # Proof and Ship tasks closed as completed record real merged PRs.
        for number in (5, 6):
            self.data[f"/issues/{number}"]["state"] = "closed"
            self.data[f"/issues/{number}"]["state_reason"] = "completed"
        self.evidence.cache.clear()
        self.assertEqual({stage for _, stage in self.evidence.graph(100, ROOT, BASE)},
                         {"intent", "spec", "plan", "build"})
        # An open task for an untracked stage is still an error.
        self.data["/issues/5"]["state"] = "open"
        self.data["/issues/5"]["state_reason"] = None
        self.evidence.cache.clear()
        with self.assertRaisesRegex(local.Violation, "does not track"):
            self.evidence.graph(100, ROOT, BASE)

    def test_fix_merge_requires_non_author_approval(self):
        """T5 (S7, S18): a fix needs a review, and no stage tracking."""
        self.reviews()
        with self.assertRaisesRegex(local.Violation, "approving review"):
            self.evidence.validate(BASE, HEAD, ("fix", "", ""), 9, "fix/broken-rule")
        self.reviews(self.approval())
        self.evidence.validate(BASE, HEAD, ("fix", "", ""), 9, "fix/broken-rule")

    def test_fix_follows_the_existing_contracts_rule(self):
        """T7 (S10): the contracts rule is unchanged by the fix lane."""
        conventions = (Path(__file__).resolve().parents[1] / "AGENTS.md").read_text()
        self.assertIn("packages/", conventions)
        self.assertIn("Kind: contracts", conventions)

    def test_explicit_fallback_preserves_gates(self):
        parent = self.data["/issues/100"]
        parent["type"] = {"name": "Feature"}
        parent["labels"] = [{"name": "intent"}]
        parent["body"] += "**Issue type mode:** label\n**Fallback approved by:** owner in setup review\n"
        self.validate()

    def test_no_silent_label_fallback(self):
        parent = self.data["/issues/100"]
        parent["type"] = None
        parent["labels"] = [{"name": "intent"}]
        with self.assertRaisesRegex(local.Violation, "explicitly approved"):
            self.validate()

    def test_missing_artifact_section_is_blocked(self):
        self.data["/issues/4"]["body"] = self.data["/issues/4"]["body"].replace("/build.md", "/build.md#missing")
        with self.assertRaisesRegex(local.Violation, "section link"):
            self.validate()

    def test_handoff_needs_no_next_stage_document(self):
        del self.files[ROOT + "/build.md"]
        self.evidence.handoff(4, BASE)

    def test_handoff_blocks_missing_dependency_merge(self):
        self.pr["merged"] = False
        with self.assertRaises(local.Violation):
            self.evidence.handoff(4, BASE)

    def test_setup_report_names_authoring_identity(self):
        """T11 (S16): required review implies a separate PR author."""
        self.data["/issue-types"] = [{"name": "Intent"}]
        self.data["/rules/branches/main"] = [
            {"type": "pull_request", "parameters": {"required_approving_review_count": 1,
                                                    "dismiss_stale_reviews_on_push": True}}]
        self.data["/branches/main/protection"] = {}
        report = self.evidence.setup()
        self.assertTrue(any("PR authoring identity" in note for note in self.evidence.notes(report)))
        self.data["/rules/branches/main"] = []
        self.evidence.cache.clear()
        self.assertEqual(self.evidence.notes(self.evidence.setup()), [])

    def test_setup_reports_real_policy(self):
        self.data["/issue-types"] = [{"name": "Intent"}]
        self.data["/rules/branches/main"] = [
            {"type": "required_status_checks", "parameters": {"required_status_checks": [{"context": "SDLC history"}, {"context": "Template verification"}]}},
            {"type": "pull_request", "parameters": {"required_approving_review_count": 1, "dismiss_stale_reviews_on_push": True}}]
        self.data["/branches/main/protection"] = {}
        self.assertEqual(set(self.evidence.setup().values()), {"configured"})

    def test_setup_does_not_invent_review_policy(self):
        self.data["/issue-types"] = [{"name": "Intent"}]
        self.data["/rules/branches/main"] = []
        self.data["/branches/main/protection"] = {}
        self.assertNotEqual(set(self.evidence.setup().values()), {"configured"})


class TransportTests(unittest.TestCase):
    def test_paginated_reads_flatten_without_writes(self):
        result = subprocess.CompletedProcess([], 0, '[[{"number":1}],[{"number":2}]]', '')
        with patch.object(subprocess, "run", return_value=result) as run:
            self.assertEqual(remote.read_api("repos/example/repo/issues", True), [{"number": 1}, {"number": 2}])
            args = run.call_args.args[0]
            self.assertEqual(args[args.index("--method") + 1], "GET")
            self.assertIn("--paginate", args)
            self.assertEqual(run.call_args.kwargs["timeout"], 45)

    def test_error_does_not_echo_private_response(self):
        with patch.object(subprocess, "run", return_value=subprocess.CompletedProcess([], 1, 'private body', 'secret token')):
            with self.assertRaises(local.Violation) as error:
                remote.read_api("repos/example/repo/issues")
            self.assertNotIn("secret", str(error.exception))
            self.assertNotIn("private", str(error.exception))

    def test_timeout_blocks_evidence(self):
        with patch.object(subprocess, "run", side_effect=subprocess.TimeoutExpired([], 45)):
            with self.assertRaises(local.Violation):
                remote.read_api("repos/example/repo/issues")

    def test_malformed_pages_are_rejected(self):
        with patch.object(subprocess, "run", return_value=subprocess.CompletedProcess([], 0, '[{"not":"a page"}]', '')):
            with self.assertRaises(local.Violation):
                remote.read_api("repos/example/repo/issues", True)

    def test_external_repository_urls_are_rejected(self):
        with self.assertRaises(local.Violation):
            remote.github_url("https://attacker.invalid/example/repo/pull/1", REPO, "pull")


if __name__ == "__main__":
    unittest.main()
