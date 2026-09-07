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
                      ROOT + "/intent.md": "**Status:** accepted\n## Phases\nSingle phase\n"}
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
