from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.validate_skills import parse_frontmatter, validate_repository, validate_skill


def skill_document(frontmatter: str, body: str = "Instructions.\n") -> str:
    return f"---\n{frontmatter}\n---\n{body}"


class FrontmatterTests(unittest.TestCase):
    def test_accepts_standard_yaml_features(self) -> None:
        documents = {
            "inline comment": skill_document("name: demo # comment\ndescription: Valid."),
            "block indentation": skill_document(
                "name: demo\ndescription: |2-\n  Use when requested."
            ),
            "multiline quote": skill_document(
                'name: demo\ndescription: "Use when\n  requested."'
            ),
            "embedded dashes": skill_document("name: demo\ndescription: value---value"),
            "indented delimiter text": skill_document(
                "name: demo\ndescription: |\n  first\n  ---\n  last"
            ),
        }

        for case, document in documents.items():
            with self.subTest(case=case):
                fields, errors = parse_frontmatter(document)
                self.assertEqual([], errors)
                self.assertEqual("demo", fields["name"])
                self.assertIsInstance(fields["description"], str)

    def test_rejects_malformed_yaml(self) -> None:
        frontmatters = {
            "unquoted colon": "name: demo\ndescription: Use when: requested",
            "unterminated quote": 'name: demo\ndescription: "unterminated',
            "duplicate key": "name: demo\ndescription: First.\ndescription: Second.",
            "nested duplicate key": (
                "name: demo\ndescription: Valid.\nmetadata:\n  key: first\n  key: second"
            ),
        }

        for case, frontmatter in frontmatters.items():
            with self.subTest(case=case):
                _fields, errors = parse_frontmatter(skill_document(frontmatter))
                self.assertTrue(errors)
                self.assertIn("invalid YAML frontmatter", errors[0])

    def test_requires_exact_delimiter_lines(self) -> None:
        documents = {
            "missing opener": "name: demo\ndescription: Valid.\n---\nBody.",
            "spaced opener": " ---\nname: demo\ndescription: Valid.\n---\nBody.",
            "missing closer": "---\nname: demo\ndescription: Valid.\nBody.",
            "spaced closer": "---\nname: demo\ndescription: Valid.\n ---\nBody.",
        }

        for case, document in documents.items():
            with self.subTest(case=case):
                _fields, errors = parse_frontmatter(document)
                self.assertTrue(errors)

    def test_requires_frontmatter_mapping(self) -> None:
        for frontmatter in ("", "[name, description]", "plain scalar"):
            with self.subTest(frontmatter=frontmatter):
                _fields, errors = parse_frontmatter(skill_document(frontmatter))
                self.assertTrue(errors)
                self.assertIn("frontmatter must be a mapping", errors[0])


class FieldValidationTests(unittest.TestCase):
    def validate(self, frontmatter: str, directory: str = "demo") -> list[str]:
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_dir = Path(temp_dir) / directory
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text(
                skill_document(frontmatter), encoding="utf-8"
            )
            return validate_skill(skill_dir)

    def test_accepts_all_registered_fields(self) -> None:
        errors = self.validate(
            "\n".join(
                [
                    "name: demo",
                    "description: Use when testing.",
                    "license: Apache-2.0",
                    "compatibility: Requires Python 3.",
                    "metadata:",
                    "  author: Himadajin",
                    'allowed-tools: "Bash Read"',
                    "disable-model-invocation: true",
                ]
            )
        )
        self.assertEqual([], errors)

    def test_rejects_unknown_field(self) -> None:
        errors = self.validate("name: demo\ndescription: Valid.\ndescriptino: typo")
        self.assertIn("unknown frontmatter field: descriptino", errors)

    def test_requires_name_and_description(self) -> None:
        self.assertIn(
            "frontmatter is missing required field: name",
            self.validate("description: Valid."),
        )
        self.assertIn(
            "frontmatter is missing required field: description",
            self.validate("name: demo"),
        )

    def test_rejects_wrong_field_types(self) -> None:
        cases = {
            "name": ("name: 123\ndescription: Valid.", "name must be a string"),
            "description": (
                "name: demo\ndescription: [one, two]",
                "description must be a string",
            ),
            "license": (
                "name: demo\ndescription: Valid.\nlicense: [MIT]",
                "license must be a string",
            ),
            "metadata": (
                "name: demo\ndescription: Valid.\nmetadata:\n  version: 1",
                "metadata value for 'version' must be a string",
            ),
            "metadata key": (
                "name: demo\ndescription: Valid.\nmetadata:\n  1: version",
                "metadata key must be a string",
            ),
            "allowed-tools": (
                "name: demo\ndescription: Valid.\nallowed-tools: [Bash]",
                "allowed-tools must be a string",
            ),
            "extension": (
                'name: demo\ndescription: Valid.\ndisable-model-invocation: "true"',
                "disable-model-invocation must be a boolean",
            ),
        }

        for case, (frontmatter, expected) in cases.items():
            with self.subTest(case=case):
                self.assertTrue(any(expected in error for error in self.validate(frontmatter)))

    def test_accepts_length_boundaries(self) -> None:
        name = "a" * 64
        errors = self.validate(
            "\n".join(
                [
                    f"name: {name}",
                    f"description: {'d' * 1024}",
                    f"compatibility: {'c' * 500}",
                ]
            ),
            directory=name,
        )
        self.assertEqual([], errors)

    def test_rejects_empty_and_overlong_fields(self) -> None:
        cases = {
            "empty description": ("name: demo\ndescription: ''", "at least 1"),
            "long description": (
                f"name: demo\ndescription: {'x' * 1025}",
                "at most 1024",
            ),
            "empty compatibility": (
                "name: demo\ndescription: Valid.\ncompatibility: ''",
                "at least 1",
            ),
            "long compatibility": (
                f"name: demo\ndescription: Valid.\ncompatibility: {'x' * 501}",
                "at most 500",
            ),
        }

        for case, (frontmatter, expected) in cases.items():
            with self.subTest(case=case):
                self.assertTrue(any(expected in error for error in self.validate(frontmatter)))

    def test_enforces_ascii_name_format_and_directory_match(self) -> None:
        cases = {
            "unicode": ("name: démo\ndescription: Valid.", "ASCII lowercase"),
            "double hyphen": (
                "name: de--mo\ndescription: Valid.",
                "ASCII lowercase",
            ),
            "overlong": (
                f"name: {'a' * 65}\ndescription: Valid.",
                "at most 64",
            ),
            "directory mismatch": (
                "name: other\ndescription: Valid.",
                "does not match directory name",
            ),
        }

        for case, (frontmatter, expected) in cases.items():
            with self.subTest(case=case):
                self.assertTrue(any(expected in error for error in self.validate(frontmatter)))


class RepositoryLayoutTests(unittest.TestCase):
    def make_repository(self) -> tuple[tempfile.TemporaryDirectory[str], Path, Path]:
        temp_dir = tempfile.TemporaryDirectory()
        root = Path(temp_dir.name)
        skill_dir = root / "skills" / "engineering" / "demo"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(
            skill_document("name: demo\ndescription: Valid."), encoding="utf-8"
        )
        return temp_dir, root, skill_dir

    def test_accepts_valid_repository(self) -> None:
        temp_dir, root, _skill_dir = self.make_repository()
        self.addCleanup(temp_dir.cleanup)
        count, errors = validate_repository(root)
        self.assertEqual(1, count)
        self.assertEqual([], errors)

    def test_rejects_invalid_layouts(self) -> None:
        cases = ("lowercase only", "both cases", "nested", "category level", "missing")
        for case in cases:
            with self.subTest(case=case):
                temp_dir, root, skill_dir = self.make_repository()
                self.addCleanup(temp_dir.cleanup)
                skill_md = skill_dir / "SKILL.md"

                if case == "lowercase only":
                    skill_md.rename(skill_dir / "skill.md")
                elif case == "both cases":
                    (skill_dir / "skill.md").write_text("duplicate", encoding="utf-8")
                elif case == "nested":
                    nested = skill_dir / "references" / "SKILL.md"
                    nested.parent.mkdir()
                    nested.write_text("duplicate", encoding="utf-8")
                elif case == "category level":
                    (skill_dir.parent / "SKILL.md").write_text("misplaced", encoding="utf-8")
                elif case == "missing":
                    skill_md.unlink()

                _count, errors = validate_repository(root)
                self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()
