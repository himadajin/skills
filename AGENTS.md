# AGENTS.md

## Repository Scope

This repository contains Himadajin's personal Agent Skills. It does not define a
separate skill framework or local best-practice system.

For general Agent Skills behavior, format, or development practice, treat the
official documentation as the source of truth:

- [Agent Skills LLM index](https://agentskills.io/llms.txt)
- [Agent Skills specification](https://agentskills.io/specification.md)
- [Best practices for skill creators](https://agentskills.io/skill-creation/best-practices.md)
- [Optimizing skill descriptions](https://agentskills.io/skill-creation/optimizing-descriptions.md)
- [OpenAI prompt guidance](https://developers.openai.com/api/docs/guides/prompt-guidance.md)

Use the Agent Skills LLM index to find additional topic-specific pages when a
task needs them.

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

## Local Map

- The root `README.md` owns human-facing installation and cross-agent sharing
  notes.
- `docs/releasing.md` records, as a factual description, how release zips are
  produced. Releases happen only when the repository owner manually runs the
  GitHub Actions release workflow; agents must not initiate releases.
- Each `skills/<skill-name>/SKILL.md` owns that skill's behavior. Supporting
  files under that skill's subdirectories belong to that skill unless another
  skill explicitly links to them.
- Many skills are intentionally written in Japanese; keep the affected skill's
  language unless the task asks otherwise.
- `/works/`, `/local/`, and `/tmp/` are local workspace context. Use them when
  the user points to them, but do not infer repository rules from them.

## Validation

There is no repository-wide build step at the time of writing. For skill and
documentation changes, validate the touched files and references directly.
