#!/usr/bin/env python3
"""Create and update stage tracking issues. Never records a human decision."""

import argparse
import json
import re
import subprocess
import sys

import check_github as remote
import check_sdlc as local

Violation = local.Violation

# Fields that hold a person's decision. A command never writes one.
DECISIONS = ("Accepted by", "Approved by", "Confirmed by", "Blocking findings",
             "Fallback approved by", "Age acceptance")
PLACEHOLDER = ("Blocked placeholder. It links the governing intent until its own artifact "
               "exists. Add Review PR when opened. After merge, add Approved artifact as a "
               "commit permalink, verify the handoff, then set Done and close.")
CRITERIA = {
    "intent": "Owner acceptance recorded in intent.md; Intent-only PR reviewed by a human and merged.",
    "spec": "Owner acceptance recorded in spec.md; Spec-only PR reviewed by a human and merged.",
    "plan": "Owner approval recorded in plan.md; Plan-only PR reviewed by a human and merged.",
    "build": "build.md names the exact approved Plan commit; make test passes; a non-author approving review before merge.",
    "proof": "proof.md names the exact merged Build, passes every S-rule, and its PR merges.",
    "ship": "ship.md records successful delivery of the proved Build and its PR merges.",
}


def write_api(method, endpoint, fields):
    """One write call. Errors never echo response bodies."""
    args = ["gh", "api", "--method", method, endpoint]
    for key, value in fields.items():
        args += ["-F" if isinstance(value, int) else "-f", f"{key}={value}"]
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=45)
    except (OSError, subprocess.TimeoutExpired) as error:
        raise Violation("GitHub write unavailable; verify what landed before retrying") from error
    if result.returncode:
        raise Violation(f"GitHub refused {method} {endpoint.split('?')[0]}")
    try:
        return json.loads(result.stdout) if result.stdout.strip() else {}
    except ValueError as error:
        raise Violation("GitHub returned malformed evidence") from error


class Tracker:
    """Reads evidence with the existing checks, then writes tracking fields."""

    def __init__(self, repo, read=remote.read_api, write=write_api, dry_run=False):
        self.evidence = remote.Evidence(repo, read)
        self.repo, self.writer, self.dry_run = repo, write, dry_run
        self.prefix = "repos/" + repo
        self.done = []

    def apply(self, description, method, endpoint, fields):
        """Every write goes through here, so dry run and the report are one rule."""
        for name in DECISIONS:
            if re.search(rf"\*\*{re.escape(name)}:\*\*\s*\S", str(fields.get("body", ""))):
                raise Violation(f"a command never records {name}; a person decides that")
        if fields.get("state_reason") == "completed" and not fields.pop("merged", None):
            raise Violation("a task completes only against a merged PR")
        fields.pop("merged", None)
        if self.dry_run:
            self.done.append("would " + description)
            return {}
        result = self.writer(method, self.prefix + endpoint, fields)
        self.done.append(description)
        return result

    def report(self):
        return "\n".join(self.done) if self.done else "nothing to change"

    def field(self, body, name, value):
        """Replace a field in an issue body, or add it before the free text."""
        pattern = rf"^\*\*{re.escape(name)}:\*\* *[^\n]*$"
        if re.search(pattern, body, re.M):
            return re.sub(pattern, f"**{name}:** {value}", body, count=1, flags=re.M)
        headers, _, rest = body.partition("\n\n")
        return f"{headers}\n**{name}:** {value}\n\n{rest}"

    def accepted_intent(self, outcome, base):
        root = "features/" + outcome
        document = local.content(base, root + "/intent.md")
        if not document:
            raise Violation(f"{root}/intent.md is not on {base}; merge its Intent PR first")
        if local.field(document, "Status", False) != "accepted":
            raise Violation("the intent is not accepted; a person accepts it before tracking")
        return root, document

    def existing_parent(self, outcome):
        """An outcome's parent issue, when its graph already exists."""
        found = self.evidence.api(self.prefix + "/issues?state=all&per_page=100", False)
        for issue in found if isinstance(found, list) else []:
            body = issue.get("body") or ""
            if local.field(body, "Outcome", False) == outcome and not local.field(body, "Stage", False):
                return issue
        return None

    def create(self, outcome, base):
        root, intent = self.accepted_intent(outcome, base)
        if self.existing_parent(outcome):
            return "tracking already exists for " + outcome
        stages = local.tracked_stages(local.delivery(base, False)[0])
        phases = re.findall(rf"\bP[1-9][0-9]*-{local.SLUG}", local.section(intent, "Phases")) or ["single"]
        title = local.content(base, root + "/intent.md").splitlines()[0].lstrip("# ")
        parent = self.apply(f"create the parent Intent issue for {outcome}", "POST", "/issues", {
            "title": f"[{outcome.split('-')[0]}] {title}", "type": "Intent",
            "body": f"**Outcome:** {outcome}\n**Status:** Accepted\n"
                    f"**Artifact:** {local.CONVENTIONS and ''}{root}/intent.md\n\n"
                    "## Artifact index\n\nLinks to the stage artifacts as they become available.\n",
        })
        parent_url = f"https://github.com/{self.repo}/issues/{parent.get('number', 0)}"
        for phase in phases:
            for stage in stages:
                if stage == "intent" and phase != phases[0]:
                    continue
                shown = "single" if phase == "single" else phase
                self.apply(f"create the {stage} task for {shown}", "POST", "/issues", {
                    "title": f"[{outcome.split('-')[0]}] {shown} {stage}: {outcome}",
                    "type": "Task",
                    "body": f"**Outcome:** {outcome}\n**Stage:** {stage}\n**Phase:** {shown}\n"
                            f"**Parent issue:** {parent_url}\n**Owner:** <accountable person>\n"
                            f"**Status:** {'Ready' if stage == stages[0] else 'Blocked'}\n"
                            f"**Artifact:** {root}/intent.md\n"
                            f"**Completion criteria:** {CRITERIA[stage]}\n\n{PLACEHOLDER}\n",
                })
        return self.report()

    def task(self, number, outcome):
        issue = self.evidence.issue(number)
        body = issue.get("body") or ""
        if local.field(body, "Outcome", False) != outcome:
            raise Violation(f"issue #{number} tracks another outcome")
        if local.field(body, "Status", False) in {"Cancelled", "Done"}:
            raise Violation(f"issue #{number} is cancelled or already done")
        return issue, body

    def link(self, number, outcome, pull):
        issue, body = self.task(number, outcome)
        url = f"https://github.com/{self.repo}/pull/{pull}"
        body = self.field(self.field(body, "Review PR", url), "Status", "In review")
        self.apply(f"link PR #{pull} on task #{number}", "PATCH", f"/issues/{number}", {"body": body})
        return self.report()

    def complete(self, number, outcome, base):
        issue, body = self.task(number, outcome)
        stage = local.field(body, "Stage")
        phase = local.field(body, "Phase")
        root = "features/" + outcome
        directory = root if phase == "single" else f"{root}/{phase}"
        path = local.stage_path(stage, root, directory)
        pull = remote.github_url(local.field(body, "Review PR"), self.repo, "pull")
        merge, _ = self.evidence.merged(pull, base, stage)
        self.evidence.predecessor_scope(pull, stage, root, directory)
        local.require_status(merge, path, local.STATUS[stage])
        if local.content(merge, path) != local.content(base, path):
            raise Violation("the artifact changed after its reviewed merge")
        permalink = f"https://github.com/{self.repo}/blob/{merge}/{path}"
        for name, value in (("Artifact", permalink), ("Approved artifact", permalink),
                            ("Status", "Done")):
            body = self.field(body, name, value)
        self.apply(f"complete task #{number} at {merge[:12]}", "PATCH", f"/issues/{number}",
                   {"body": body, "state": "closed", "state_reason": "completed", "merged": merge})
        return self.report()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("create", "link", "complete"))
    parser.add_argument("--repo", required=True)
    parser.add_argument("--outcome", required=True)
    parser.add_argument("--issue", type=int)
    parser.add_argument("--pr", type=int)
    parser.add_argument("--base", default="origin/main")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    tracker = Tracker(args.repo, dry_run=args.dry_run)
    base = local.git("rev-parse", "--verify", "--end-of-options", f"{args.base}^{{commit}}").strip()
    if args.command == "create":
        print(tracker.create(args.outcome, base))
    elif args.command == "link":
        if not args.issue or not args.pr:
            parser.error("link needs --issue and --pr")
        print(tracker.link(args.issue, args.outcome, args.pr))
    else:
        if not args.issue:
            parser.error("complete needs --issue")
        print(tracker.complete(args.issue, args.outcome, base))
    print("The checks still verify this graph; a command's success is not evidence.")


if __name__ == "__main__":
    try:
        main()
    except Violation as error:
        print("track: " + str(error), file=sys.stderr)
        sys.exit(1)
