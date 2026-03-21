"""Tests for thin-card rewrite-first helper checks."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


SCRIPT_PATH = Path(__file__).with_name("check_ultrabrain_thin_card.py")


def run_checker(content: str) -> subprocess.CompletedProcess[str]:
    with TemporaryDirectory() as temp_dir:
        response_path = Path(temp_dir) / "response.txt"
        response_path.write_text(content, encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(SCRIPT_PATH), str(response_path)],
            capture_output=True,
            text=True,
            check=False,
        )


class ThinCardCheckerTests(unittest.TestCase):
    def test_passes_for_rewrite_first_thin_card_response(self) -> None:
        result = run_checker(
            """decision=rewrite-first

Why the card is too thin:
- missing trigger and reasoning

Rewrite target:
- Rule: write the smoke test first
- Trigger: when the integration path is still expanding
- Why: the narrow test keeps the scope understandable
"""
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("PASS:", result.stdout)

    def test_fails_when_response_jumps_to_create(self) -> None:
        result = run_checker(
            """decision=create

This card is too thin but let's create it anyway.
"""
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("decision=create/update", result.stderr)

    def test_fails_when_response_includes_finished_card_signals(self) -> None:
        result = run_checker(
            """decision=rewrite-first

Why the card is too thin:
- missing trigger and reasoning

Suggested filename: write-the-smoke-test-first.md

Frontmatter:
- title: Write the smoke test first

Add to testing-moc.
Create a source note for the Slack thread.
"""
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("finished-output signals", result.stderr)


if __name__ == "__main__":
    unittest.main()
