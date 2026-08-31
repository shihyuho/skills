#!/usr/bin/env python3
"""Inspect an SDKMAN environment without activating or mutating it."""

from __future__ import annotations

import os
import sys

# Running a file named inspect.py adds its directory to sys.path, which would
# shadow Python's stdlib inspect module when another stdlib module imports it.
_SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
if sys.path and os.path.abspath(sys.path[0]) == _SCRIPT_DIRECTORY:
    del sys.path[0]

import argparse
import json
from pathlib import Path
import re
import subprocess
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


SCHEMA_VERSION = 1
CANDIDATE_RE = re.compile(r"^[a-z][a-z0-9]*$")
SAFE_VALUE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+~-]*$")
PREFIX_BOUNDARIES = frozenset(".-+")
ERROR_CODES = {
    "git_unavailable",
    "invalid_input",
    "invalid_workload",
    "inspection_failed",
    "malformed_sdkmanrc",
    "sdkman_unavailable",
    "unsafe_candidate_path",
    "unsafe_current_link",
}
CHOICE_CODES = {"ambiguous_candidate", "no_installed_match"}
APPROVAL_CODES = {"missing_exact_candidate"}


class ContractError(Exception):
    """An inspection contract error that must become JSON."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise ContractError("invalid_input", message)


def parse_assignment(raw: str, option: str) -> Tuple[str, str]:
    if "=" not in raw:
        raise ContractError("invalid_input", "%s expects CANDIDATE=VALUE" % option)
    candidate, value = raw.split("=", 1)
    if not CANDIDATE_RE.fullmatch(candidate):
        raise ContractError("invalid_input", "Unsafe candidate name for %s" % option)
    if not value or not SAFE_VALUE_RE.fullmatch(value):
        raise ContractError("invalid_input", "Unsafe or empty value for %s" % option)
    return candidate, value


def parse_assignments(values: Sequence[str], option: str) -> Dict[str, str]:
    parsed: Dict[str, str] = {}
    for raw in values:
        candidate, value = parse_assignment(raw, option)
        if candidate in parsed:
            raise ContractError("invalid_input", "Duplicate %s for %s" % (option, candidate))
        parsed[candidate] = value
    return parsed


def build_parser() -> JsonArgumentParser:
    parser = JsonArgumentParser(add_help=False)
    parser.add_argument("--workload-dir", required=True)
    parser.add_argument("--exact", action="append", default=[])
    parser.add_argument("--version-prefix", action="append", default=[])
    parser.add_argument("--vendor-suffix", action="append", default=[])
    parser.add_argument("--delegate", action="append", default=[])
    return parser


def initial_workload(raw: Optional[str]) -> Dict[str, object]:
    directory = str(Path(raw or ".").expanduser().absolute())
    return {
        "directory": directory,
        "boundary": None,
        "inside_git": False,
        "sdkmanrc": None,
    }


def emit(status: str, workload: Dict[str, object], plan: List[dict], blockers: List[dict], diagnostics: List[dict]) -> int:
    payload = {
        "schema_version": SCHEMA_VERSION,
        "status": status,
        "workload": workload,
        "plan": plan,
        "blockers": blockers,
        "diagnostics": diagnostics,
    }
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    if status in ("ready", "no_switch"):
        return 0
    if status in ("choice_required", "approval_required"):
        return 2
    return 1


def error_result(workload: Dict[str, object], error: ContractError) -> int:
    return emit(
        "error",
        workload,
        [],
        [{"code": error.code, "message": error.message}],
        [],
    )


def resolve_workload(raw: str) -> Dict[str, object]:
    try:
        directory = Path(raw).expanduser().resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise ContractError("invalid_workload", "Workload directory is unavailable: %s" % exc)
    if not directory.is_dir():
        raise ContractError("invalid_workload", "Workload path is not a directory")

    try:
        git = subprocess.run(
            ["git", "-C", str(directory), "rev-parse", "--show-toplevel"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        raise ContractError("git_unavailable", "git is required for worktree boundary discovery")

    if git.returncode == 0:
        try:
            boundary = Path(git.stdout.strip()).resolve(strict=True)
        except (OSError, RuntimeError) as exc:
            raise ContractError("invalid_workload", "Git worktree boundary is unavailable: %s" % exc)
        if directory != boundary and boundary not in directory.parents:
            raise ContractError("invalid_workload", "Workload directory escapes its Git worktree")
        inside_git = True
    else:
        boundary = directory
        inside_git = False

    sdkmanrc = find_sdkmanrc(directory, boundary)
    return {
        "directory": str(directory),
        "boundary": str(boundary),
        "inside_git": inside_git,
        "sdkmanrc": str(sdkmanrc) if sdkmanrc else None,
    }


def find_sdkmanrc(directory: Path, boundary: Path) -> Optional[Path]:
    cursor = directory
    while True:
        candidate = cursor / ".sdkmanrc"
        if candidate.is_file():
            return candidate
        if cursor == boundary:
            return None
        if boundary not in cursor.parents:
            return None
        cursor = cursor.parent


def validate_value(value: str, context: str) -> None:
    if not SAFE_VALUE_RE.fullmatch(value):
        raise ContractError("malformed_sdkmanrc", "Unsafe value in %s" % context)


def parse_sdkmanrc(path: Optional[str]) -> List[Tuple[str, str]]:
    if path is None:
        return []
    declarations: List[Tuple[str, str]] = []
    seen = set()
    try:
        lines = Path(path).read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        raise ContractError("malformed_sdkmanrc", "Cannot read .sdkmanrc: %s" % exc)

    for line_number, raw in enumerate(lines, 1):
        normalized = re.sub(r"\s", "", raw.split("#", 1)[0])
        if not normalized:
            continue
        match = re.fullmatch(r"([a-z][a-z0-9]*)=(.+)", normalized)
        if match is None:
            raise ContractError(
                "malformed_sdkmanrc",
                "Invalid candidate declaration at .sdkmanrc line %d" % line_number,
            )
        candidate, version = match.groups()
        validate_value(version, ".sdkmanrc line %d" % line_number)
        if candidate in seen:
            raise ContractError(
                "malformed_sdkmanrc",
                "Duplicate candidate %s in .sdkmanrc" % candidate,
            )
        seen.add(candidate)
        declarations.append((candidate, version))
    return declarations


def requested_exact(value: str) -> dict:
    return {"kind": "exact", "value": value, "vendor_suffix": None}


def requested_prefix(value: str, vendor: Optional[str]) -> dict:
    return {"kind": "version_prefix", "value": value, "vendor_suffix": vendor}


def build_constraints(
    declarations: Sequence[Tuple[str, str]],
    exact: Dict[str, str],
    prefixes: Dict[str, str],
    vendors: Dict[str, str],
    delegations: Dict[str, str],
) -> Tuple[List[dict], List[dict]]:
    explicit = set(exact) | set(prefixes)
    conflicts = set(exact) & (set(prefixes) | set(vendors))
    if conflicts:
        raise ContractError("invalid_input", "Exact and non-exact constraints conflict for %s" % sorted(conflicts)[0])
    if set(vendors) - set(prefixes):
        raise ContractError("invalid_input", "Vendor suffix requires a version prefix")
    if explicit & set(delegations):
        raise ContractError("invalid_input", "Explicit constraints cannot be delegated")
    for owner in delegations.values():
        if owner not in ("wrapper", "toolchain"):
            raise ContractError("invalid_input", "Delegation owner must be wrapper or toolchain")

    constraints: List[dict] = []
    diagnostics: List[dict] = []
    seen = set()
    for candidate, version in declarations:
        seen.add(candidate)
        if candidate in delegations:
            diagnostics.append(
                {
                    "code": "delegated_candidate",
                    "candidate": candidate,
                    "owner": delegations[candidate],
                    "message": "%s is owned by the workload %s" % (candidate, delegations[candidate]),
                }
            )
            continue
        if candidate in exact:
            constraints.append({"candidate": candidate, "source": "explicit", "requested": requested_exact(exact[candidate])})
        elif candidate in prefixes:
            constraints.append(
                {
                    "candidate": candidate,
                    "source": "explicit",
                    "requested": requested_prefix(prefixes[candidate], vendors.get(candidate)),
                }
            )
        else:
            constraints.append({"candidate": candidate, "source": "sdkmanrc", "requested": requested_exact(version)})

    for candidate in sorted(explicit - seen):
        if candidate in exact:
            requested = requested_exact(exact[candidate])
        else:
            requested = requested_prefix(prefixes[candidate], vendors.get(candidate))
        constraints.append({"candidate": candidate, "source": "explicit", "requested": requested})

    return constraints, diagnostics


def is_contained(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


def safe_installed_home(candidate_root: Path, version: str) -> Optional[Path]:
    version_path = candidate_root / version
    if not (version_path.is_dir() or version_path.is_symlink()):
        return None
    try:
        resolved_root = candidate_root.resolve(strict=True)
        resolved = version_path.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise ContractError("unsafe_candidate_path", "Cannot resolve installed candidate %s: %s" % (version, exc))
    if not is_contained(resolved, resolved_root):
        raise ContractError("unsafe_candidate_path", "Installed candidate %s escapes its candidate directory" % version)
    if not resolved.is_dir():
        return None
    return version_path.absolute()


def installed_names(candidate_root: Path) -> List[str]:
    if not candidate_root.is_dir():
        return []
    names = []
    for child in candidate_root.iterdir():
        if child.name == "current" or not SAFE_VALUE_RE.fullmatch(child.name):
            continue
        if child.is_dir() or child.is_symlink():
            names.append(child.name)
    return sorted(names)


def prefix_matches(version: str, prefix: str) -> bool:
    if version == prefix:
        return True
    return version.startswith(prefix) and len(version) > len(prefix) and version[len(prefix)] in PREFIX_BOUNDARIES


def home_variable(candidate: str) -> str:
    return candidate.upper() + "_HOME"


def validated_current(candidate_root: Path) -> Optional[Path]:
    current = candidate_root / "current"
    if not current.exists() and not current.is_symlink():
        return None
    try:
        resolved_root = candidate_root.resolve(strict=True)
        resolved_current = current.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise ContractError("unsafe_current_link", "Cannot resolve candidate current link: %s" % exc)
    if not is_contained(resolved_current, resolved_root):
        raise ContractError("unsafe_current_link", "Candidate current link escapes its candidate directory")
    return resolved_current


def default_match(candidate_root: Path, matches: Sequence[str]) -> Optional[str]:
    resolved_current = validated_current(candidate_root)
    if resolved_current is None:
        return None
    for version in matches:
        home = safe_installed_home(candidate_root, version)
        if home is not None and home.resolve(strict=True) == resolved_current:
            return version
    return None


def environment_match(candidate: str, candidate_root: Path, matches: Sequence[str]) -> Optional[str]:
    value = os.environ.get(home_variable(candidate))
    if not value:
        return None
    try:
        active = Path(value).expanduser().resolve(strict=True)
    except (OSError, RuntimeError):
        return None
    for version in matches:
        home = safe_installed_home(candidate_root, version)
        if home is not None and home.resolve(strict=True) == active:
            return version
    return None


def empty_plan_item(constraint: dict) -> dict:
    return {
        "candidate": constraint["candidate"],
        "source": constraint["source"],
        "requested": constraint["requested"],
        "exact_id": None,
        "candidate_home": None,
        "bin_directory": None,
        "home_variable": home_variable(constraint["candidate"]),
        "resolution": None,
        "activation": None,
    }


def resolved_plan_item(constraint: dict, version: str, home: Path, resolution: str, candidate_root: Path) -> dict:
    item = empty_plan_item(constraint)
    bin_path = home / "bin"
    current = validated_current(candidate_root)
    item.update(
        {
            "exact_id": version,
            "candidate_home": str(home),
            "bin_directory": str(bin_path if bin_path.is_dir() else home),
            "resolution": resolution,
            "activation": "sdk_use" if current is not None else "direct_environment",
        }
    )
    return item


def resolve_constraint(constraint: dict, candidates_dir: Path) -> Tuple[dict, Optional[dict]]:
    candidate = constraint["candidate"]
    requested = constraint["requested"]
    candidate_root = candidates_dir / candidate

    if requested["kind"] == "exact":
        version = requested["value"]
        home = safe_installed_home(candidate_root, version)
        if home is None:
            return empty_plan_item(constraint), {
                "code": "missing_exact_candidate",
                "candidate": candidate,
                "requested": requested,
                "message": "Exact candidate %s=%s is not installed" % (candidate, version),
            }
        return resolved_plan_item(constraint, version, home, "exact", candidate_root), None

    prefix = requested["value"]
    vendor = requested["vendor_suffix"]
    matches = [name for name in installed_names(candidate_root) if prefix_matches(name, prefix)]
    if vendor is not None:
        matches = [name for name in matches if name.endswith("-" + vendor)]
    for version in matches:
        safe_installed_home(candidate_root, version)

    if not matches:
        return empty_plan_item(constraint), {
            "code": "no_installed_match",
            "candidate": candidate,
            "requested": requested,
            "matches": [],
            "message": "No installed candidate matches the requested constraint",
        }

    active = environment_match(candidate, candidate_root, matches)
    if active is not None:
        home = safe_installed_home(candidate_root, active)
        assert home is not None
        return resolved_plan_item(constraint, active, home, "current_match", candidate_root), None

    default = default_match(candidate_root, matches)
    if default is not None:
        home = safe_installed_home(candidate_root, default)
        assert home is not None
        return resolved_plan_item(constraint, default, home, "default_match", candidate_root), None

    if len(matches) == 1:
        home = safe_installed_home(candidate_root, matches[0])
        assert home is not None
        return resolved_plan_item(constraint, matches[0], home, "sole_installed_match", candidate_root), None

    return empty_plan_item(constraint), {
        "code": "ambiguous_candidate",
        "candidate": candidate,
        "requested": requested,
        "matches": matches,
        "message": "Multiple installed candidates match the requested constraint",
    }


def verdict(blockers: Iterable[dict], plan: Sequence[dict]) -> str:
    codes = {blocker["code"] for blocker in blockers}
    if codes & ERROR_CODES:
        return "error"
    if codes & CHOICE_CODES:
        return "choice_required"
    if codes & APPROVAL_CODES:
        return "approval_required"
    if not plan:
        return "no_switch"
    return "ready"


def run(argv: Optional[Sequence[str]] = None) -> int:
    raw_workload: Optional[str] = None
    if argv is None:
        argv = sys.argv[1:]
    for index, token in enumerate(argv):
        if token == "--workload-dir" and index + 1 < len(argv):
            raw_workload = argv[index + 1]
            break
    workload = initial_workload(raw_workload)

    try:
        args = build_parser().parse_args(argv)
        workload = resolve_workload(args.workload_dir)
        exact = parse_assignments(args.exact, "--exact")
        prefixes = parse_assignments(args.version_prefix, "--version-prefix")
        vendors = parse_assignments(args.vendor_suffix, "--vendor-suffix")
        delegations = parse_assignments(args.delegate, "--delegate")
        declarations = parse_sdkmanrc(workload["sdkmanrc"])
        constraints, diagnostics = build_constraints(
            declarations,
            exact,
            prefixes,
            vendors,
            delegations,
        )
        if not constraints:
            return emit("no_switch", workload, [], [], diagnostics)

        sdkman_dir = Path(os.environ.get("SDKMAN_DIR", str(Path.home() / ".sdkman"))).expanduser()
        candidates_dir = sdkman_dir / "candidates"
        if not candidates_dir.is_dir():
            raise ContractError("sdkman_unavailable", "SDKMAN candidates directory is unavailable")

        plan: List[dict] = []
        blockers: List[dict] = []
        for constraint in constraints:
            item, blocker = resolve_constraint(constraint, candidates_dir)
            plan.append(item)
            if blocker is not None:
                blockers.append(blocker)
        status = verdict(blockers, plan)
        return emit(status, workload, plan, blockers, diagnostics)
    except ContractError as exc:
        return error_result(workload, exc)
    except Exception as exc:  # JSON is the inspector's failure boundary.
        return error_result(workload, ContractError("inspection_failed", "Inspection failed: %s" % exc))


if __name__ == "__main__":
    sys.exit(run())
