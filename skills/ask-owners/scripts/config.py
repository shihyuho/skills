#!/usr/bin/env python3
"""Read, save or clear ask-owners' discussion skill preference (Python 3.8+)."""

import argparse
from decimal import Decimal
import json
import os
from pathlib import Path
import stat
import sys
import tempfile


KEY = "contentSkill"
CONSENT = "discussion-v1"


def unique_members(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON object member")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError("non-JSON numeric constant: " + value)


def validate_selector(selector):
    if not isinstance(selector, str) or not selector.strip():
        raise ValueError("selector must be a non-blank string")


def read_config(path):
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {}
    data = json.loads(raw, object_pairs_hook=unique_members,
                      parse_float=Decimal, parse_constant=reject_constant)
    if not isinstance(data, dict):
        raise ValueError("config must be a JSON object")
    if KEY in data:
        choice = data[KEY]
        if not isinstance(choice, dict) or choice.get("consent") != CONSENT:
            raise ValueError("contentSkill needs supported discussion delegation consent")
        validate_selector(choice.get("selector"))
    return data


def encode(value):
    # Keep unknown numeric values exact instead of rounding them through floats.
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, dict):
        return "{" + ", ".join(json.dumps(k) + ": " + encode(v)
                                for k, v in value.items()) + "}"
    if isinstance(value, list):
        return "[" + ", ".join(encode(v) for v in value) + "]"
    return json.dumps(value, ensure_ascii=True, allow_nan=False)


def atomic_write(path, data):
    destination = path.resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    mode = stat.S_IMODE(destination.stat().st_mode) if destination.exists() else None
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n",
                                         dir=str(destination.parent),
                                         prefix=".ask-owners-", suffix=".tmp",
                                         delete=False) as output:
            temporary = Path(output.name)
            output.write(encode(data) + "\n")
            output.flush()
            os.fsync(output.fileno())
        if mode is not None:
            os.chmod(str(temporary), mode)
        os.replace(str(temporary), str(destination))
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink()


def operate(root, operation, selector=None):
    if operation not in ("read", "save", "clear"):
        raise ValueError("unknown config operation")
    if operation == "save":
        validate_selector(selector)
    path = root.expanduser().absolute() / "ask-owners" / "config.json"
    data = read_config(path)
    before = data.get(KEY)
    previous = before["selector"] if before is not None else None
    if operation == "clear":
        data.pop(KEY, None)
    elif operation == "save":
        data[KEY] = dict(before or {}, selector=selector, consent=CONSENT)
    after = data.get(KEY)
    current = after["selector"] if after is not None else None
    changed = before != after
    if changed:
        atomic_write(path, data)
    return {"operation": operation, "path": str(path), "previous": previous,
            "current": current, "changed": changed}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config-root", type=Path,
                        default=Path.home() / ".config" / "softleader" / "agent-skills",
                        help="config root explicitly selected by user-level instructions")
    commands = parser.add_subparsers(dest="operation", required=True)
    commands.add_parser("read", help="validate and read without creating files")
    commands.add_parser("clear", help="remove only the content skill preference")
    save = commands.add_parser("save", help="remember the loaded skill and delegation consent")
    save.add_argument("--selector", required=True)
    args = parser.parse_args(argv)
    try:
        result = operate(args.config_root, args.operation, getattr(args, "selector", None))
    except (OSError, ValueError, RuntimeError) as error:
        path = args.config_root.expanduser().absolute() / "ask-owners" / "config.json"
        print(json.dumps({"path": str(path), "error": str(error)}), file=sys.stderr)
        return 1
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
