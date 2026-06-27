---
name: option-proposer
description: A skill for deliberate decision support: investigate enough context, present distinct options, compare their tradeoffs, and recommend one. Use only when the user explicitly names this skill or says to use this skill.
---

# Option Proposer

Help the user decide before execution. Produce comparable options and one recommendation; do not start doing the work those options describe.

## Core Instructions

- Treat the request as decision support, not execution.
- Identify the user's decision, constraints, priorities, and the work that must remain unperformed.
- Inspect the codebase, docs, configs, issues, or local artifacts when local context could change the options.
- Research the internet when current external facts could change the comparison, the user asks for research, or up-to-date accuracy matters. Cite web sources when used.
- Gather enough context to make the options meaningfully different, then stop researching.
- Ask a clarification question only when no useful options can be proposed without the answer. Otherwise, state concise assumptions and proceed.
- Use the option count requested by the user; default to exactly 3 options when no count is specified.
- Do not invent invalid, unsafe, or meaningless options just to satisfy a count. Explain briefly when fewer defensible options exist.
- Make options differ by real strategy, risk profile, cost, reversibility, maintainability, user impact, time to value, or another decision-relevant axis.
- Keep each option concrete enough that the user can choose among them.
- Use the user's language and natural field labels for that language, while preserving the output structure.
- Favor reversible, low-risk options when the user's priorities are unclear, and state that assumption in the recommendation.

## Boundaries

- Do not perform the underlying task.
- Do not edit files, commit changes, send messages, create resources, purchase anything, or take irreversible actions.
- Do not run implementation, migration, install, deploy, formatting, or test commands unless the user separately asks for execution after the options are delivered.
- Do not include implementation steps unless the user explicitly asks for implementation planning.
- Do not add extra sections unless they materially improve the user's ability to choose.

## Output Contract

Use this structure unless the user provides a stricter format. The labels below describe semantic roles; adapt their wording to the user's language and context.

**Context**

- Include only assumptions, findings, constraints, or uncertainties that affect the choice.
- If no meaningful context was needed, say so briefly.

**Options**

Repeat this block for the requested number of options:

1. **Option name**
   - **Summary**: Describe what this option does.
   - **Pros**:
     - State the main benefits.
   - **Cons**:
     - State the main costs, risks, or weaknesses.

**Recommendation**
- Name the recommended option.
- Explain the deciding factor in terms of the user's priorities, the investigated context, risk, reversibility, cost, quality, or time to value.
- Stop after the recommendation. Do not begin executing the recommended option.

## Compactness

- Use one to three bullets for each Pros and Cons field.
- When the user asks for many options, use one bullet per field and keep the recommendation brief.
