# AGENTS.md

This repository contains Himadajin's personal Agent Skills.

For general Agent Skills behavior, format, or development practice,
treat the official documentation as the source of truth:

- [Agent Skills LLM index](https://agentskills.io/llms.txt)
- [OpenAI prompt guidance](https://developers.openai.com/api/docs/guides/prompt-guidance.md)
- [Anthropic Prompt engineering overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview.md)

Use the Agent Skills LLM index to find additional topic-specific pages
when a task needs them.

## Engineering Principles

Rules in this repository are read by agents,
both in this file and in each skill.
Prefer a few rules that state their intent
over many local instructions or special cases:
a rule with a reason generalizes to cases its author did not foresee,
so the next decision can be derived instead of newly specified.

Before keeping a rule, check two things:

- Removing it would change what an agent does next.
  If not, it is not a rule; drop it.
- It explains more than the single incident that prompted it.
  If not, generalize it or leave it out.

When behavior needs to change,
first try to derive it from the existing rules
and their source-of-truth documents.
If it does not fit, make changes in this order:

1. Remove a rule or special case.
2. Generalize an existing rule so it covers the new behavior.
3. Add a new rule only when 1 and 2 cannot express it.

A new or changed rule names one default behavior
and the signal that shows it was followed,
rather than listing competing options.

Keep rules close to their source of truth:

- Skill activation boundaries belong in the frontmatter `description`;
  if a behavior change affects when a skill should or should not activate,
  reflect that boundary there rather than only in the body.
- Mandatory workflow and decision rules belong in the skill's `SKILL.md`.
- Detailed rubrics, templates, examples, and long references
  belong under that skill's `references/`, `assets/`, or `scripts/` directory.
- Repository-wide editing rules belong in this file
  only when they apply across skills
  and are not already covered by official documentation.

## Local Map

- `README.md`: human-facing installation and cross-agent sharing notes.
- `docs/releasing.md`: how release zips are produced.
  Releases are started manually by the repository owner;
  agents must not initiate one.
- `skills/<category>/<skill-name>/SKILL.md` owns that skill,
  including the supporting files under its directory.
  Categories: `engineering` (artifacts that lead to implementation),
  `productivity` (dialogue and decision support),
  `meta` (skill and prompt development),
  `writing` (Japanese prose),
  and `creativity` (creative output).
  `skills/deprecated/` holds retired skills kept for reference.
- Many skills are intentionally written in Japanese;
  keep each skill's language unless the task asks otherwise.
- `/works/`, `/local/`, and `/tmp/` are gitignored local workspace.
  Use them only when the user points to them,
  and never infer repository rules from them.

## Validation

There is no repository-wide build step at the time of writing.
For skill and documentation changes,
validate the touched files and references directly.

## Commits and pull requests

When writing a pull request title or a commit message:

- Keep it to a single line.
- Write it in concise English.
- Follow the [Conventional Commits](https://www.conventionalcommits.org/) format.
