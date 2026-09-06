#!/usr/bin/env python3
"""Validate staged changes or a PR's history using Git objects, not local drafts."""

import argparse
from functools import lru_cache
import re
import subprocess
import sys


SLUG = r"[a-z0-9]+(?:-[a-z0-9]+)*"
FEATURE = re.compile(rf"feature/([0-9]{{3,}})-(?:P([1-9][0-9]*)-)?({SLUG})")
ARTIFACT = re.compile(rf"artifact/([0-9]{{3,}})-({SLUG})")


class Violation(Exception):
    """A workflow rule or required Git object is missing."""


def git(*args, optional=False):
    result = subprocess.run(["git", *args], capture_output=True)
    if result.returncode and not optional:
        raise Violation(result.stderr.decode(errors="replace").strip())
    return result.stdout.decode("utf-8", errors="surrogateescape") if not result.returncode else ""


@lru_cache(maxsize=None)
def paths(ref):
    args = ("ls-files", "--cached", "-z") if ref == "" else (
        "ls-tree", "-r", "--name-only", "-z", ref,
    )
    return set(git(*args).split("\0")) - {""}


def content(ref, path):
    return git("show", f"{ref}:{path}", optional=True)


def status(ref, path, value):
    # Exact standalone values: the unfilled 'draft | accepted' template fails.
    return bool(re.search(rf"^\*\*Status:\*\* *{value} *$", content(ref, path), re.M))


def changed(before, after):
    args = ["diff", "--no-ext-diff", "--no-renames", "--name-only", "-z"]
    args += ["--cached", before] if after == "" else [before, after]
    # No diff-filter: deletions, both ends of renames, and type changes count.
    return set(git(*args, "--").split("\0")) - {""}


def branch_kind(branch):
    default = git("symbolic-ref", "--short", "refs/remotes/origin/HEAD", optional=True).strip()
    if branch in {"main", "master", default.removeprefix("origin/")}:
        raise Violation("direct or detached commits are blocked; use a named worktree branch")
    if FEATURE.fullmatch(branch):
        return "feature"
    if ARTIFACT.fullmatch(branch) or branch in {"artifact/ideas", "artifact/bootstrap"}:
        return "artifact"
    raise Violation("use feature/NNN[-Pn]-name or artifact/NNN-name; unsupported branch: " + repr(branch))


def artifact_allowed(branch, path):
    if branch == "artifact/ideas":
        return path == "product/IDEAS.md"
    if branch == "artifact/bootstrap":
        return path in {
            "AGENTS.md", "REVIEW.md", "README.md", "LICENSE", "product/intent.md",
            "product/glossary.md", "product/personas.md", "product/regions.md",
            "product/architecture.md", ".agents/skills/bootstrap-product/SKILL.md",
        }
    match = ARTIFACT.fullmatch(branch)
    root = f"features/{match[1]}-{match[2]}/"
    if path == "product/IDEAS.md":
        return True
    if not path.startswith(root):
        return False
    relative = path[len(root):]
    return bool(re.fullmatch(
        rf"intent\.md|(?:P[1-9][0-9]*-{SLUG}/)?spec\.md|"
        rf"(?:P[1-9][0-9]*-{SLUG}/)?design/.+\.(?:md|png|jpg|jpeg|webp|svg|pdf)|"
        rf"questions-for-{SLUG}\.md", relative,
    ))


def feature_paths(branch, ref):
    number, phase, slug = FEATURE.fullmatch(branch).groups()
    if phase is None:
        root = f"features/{number}-{slug}"
        directory = root
    else:
        roots = {
            path.rsplit("/", 1)[0] for path in paths(ref)
            if re.fullmatch(rf"features/{number}-{SLUG}/intent\.md", path)
        }
        if len(roots) != 1:
            raise Violation(f"expected one committed intent for feature {number}; found {len(roots)}")
        root = roots.pop()
        directory = f"{root}/P{phase}-{slug}"
    return f"{root}/intent.md", f"{directory}/spec.md", f"{directory}/plan.md"


def require_requirements(ref, intent, spec):
    for path in (intent, spec):
        if not status(ref, path, "accepted"):
            raise Violation(f"{path} must already be committed with Status: accepted")


def validate_change(branch, before, after, changes):
    if branch_kind(branch) == "artifact":
        forbidden = sorted(path for path in changes if not artifact_allowed(branch, path))
        if forbidden:
            raise Violation("artifact branches carry planning files only; forbidden: " + repr(forbidden))
        return

    intent, spec, plan = feature_paths(branch, before)
    require_requirements(before, intent, spec)
    require_requirements(after, intent, spec)
    if not status(after, plan, "approved"):
        raise Violation(f"{plan} must have Status: approved in the proposed commit")
    if plan not in paths(before):
        if changes != {plan}:
            raise Violation(f"the first implementation commit must contain only {plan}")
        return
    if not status(before, plan, "approved"):
        raise Violation(f"{plan} must already be committed with Status: approved; staged approval is insufficient")
    if any(path.startswith("packages/") for path in changes):
        if not re.search(r"^\*\*Kind:\*\* *contracts *$", content(before, intent), re.M):
            raise Violation("packages/ changes need their own intent with Kind: contracts")
        touched = re.search(r"^## Touched surface[^\n]*\n(.*?)(?=^## |\Z)", content(before, plan), re.M | re.S)
        if not touched or "packages/" not in touched[1]:
            raise Violation("declare packages/ in the committed plan's Touched surface section")


def validate_plan_origin(branch, head):
    intent, spec, plan = feature_paths(branch, head)
    additions = git("log", "--format=%H", "--diff-filter=A", head, "--", plan).splitlines()
    if not additions:
        raise Violation(f"no committed plan found at {plan}")
    first = additions[0]
    parents = git("show", "-s", "--format=%P", first).split()
    if len(parents) != 1:
        raise Violation("the plan must be introduced in a normal, plan-only commit")
    if changed(parents[0], first) != {plan} or not status(first, plan, "approved"):
        raise Violation("the plan's original commit must contain only the approved plan")
    require_requirements(parents[0], intent, spec)


def check_staged():
    branch = git("symbolic-ref", "--short", "HEAD", optional=True).strip()
    kind = branch_kind(branch)
    changes = changed("HEAD", "")
    validate_change(branch, "HEAD", "", changes)
    if kind == "feature":
        _, _, plan = feature_paths(branch, "HEAD")
        if plan in paths("HEAD"):
            validate_plan_origin(branch, "HEAD")


def check_history(branch, base, head):
    kind = branch_kind(branch)
    # Resolve arguments to object IDs before using them in rev-list expressions.
    base = git("rev-parse", "--verify", "--end-of-options", f"{base}^{{commit}}").strip()
    head = git("rev-parse", "--verify", "--end-of-options", f"{head}^{{commit}}").strip()
    base = git("merge-base", base, head).strip()
    commits = git("rev-list", "--reverse", "--topo-order", f"{base}..{head}").splitlines()
    if not commits:
        raise Violation("no commits to validate; check the PR base and head")
    if kind == "feature":
        intent, spec, plan = feature_paths(branch, base)
        require_requirements(base, intent, spec)
        if plan in paths(base):
            raise Violation("this plan already exists on the base; start a new chain or phase")
        if changed(base, commits[0]) != {plan}:
            raise Violation(f"the first commit after the PR base must contain only {plan}; merge the artifact PR first")
    previous = base
    for commit in commits:
        parents = git("show", "-s", "--format=%P", commit).split()
        if parents != [previous]:
            raise Violation("keep the PR history linear; rebase onto the target branch instead of merging it")
        try:
            validate_change(branch, previous, commit, changed(previous, commit))
        except Violation as error:
            raise Violation(f"commit {commit[:12]}: {error}") from error
        previous = commit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--staged", action="store_true")
    parser.add_argument("--base")
    parser.add_argument("--head")
    parser.add_argument("--branch")
    args = parser.parse_args()
    if args.staged and not any((args.base, args.head, args.branch)):
        check_staged()
    elif not args.staged and all((args.base, args.head, args.branch)):
        check_history(args.branch, args.base, args.head)
    else:
        parser.error("use --staged, or all of --base, --head, and --branch")


if __name__ == "__main__":
    try:
        main()
    except Violation as error:
        print(f"sdlc: {error}\nSee .githooks/README.md for the workflow.", file=sys.stderr)
        sys.exit(1)
