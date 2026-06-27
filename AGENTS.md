# AGENTS.md

## Project Role

This repository contains Himadajin's personal Agent Skills. It does not define a
separate skill framework or local best-practice system. When changing skills,
treat the public Agent Skills documentation as the source of truth for the
general format and development guidance.

Use this file only for repository-specific routing, priorities, and editing
judgment.

## External Sources

Consult current official documentation when a task depends on general Agent
Skills behavior, format, or development practice. Prefer

- [Agent Skills LLM index](https://agentskills.io/llms.txt)
- [Agent Skills specification](https://agentskills.io/specification.md)
- [Best practices for skill creators](https://agentskills.io/skill-creation/best-practices.md)
- [Optimizing skill descriptions](https://agentskills.io/skill-creation/optimizing-descriptions.md)
- [OpenAI prompt guidance](https://developers.openai.com/api/docs/guides/prompt-guidance.md)

Use the Agent Skills LLM index to find additional topic-specific pages, such as
evaluating skill output quality or using scripts in skills, when the task calls
for them.

## Engineering Principles

Prefer a few well-formed rules with real explanatory power over many local
instructions or special cases. A good rule should be coherent with the rest of
the repository, explain more than one case, and make future decisions easier.

A well-formed rule in this repository should:

- Fit the existing skill definition, official source material, and repository
  structure.
- Apply beyond a single incident or personal preference.
- Change what an agent should do next, not merely state taste.
- Reduce ambiguity by naming the default behavior or validation signal instead
  of adding competing options.

When adding or changing skill behavior, first try to derive it from the existing
skill definition and its source-of-truth documents. If the behavior does not
fit, consider changes in this order:

1. Remove an unnecessary rule or special case.
2. Refine or generalize an existing rule so it explains the new behavior.
3. Add a new rule only when the behavior cannot be expressed cleanly by the
   existing rules.

Keep rules close to their source of truth:

- Skill activation boundaries belong in the frontmatter `description`; if a
  behavior change affects when a skill should or should not activate, reflect
  that boundary there rather than only in the body.
- Mandatory workflow and decision rules belong in the skill's `SKILL.md`.
- Detailed rubrics, templates, examples, and long references belong under that
  skill's `references/`, `assets/`, or `scripts/` directory.
- Repository-wide editing rules belong in this file only when they apply across
  skills and are not already covered by official documentation.

## Local Source Of Truth

- The root `README.md` owns human-facing installation and cross-agent sharing
  notes; this file owns agent-facing repository editing judgment.
- Each `skills/<skill-name>/SKILL.md` owns that skill's current behavior.
- Files under a skill's `references/`, `assets/`, or `scripts/` directory support
  that skill only, unless another skill explicitly links to them.
- `/works/`, `/local/`, and `/tmp/` are local workspace context. Use them when
  the user points to them, but do not infer repository rules from them.

## Editing Skills

- Read the affected `SKILL.md` completely before editing it.
- Read only the referenced files needed for the behavior being changed.
- Preserve the language and style of the file being edited; many files in this
  repository are intentionally written in Japanese.
- When changing public skill behavior, check whether the `description`,
  `SKILL.md`, relevant references, and any agent-specific metadata or prompts
  must change together.
- Prefer ASCII for machine-facing identifiers, filenames, fixed labels, and
  stable IDs unless an existing convention requires otherwise.

## Validation

There is no repository-wide build step at the time of writing. For skill and
documentation changes, validate by:

- Re-reading the changed files for internal consistency.
- Checking links and relative file references you touched.
- Using `rg` in tracked source files to find stale terminology, trigger phrases,
  filenames, and cross-references affected by the change.

If future work adds package metadata, scripts, or eval harnesses, document the
exact commands here rather than relying on generic advice.

## Change Hygiene

- Keep changes narrowly scoped to the requested skill, reference, or repository
  instruction file.
- Do not rewrite unrelated prose for style consistency alone.
- Do not overwrite user work or generated artifacts unrelated to the task.
- Before finalizing, inspect the diff, then briefly report the files changed and
  any validation that was or was not run.
