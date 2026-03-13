#!/usr/bin/env python3
"""Check whether a thin-card capture response follows the rewrite-first rule."""

from __future__ import annotations

import re
import sys
from pathlib import Path


THIN_PATTERNS = [
    r"too thin",
    r"太薄",
    r"not yet self-contained",
    r"不夠自足",
    r"不夠完整",
]

REWRITE_PATTERNS = [
    r"decision=rewrite-first",
    r"rewrite the card",
    r"rewrite-first",
    r"先重寫",
    r"重寫",
]

FINAL_DECISION_PATTERNS = [
    r"decision=create",
    r"decision=update",
]


def has_any_pattern(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: check_ultrabrain_thin_card.py <response-file>", file=sys.stderr)
        return 2

    response_path = Path(sys.argv[1])
    if not response_path.exists():
        print(f"Missing response file: {response_path}", file=sys.stderr)
        return 2

    text = response_path.read_text(encoding="utf-8")

    has_thin = has_any_pattern(text, THIN_PATTERNS)
    has_rewrite = has_any_pattern(text, REWRITE_PATTERNS)
    has_final_decision = has_any_pattern(text, FINAL_DECISION_PATTERNS)

    if has_final_decision:
        print(
            "FAIL: response jumped to decision=create/update instead of stopping at rewrite-first",
            file=sys.stderr,
        )
        return 1

    if has_thin and has_rewrite:
        print("PASS: response identifies a thin card and requires rewrite-first handling")
        return 0

    print(
        "FAIL: response did not provide machine-detectable thin-card rewrite-first signals",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
