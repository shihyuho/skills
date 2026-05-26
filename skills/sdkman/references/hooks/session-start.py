#!/usr/bin/env python3
"""SDKMAN SessionStart hook — advisory preference nudge.

Fires once at session start. When the machine has SDKMAN *and* the working
directory looks like a JVM project, it injects a one-line reminder that `sdk`
is the preferred way to change the Java/Gradle/Maven/Kotlin version, and that
versions declared by the project are defaults — an explicit version the user
asks for wins. It never enforces anything; it only surfaces the preference so
the model doesn't reach for `JAVA_HOME` edits or jenv/asdf instead.

Silent when SDKMAN is absent or the directory isn't a JVM project. Any
unexpected error → exit 0.

Installation: see references/setup.md.
"""

import json
import os
import sys

PROJECT_MARKERS = (
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "settings.gradle",
    "settings.gradle.kts",
    ".sdkmanrc",
    "gradlew",
    "mvnw",
)

REMINDER = (
    "This machine has SDKMAN and the working directory is a JVM project. "
    "Prefer `sdk` (e.g. `sdk use java <id>`) for any Java/Gradle/Maven/Kotlin "
    "version change rather than editing JAVA_HOME or using jenv/asdf. Treat "
    "versions declared in pom.xml, build.gradle, or .sdkmanrc as defaults — if "
    "the user asks to build or test under a specific version, honor that over "
    "the project default. See the sdkman skill for the switching patterns."
)


def sdkman_present() -> bool:
    sdkman_dir = os.environ.get("SDKMAN_DIR") or os.path.join(
        os.path.expanduser("~"), ".sdkman"
    )
    return os.path.isfile(os.path.join(sdkman_dir, "bin", "sdkman-init.sh"))


def is_jvm_project(cwd: str) -> bool:
    return any(os.path.exists(os.path.join(cwd, marker)) for marker in PROJECT_MARKERS)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        payload = {}

    cwd = payload.get("cwd") or os.getcwd()
    if not sdkman_present() or not is_jvm_project(cwd):
        return 0

    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": REMINDER,
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
