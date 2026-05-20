#!/usr/bin/env python3
"""SDKMAN PostToolUse hook — reactive catch-all.

Fires after every Bash tool call and scans the command output for Java
version-mismatch error signatures. Because it keys off the *error* rather than
the command, it covers builds invoked through any wrapper — make, just, npm
scripts, custom shell scripts, Docker — not just direct mvn/gradle. When a
signature is found it injects guidance to switch the JDK via SDKMAN and retry.

It stays silent unless a real version error appears, so compliant builds pass
with zero model overhead. Any unexpected error → exit 0.

Installation: see references/setup.md.
"""

import json
import os
import re
import sys

# (signature regex, "compiled-for too new for current runtime"?) — when True we
# can derive the required JDK from a class-file major version (major - 44).
SIGNATURES = [
    re.compile(r"UnsupportedClassVersionError", re.IGNORECASE),
    re.compile(r"compiled by a more recent version of the Java", re.IGNORECASE),
    re.compile(r"Unsupported class file major version", re.IGNORECASE),
    re.compile(r"invalid target release", re.IGNORECASE),
    re.compile(r"release version \d+ not supported", re.IGNORECASE),
    re.compile(r"(Source|Target) option \d+ is no longer supported", re.IGNORECASE),
    re.compile(r"requires a Java \d+ toolchain", re.IGNORECASE),
    re.compile(r"Could not (?:find|target).{0,40}Java", re.IGNORECASE),
]


def sdkman_present() -> bool:
    sdkman_dir = os.environ.get("SDKMAN_DIR") or os.path.join(
        os.path.expanduser("~"), ".sdkman"
    )
    return os.path.isfile(os.path.join(sdkman_dir, "bin", "sdkman-init.sh"))


def output_text(payload: dict) -> str:
    resp = payload.get("tool_response")
    if isinstance(resp, str):
        return resp
    if isinstance(resp, dict):
        parts = [resp.get("stdout", ""), resp.get("stderr", "")]
        if isinstance(resp.get("content"), str):
            parts.append(resp["content"])
        return "\n".join(p for p in parts if p)
    return ""


def required_jdk(text: str):
    """Best-effort: derive the JDK the build needs from the error text."""
    m = re.search(r"class file (?:major )?version[: ]+(\d+)", text, re.IGNORECASE)
    if m:  # class-file major 52==8 ... 65==21
        return int(m.group(1)) - 44
    for pat in (
        r"invalid target release:\s*([\d.]+)",
        r"release version (\d+) not supported",
        r"requires a Java (\d+) toolchain",
        r"(?:Source|Target) option (\d+) is no longer supported",
    ):
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            v = m.group(1)
            return int(v.split(".")[-1]) if "." in v else int(v)
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    if payload.get("tool_name") != "Bash" or not sdkman_present():
        return 0

    text = output_text(payload)
    if not text or not any(sig.search(text) for sig in SIGNATURES):
        return 0

    want = required_jdk(text)
    target = (
        f"Java {want}" if want and 6 <= want <= 30 else "the JDK this project targets"
    )
    context = (
        f"A build just failed with a Java version mismatch. The active JDK does not "
        f"match {target}. Use the sdkman skill to switch the shell to {target} "
        f"(`sdk use java <jdk-id>`; list installed ids with "
        f'`ls "${{SDKMAN_DIR:-$HOME/.sdkman}}/candidates/java/"`), then re-run the same '
        f"build command. If {target} is not installed, stop and ask the user before "
        f"running `sdk install`."
    )
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": context,
            }
        },
        sys.stdout,
    )
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
