#!/usr/bin/env python3
"""Validate skills under skills/<category>/ against the Agent Skills specification.

Skills live two levels deep: skills/<category>/<skill-name>/SKILL.md.

Checks the mandatory rules from https://agentskills.io/specification:

- every skill directory under skills/<category>/ contains exactly one SKILL.md
  (at its root), and no SKILL.md sits at the category level
- SKILL.md starts with a closed YAML frontmatter block delimited by `---` lines
- name: 1-64 ASCII lowercase alphanumerics and single hyphens, no leading /
  trailing hyphen, and matches the directory name
- description: string, 1-1024 characters
- compatibility (optional): string, 1-500 characters
- license and allowed-tools (optional): strings
- metadata (optional): a string-to-string mapping
- disable-model-invocation (repository extension, optional): boolean

Usage: uv run --locked python scripts/validate_skills.py [repo-root]
Exits 1 if any skill violates a validation rule.
"""

from __future__ import annotations

import re
import sys
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

FieldValidator = Callable[[Any, Path], list[str]]


def _string_field(
    field: str, *, minimum: int | None = None, maximum: int | None = None
) -> FieldValidator:
    def validate(value: Any, _skill_dir: Path) -> list[str]:
        if not isinstance(value, str):
            return [f"{field} must be a string (got {type(value).__name__})"]
        if minimum is not None and len(value) < minimum:
            return [f"{field} must be at least {minimum} character(s) (got {len(value)})"]
        if maximum is not None and len(value) > maximum:
            return [f"{field} must be at most {maximum} characters (got {len(value)})"]
        return []

    return validate


def _validate_name(value: Any, skill_dir: Path) -> list[str]:
    errors = _string_field("name", minimum=1, maximum=64)(value, skill_dir)
    if errors:
        return errors

    errors = []
    if not NAME_RE.fullmatch(value):
        errors.append(
            "name must use only ASCII lowercase letters, digits, and single "
            f"hyphens, with no leading/trailing hyphen (got {value!r})"
        )
    if value != skill_dir.name:
        errors.append(f"name {value!r} does not match directory name {skill_dir.name!r}")
    return errors


def _validate_metadata(value: Any, _skill_dir: Path) -> list[str]:
    if not isinstance(value, Mapping):
        return [f"metadata must be a mapping (got {type(value).__name__})"]

    errors = []
    for key, item in value.items():
        if not isinstance(key, str):
            errors.append(f"metadata key must be a string (got {type(key).__name__})")
        if not isinstance(item, str):
            errors.append(
                f"metadata value for {key!r} must be a string "
                f"(got {type(item).__name__})"
            )
    return errors


def _validate_boolean(field: str) -> FieldValidator:
    def validate(value: Any, _skill_dir: Path) -> list[str]:
        if not isinstance(value, bool):
            return [f"{field} must be a boolean (got {type(value).__name__})"]
        return []

    return validate


# This registry is the complete set of frontmatter fields accepted by this
# repository. Add future specification or repository fields here together with
# tests for their type and constraints.
FIELD_VALIDATORS: dict[str, FieldValidator] = {
    "name": _validate_name,
    "description": _string_field("description", minimum=1, maximum=1024),
    "license": _string_field("license"),
    "compatibility": _string_field("compatibility", minimum=1, maximum=500),
    "metadata": _validate_metadata,
    "allowed-tools": _string_field("allowed-tools"),
    "disable-model-invocation": _validate_boolean("disable-model-invocation"),
}
REQUIRED_FIELDS = {"name", "description"}


def parse_frontmatter(text: str) -> tuple[dict[str, Any], list[str]]:
    """Parse exact `---`-delimited YAML frontmatter."""
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return {}, ["SKILL.md does not start with an exact `---` delimiter line"]

    try:
        end = lines.index("---", 1)
    except ValueError:
        return {}, ["frontmatter block is not closed with an exact `---` delimiter line"]

    yaml = YAML(typ="safe")
    yaml.allow_duplicate_keys = False
    try:
        loaded = yaml.load("\n".join(lines[1:end]))
    except YAMLError as error:
        problem = getattr(error, "problem", None)
        return {}, [f"invalid YAML frontmatter: {problem or str(error).splitlines()[0]}"]

    if not isinstance(loaded, Mapping):
        kind = "null" if loaded is None else type(loaded).__name__
        return {}, [f"frontmatter must be a mapping (got {kind})"]

    fields: dict[str, Any] = {}
    errors = []
    for key, value in loaded.items():
        if not isinstance(key, str):
            errors.append(f"frontmatter key must be a string (got {type(key).__name__})")
            continue
        fields[key] = value
    return fields, errors


def validate_skill(skill_dir: Path) -> list[str]:
    """Return validation errors for one skill directory."""
    errors = []
    skill_md = skill_dir / "SKILL.md"

    strays = [
        path.relative_to(skill_dir)
        for path in skill_dir.rglob("*")
        if path.is_file() and path.name.lower() == "skill.md" and path != skill_md
    ]
    for stray in strays:
        errors.append(f"extra SKILL.md inside the bundle: {stray}")

    if not skill_md.is_file():
        errors.append("missing SKILL.md")
        return errors

    fields, parse_errors = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    errors.extend(parse_errors)
    if parse_errors:
        return errors

    for field in sorted(REQUIRED_FIELDS - fields.keys()):
        errors.append(f"frontmatter is missing required field: {field}")

    for field, value in fields.items():
        validator = FIELD_VALIDATORS.get(field)
        if validator is None:
            errors.append(f"unknown frontmatter field: {field}")
            continue
        errors.extend(validator(value, skill_dir))
    return errors


def validate_repository(root: Path) -> tuple[int, list[str]]:
    """Return the number of discovered skills and formatted errors."""
    skills_root = root / "skills"
    if not skills_root.is_dir():
        return 0, [f"{skills_root} is not a directory"]

    category_dirs = sorted(path for path in skills_root.iterdir() if path.is_dir())
    skill_dirs = sorted(
        path
        for category_dir in category_dirs
        for path in category_dir.iterdir()
        if path.is_dir()
    )
    if not skill_dirs:
        return 0, [f"no skill directories found under {skills_root}"]

    errors = []
    for category_dir in category_dirs:
        for misplaced in category_dir.iterdir():
            if misplaced.is_file() and misplaced.name.lower() == "skill.md":
                rel = misplaced.relative_to(root)
                errors.append(
                    f"{rel}: SKILL.md at category level; skills belong in "
                    f"{category_dir.relative_to(root)}/<skill-name>/"
                )

    for skill_dir in skill_dirs:
        rel = skill_dir.relative_to(root)
        errors.extend(f"{rel}: {message}" for message in validate_skill(skill_dir))
    return len(skill_dirs), errors


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) > 1:
        print("usage: validate_skills.py [repo-root]", file=sys.stderr)
        return 2

    root = Path(args[0]) if args else Path(__file__).resolve().parent.parent
    count, errors = validate_repository(root)
    for message in errors:
        print(f"error: {message}")
    print(f"validated {count} skills: {'FAILED' if errors else 'ok'}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
