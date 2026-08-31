#!/usr/bin/env python3
"""Deterministic tests for the bundled SDKMAN inspector."""

from __future__ import annotations

import ast
from contextlib import redirect_stdout
import importlib.util
import io
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
from typing import Dict, Optional, Tuple, Union
import unittest
from unittest import mock


INSPECTOR = Path(__file__).parents[1] / "scripts" / "inspect.py"
sys.dont_write_bytecode = True


def load_inspector_module():
    spec = importlib.util.spec_from_file_location("sdkman_read_only_inspector", INSPECTOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load inspector module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class InspectorFixture:
    def __init__(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.repo = self.root / "repo"
        self.sdkman = self.root / "sdkman"
        self.repo.mkdir()
        (self.sdkman / "candidates").mkdir(parents=True)
        subprocess.run(
            ["git", "init", "--quiet", str(self.repo)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    def close(self) -> None:
        self.tempdir.cleanup()

    def install(self, candidate: str, version: str, *, current: bool = False) -> Path:
        candidate_root = self.sdkman / "candidates" / candidate
        home = candidate_root / version
        (home / "bin").mkdir(parents=True)
        if current:
            (candidate_root / "current").symlink_to(version)
        return home

    def write_sdkmanrc(self, text: str, directory: Optional[Path] = None) -> Path:
        target = (directory or self.repo) / ".sdkmanrc"
        target.write_text(text, encoding="utf-8")
        return target

    def run(
        self, *args: str, workload: Optional[Path] = None
    ) -> Tuple[subprocess.CompletedProcess, dict]:
        environment = os.environ.copy()
        environment["SDKMAN_DIR"] = str(self.sdkman)
        command = [
            "python3",
            str(INSPECTOR),
            "--workload-dir",
            str(workload or self.repo),
            *args,
        ]
        completed = subprocess.run(
            command,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        return completed, json.loads(completed.stdout)

    def snapshot(self) -> Dict[str, Tuple[str, Union[bytes, str]]]:
        snapshot: Dict[str, Tuple[str, Union[bytes, str]]] = {}
        for path in sorted(self.root.rglob("*")):
            relative = str(path.relative_to(self.root))
            if path.is_symlink():
                snapshot[relative] = ("link", os.readlink(path))
            elif path.is_file():
                snapshot[relative] = ("file", path.read_bytes())
            elif path.is_dir():
                snapshot[relative] = ("dir", "")
        return snapshot


class InspectorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = InspectorFixture()

    def tearDown(self) -> None:
        self.fixture.close()

    def test_ready_exact_uses_sdk_use_when_current_exists(self) -> None:
        home = self.fixture.install("java", "21.0.8-tem", current=True)

        completed, result = self.fixture.run("--exact", "java=21.0.8-tem")

        self.assertEqual(0, completed.returncode)
        self.assertEqual("", completed.stderr)
        self.assertEqual(1, result["schema_version"])
        self.assertEqual("ready", result["status"])
        self.assertEqual("21.0.8-tem", result["plan"][0]["exact_id"])
        self.assertEqual(str(home), result["plan"][0]["candidate_home"])
        self.assertEqual("JAVA_HOME", result["plan"][0]["home_variable"])
        self.assertEqual("sdk_use", result["plan"][0]["activation"])

    def test_ready_uses_direct_environment_when_current_is_missing(self) -> None:
        self.fixture.install("gradle", "8.10")

        _, result = self.fixture.run("--exact", "gradle=8.10")

        self.assertEqual("ready", result["status"])
        self.assertEqual("direct_environment", result["plan"][0]["activation"])
        self.assertEqual("GRADLE_HOME", result["plan"][0]["home_variable"])

    def test_choice_required_for_ambiguous_prefix(self) -> None:
        self.fixture.install("java", "25-tem")
        self.fixture.install("java", "25-graalce")

        completed, result = self.fixture.run("--version-prefix", "java=25")

        self.assertEqual(2, completed.returncode)
        self.assertEqual("choice_required", result["status"])
        self.assertEqual(
            ["25-graalce", "25-tem"],
            result["blockers"][0]["matches"],
        )

    def test_choice_required_when_no_installed_candidate_matches(self) -> None:
        completed, result = self.fixture.run("--version-prefix", "java=26")

        self.assertEqual(2, completed.returncode)
        self.assertEqual("choice_required", result["status"])
        self.assertEqual("no_installed_match", result["blockers"][0]["code"])

    def test_default_link_resolves_an_ambiguous_prefix(self) -> None:
        self.fixture.install("java", "25-tem", current=True)
        self.fixture.install("java", "25-graalce")

        _, result = self.fixture.run("--version-prefix", "java=25")

        self.assertEqual("ready", result["status"])
        self.assertEqual("25-tem", result["plan"][0]["exact_id"])
        self.assertEqual("default_match", result["plan"][0]["resolution"])

    def test_active_candidate_home_resolves_before_default(self) -> None:
        active = self.fixture.install("java", "25-graalce")
        self.fixture.install("java", "25-tem", current=True)

        with mock.patch.dict(os.environ, {"JAVA_HOME": str(active)}):
            _, result = self.fixture.run("--version-prefix", "java=25")

        self.assertEqual("ready", result["status"])
        self.assertEqual("25-graalce", result["plan"][0]["exact_id"])
        self.assertEqual("current_match", result["plan"][0]["resolution"])

    def test_vendor_suffix_narrows_without_rewriting_identity(self) -> None:
        self.fixture.install("java", "25-tem")
        self.fixture.install("java", "25-graalce")

        _, result = self.fixture.run(
            "--version-prefix",
            "java=25",
            "--vendor-suffix",
            "java=graalce",
        )

        self.assertEqual("ready", result["status"])
        self.assertEqual("25-graalce", result["plan"][0]["exact_id"])
        self.assertEqual("graalce", result["plan"][0]["requested"]["vendor_suffix"])

    def test_approval_required_for_missing_exact_candidate(self) -> None:
        completed, result = self.fixture.run("--exact", "java=21.0.8-tem")

        self.assertEqual(2, completed.returncode)
        self.assertEqual("approval_required", result["status"])
        self.assertEqual("missing_exact_candidate", result["blockers"][0]["code"])
        self.assertIsNone(result["plan"][0]["candidate_home"])

    def test_no_switch_skips_sdkman_when_workload_owner_is_delegated(self) -> None:
        self.fixture.write_sdkmanrc("java=21.0.8-tem\n")

        completed, result = self.fixture.run("--delegate", "java=toolchain")

        self.assertEqual(0, completed.returncode)
        self.assertEqual("no_switch", result["status"])
        self.assertEqual([], result["plan"])
        self.assertEqual("delegated_candidate", result["diagnostics"][0]["code"])

    def test_error_for_malformed_sdkmanrc(self) -> None:
        self.fixture.write_sdkmanrc("export JAVA_HOME=/tmp/java\n")

        completed, result = self.fixture.run()

        self.assertEqual(1, completed.returncode)
        self.assertEqual("error", result["status"])
        self.assertEqual("malformed_sdkmanrc", result["blockers"][0]["code"])

    def test_error_for_duplicate_sdkmanrc_candidate(self) -> None:
        self.fixture.write_sdkmanrc("java=21-tem\njava=25-tem\n")

        _, result = self.fixture.run()

        self.assertEqual("error", result["status"])
        self.assertEqual("malformed_sdkmanrc", result["blockers"][0]["code"])

    def test_explicit_override_preserves_other_declarations(self) -> None:
        self.fixture.write_sdkmanrc("java=17.0.12-tem\nmaven=3.9.9\n")
        self.fixture.install("java", "21.0.8-tem", current=True)
        self.fixture.install("maven", "3.9.9", current=True)

        _, result = self.fixture.run("--exact", "java=21.0.8-tem")

        self.assertEqual("ready", result["status"])
        self.assertEqual(["java", "maven"], [item["candidate"] for item in result["plan"]])
        self.assertEqual("explicit", result["plan"][0]["source"])
        self.assertEqual("sdkmanrc", result["plan"][1]["source"])

    def test_all_or_nothing_plan_reports_every_candidate(self) -> None:
        self.fixture.write_sdkmanrc("java=21.0.8-tem\nmaven=3.9.9\n")
        self.fixture.install("java", "21.0.8-tem", current=True)

        _, result = self.fixture.run()

        self.assertEqual("approval_required", result["status"])
        self.assertEqual(["java", "maven"], [item["candidate"] for item in result["plan"]])
        self.assertEqual("21.0.8-tem", result["plan"][0]["exact_id"])
        self.assertIsNone(result["plan"][1]["exact_id"])

    def test_nested_repository_does_not_read_parent_sdkmanrc(self) -> None:
        self.fixture.write_sdkmanrc("java=21.0.8-tem\n")
        nested = self.fixture.repo / "isolated"
        nested.mkdir()
        subprocess.run(
            ["git", "init", "--quiet", str(nested)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        _, result = self.fixture.run(workload=nested)

        self.assertEqual("no_switch", result["status"])
        self.assertEqual(str(nested.resolve()), result["workload"]["boundary"])
        self.assertIsNone(result["workload"]["sdkmanrc"])

    def test_linked_worktree_does_not_read_originating_checkout_sdkmanrc(self) -> None:
        tracked = self.fixture.repo / "tracked.txt"
        tracked.write_text("fixture\n", encoding="utf-8")
        subprocess.run(
            ["git", "-C", str(self.fixture.repo), "add", "tracked.txt"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(self.fixture.repo),
                "-c",
                "user.name=SDKMAN Inspector Tests",
                "-c",
                "user.email=sdkman-inspector@example.invalid",
                "commit",
                "--quiet",
                "-m",
                "fixture",
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        self.fixture.write_sdkmanrc("java=21.0.8-tem\n")
        linked = self.fixture.root / "linked-worktree"
        subprocess.run(
            [
                "git",
                "-C",
                str(self.fixture.repo),
                "worktree",
                "add",
                "--quiet",
                "--detach",
                str(linked),
                "HEAD",
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        _, result = self.fixture.run(workload=linked)

        self.assertEqual("no_switch", result["status"])
        self.assertEqual(str(linked.resolve()), result["workload"]["boundary"])
        self.assertIsNone(result["workload"]["sdkmanrc"])

    def test_invalid_workload_is_json_error(self) -> None:
        completed, result = self.fixture.run(workload=self.fixture.root / "missing")

        self.assertEqual(1, completed.returncode)
        self.assertEqual("invalid_workload", result["blockers"][0]["code"])

    def test_invalid_constraint_is_json_error(self) -> None:
        completed, result = self.fixture.run("--exact", "java=../../escape")

        self.assertEqual(1, completed.returncode)
        self.assertEqual("error", result["status"])
        self.assertEqual("invalid_input", result["blockers"][0]["code"])
        self.assertEqual("", completed.stderr)

    def test_conflicting_constraints_are_invalid_input(self) -> None:
        _, result = self.fixture.run(
            "--exact",
            "java=21.0.8-tem",
            "--version-prefix",
            "java=21",
        )

        self.assertEqual("error", result["status"])
        self.assertEqual("invalid_input", result["blockers"][0]["code"])

    def test_sdkman_unavailable_is_error_only_when_a_plan_exists(self) -> None:
        (self.fixture.sdkman / "candidates").rmdir()

        _, result = self.fixture.run("--exact", "java=21.0.8-tem")

        self.assertEqual("error", result["status"])
        self.assertEqual("sdkman_unavailable", result["blockers"][0]["code"])

    def test_candidate_symlink_may_not_escape_candidate_directory(self) -> None:
        outside = self.fixture.root / "outside-java"
        outside.mkdir()
        candidate_root = self.fixture.sdkman / "candidates" / "java"
        candidate_root.mkdir()
        (candidate_root / "21-local").symlink_to(outside, target_is_directory=True)

        _, result = self.fixture.run("--exact", "java=21-local")

        self.assertEqual("error", result["status"])
        self.assertEqual("unsafe_candidate_path", result["blockers"][0]["code"])

    def test_current_link_may_not_escape_candidate_directory(self) -> None:
        self.fixture.install("java", "25-tem")
        self.fixture.install("java", "25-graalce")
        outside = self.fixture.root / "outside-current"
        outside.mkdir()
        current = self.fixture.sdkman / "candidates" / "java" / "current"
        current.symlink_to(outside, target_is_directory=True)

        _, result = self.fixture.run("--version-prefix", "java=25")

        self.assertEqual("error", result["status"])
        self.assertEqual("unsafe_current_link", result["blockers"][0]["code"])

    def test_unrelated_candidates_are_not_enumerated(self) -> None:
        self.fixture.install("java", "21-tem", current=True)
        outside = self.fixture.root / "outside-maven"
        outside.mkdir()
        maven_root = self.fixture.sdkman / "candidates" / "maven"
        maven_root.mkdir()
        (maven_root / "3.9-local").symlink_to(outside, target_is_directory=True)

        _, result = self.fixture.run("--exact", "java=21-tem")

        self.assertEqual("ready", result["status"])
        self.assertEqual(["java"], [item["candidate"] for item in result["plan"]])

    def test_git_unavailable_has_a_stable_error_code(self) -> None:
        module = load_inspector_module()

        with mock.patch.object(module.subprocess, "run", side_effect=FileNotFoundError):
            with self.assertRaises(module.ContractError) as raised:
                module.resolve_workload(str(self.fixture.repo))

        self.assertEqual("git_unavailable", raised.exception.code)

    def test_unexpected_failure_still_returns_versioned_json(self) -> None:
        module = load_inspector_module()
        output = io.StringIO()

        with mock.patch.object(module, "resolve_workload", side_effect=RuntimeError("boom")):
            with redirect_stdout(output):
                exit_code = module.run(["--workload-dir", str(self.fixture.repo)])

        result = json.loads(output.getvalue())
        self.assertEqual(1, exit_code)
        self.assertEqual(1, result["schema_version"])
        self.assertEqual("inspection_failed", result["blockers"][0]["code"])

    def test_inspection_is_deterministic_and_read_only(self) -> None:
        self.fixture.write_sdkmanrc("java=21.0.8-tem\n")
        self.fixture.install("java", "21.0.8-tem", current=True)
        before = self.fixture.snapshot()

        first, first_result = self.fixture.run()
        second, second_result = self.fixture.run()

        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(first_result, second_result)
        self.assertEqual(before, self.fixture.snapshot())

    def test_inspection_uses_no_network_api_or_external_command_except_git(self) -> None:
        self.fixture.write_sdkmanrc("java=21.0.8-tem\n")
        self.fixture.install("java", "21.0.8-tem", current=True)
        module = load_inspector_module()
        output = io.StringIO()

        with mock.patch.dict(
            os.environ,
            {"SDKMAN_DIR": str(self.fixture.sdkman)},
            clear=False,
        ):
            with mock.patch.object(
                socket,
                "socket",
                side_effect=AssertionError("network access is forbidden"),
            ):
                with redirect_stdout(output):
                    exit_code = module.run(
                        ["--workload-dir", str(self.fixture.repo)]
                    )

        self.assertEqual(0, exit_code)
        self.assertEqual("ready", json.loads(output.getvalue())["status"])

        tree = ast.parse(INSPECTOR.read_text(encoding="utf-8"))
        imported = set()
        external_commands = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".", 1)[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".", 1)[0])
            elif (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "subprocess"
            ):
                self.assertEqual("run", node.func.attr)
                self.assertTrue(node.args)
                command = node.args[0]
                self.assertIsInstance(command, (ast.List, ast.Tuple))
                self.assertTrue(command.elts)
                executable = command.elts[0]
                self.assertIsInstance(executable, ast.Constant)
                external_commands.append(executable.value)
        self.assertTrue({"socket", "urllib", "http", "requests"}.isdisjoint(imported))
        self.assertEqual(["git"], external_commands)


if __name__ == "__main__":
    unittest.main()
