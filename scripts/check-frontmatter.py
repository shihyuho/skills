#!/usr/bin/env python3
"""Validate YAML frontmatter across the repo.

Catches the failure mode where a plain (unquoted) scalar value contains a
`: ` (colon + space), which YAML reads as a mapping indicator and rejects with
"mapping values are not allowed in this context" — the same error Claude Code's
skill loader surfaces.

Also enforces the AGENTS.md rule that every SKILL.md frontmatter carries
`name`, `description`, and `license`, plus the value limits from the Agent
Skills spec (https://agentskills.io/specification) that the spec marks as hard
requirements: `name` format and directory match, `description` length, and
`compatibility` length.

Field names are deliberately not whitelisted: Claude Code documents extension
fields (`argument-hint`, `when_to_use`, `model`, …) that the spec's own field
list does not carry, and this repo wants them available.

Exit code is non-zero if any file fails, so it doubles as a CI / pre-commit gate.
"""

import glob
import os
import sys
import unicodedata

import yaml

SKILL_REQUIRED = ("name", "description", "license")

# Hard limits from the Agent Skills spec.
NAME_MAX = 64
DESCRIPTION_MAX = 1024
COMPATIBILITY_MAX = 500


def validate_spec_values(data, path):
    """Check the spec's value constraints on a skill's frontmatter.

    Only validates values that are present; presence of the required keys is
    the caller's job.
    """
    errors = []
    directory = os.path.basename(os.path.dirname(path))

    name = data.get("name")
    if "name" in data:
        if not isinstance(name, str) or not name.strip():
            errors.append(f"{path}: 'name' must be a non-empty string")
        else:
            normalized = unicodedata.normalize("NFKC", name.strip())
            if len(normalized) > NAME_MAX:
                errors.append(
                    f"{path}: 'name' exceeds {NAME_MAX} characters "
                    f"({len(normalized)} chars)"
                )
            if normalized != normalized.lower():
                errors.append(f"{path}: 'name' must be lowercase (got {name!r})")
            if normalized.startswith("-") or normalized.endswith("-"):
                errors.append(f"{path}: 'name' must not start or end with a hyphen")
            if "--" in normalized:
                errors.append(f"{path}: 'name' must not contain consecutive hyphens")
            if any(not (ch.isalnum() or ch == "-") for ch in normalized):
                errors.append(
                    f"{path}: 'name' may only contain letters, digits, and hyphens "
                    f"(got {name!r})"
                )
            if normalized != unicodedata.normalize("NFKC", directory):
                errors.append(
                    f"{path}: 'name' {name!r} does not match its directory name "
                    f"{directory!r}"
                )

    description = data.get("description")
    if "description" in data:
        if not isinstance(description, str) or not description.strip():
            errors.append(f"{path}: 'description' must be a non-empty string")
        elif len(description) > DESCRIPTION_MAX:
            errors.append(
                f"{path}: 'description' exceeds {DESCRIPTION_MAX} characters "
                f"({len(description)} chars)"
            )

    compatibility = data.get("compatibility")
    if "compatibility" in data:
        if not isinstance(compatibility, str):
            errors.append(f"{path}: 'compatibility' must be a string")
        elif len(compatibility) > COMPATIBILITY_MAX:
            errors.append(
                f"{path}: 'compatibility' exceeds {COMPATIBILITY_MAX} characters "
                f"({len(compatibility)} chars)"
            )

    return errors


def split_frontmatter(text):
    """Return the YAML frontmatter block, or None if the file has none."""
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    return parts[1]


def main():
    errors = []
    targets = sorted(glob.glob("skills/*/SKILL.md") + glob.glob("commands/*.md"))

    for path in targets:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()

        fm = split_frontmatter(text)
        if fm is None:
            errors.append(f"{path}: missing YAML frontmatter (--- block)")
            continue

        try:
            data = yaml.safe_load(fm)
        except yaml.YAMLError as exc:
            first = str(exc).splitlines()[0]
            errors.append(f"{path}: invalid YAML — {first}")
            continue

        if not isinstance(data, dict):
            errors.append(f"{path}: frontmatter is not a mapping")
            continue

        if path.startswith("skills/"):
            missing = [k for k in SKILL_REQUIRED if k not in data]
            if missing:
                errors.append(f"{path}: missing required key(s): {', '.join(missing)}")
            errors.extend(validate_spec_values(data, path))

    if errors:
        print(f"Frontmatter check failed ({len(errors)} issue(s)):\n", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"Frontmatter OK — {len(targets)} file(s) validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
