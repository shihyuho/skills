#!/usr/bin/env python3
"""Resolve harvest context_id from environment or timestamp.

No third-party dependencies required.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import uuid


PATTERNS = [
    re.compile(r"SESSION.*ID", re.IGNORECASE),
    re.compile(r"CONVERSATION.*ID", re.IGNORECASE),
    re.compile(r"THREAD.*ID", re.IGNORECASE),
]

PRIORITY_KEYS = [
    "OPENCODE_SESSION_ID",
    "OPENCODE_CONVERSATION_ID",
    "OPENCODE_THREAD_ID",
    "SESSION_ID",
    "CONVERSATION_ID",
    "THREAD_ID",
]


def find_context_env() -> tuple[str | None, str | None]:
    for key in PRIORITY_KEYS:
        value = os.environ.get(key, "").strip()
        if value:
            return key, value

    for key in sorted(os.environ.keys()):
        value = os.environ.get(key, "").strip()
        if not value:
            continue
        if any(pattern.search(key) for pattern in PATTERNS):
            return key, value
    return None, None


def infer_latest_opencode_session_id() -> str | None:
    try:
        proc = subprocess.run(
            ["opencode", "session", "list", "--format", "json", "-n", "1"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.SubprocessError):
        return None

    payload = proc.stdout.strip()
    if not payload:
        return None

    try:
        sessions = json.loads(payload)
    except json.JSONDecodeError:
        return None

    if not isinstance(sessions, list) or not sessions:
        return None

    first = sessions[0]
    if not isinstance(first, dict):
        return None

    session_id = str(first.get("id", "")).strip()
    if session_id.startswith("ses_"):
        return session_id

    return None


def generate_stateless_context_id() -> str:
    timestamp = dt.datetime.now().strftime("%Y%m%d%H%M%S")
    suffix = uuid.uuid4().hex[:6]
    return f"ctx-{timestamp}-{suffix}"


def resolve_context_id(infer_latest_session: bool) -> dict[str, str | None]:
    matched_key, matched_value = find_context_env()
    if matched_key and matched_value:
        return {
            "context_id": matched_value,
            "source": "env",
            "matched_env_key": matched_key,
        }

    if infer_latest_session:
        inferred = infer_latest_opencode_session_id()
        if inferred:
            return {
                "context_id": inferred,
                "source": "opencode_session_list",
                "matched_env_key": None,
            }

    return {
        "context_id": generate_stateless_context_id(),
        "source": "generated",
        "matched_env_key": None,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Resolve harvest context_id from env var or timestamp"
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--infer-latest-session",
        action="store_true",
        help="Best-effort infer context_id from `opencode session list --format json -n 1` when env keys are unavailable",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = resolve_context_id(infer_latest_session=args.infer_latest_session)

    if args.format == "json":
        sys.stdout.write(json.dumps(result, ensure_ascii=True) + "\n")
        return 0

    sys.stdout.write(f"{result['context_id']}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
