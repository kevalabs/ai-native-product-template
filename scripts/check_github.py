#!/usr/bin/env python3
"""Read-only GitHub evidence checks. Never creates issues, reviews, or merges."""

import argparse
import json
import re
import subprocess
import sys
from urllib.parse import quote, unquote

import check_sdlc as local

Violation = local.Violation


def read_api(endpoint, pages=False):
    args = ["gh", "api", "--method", "GET", endpoint]
    if pages:
        args += ["--paginate", "--slurp"]
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=45)
    except (OSError, subprocess.TimeoutExpired) as error:
        raise Violation("GitHub evidence unavailable; check gh authentication/network and retry") from error
    if result.returncode:
        # Do not echo API bodies, tokens, or private issue content.
        raise Violation("GitHub evidence unavailable at " + endpoint.split("?")[0])
    try:
        value = json.loads(result.stdout)
        if pages:
            if not isinstance(value, list) or any(not isinstance(page, list) for page in value):
                raise ValueError("invalid pages")
            return [item for page in value for item in page]
        return value
    except (ValueError, TypeError) as error:
        raise Violation("GitHub returned malformed evidence") from error


def github_url(value, repo, kind):
    match = re.fullmatch(rf"https://github\.com/{re.escape(repo)}/{kind}/([1-9][0-9]*)", value)
    if not match:
        raise Violation(f"expected a {kind} URL in {repo}")
    return int(match[1])


def permalink(value, repo, path):
    match = re.fullmatch(rf"https://github\.com/{re.escape(repo)}/blob/({local.SHA})/{re.escape(path)}(?:#[\w-]+)?", unquote(value))
    if not match:
        raise Violation("completion needs a commit permalink to " + path)
    return match[1]


def ancestor(older, newer):
    if not re.fullmatch(local.SHA, older):
        raise Violation("expected a full commit ID")
    result = subprocess.run(["git", "merge-base", "--is-ancestor", older, newer], capture_output=True)
    if result.returncode:
        raise Violation("predecessor merge is missing from the current base")


class Evidence:
    def __init__(self, repo, api=read_api):
        if not re.fullmatch(r"[\w.-]+/[\w.-]+", repo):
            raise Violation("invalid repository identity")
        self.repo, self.api, self.cache = repo, api, {}
        self.prefix = "repos/" + repo

    def get(self, suffix, pages=False):
        key = (suffix, pages)
        if key not in self.cache:
            value = self.api(self.prefix + suffix, pages)
            if not isinstance(value, list if pages else dict):
                raise Violation("GitHub returned malformed " + suffix)
            self.cache[key] = value
        return self.cache[key]

    def issue(self, number):
        issue = self.get(f"/issues/{number}")
        if "pull_request" in issue or issue.get("number") != number:
            raise Violation("stage tracking must link an issue, not a PR")
        return issue

    def pull(self, number):
        pr = self.get(f"/pulls/{number}")
        if pr.get("base", {}).get("repo", {}).get("full_name") != self.repo:
            raise Violation("predecessor PR belongs to another repository")
        return pr

    def merged(self, number, base):
        pr = self.pull(number)
        if not pr.get("merged") or pr.get("base", {}).get("ref") != self.get("")["default_branch"]:
            raise Violation(f"predecessor PR #{number} must merge into the default branch")
        commit = pr.get("merge_commit_sha", "")
        ancestor(commit, base)
        if pr.get("merged_by", {}).get("type") != "User":
            # A bot merge is acceptable only with a current human approving review.
            self.review(number, pr, require_approval=True)
        else:
            self.review(number, pr)
        return commit, pr

    def review(self, number, pr, require_approval=False):
        latest = {}
        for review in self.get(f"/pulls/{number}/reviews", True):
            user = review.get("user", {})
            if user.get("type") == "User" and review.get("state") in {"APPROVED", "CHANGES_REQUESTED", "DISMISSED"}:
                latest[user.get("login")] = review
        if any(r.get("state") == "CHANGES_REQUESTED" for r in latest.values()):
            raise Violation("predecessor has an unresolved changes-requested review")
        approved = any(r.get("state") == "APPROVED" and r.get("commit_id") == pr.get("head", {}).get("sha")
                       and r.get("user", {}).get("login") != pr.get("user", {}).get("login") for r in latest.values())
        if require_approval and not approved:
            raise Violation("predecessor needs a current human approving review")
        return approved

    def predecessor_scope(self, number, stage, root, directory):
        path = local.stage_path(stage, root, directory)
        files = {entry.get("filename") for entry in self.get(f"/pulls/{number}/files", True)}
        if path not in files:
            raise Violation("predecessor PR did not deliver its stage artifact")
        if stage in {"plan", "proof", "ship"} and files != {path}:
            raise Violation("predecessor PR bundled stages or implementation")
        if stage in {"intent", "spec"}:
            for filename in files:
                if not isinstance(filename, str) or (filename != path and not filename.startswith(directory + "/design/") and not re.fullmatch(rf"{re.escape(root)}/questions-for-{local.SLUG}\.md", filename)):
                    raise Violation("predecessor PR bundled planning stages")

    def unchanged_prerequisites(self, stage, root, directory, merge, base):
        for path in local.prerequisites(stage, root, directory):
            local.require_status(merge, path, local.STATUS[path.rsplit("/", 1)[1][:-3]])
            if local.content(merge, path) != local.content(base, path):
                raise Violation("requirements changed after predecessor review; repeat the affected stage")

    def graph(self, parent_number, root):
        parent = self.issue(parent_number)
        body = parent.get("body") or ""
        if local.field(body, "Outcome") != root.rsplit("/", 1)[-1]:
            raise Violation("parent issue tracks a different outcome")
        if parent.get("state") != "open" or local.field(body, "Status", False).lower() in {"cancelled", "shipped"}:
            raise Violation("closed, cancelled, or shipped parent cannot authorize active work")
        if (parent.get("type") or {}).get("name") != "Intent":
            fallback = local.field(body, "Issue type mode", False) == "label" and local.field(body, "Fallback approved by", False)
            if not fallback or "intent" not in {label["name"] for label in parent.get("labels", [])}:
                raise Violation("parent requires Intent type or an explicitly approved intent-label fallback")
        records = {}

        def add(issue, expected_phase):
            full = self.issue(issue["number"])
            text = full.get("body") or ""
            key = (local.field(text, "Phase"), local.field(text, "Stage"))
            if key[0] != expected_phase or key[1] not in local.STAGES or key in records:
                raise Violation("duplicate or mismatched stage task")
            if (full.get("type") or {}).get("name") != "Task":
                raise Violation("stage sub-issues must have type Task")
            if local.field(text, "Outcome") != root.rsplit("/", 1)[-1]:
                raise Violation("stage task tracks another outcome")
            if github_url(local.field(text, "Parent issue"), self.repo, "issues") != parent_number:
                raise Violation("stage task must link its root Intent issue")
            records[key] = full

        children = self.get(f"/issues/{parent_number}/sub_issues", True)
        phases = []
        for child in children:
            text = self.issue(child["number"]).get("body") or ""
            if local.field(text, "Stage", False) == "phase":
                phase = local.field(text, "Phase")
                if not re.fullmatch(rf"P[1-9][0-9]*-{local.SLUG}", phase) or phase in phases:
                    raise Violation("duplicate or invalid phase group")
                phases.append(phase)
                for task in self.get(f"/issues/{child['number']}/sub_issues", True):
                    add(task, phase)
            else:
                add(child, "single")
        expected = {("single", "intent")}
        for phase in phases or ["single"]:
            expected.update((phase, stage) for stage in local.STAGES[1:])
        if set(records) != expected:
            raise Violation("parent must have exactly one task per required stage and phase")
        if not local.field(body, "Artifact", False):
            raise Violation("parent must link its governing intent artifact")
        return records

    def active_task(self, task, document, stage, phase, current_pr=None):
        body = task.get("body") or ""
        for name in ("Outcome", "Phase", "Stage", "Parent issue"):
            if local.field(body, name) != local.field(document, name):
                raise Violation("task and artifact disagree on " + name)
        for name in ("Owner", "Artifact", "Completion criteria"):
            local.field(body, name)
        if task.get("state") != "open" or local.field(body, "Status") not in {"Ready", "In progress", "In review"}:
            raise Violation("active task must be open and ready, in progress, or in review")
        if current_pr is not None and github_url(local.field(body, "Review PR"), self.repo, "pull") != current_pr:
            raise Violation("stage task does not link its current review PR")
        for dependency in self.get(f"/issues/{task['number']}/dependencies/blocked_by", True):
            record = self.issue(dependency["number"])
            text = record.get("body") or ""
            if record.get("state") != "closed" or record.get("state_reason") != "completed" or local.field(text, "Status") != "Done":
                raise Violation("task has an unfinished or cancelled dependency")

    def link(self, url, artifact, ref, branch=None):
        prefix = f"https://github.com/{self.repo}/blob/"
        value = unquote(url)
        body, _, anchor = value.partition("#")
        suffix = "/" + artifact
        if not body.startswith(prefix) or not body.endswith(suffix):
            raise Violation("artifact link points to the wrong repository or document")
        revision = body[len(prefix):-len(suffix)]
        if revision not in {ref, branch}:
            if not re.fullmatch(local.SHA, revision) or local.content(revision, artifact) != local.content(ref, artifact):
                raise Violation("artifact link does not show the reviewed content")
        if not local.content(ref, artifact):
            raise Violation("linked artifact does not exist")
        if anchor:
            headings = re.findall(r"^#+ (.+)$", local.content(ref, artifact), re.M)
            slugs = {re.sub(r"[^\w\s-]", "", h.lower()).replace(" ", "-") for h in headings}
            if anchor not in slugs:
                raise Violation("artifact section link does not resolve")

    def validate(self, base, head, selected, current_pr=None, branch=None):
        stage, root, directory = selected
        if stage == "bootstrap":
            return
        artifact = local.stage_path(stage, root, directory)
        document = local.content(head, artifact)
        phase = "single" if root == directory else directory.rsplit("/", 1)[-1]
        if local.field(document, "Stage") != stage or local.field(document, "Phase") != phase:
            raise Violation("artifact stage or phase is incorrect")
        parent = github_url(local.field(document, "Parent issue"), self.repo, "issues")
        records = self.graph(parent, root)
        # The phase list must agree with the committed intent, not just the issue graph.
        declared = set(re.findall(r"\bP[1-9][0-9]*-" + local.SLUG, local.section(local.content(head, root + "/intent.md"), "Phases")))
        actual = {p for p, s in records if p != "single"}
        if actual != declared:
            raise Violation("phase groups differ from the accepted intent")
        task = records[(phase, stage)]
        if task["number"] != github_url(local.field(document, "Stage issue"), self.repo, "issues"):
            raise Violation("artifact backlink points to another stage task")
        self.active_task(task, document, stage, phase, current_pr)
        self.link(local.field(task["body"], "Artifact"), artifact, head, branch)
        self.link(local.field(self.issue(parent)["body"], "Artifact"), root + "/intent.md", head, branch)
        if current_pr:
            pr = self.pull(current_pr)
            if pr.get("head", {}).get("sha") != head:
                raise Violation("PR head changed; rerun checks for the current version")
            if local.field(pr.get("body") or "", "Stage issue", False) != local.field(document, "Stage issue"):
                raise Violation("PR body must link its stage issue")
        if stage == "intent":
            return
        predecessor = local.STAGES[local.STAGES.index(stage) - 1]
        prior_phase = "single" if predecessor == "intent" else phase
        prior = records[(prior_phase, predecessor)]
        prior_body = prior.get("body") or ""
        deps = self.get(f"/issues/{task['number']}/dependencies/blocked_by", True)
        if prior["number"] not in {d["number"] for d in deps}:
            raise Violation("stage task must depend on its predecessor task")
        number = github_url(local.field(document, "Predecessor PR"), self.repo, "pull")
        if github_url(local.field(prior_body, "Review PR"), self.repo, "pull") != number:
            raise Violation("predecessor task and artifact disagree on merged PR")
        if prior.get("state") != "closed" or local.field(prior_body, "Status") != "Done":
            raise Violation("predecessor task lacks a completed handoff")
        merge, _ = self.merged(number, base)
        self.predecessor_scope(number, predecessor, root, directory)
        self.unchanged_prerequisites(stage, root, directory, merge, base)
        prior_path = local.stage_path(predecessor, root, directory)
        if local.content(merge, prior_path) != local.content(base, prior_path):
            raise Violation("predecessor artifact changed after its reviewed merge")
        local.require_status(merge, prior_path, local.STATUS[predecessor])
        approved = permalink(local.field(prior_body, "Approved artifact"), self.repo, prior_path)
        ancestor(approved, base)
        if local.content(approved, prior_path) != local.content(merge, prior_path):
            raise Violation("approved artifact version differs from the merged predecessor")
        if stage == "build":
            ancestor(local.field(document, "Plan commit"), base)
            if local.content(local.field(document, "Plan commit"), prior_path) != local.content(merge, prior_path):
                raise Violation("Build cites another Plan version")
        if stage == "proof" and local.field(document, "Build commit") != merge:
            raise Violation("proof must test the exact merged Build version")
        if stage == "ship" and local.field(document, "Proof commit") != merge:
            raise Violation("Ship must cite the exact merged Proof version")
        # Accept older artifacts as historical records, never as unverifiable merges.
        # New stage artifacts must always carry current tracking metadata.
        prior_doc = local.content(merge, prior_path)
        if local.field(prior_doc, "Stage", False):
            if local.field(prior_doc, "Stage issue") != f"https://github.com/{self.repo}/issues/{prior['number']}":
                raise Violation("predecessor backlink does not match its completed task")
        elif not local.section(document, "Transition"):
            raise Violation("legacy predecessor needs an explicit Transition record of missing backlinks")

    def handoff(self, number, base):
        """Check a placeholder task before creating the next stage's artifact."""
        task = self.issue(number)
        body = task.get("body") or ""
        stage = local.field(body, "Stage")
        if stage not in local.STAGES:
            raise Violation("unknown next stage")
        outcome = local.field(body, "Outcome")
        if not re.fullmatch(rf"[0-9]{{3,}}-{local.SLUG}", outcome):
            raise Violation("invalid outcome directory")
        root = "features/" + outcome
        phase = local.field(body, "Phase")
        if phase != "single" and not re.fullmatch(rf"P[1-9][0-9]*-{local.SLUG}", phase):
            raise Violation("invalid phase")
        directory = root if phase == "single" else root + "/" + phase
        parent = github_url(local.field(body, "Parent issue"), self.repo, "issues")
        records = self.graph(parent, root)
        if records.get((phase, stage), {}).get("number") != number:
            raise Violation("task is not in the declared outcome and phase")
        if task.get("state") != "open" or local.field(body, "Status") in {"Done", "Cancelled"}:
            raise Violation("closed or cancelled task cannot start work")
        if stage == "intent":
            return
        prior_stage = local.STAGES[local.STAGES.index(stage) - 1]
        prior = records[("single" if prior_stage == "intent" else phase, prior_stage)]
        deps = self.get(f"/issues/{number}/dependencies/blocked_by", True)
        if prior["number"] not in {d["number"] for d in deps}:
            raise Violation("next stage must depend on its predecessor task")
        for dep in deps:
            record = self.issue(dep["number"])
            text = record.get("body") or ""
            if record.get("state") != "closed" or record.get("state_reason") != "completed" or local.field(text, "Status") != "Done":
                raise Violation("next stage has an unmet dependency")
            merge, _ = self.merged(github_url(local.field(text, "Review PR"), self.repo, "pull"), base)
            # Every dependency needs immutable evidence, not just a closed issue.
            url = local.field(text, "Approved artifact")
            match = re.fullmatch(rf"https://github\.com/{re.escape(self.repo)}/blob/({local.SHA})/(features/[\w./-]+\.md)(?:#[\w-]+)?", url)
            if not match or not local.content(match[1], match[2]) or local.content(match[1], match[2]) != local.content(merge, match[2]):
                raise Violation("dependency lacks its approved merged artifact")
        document = prior.get("body") or ""
        commit, _ = self.merged(github_url(local.field(document, "Review PR"), self.repo, "pull"), base)
        self.predecessor_scope(github_url(local.field(document, "Review PR"), self.repo, "pull"), prior_stage, root, directory)
        self.unchanged_prerequisites(stage, root, directory, commit, base)
        path = local.stage_path(prior_stage, root, directory)
        local.require_status(commit, path, local.STATUS[prior_stage])
        if local.content(commit, path) != local.content(base, path):
            raise Violation("predecessor changed after its approved merge")
        approved = permalink(local.field(document, "Approved artifact"), self.repo, path)
        ancestor(approved, base)
        if local.content(approved, path) != local.content(commit, path):
            raise Violation("predecessor approval does not match merged content")

    def setup(self):
        report = {}
        try:
            types = self.get("/issue-types", True)
            report["Intent type"] = "configured" if any(t.get("name") == "Intent" for t in types) else "missing"
        except Violation:
            report["Intent type"] = "unverifiable"
        default = self.get("")["default_branch"]
        rules = None
        protection = None
        try:
            rules = self.get("/rules/branches/" + quote(default, safe=""), True)
        except Violation:
            pass
        try:
            protection = self.get("/branches/" + quote(default, safe="") + "/protection")
        except Violation:
            pass
        checks = set()
        reviews = False
        if protection:
            check_settings = protection.get("required_status_checks") or {}
            checks.update(check_settings.get("contexts", []))
            checks.update(c.get("context") for c in check_settings.get("checks", []))
            setting = protection.get("required_pull_request_reviews") or {}
            reviews = setting.get("required_approving_review_count", 0) >= 1 and setting.get("dismiss_stale_reviews", False)
        for rule in rules or []:
            parameters = rule.get("parameters", {})
            if rule.get("type") == "required_status_checks":
                checks.update(c.get("context") for c in parameters.get("required_status_checks", []))
            if rule.get("type") == "pull_request":
                reviews |= parameters.get("required_approving_review_count", 0) >= 1 and parameters.get("dismiss_stale_reviews_on_push", False)
        known = protection is not None or rules is not None
        for check in ("SDLC history", "Template verification"):
            report[check] = "configured" if check in checks else ("missing or inaccessible" if known else "unverifiable")
        report["Human review with renewed approval"] = "configured" if reviews else ("missing or inaccessible" if known else "unverifiable")
        return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--setup-check", action="store_true")
    parser.add_argument("--handoff", action="store_true", help="verify a stage task before writing its artifact")
    parser.add_argument("--issue", type=int)
    parser.add_argument("--base")
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--branch")
    parser.add_argument("--pr", type=int)
    args = parser.parse_args()
    evidence = Evidence(args.repo)
    if args.setup_check:
        report = evidence.setup()
        for name, state in report.items():
            print(f"{name}: {state}")
        if any(state != "configured" for state in report.values()):
            raise Violation("setup is incomplete; an administrator must review the reported policy")
        return
    if args.handoff:
        if not args.issue or not args.base:
            parser.error("handoff requires --issue and --base")
        base = local.git("rev-parse", "--verify", "--end-of-options", f"{args.base}^{{commit}}").strip()
        evidence.handoff(args.issue, base)
        print("Entry gate verified; the requested stage may start.")
        return
    if not args.base or not args.branch:
        parser.error("provide --base and --branch for stage evidence")
    base, head, selected = local.check_history(args.branch, args.base, args.head)
    evidence.validate(base, head, selected, args.pr, args.branch)
    print("GitHub predecessor and artifact links verified. Human review must verify attributed approval sources and outcome evidence.")


if __name__ == "__main__":
    try:
        main()
    except (Violation, KeyError, TypeError, ValueError) as error:
        message = str(error) if isinstance(error, Violation) else "GitHub returned incomplete evidence; verify access and retry"
        print("sdlc: " + message, file=sys.stderr)
        sys.exit(1)
