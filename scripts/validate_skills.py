#!/usr/bin/env python3
"""Validate skills under skills/ against the Agent Skills specification.

Checks the mandatory rules from https://agentskills.io/specification.md:

- every directory under skills/ contains exactly one SKILL.md (at its root)
- SKILL.md starts with a closed YAML frontmatter block
- name: 1-64 chars, lowercase alphanumerics and single hyphens, no leading /
  trailing hyphen, and matches the directory name
- description: 1-1024 chars
- compatibility (optional): 1-500 chars

The frontmatter parser is intentionally lenient (plain `key: value` lines plus
block scalars), matching how agents actually read SKILL.md: strict YAML
rejects unquoted values that contain ": ", which are valid in practice.

Usage: python3 scripts/validate_skills.py [repo-root]
Exits 1 if any skill violates a mandatory rule.
"""

import re
import sys
from pathlib import Path

KNOWN_FIELDS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):(.*)$")
BLOCK_INDICATOR_RE = re.compile(r"^[>|][+-]?$")


def parse_frontmatter(text):
    """Return (fields, errors). fields maps top-level keys to string values
    (nested mappings are stored as None: present but unparsed)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, ["SKILL.md does not start with a `---` frontmatter block"]
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return {}, ["frontmatter block is not closed with `---`"]

    fields = {}
    errors = []
    i = 1
    while i < end:
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        m = KEY_RE.match(line)
        if not m:
            errors.append(f"unparsable frontmatter line {i + 1}: {line!r}")
            i += 1
            continue
        key, rest = m.group(1), m.group(2).strip()
        i += 1
        if BLOCK_INDICATOR_RE.match(rest):
            block = []
            while i < end and (not lines[i].strip() or lines[i][:1] in (" ", "\t")):
                block.append(lines[i].strip())
                i += 1
            joiner = "\n" if rest[0] == "|" else " "
            value = joiner.join(part for part in block if part).strip()
        elif rest == "":
            # nested mapping (e.g. metadata:); skip its indented body
            while i < end and (not lines[i].strip() or lines[i][:1] in (" ", "\t")):
                i += 1
            value = None
        else:
            value = rest
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
                value = value[1:-1]
        if key in fields:
            errors.append(f"duplicate frontmatter key: {key}")
        fields[key] = value
    return fields, errors


def validate_skill(skill_dir):
    """Return (errors, warnings) for one skill directory."""
    errors = []
    warnings = []

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return [f"missing SKILL.md"], warnings

    strays = [
        p.relative_to(skill_dir)
        for p in skill_dir.rglob("*")
        if p.is_file() and p.name.lower() == "skill.md" and p != skill_md
    ]
    for stray in strays:
        errors.append(f"extra SKILL.md inside the bundle: {stray}")

    fields, parse_errors = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    errors.extend(parse_errors)

    name = fields.get("name")
    if not name:
        errors.append("frontmatter is missing required field: name")
    else:
        if not 1 <= len(name) <= 64:
            errors.append(f"name must be 1-64 characters (got {len(name)})")
        if not NAME_RE.match(name):
            errors.append(
                "name must use only lowercase letters, digits, and single "
                f"hyphens, with no leading/trailing hyphen (got {name!r})"
            )
        if name != skill_dir.name:
            errors.append(
                f"name {name!r} does not match directory name {skill_dir.name!r}"
            )

    description = fields.get("description")
    if not description:
        errors.append("frontmatter is missing required field: description")
    elif len(description) > 1024:
        errors.append(f"description must be at most 1024 characters (got {len(description)})")

    compatibility = fields.get("compatibility")
    if compatibility is not None and not 1 <= len(compatibility) <= 500:
        errors.append(
            f"compatibility must be 1-500 characters (got {len(compatibility or '')})"
        )

    for key in fields:
        if key not in KNOWN_FIELDS:
            warnings.append(f"unknown frontmatter field: {key}")

    return errors, warnings


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    skills_root = root / "skills"
    if not skills_root.is_dir():
        print(f"error: {skills_root} is not a directory", file=sys.stderr)
        return 1

    skill_dirs = sorted(p for p in skills_root.iterdir() if p.is_dir())
    if not skill_dirs:
        print(f"error: no skill directories found under {skills_root}", file=sys.stderr)
        return 1

    failed = False
    for skill_dir in skill_dirs:
        errors, warnings = validate_skill(skill_dir)
        rel = skill_dir.relative_to(root)
        for message in errors:
            print(f"error: {rel}: {message}")
        for message in warnings:
            print(f"warning: {rel}: {message}")
        if errors:
            failed = True

    print(f"validated {len(skill_dirs)} skills: {'FAILED' if failed else 'ok'}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
