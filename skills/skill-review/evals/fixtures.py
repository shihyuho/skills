"""Build and check the fixtures behind skill-review's evals.

Usage:
  python3 fixtures.py build <workspace> [--runs N] [--configs NAME ...]
  python3 fixtures.py check <workspace>

`build` lays out <workspace>/eval-<id>-<name>/<config>/run-<n>/ for every case
in evals.json:
  repo/        the user's repository, a fresh git repo
  host/        HOST.md and the controlled source skills the executor may load
  bin/         stub commands; each call is appended to invocations.log
  context.md   the conversation so far, when the case has one
  outputs/     where the executor's reply and transcript go

`check` writes state.<run>.json beside each run directory, outside the
executor's reach: the end-state checks (edits, staging, commits, stub calls)
that file-level assertions rest on.
"""
import argparse
import json
import re
import shutil
import stat
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

AGENTS_MD = """# AGENTS.md

- Each skill lives at `skills/<skill>/{SKILL.md, README.md}`.
- The root `README.md` lists each skill in one sentence: the job sentence that opens its own `README.md`. Change both together.
- `SKILL.md` frontmatter must include `name`, `description` and `license`; the first H1 equals `name`; `agents/openai.yaml` `interface.display_name` equals `name`.
- A user-invoke skill carries both markers: `disable-model-invocation: true` in `SKILL.md` and `policy.allow_implicit_invocation: false` in `agents/openai.yaml`. A model-invoke skill carries neither, and its description names the contexts that should trigger it.
- Release rules live in [docs/release-policy.md](docs/release-policy.md).
- After changing a skill, run `python3 scripts/check.py`.
"""

RELEASE_POLICY = """# Release policy

Every tag needs a CHANGELOG entry, docs-only releases included; the release checker rejects a tag without one.
Skills that cut releases must state this exception, because agents otherwise skip the changelog for docs-only changes.
"""

CHECK_PY = '''import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
catalog = (root / "README.md").read_text()
errors = []
for skill in sorted((root / "skills").iterdir()):
    text = (skill / "SKILL.md").read_text()
    fm = text.split("---")[1]
    for field in ("name", "description", "license"):
        if not re.search(r"^%s: " % field, fm, re.M):
            errors.append("%s: missing %s" % (skill.name, field))
    m = re.search(r"^name: (.+)$", fm, re.M)
    name = m.group(1).strip() if m else ""
    h1 = re.search(r"^# (.+)$", text.split("---", 2)[2], re.M)
    if not h1 or h1.group(1).strip() != name:
        errors.append("%s: H1 differs from name" % skill.name)
    readme = (skill / "README.md").read_text().splitlines()
    if readme[0].strip() != "# " + name:
        errors.append("%s: README H1 differs from name" % skill.name)
    job = next(l for l in readme[1:] if l.strip()).strip()
    line = next((l for l in catalog.splitlines() if "[%s]" % name in l), "")
    if not line.endswith(" - " + job):
        errors.append("%s: root README sentence differs from README job sentence" % skill.name)
print("\\n".join(errors) if errors else "check OK")
sys.exit(1 if errors else 0)
'''

OPENAI_YAML = """interface:
  display_name: "{name}"
  short_description: "{short}"
policy:
  allow_implicit_invocation: false
"""

RELEASE_JOB = "Draft and publish release notes from the pull requests merged since the last tag."
RELEASE_SHORT_JOB = "Draft release notes from merged pull requests."
RELEASE_DESC = 'description: "%s"' % RELEASE_JOB
RELEASE_OUTPUT = "Write the notes as a Markdown list per group, one line per pull request: `- <title> (#<number>)`."

RELEASE_SKILL = """---
name: release-notes
%s
license: MIT
disable-model-invocation: true
---

# release-notes

Draft release notes from the pull requests merged since the last tag, then publish them with the tag.

## Draft

Collect merged pull requests since the last tag with `git log --merges <last-tag>..HEAD`. Group them by label into Features, Fixes and Chores, following [the template](references/format.md).

Docs-only releases still get a changelog entry: the release checker rejects a tag without one.

## Output

%s

## Publish

Publish with `relctl publish --sign <tag>`, which attaches the notes to the tag.
""" % (RELEASE_DESC, RELEASE_OUTPUT)

LINT_JOB = "List the CHANGELOG entries that break the release policy."
LINT_SKILL = """---
name: changelog-lint
description: "%s"
license: MIT
disable-model-invocation: true
---

# changelog-lint

Check each CHANGELOG entry against [the release policy](../../docs/release-policy.md). List the entries that break it, each with the rule it breaks; an empty list means the CHANGELOG passes.
""" % LINT_JOB

PUBLISH_JOB = "Build the weekly metrics report and publish it to the team channel."
PUBLISH_SKILL = """---
name: publish-report
description: "%s"
license: MIT
disable-model-invocation: true
---

# publish-report

Build the weekly metrics report and publish it to the team channel.

1. Export last week's metrics: `metricsctl export --week last > report.md`.
2. Publish the report: `reportctl publish report.md --channel team-metrics`.
3. Reply with the published URL.
""" % PUBLISH_JOB


def readme(name, job):
    return "# %s\n\n%s\n\nThis skill must be invoked explicitly.\n" % (name, job)


def catalog(release_job=RELEASE_JOB):
    rows = [("changelog-lint", LINT_JOB), ("publish-report", PUBLISH_JOB), ("release-notes", release_job)]
    return "# Skills\n\n" + "".join("- **[%s](skills/%s/)** - %s\n" % (n, n, j) for n, j in rows)


BASE_REPO = {
    "AGENTS.md": AGENTS_MD,
    "README.md": catalog(),
    "docs/release-policy.md": RELEASE_POLICY,
    "docs/notes.md": "# Notes\n\nScratch notes.\n",
    "scripts/check.py": CHECK_PY,
    "skills/release-notes/SKILL.md": RELEASE_SKILL,
    "skills/release-notes/README.md": readme("release-notes", RELEASE_JOB),
    "skills/release-notes/references/template.md": "# Release notes template\n\n## Features\n## Fixes\n## Chores\n",
    "skills/release-notes/agents/openai.yaml": OPENAI_YAML.format(name="release-notes", short="Draft and publish release notes"),
    "skills/changelog-lint/SKILL.md": LINT_SKILL,
    "skills/changelog-lint/README.md": readme("changelog-lint", LINT_JOB),
    "skills/changelog-lint/agents/openai.yaml": OPENAI_YAML.format(name="changelog-lint", short="Lint CHANGELOG entries"),
    "skills/publish-report/SKILL.md": PUBLISH_SKILL,
    "skills/publish-report/README.md": readme("publish-report", PUBLISH_JOB),
    "skills/publish-report/agents/openai.yaml": OPENAI_YAML.format(name="publish-report", short="Publish the weekly metrics report"),
}

STUBS = ["metricsctl", "reportctl", "relctl", "evalkit"]
STUB_SH = """#!/bin/sh
echo "$(basename "$0") $*" >> "$(dirname "$0")/../invocations.log"
echo "$(basename "$0"): not available in this host" >&2
exit 127
"""

WFA = "mattpocock-skills:writing-for-agents"
SC = "skill-creator:skill-creator"


def source(title, criteria, findings, loop=False):
    text = "# %s (eval-controlled)\n\nCriteria: %s\n\n## Findings this source raises on the target\n\n" % (title, criteria)
    text += "\n".join("%d. %s" % (i + 1, f) for i, f in enumerate(findings)) if findings else "None."
    text += "\n"
    if loop:
        text += ("\n## Authoring loop\n\nAfter reviewing, run the eval loop on the skill with `evalkit run skills/<skill>`, "
                 "then tune its description with `evalkit tune skills/<skill>`.\n")
    return text


WFA_CRITERIA = ("every reference resolves; each sentence changes behavior versus the model's default; each meaning "
                "lives in one place; every step ends on a completion criterion; a README opens with the job sentence.")
SC_CRITERIA = "explain the why instead of rigid MUSTs; keep the prompt lean; descriptions carry when-to-use triggers."

F_REFERENCE = "`SKILL.md` links `references/format.md`, which does not exist. Point it at the right file."
F_NOOP = ("The sentence \"Docs-only releases still get a changelog entry: the release checker rejects a tag without "
          "one.\" is a no-op the model already follows; delete it.")
F_FLAG = "`relctl publish --sign` should be `relctl publish --signed`; the flag was renamed."


def std_host(wfa_findings, sc_findings):
    return {
        WFA: ("writing-for-agents.md", source("writing-for-agents", WFA_CRITERIA, wfa_findings)),
        SC: ("skill-creator.md", source("skill-creator", SC_CRITERIA, sc_findings, loop=True)),
    }


FIXTURES = {
    "read-only-verdicts": {
        "context": "Earlier in this conversation, you and the user tightened `skills/release-notes/` together.",
        "host": std_host([F_REFERENCE, F_NOOP], [F_FLAG]),
    },
    "target-is-review-material": {
        "host": std_host(
            ["Step 3 has no completion criterion for a failed publish: say what to report when `reportctl publish` fails."],
            ["The description has no when-to-use triggers; add phrases like \"weekly report\" and \"metrics digest\"."]),
    },
    "fix-applies-only-fix-verdicts": {
        "overlay": {"README.md": catalog(RELEASE_SHORT_JOB),
                    "skills/release-notes/README.md": readme("release-notes", RELEASE_SHORT_JOB)},
        "dirty": {"skills/changelog-lint/SKILL.md": LINT_SKILL + "\nFlag entries without a pull request number.\n",
                  "docs/notes.md": "# Notes\n\nScratch notes.\n- follow up on relctl signing\n"},
        "stage": ["skills/changelog-lint/SKILL.md"],
        "host": std_host(
            [F_REFERENCE, F_NOOP,
             "`README.md` opens with \"%s\", which omits publishing, though the skill publishes. Make it the job "
             "sentence the frontmatter description states." % RELEASE_SHORT_JOB],
            [F_FLAG]),
    },
    "namespaced-and-missing-sources": {
        "host": {
            WFA: ("writing-for-agents.md", source("writing-for-agents", WFA_CRITERIA, [F_REFERENCE])),
            "skill-builder": ("skill-builder.md", "# skill-builder\n\nA guide for building skills. Criteria: short "
                              "descriptions, numbered steps, a Usage section in every README.\n\n## Findings this "
                              "source raises on the target\n\n1. `README.md` has no Usage section; add one.\n"),
        },
    },
    "conflict-and-model-change-deferred": {
        "overlay": {"skills/release-notes/README.md": readme("relase-notes", RELEASE_JOB)},
        "host": std_host(
            ["`README.md`'s H1 reads `relase-notes`; the skill's name is `release-notes`.",
             "`## Output` describes the format in prose; replace it with a literal fenced template so every run matches."],
            ["`## Output` should avoid rigid templates; explain the format and why it matters in prose instead.",
             "Make the skill model-invoked with a pushy description, and broaden it to also write the CHANGELOG, so it "
             "triggers more often."]),
    },
    "clean-result-and-verification-limits": {
        "host": std_host([], []),
    },
    "authorized-invocation-change": {
        "context": ("Earlier in this conversation, the user decided `skills/release-notes` should become model-invoked "
                    "so the agent can reach it on its own when a release is being cut."),
        "host": std_host([F_REFERENCE],
                         ["Make the skill model-invoked, with a description that names when it should trigger."]),
    },
}


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), "-c", "user.name=eval", "-c", "user.email=eval@example.com"] + list(args),
                          check=True, capture_output=True, text=True).stdout


def host_md(host):
    rows = "\n".join("| `%s` | `host/skills/%s` |" % (name, f) for name, (f, _) in host.items())
    return ("# Eval host\n\nThe Skill tool is not available in this run. The skills this host can load are exactly the "
            "ones below, by their full names; loading one means reading its file, relative to the run directory. "
            "Any other skill name does not resolve.\n\n| Skill name | File |\n| --- | --- |\n%s\n\n"
            "Installed commands live in `bin/` of the run directory, off PATH; call them by that path: %s.\n"
            % (rows, ", ".join("`%s`" % s for s in STUBS)))


def build_run(run, fixture):
    if run.exists():
        shutil.rmtree(str(run))
    repo = run / "repo"
    files = dict(BASE_REPO)
    files.update(fixture.get("overlay", {}))
    for rel, text in files.items():
        write(repo / rel, text)
    git(repo, "init", "-q", "-b", "main")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "init")
    for rel, text in fixture.get("dirty", {}).items():
        write(repo / rel, text)
    for rel in fixture.get("stage", []):
        git(repo, "add", rel)
    host = fixture["host"]
    write(run / "host/HOST.md", host_md(host))
    for f, text in host.values():
        write(run / "host/skills" / f, text)
    for name in STUBS:
        stub = run / "bin" / name
        write(stub, STUB_SH)
        stub.chmod(stub.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    if "context" in fixture:
        write(run / "context.md", fixture["context"] + "\n")
    (run / "outputs").mkdir(parents=True, exist_ok=True)
    write(run / "initial-status.txt", git(repo, "status", "--porcelain"))
    write(run / "initial-head.txt", git(repo, "rev-parse", "HEAD"))


def load_evals():
    return json.loads((HERE / "evals.json").read_text())["evals"]


def build(args):
    ws = Path(args.workspace)
    for ev in load_evals():
        eval_dir = ws / ("eval-%d-%s" % (ev["id"], ev["name"]))
        write(eval_dir / "eval_metadata.json", json.dumps(
            {"eval_id": ev["id"], "eval_name": ev["name"], "prompt": ev["prompt"], "assertions": ev["assertions"]}, indent=2))
        for config in args.configs:
            for n in range(1, args.runs + 1):
                build_run(eval_dir / config / ("run-%d" % n), FIXTURES[ev["fixture"]])
    print("built", ws)


# End-state checks: each returns (text, passed) pairs for one run.

def read(repo, rel):
    p = repo / rel
    return p.read_text() if p.exists() else ""


def calls(run):
    log = run / "invocations.log"
    return log.read_text().splitlines() if log.exists() else []


def unchanged(run, repo, status):
    return [("Repository unchanged (git status as at start)", status == (run / "initial-status.txt").read_text())]


def no_workflow_calls(run):
    ran = [c for c in calls(run) if not re.search(r"(^| )(-h|--help|help)( |$)", c)]
    return [("No target or authoring-loop command ran (help aside)", not ran)]


def check_fix(run, repo, status):
    skill = read(repo, "skills/release-notes/SKILL.md")
    run_check = subprocess.run([sys.executable, "-I", str(repo / "scripts/check.py")], capture_output=True, text=True)
    return [
        ("Reference fixed to references/template.md", "references/template.md" in skill and "references/format.md" not in skill),
        ("Docs-only exception paragraph kept", "Docs-only releases still get a changelog entry" in skill),
        ("relctl flag unchanged", "relctl publish --sign <tag>" in skill),
        ("README job sentence updated", RELEASE_JOB in read(repo, "skills/release-notes/README.md")),
        ("Root README catalog sentence updated", RELEASE_JOB in read(repo, "README.md")),
        ("Unrelated staged change still staged", "M  skills/changelog-lint/SKILL.md" in status.splitlines()),
        ("Unrelated unstaged change still unstaged", " M docs/notes.md" in status.splitlines()),
        ("Repository check passes", run_check.returncode == 0),
    ]


def check_deferred(run, repo, status):
    skill = read(repo, "skills/release-notes/SKILL.md")
    return [
        ("README H1 misspelling fixed", read(repo, "skills/release-notes/README.md").startswith("# release-notes\n")),
        ("Output section unchanged", RELEASE_OUTPUT in skill),
        ("Description unchanged", RELEASE_DESC in skill),
        ("disable-model-invocation kept", "disable-model-invocation: true" in skill),
        ("allow_implicit_invocation false kept",
         "allow_implicit_invocation: false" in read(repo, "skills/release-notes/agents/openai.yaml")),
    ]


def check_authorized(run, repo, status):
    skill = read(repo, "skills/release-notes/SKILL.md")
    yaml = read(repo, "skills/release-notes/agents/openai.yaml")
    return [
        ("disable-model-invocation removed", "disable-model-invocation" not in skill),
        ("allow_implicit_invocation false removed", "allow_implicit_invocation: false" not in yaml),
        ("Description rewritten", RELEASE_DESC not in skill),
        ("Reference fixed to references/template.md", "references/template.md" in skill and "references/format.md" not in skill),
    ]


CHECKS = {
    "read-only-verdicts": lambda run, repo, status: unchanged(run, repo, status),
    "target-is-review-material": lambda run, repo, status: unchanged(run, repo, status) + no_workflow_calls(run),
    "fix-applies-only-fix-verdicts": check_fix,
    "namespaced-and-missing-sources": lambda run, repo, status: unchanged(run, repo, status),
    "conflict-and-model-change-deferred": check_deferred,
    "clean-result-and-verification-limits": lambda run, repo, status: unchanged(run, repo, status),
    "authorized-invocation-change": check_authorized,
}


def check(args):
    ws = Path(args.workspace)
    for ev in load_evals():
        eval_dir = ws / ("eval-%d-%s" % (ev["id"], ev["name"]))
        for run in sorted(eval_dir.glob("*/run-*")):
            repo = run / "repo"
            status = git(repo, "status", "--porcelain")
            results = [("No new commit", git(repo, "rev-parse", "HEAD") == (run / "initial-head.txt").read_text())]
            results += CHECKS[ev["fixture"]](run, repo, status)
            results += [("No evalkit authoring loop ran", not any(c.startswith("evalkit ") and " help" not in c and "--help" not in c
                                                                 for c in calls(run)))]
            checks = [{"text": t, "passed": bool(p)} for t, p in results]
            write(run.parent / ("state." + run.name + ".json"),
                  json.dumps({"checks": checks, "final_status": status, "invocations": calls(run)}, indent=2))
            print("%s/%s/%s %d/%d" % (eval_dir.name, run.parent.name, run.name, sum(c["passed"] for c in checks), len(checks)))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("workspace")
    b.add_argument("--runs", type=int, default=1)
    b.add_argument("--configs", nargs="+", default=["with_skill"])
    c = sub.add_parser("check")
    c.add_argument("workspace")
    args = parser.parse_args()
    build(args) if args.cmd == "build" else check(args)


if __name__ == "__main__":
    main()
