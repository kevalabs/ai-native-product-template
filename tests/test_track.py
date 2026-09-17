"""Tracking commands run against fake GitHub responses; no credentials needed."""

import copy
import unittest.mock
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import check_sdlc as local
import track

ROOT_DIR = Path(__file__).resolve().parents[1]
REPO = "example/repo"
URL = "https://github.com/" + REPO
OUTCOME = "001-demo"
ROOT = "features/" + OUTCOME
BASE = "a" * 40


class Recorder:
    """Stands in for the GitHub API, remembering every write."""

    def __init__(self, data):
        self.data = data
        self.writes = []
        self.fail_on = None

    def read(self, endpoint, pages=False):
        key = endpoint.removeprefix("repos/" + REPO)
        if key not in self.data:
            raise local.Violation("GitHub evidence unavailable at " + key)
        return copy.deepcopy(self.data[key])

    def write(self, method, endpoint, fields):
        key = endpoint.removeprefix("repos/" + REPO)
        if self.fail_on and self.fail_on in key:
            raise local.Violation("GitHub evidence unavailable at " + key)
        self.writes.append((method, key, fields))
        number = len(self.data) + 100
        record = {"number": number, "id": number, **fields}
        self.data[f"/issues/{number}"] = record
        return record


class TrackTests(unittest.TestCase):
    def setUp(self):
        self.data = {"": {"default_branch": "main"}}
        self.files = {
            ROOT + "/intent.md": ("**Status:** accepted\n**Accepted by:** Owner\n"
                                  "\n## Phases\n\nSingle phase\n"),
            "AGENTS.md": ("## Delivery settings\n- **Delivery:** merged source\n"
                          "- **Test paths:** tests/\n"),
        }
        self.recorder = Recorder(self.data)
        self.tracker = track.Tracker(REPO, self.recorder.read, self.recorder.write)
        self.content = unittest.mock.patch.object(
            local, "content", side_effect=lambda ref, path: self.files.get(path, ""))
        self.content.start()
        self.addCleanup(self.content.stop)

    def test_dry_run_reports_without_writing(self):
        """T5 (S6, S9): a dry run says what it would do and writes nothing."""
        planned = track.Tracker(REPO, self.recorder.read, self.recorder.write, dry_run=True)
        planned.apply("create the parent issue", "POST", "/issues", {"title": "x"})
        self.assertEqual(self.recorder.writes, [])
        self.assertIn("create the parent issue", planned.report())
        self.tracker.apply("create the parent issue", "POST", "/issues", {"title": "x"})
        self.assertEqual(len(self.recorder.writes), 1)
        self.assertIn("create the parent issue", self.tracker.report())

    def test_no_command_writes_a_human_decision(self):
        """T6 (S7, S13): approvals, reviews, merges, and tags stay human."""
        for field in ("Accepted by", "Approved by", "Confirmed by", "Blocking findings"):
            with self.assertRaisesRegex(local.Violation, field):
                self.tracker.apply("write a decision", "PATCH", "/issues/1",
                                   {"body": f"**{field}:** someone\n"})
        self.assertEqual(self.recorder.writes, [])
        source = (ROOT_DIR / "scripts/track.py").read_text()
        for endpoint in ("/merge", "/reviews", "/git/refs", "/git/tags"):
            self.assertNotIn(endpoint, source)

    def test_partial_and_unavailable_results_are_honest(self):
        """T7 (S10, S19): a failure names what landed and never claims success."""
        self.tracker.apply("first write", "POST", "/issues", {"title": "one"})
        self.recorder.fail_on = "/issues/999"
        with self.assertRaises(local.Violation):
            self.tracker.apply("second write", "PATCH", "/issues/999", {"body": "two"})
        report = self.tracker.report()
        self.assertIn("first write", report)
        self.assertNotIn("second write", report)

    def test_no_workflow_secret_or_bot_identity_is_installed(self):
        """T8 (S11): local commands only, using existing authentication."""
        source = (ROOT_DIR / "scripts/track.py").read_text()
        for forbidden in ("GH_TOKEN", "secrets.", "private_key", "installation"):
            self.assertNotIn(forbidden, source)
        workflow = (ROOT_DIR / ".github/workflows/verify.yml").read_text()
        self.assertNotIn("track.py", workflow)
        self.assertIn("issues: read", workflow)

    def task_body(self, stage="spec", phase="single", status="Ready", pull=None):
        body = (f"**Outcome:** {OUTCOME}\n**Stage:** {stage}\n**Phase:** {phase}\n"
                f"**Parent issue:** {URL}/issues/100\n**Owner:** Owner\n"
                f"**Status:** {status}\n**Artifact:** {ROOT}/intent.md\n"
                "**Completion criteria:** approved outcome and merged evidence\n")
        if pull:
            body += f"**Review PR:** {URL}/pull/{pull}\n"
        return body

    def test_create_builds_the_graph_for_each_phase_shape(self):
        """T1 (S1, S2, S16): the graph matches the intent and delivery mode."""
        self.data["/issues?state=all&per_page=100"] = []
        self.tracker.create(OUTCOME, BASE)
        stages = [f["type"] for _, _, f in self.recorder.writes]
        self.assertEqual(stages.count("Intent"), 1)
        self.assertEqual(stages.count("Task"), 4)
        self.files[ROOT + "/intent.md"] = ("**Status:** accepted\n\n## Phases\n\n"
                                           "- P1-first — one outcome\n- P2-second — another\n")
        self.recorder.writes.clear()
        self.data["/issues?state=all&per_page=100"] = []
        track.Tracker(REPO, self.recorder.read, self.recorder.write).create(OUTCOME, BASE)
        bodies = [f["body"] for _, _, f in self.recorder.writes]
        self.assertTrue(any("**Phase:** P1-first" in b for b in bodies))
        self.assertTrue(any("**Phase:** P2-second" in b for b in bodies))
        self.files[ROOT + "/intent.md"] = "**Status:** draft\n"
        with self.assertRaisesRegex(local.Violation, "not accepted"):
            track.Tracker(REPO, self.recorder.read, self.recorder.write).create(OUTCOME, BASE)

    def test_repeated_run_creates_no_duplicate(self):
        """T4 (S5, S17, S20): reading first makes a second run a report."""
        self.data["/issues?state=all&per_page=100"] = [
            {"number": 100, "body": f"**Outcome:** {OUTCOME}\n**Status:** Accepted\n"}]
        self.assertIn("already exists", self.tracker.create(OUTCOME, BASE))
        self.assertEqual(self.recorder.writes, [])

    def test_link_records_the_pr_and_status(self):
        """T2 (S3): one command records the PR before the checks run."""
        self.data["/issues/5"] = {"number": 5, "id": 5, "state": "open", "body": self.task_body()}
        self.tracker.link(5, OUTCOME, 42)
        body = self.recorder.writes[0][2]["body"]
        self.assertIn(f"**Review PR:** {URL}/pull/42", body)
        self.assertIn("**Status:** In review", body)

    def test_cancelled_shipped_and_foreign_targets_refuse(self):
        """T9 (S12, S18): a command acts only on live work in its outcome."""
        self.data["/issues/5"] = {"number": 5, "id": 5, "state": "open",
                                  "body": self.task_body().replace("**Outcome:** " + OUTCOME,
                                                                   "**Outcome:** 002-other")}
        with self.assertRaisesRegex(local.Violation, "another outcome"):
            self.tracker.link(5, OUTCOME, 42)
        self.data["/issues/6"] = {"number": 6, "id": 6, "state": "open",
                                  "body": self.task_body(status="Cancelled")}
        with self.assertRaisesRegex(local.Violation, "cancelled"):
            self.tracker.link(6, OUTCOME, 42)
        self.assertEqual(self.recorder.writes, [])

    def test_complete_records_the_merge_or_refuses(self):
        """T3 (S4, S8): completion needs a merged PR and a matching artifact."""
        self.data["/issues/5"] = {"number": 5, "id": 5, "state": "open",
                                  "body": self.task_body(pull=9)}
        self.data["/pulls/9"] = {"base": {"repo": {"full_name": REPO}, "ref": "main"},
                                 "merged": True, "merge_commit_sha": BASE,
                                 "head": {"sha": BASE}, "merged_by": {"type": "User"},
                                 "user": {"login": "author"}}
        self.data["/pulls/9/reviews"] = []
        self.data["/pulls/9/files"] = [{"filename": ROOT + "/spec.md"}]
        self.files[ROOT + "/spec.md"] = "**Status:** accepted\n"
        with unittest.mock.patch.object(track.remote, "ancestor"):
            self.tracker.complete(5, OUTCOME, BASE)
            fields = self.recorder.writes[0][2]
            self.assertEqual(fields["state_reason"], "completed")
            self.assertIn(f"blob/{BASE}/{ROOT}/spec.md", fields["body"])
            self.assertIn("**Status:** Done", fields["body"])
            self.recorder.writes.clear()
            self.data["/pulls/9"]["merged"] = False
            self.data["/issues/5"]["body"] = self.task_body(pull=9)
            with self.assertRaisesRegex(local.Violation, "must merge"):
                track.Tracker(REPO, self.recorder.read, self.recorder.write).complete(5, OUTCOME, BASE)
            self.assertEqual(self.recorder.writes, [])

    def test_guidance_describes_the_commands_and_refusals(self):
        """T10 (S14, S15): the commands and their limits are written down."""
        for name in ("AGENTS.md", "README.md", ".githooks/README.md",
                     "product/capabilities/sdlc-workflow.md", "product/glossary.md"):
            text = (ROOT_DIR / name).read_text()
            self.assertIn("track", text.lower(), name)
        guide = (ROOT_DIR / ".githooks/README.md").read_text()
        self.assertIn("make track-create", guide)
        self.assertIn("make track-link", guide)
        self.assertIn("make track-complete", guide)
        conventions = (ROOT_DIR / "AGENTS.md").read_text()
        self.assertIn("not evidence", conventions.lower())


if __name__ == "__main__":
    unittest.main()
