#!/usr/bin/env python3
"""Validate one stage against the index, committed history, and its predecessor."""

import argparse
from functools import lru_cache
from pathlib import PurePosixPath
import re
import subprocess
import sys

SLUG = r"[a-z0-9]+(?:-[a-z0-9]+)*"
FEATURE = re.compile(rf"(?:feature|proof|ship)/([0-9]{{3,}})-(?:P([1-9][0-9]*)-)?({SLUG})")
ARTIFACT = re.compile(rf"artifact/([0-9]{{3,}})-({SLUG})")
STAGES = ("intent", "spec", "plan", "build", "proof", "ship")
STATUS = dict(intent="accepted", spec="accepted", plan="approved", build="ready", proof="passed", ship="delivered")
SHA = r"[0-9a-f]{40}"
CONVENTIONS = "AGENTS.md"
MODES = ("merged source", "runtime artifact")


class Violation(Exception):
    """A workflow rule or required evidence is missing."""


def git(*args, optional=False):
    result = subprocess.run(["git", *args], capture_output=True)
    if result.returncode and not optional:
        raise Violation(result.stderr.decode(errors="replace").strip())
    return result.stdout.decode("utf-8", errors="surrogateescape") if not result.returncode else ""


@lru_cache(maxsize=None)
def paths(ref):
    args = ("ls-files", "--cached", "-z") if ref == "" else ("ls-tree", "-r", "--name-only", "-z", ref)
    return set(git(*args).split("\0")) - {""}


def content(ref, path):
    return git("show", f"{ref}:{path}", optional=True)


def field(document, name, required=True):
    values = re.findall(rf"^\*\*{re.escape(name)}:\*\* *([^\n]+?) *$", document, re.M)
    if len(values) != 1 or values[0].startswith("<"):
        if required:
            raise Violation(f"expected one filled {name} header")
        return ""
    return values[0]


def section(document, name):
    match = re.search(rf"^## {re.escape(name)}[^\n]*\n(.*?)(?=^## |\Z)", document, re.M | re.S)
    return match[1].strip() if match else ""


def delivery(ref, required=True):
    """Read the product's delivery mode and test paths from its conventions file.

    Tracking reads this tolerantly: a product that has not declared the
    setting keeps the six-stage shape, and the Build check reports the
    missing declaration explicitly rather than every stage failing.
    """
    # Settings are written as a list, like the other sections of the conventions file.
    settings = re.sub(r"^[-*] +", "", section(content(ref, CONVENTIONS), "Delivery settings"), flags=re.M)
    if not settings:
        if not required:
            return MODES[1], []
        raise Violation(
            f"{CONVENTIONS} needs a '## Delivery settings' section declaring "
            "Delivery: " + " or ".join(MODES))
    mode = field(settings, "Delivery", required)
    if mode not in MODES:
        if not required and not mode:
            return MODES[1], []
        raise Violation("Delivery must be exactly " + " or ".join(MODES) + f"; found {mode!r}")
    return mode, [p.strip() for p in field(settings, "Test paths").split(",") if p.strip()]


def tracked_stages(mode):
    """Merged-source delivery records Test + Review and Ship inside Build."""
    return STAGES[:4] if mode == "merged source" else STAGES


def spec_rules(ref, directory):
    return set(re.findall(r"^- (S[0-9]+)\b", content(ref, directory + "/spec.md"), re.M))


def named_tests(ref, test_paths):
    """Every test file's text, so a record's named test can be found literally."""
    files = [p for p in paths(ref) if any(p == t or p.startswith(t.rstrip("/") + "/") for t in test_paths)]
    if not files:
        raise Violation("no files under the declared Test paths: " + ", ".join(test_paths))
    return "\n".join(content(ref, path) for path in files)


def requirement_results(ref, document, directory, test_paths):
    """One passing result per Spec rule, each naming a test that exists."""
    required = spec_rules(ref, directory)
    results = re.findall(r"^- (S[0-9]+): (PASS|FAIL) — (.+)$", section(document, "Requirement results"), re.M)
    missing = required - {rule for rule, _, _ in results}
    if not required:
        raise Violation(directory + "/spec.md has no numbered S-rules to prove")
    if missing:
        raise Violation("Build record has no result for " + ", ".join(sorted(missing)))
    failed = sorted(rule for rule, verdict, _ in results if verdict != "PASS")
    if failed:
        raise Violation("Build record reports a failing rule: " + ", ".join(failed))
    suite = named_tests(ref, test_paths)
    for rule, _, evidence in results:
        name = evidence.split()[0].strip("`,;")
        if name not in suite:
            raise Violation(f"{rule} names {name}, which no file under the declared Test paths contains")


def intent_results(document, root, ref, last_phase):
    """One line per Intent success criterion; the last phase leaves none open."""
    criteria = re.findall(r"^- .+$", section(content(ref, root + "/intent.md"), "Success criteria"), re.M)
    results = re.findall(r"^- (TRUE|OPEN) — .+$", section(document, "Intent results"), re.M)
    if not criteria:
        raise Violation(root + "/intent.md has no success criteria to report")
    if len(results) != len(criteria):
        raise Violation(f"Intent results needs one TRUE or OPEN line for each of the "
                        f"{len(criteria)} success criteria; found {len(results)}")
    if last_phase and "OPEN" in results:
        raise Violation("the last phase cannot leave an Intent success criterion OPEN")


def each_fact_once(document):
    """One commit hash belongs to one field; repeats are copied bookkeeping."""
    hashes = re.findall(rf"^\*\*[^:\n]+:\*\* *({SHA}) *$", document, re.M)
    repeated = {value for value in hashes if hashes.count(value) > 1}
    if repeated:
        raise Violation("name each commit once; " + ", ".join(sorted(repeated))[:12]
                        + " appears in more than one header field")


def shipped_tag(root, directory):
    """The local shipped tag for this outcome and phase, when one exists."""
    outcome = PurePosixPath(root).name
    phase = "" if root == directory else "-" + PurePosixPath(directory).name
    tag = f"shipped/{outcome}{phase}"
    return tag if git("rev-parse", "--verify", "--quiet", "--end-of-options", tag + "^{commit}", optional=True).strip() else ""


def final_phase(ref, root, directory):
    phases = re.findall(rf"\bP[1-9][0-9]*-{SLUG}", section(content(ref, root + "/intent.md"), "Phases"))
    return not phases or PurePosixPath(directory).name == phases[-1]


def status(ref, path, value):
    return field(content(ref, path), "Status", False) == value


def changed(before, after):
    args = ["diff", "--no-ext-diff", "--no-renames", "--name-only", "-z"]
    args += ["--cached", before] if after == "" else [before, after]
    return set(git(*args, "--").split("\0")) - {""}


def branch_kind(branch):
    default = git("symbolic-ref", "--short", "refs/remotes/origin/HEAD", optional=True).strip()
    if branch in {"", "main", "master", default.removeprefix("origin/")}:
        raise Violation("direct or detached commits are blocked; use a named worktree branch")
    if FEATURE.fullmatch(branch):
        return branch.split("/")[0]
    if ARTIFACT.fullmatch(branch) or branch == "artifact/bootstrap":
        return "artifact"
    raise Violation("use artifact/, feature/, proof/, or ship/ with NNN[-Pn]-name; unsupported branch: " + repr(branch))


def artifact_allowed(branch, path):
    if branch == "artifact/bootstrap":
        return path in {
            "AGENTS.md", "REVIEW.md", "README.md", "LICENSE", "product/intent.md",
            "product/glossary.md", "product/personas.md", "product/regions.md",
            "product/architecture.md", ".agents/skills/bootstrap-product/SKILL.md",
        }
    match = ARTIFACT.fullmatch(branch)
    root = f"features/{match[1]}-{match[2]}/"
    return path.startswith(root) and bool(re.fullmatch(
        rf"intent\.md|(?:P[1-9][0-9]*-{SLUG}/)?spec\.md|"
        rf"(?:P[1-9][0-9]*-{SLUG}/)?design/.+\.(?:md|png|jpg|jpeg|webp|svg|pdf)|"
        rf"questions-for-{SLUG}\.md", path[len(root):]))


def feature_paths(branch, ref):
    number, phase, slug = FEATURE.fullmatch(branch).groups()
    if phase is None:
        root = directory = f"features/{number}-{slug}"
    else:
        roots = {path.rsplit("/", 1)[0] for path in paths(ref)
                 if re.fullmatch(rf"features/{number}-{SLUG}/intent\.md", path)}
        if len(roots) != 1:
            raise Violation(f"expected one committed intent for feature {number}; found {len(roots)}")
        root = roots.pop()
        directory = f"{root}/P{phase}-{slug}"
    return f"{root}/intent.md", f"{directory}/spec.md", f"{directory}/plan.md"


def context(branch, before, changes):
    kind = branch_kind(branch)
    if branch == "artifact/bootstrap":
        return "bootstrap", "", ""
    if kind == "artifact":
        match = ARTIFACT.fullmatch(branch)
        root = f"features/{match[1]}-{match[2]}"
        primary = {p for p in changes if p == root + "/intent.md" or p.endswith("/spec.md")}
        if len(primary) != 1:
            raise Violation("an artifact PR must change exactly one intent or exact-phase spec; do not bundle stages")
        artifact = primary.pop()
        stage = PurePosixPath(artifact).stem
        directory = str(PurePosixPath(artifact).parent)
        return stage, root, directory
    intent, spec, plan = feature_paths(branch, before)
    directory = str(PurePosixPath(plan).parent)
    stage = kind if kind in {"proof", "ship"} else ("plan" if changes == {plan} else "build")
    return stage, str(PurePosixPath(intent).parent), directory


def require_status(ref, path, value):
    if not status(ref, path, value):
        raise Violation(f"{path} must already be committed with Status: {value}")


def require_requirements(ref, intent, spec):
    for path in (intent, spec):
        require_status(ref, path, "accepted")


def stage_path(stage, root, directory):
    return f"{root if stage == 'intent' else directory}/{stage}.md"


def prerequisites(stage, root, directory):
    return [stage_path(s, root, directory) for s in STAGES[:STAGES.index(stage)]]


def declared_paths(plan):
    return re.findall(r"^- ([\w./-]+)(?:\s|$)", section(plan, "Touched surface"), re.M)


def in_surface(path, allowed):
    return any(path == p or (p.endswith("/") and path.startswith(p)) for p in allowed)


def validate_record(stage, ref, root, directory):
    path = stage_path(stage, root, directory)
    document = content(ref, path)
    for name in ("Outcome", "Stage", "Phase", "Parent issue", "Stage issue", "Predecessor PR"):
        field(document, name)
    phase = "single" if root == directory else PurePosixPath(directory).name
    if field(document, "Stage") != stage or field(document, "Outcome") != PurePosixPath(root).name or field(document, "Phase") != phase:
        raise Violation(f"{path}: outcome, phase, or stage does not match this branch")
    for name, kind in (("Parent issue", "issues"), ("Stage issue", "issues"), ("Predecessor PR", "pull")):
        if not re.fullmatch(rf"https://github\.com/[\w.-]+/[\w.-]+/{kind}/[1-9][0-9]*", field(document, name)):
            raise Violation(f"{path}: {name} must be a GitHub {kind} URL")
    if stage == "build":
        commit = field(document, "Plan commit")
        if not re.fullmatch(SHA, commit) or content(commit, directory + "/plan.md") != content(ref, directory + "/plan.md"):
            raise Violation("Build must name the exact approved Plan commit")
        field(document, "Verification")
        mode, test_paths = delivery(ref)
        if mode == "merged source":
            each_fact_once(document)
            # Test + Review evidence lands here instead of a separate Proof PR.
            requirement_results(ref, document, directory, test_paths)
            intent_results(document, root, ref, final_phase(ref, root, directory))
    if stage == "proof":
        commit = field(document, "Build commit")
        if not re.fullmatch(SHA, commit) or not content(commit, directory + "/build.md"):
            raise Violation("Proof needs the exact Build commit")
        required = set(re.findall(r"^- (S[0-9]+)\b", content(ref, directory + "/spec.md"), re.M))
        results = re.findall(r"^- (S[0-9]+): (PASS|FAIL) — (.+)$", section(document, "Requirement results"), re.M)
        if not required or len(results) != len(required) or {r[0] for r in results} != required or any(r[1] != "PASS" for r in results):
            raise Violation("Proof needs one PASS with evidence for every Spec S-rule")
        for name in ("Verification", "Human review", "Intent results"):
            if not section(document, name):
                raise Violation("Proof is missing " + name)
        if field(document, "Blocking findings") != "none":
            raise Violation("unresolved proof findings block Ship")
    if stage == "ship":
        for name in ("Build commit", "Proof commit"):
            if not re.fullmatch(SHA, field(document, name)):
                raise Violation(f"Ship needs a full {name}")
        for name in ("Destination", "Delivery evidence"):
            field(document, name)
        if field(document, "Result") != "success":
            raise Violation("failed delivery cannot complete Ship")
        if field(document, "Build commit") != field(content(ref, directory + "/proof.md"), "Build commit"):
            raise Violation("Ship version differs from the proved Build")


def validate_change(branch, before, after, changes, selected=None, anchor=None):
    stage, root, directory = selected or context(branch, before, changes)
    if stage == "bootstrap":
        if any(not artifact_allowed(branch, p) for p in changes):
            raise Violation("bootstrap carries constitution documents only")
        return
    artifact = stage_path(stage, root, directory)
    anchor = before if anchor is None else anchor
    if status(anchor, directory + "/ship.md", "delivered"):
        raise Violation("shipped outcomes are immutable; start a new intent")
    if shipped_tag(root, directory):
        raise Violation("this phase is already shipped and immutable; start a new intent")
    for path in prerequisites(stage, root, directory):
        require_status(anchor, path, STATUS[PurePosixPath(path).stem])
        if content(anchor, path) != content(after, path):
            raise Violation("a stage cannot change its prerequisite: " + path)
    if stage in {"intent", "spec"}:
        if any(not artifact_allowed(branch, p) for p in changes):
            raise Violation("artifact branches carry this stage's planning files only")
        allowed = {artifact}
        for p in changes:
            if p not in allowed and not p.startswith(directory + "/design/") and not re.fullmatch(rf"{re.escape(root)}/questions-for-{SLUG}\.md", p):
                raise Violation("do not bundle stages or phases in an artifact PR")
        if field(content(after, artifact), "Status", False) not in {"draft", "accepted"}:
            raise Violation("planning artifact needs Status: draft or accepted")
        document = content(after, artifact)
        if status(after, artifact, "accepted") and field(document, "Stage", False) and not field(document, "Accepted by", False):
            raise Violation("record the owner acceptance source before merging")
    elif stage == "plan":
        if changes != {artifact}:
            raise Violation("Plan PR contains only its approved plan")
        require_status(after, artifact, "approved")
        document = content(after, artifact)
        if field(document, "Stage", False) and not field(document, "Approved by", False):
            raise Violation("record the owner approval source before committing Plan")
    elif stage == "build":
        forbidden = [p for p in changes if re.match(r"features/[0-9]{3,}-", p) and p != artifact]
        if forbidden:
            raise Violation("Build cannot amend planning or proof artifacts: " + repr(forbidden))
        require_status(after, artifact, "ready")
        validate_record(stage, after, root, directory)
        allowed = declared_paths(content(anchor, directory + "/plan.md")) + [artifact]
        if any(not in_surface(p, allowed) for p in changes):
            raise Violation("Build touches a path outside the approved plan: " + repr(sorted(p for p in changes if not in_surface(p, allowed))))
        if any(p.startswith("packages/") for p in changes):
            if field(content(anchor, root + "/intent.md"), "Kind", False) != "contracts":
                raise Violation("packages/ changes need their own intent with Kind: contracts")
    else:
        if changes != {artifact}:
            raise Violation(f"{stage} PR changes only {artifact}")
        require_status(after, artifact, STATUS[stage])
        validate_record(stage, after, root, directory)
        # Any changed product or planning file since the tested Build invalidates proof.
        proof = content(after, directory + "/proof.md")
        build = field(proof, "Build commit")
        allowed_evidence = {directory + "/proof.md", directory + "/ship.md"}
        if changed(build, after) - allowed_evidence:
            raise Violation("proof is stale: changes after the tested Build require a new Build and proof")
        if stage == "ship":
            proof_commit = field(content(after, artifact), "Proof commit")
            if content(proof_commit, directory + "/proof.md") != proof:
                raise Violation("Ship's Proof commit does not match committed proof")


def local_base():
    ref = git("symbolic-ref", "--short", "refs/remotes/origin/HEAD", optional=True).strip()
    if not ref:
        ref = "origin/main" if git("rev-parse", "--verify", "origin/main", optional=True) else "main"
    return git("merge-base", "HEAD", ref).strip()


def check_staged():
    branch = git("symbolic-ref", "--short", "HEAD", optional=True).strip()
    branch_kind(branch)
    base = local_base()
    delta = changed("HEAD", "")
    selected = context(branch, base, changed(base, ""))
    validate_change(branch, "HEAD", "", delta, selected, base)
    print("Local stage checks passed; GitHub approval and merge evidence still require the handoff check.")


def history_context(branch, base, head):
    branch_kind(branch)
    base = git("rev-parse", "--verify", "--end-of-options", f"{base}^{{commit}}").strip()
    head = git("rev-parse", "--verify", "--end-of-options", f"{head}^{{commit}}").strip()
    base = git("merge-base", base, head).strip()
    commits = git("rev-list", "--reverse", "--topo-order", f"{base}..{head}").splitlines()
    if not commits:
        raise Violation("no commits to validate; check the PR base and head")
    return base, head, commits, context(branch, base, changed(base, head))


def check_history(branch, base, head):
    base, head, commits, selected = history_context(branch, base, head)
    previous = base
    for commit in commits:
        if git("show", "-s", "--format=%P", commit).split() != [previous]:
            raise Violation("keep PR history linear; rebase onto the target branch")
        try:
            validate_change(branch, previous, commit, changed(previous, commit), selected, base)
        except Violation as error:
            raise Violation(f"commit {commit[:12]}: {error}") from error
        previous = commit
    if selected[0] == "build" and stage_path(*selected) not in changed(base, head):
        raise Violation("every Build PR must update build.md, including corrections")
    return base, head, selected


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
