"""Exercise preference updates against temporary user homes, never real settings."""

from decimal import Decimal
import importlib.util
import json
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "config.py"
SPEC = importlib.util.spec_from_file_location("ask_owners_config", SCRIPT)
config = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(config)


class PreferenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "preferences"
        self.path = self.root / "ask-owners" / "config.json"

    def write(self, text):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(text, encoding="utf-8")

    def test_absent_read_and_clear_create_nothing(self):
        for operation in ("read", "clear"):
            result = config.operate(self.root, operation)
            self.assertIsNone(result["current"])
            self.assertFalse(result["changed"])
            self.assertFalse(self.root.exists())

    def test_save_records_exact_selector_and_consent(self):
        selector = "/path with spaces/$(not-a-command)/SKILL.md"
        result = config.operate(self.root, "save", selector)
        self.assertIsNone(result["previous"])
        self.assertEqual(selector, result["current"])
        self.assertEqual({"selector": selector, "consent": "discussion-v1"},
                         json.loads(self.path.read_text())["contentSkill"])
        self.assertEqual(selector, config.operate(self.root, "read")["current"])

    def test_updates_preserve_unrelated_data_and_numeric_precision(self):
        self.write('{"unrelated":{"precise":0.12345678901234567890123456789,'
                   '"large":1e400,"tags":["甲",false,null]}}')
        original = json.loads(self.path.read_text(), parse_float=Decimal)["unrelated"]
        config.operate(self.root, "save", "skills:grill-minimal")
        result = config.operate(self.root, "save", "mattpocock:grill-with-docs")
        self.assertEqual("skills:grill-minimal", result["previous"])
        self.assertEqual(original, json.loads(self.path.read_text(),
                                             parse_float=Decimal)["unrelated"])
        config.operate(self.root, "clear")
        self.assertEqual({"unrelated": original}, json.loads(self.path.read_text(),
                                                            parse_float=Decimal))

    def test_same_choice_and_repeated_clear_are_noops(self):
        config.operate(self.root, "save", "grill-me")
        original = self.path.read_bytes()
        with mock.patch.object(config, "atomic_write") as writer:
            self.assertFalse(config.operate(self.root, "save", "grill-me")["changed"])
            writer.assert_not_called()
        self.assertEqual(original, self.path.read_bytes())
        self.assertTrue(config.operate(self.root, "clear")["changed"])
        after_clear = self.path.read_bytes()
        self.assertFalse(config.operate(self.root, "clear")["changed"])
        self.assertEqual(after_clear, self.path.read_bytes())

    def test_invalid_existing_data_blocks_every_operation_without_mutation(self):
        invalid = [
            "{", "[]", "null", '{"x":1,"x":2}', '{"x":NaN}',
            '{"contentSkill":"grill-me"}', '{"contentSkill":null}',
            '{"contentSkill":{"selector":"grill-me","consent":"future-v2"}}',
            '{"contentSkill":{"selector":" ","consent":"discussion-v1"}}',
            '{"contentSkill":{"selector":3,"consent":"discussion-v1"}}',
        ]
        for text in invalid:
            for operation in ("read", "save", "clear"):
                with self.subTest(text=text, operation=operation):
                    self.write(text)
                    before = self.path.read_bytes()
                    with self.assertRaises(ValueError):
                        config.operate(self.root, operation, "grill-me")
                    self.assertEqual(before, self.path.read_bytes())
                    self.assertEqual([self.path], list(self.path.parent.iterdir()))

    def test_invalid_selector_never_creates_config(self):
        for selector in (None, "", "  ", 1):
            with self.subTest(selector=selector), self.assertRaises(ValueError):
                config.operate(self.root, "save", selector)
        self.assertFalse(self.root.exists())

    def test_save_preserves_symlink_and_target_permissions(self):
        target = Path(self.temp.name) / "actual.json"
        target.write_text('{"other":true}', encoding="utf-8")
        target.chmod(0o640)
        self.path.parent.mkdir(parents=True)
        self.path.symlink_to(target)
        config.operate(self.root, "save", "grill-me")
        self.assertTrue(self.path.is_symlink())
        self.assertEqual(target.resolve(), self.path.resolve())
        self.assertEqual(0o640, stat.S_IMODE(target.stat().st_mode))
        self.assertTrue(json.loads(target.read_text())["other"])

    def test_failed_replace_retains_previous_file_and_cleans_temp(self):
        config.operate(self.root, "save", "grill-me")
        before = self.path.read_bytes()
        with mock.patch.object(config.os, "replace", side_effect=OSError("blocked")):
            with self.assertRaises(OSError):
                config.operate(self.root, "save", "grill-with-docs")
        self.assertEqual(before, self.path.read_bytes())
        self.assertEqual([self.path], list(self.path.parent.iterdir()))

    def test_invalid_explicit_root_has_no_fallback(self):
        self.root.write_text("not a directory", encoding="utf-8")
        with self.assertRaises(OSError):
            config.operate(self.root, "save", "grill-me")
        self.assertEqual("not a directory", self.root.read_text())

    def test_cli_returns_only_preference_fields(self):
        self.write('{"private":"DO-NOT-PRINT"}')
        selector = "plugin:grill with spaces"
        result = subprocess.run([sys.executable, "-B", str(SCRIPT), "--config-root",
                                 str(self.root), "save", "--selector", selector],
                                capture_output=True, text=True, check=True)
        self.assertNotIn("DO-NOT-PRINT", result.stdout + result.stderr)
        self.assertEqual(selector, json.loads(result.stdout)["current"])
        self.write('{"contentSkill":"legacy-without-consent"}')
        failed = subprocess.run([sys.executable, "-B", str(SCRIPT), "--config-root",
                                 str(self.root), "read"], capture_output=True, text=True)
        self.assertEqual(1, failed.returncode)
        self.assertEqual("", failed.stdout)
        self.assertIn("error", json.loads(failed.stderr))


if __name__ == "__main__":
    unittest.main()
