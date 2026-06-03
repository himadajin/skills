---
name: plan-with
description: 'Use when the user wants collaborative planning for development work before implementation: creating a plan.md for a later coding agent to execute after intent has been clarified through dialogue. Trigger for requests like "plan with me", "make a plan.md", "help me plan this feature/refactor/investigation/docs update", or when the user wants the agent to question them before writing an implementation-ready plan. Do not use for general life, business, travel, or study planning.'
---

# Plan With

Use this skill to interview the user until their real development goal is clear enough to write a standalone `plan.md` for a later coding agent. The output is a file, not a conversational `<proposed_plan>` block.

The user's initial request is a hypothesis. Your job is to discover the desired outcome, not merely refine the first wording.

## Core Rules

- Start with initial investigation before asking the first question. Inspect the repository and relevant docs to answer discoverable questions yourself.
- Use web research when outside knowledge would improve the plan, such as current official docs, practices, examples, or options the user may not know. Do not browse just because browsing is possible.
- Ask exactly one question per user turn. Do not bundle related questions.
- Every question must include your recommended answer and the reason for that recommendation.
- Ask purpose-first: clarify what the user wants to achieve before narrowing into implementation means such as frameworks, libraries, files, or APIs.
- Respect explicit constraints the user states. If an explicit constraint appears to conflict with the desired outcome, ask whether it is mandatory.
- Do not maintain a separate planning memo and do not update `plan.md` incrementally. Write the final plan once at the end.
- Do not implement the planned work. During planning, only perform investigation and the final plan-file write.
- Before writing `plan.md`, ask a one-question finalization confirmation so the user controls when refinement stops.

## Investigation

Resolve discoverable facts before asking:

- Read existing docs such as `README`, `AGENTS.md`, `CONTEXT.md`, ADRs, and existing plans when relevant.
- Search for relevant code, tests, manifests, configs, and current conventions.
- Use non-mutating commands and inspections. Avoid commands whose purpose is to perform the planned work.
- Use web research only when it can add useful outside knowledge.

When asking after investigation, first share a brief finding: one or two short sentences explaining the fact that makes the question easier to answer. Do not dump research notes.

## Question Chain

Walk down the design tree one dependency at a time. Each question should resolve the next most useful uncertainty.

Good questions usually clarify:

- the desired outcome behind the initial request
- what completion means
- target users, maintainers, or later agents when that changes the plan
- scope boundaries and explicit non-goals
- constraints that are not discoverable from the repo
- tradeoffs where a wrong assumption would change the plan's direction

Avoid questions that:

- could be answered by reading the repo or official docs
- ask the user to choose a file, API, or library before the purpose is clear
- do not have a defensible recommended answer
- collect information only because it might be nice to record

If the user asks you to produce `plan.md` while ambiguity remains, do not refuse in order to keep questioning. Planning under uncertainty is allowed; a few good questions can still produce a better plan than one-shot planning.

## Finalization

When you believe the plan is ready, or when the user asks to write it, ask one final confirmation question. Keep it narrow, for example:

> I think this is ready to turn into `plan.md`: [brief direction]. My recommendation is to write it now because [reason]. Should I create the plan file?

If the user confirms or otherwise asks you to proceed, write the plan file.

## Plan Path

Use the user-specified path when provided.

If no path is specified, write the plan at the repository root:

- Use `plan.md` if it does not exist.
- If `plan.md` exists, do not overwrite it. Automatically choose a short, meaningful English kebab-case filename based on the planned work, such as `plan-create-plan-with-skill.md`.
- Do not ask the user to name the file.

## Plan Format

The final `plan.md` must contain exactly these four English section headings, in this order:

```md
# <Short Title>

## Purpose

## Completion Conditions

## Context

## Direction
```

Write the body in the user's conversation language unless they ask otherwise. Keep the filename and section headings in English.

### Purpose

State the desired outcome discovered through dialogue. Do not merely summarize the initial request.

### Completion Conditions

Write bullet points only. Each bullet should describe a checkable condition that makes the work count as done. Do not create a separate Test Plan section.

### Context

Include only information whose absence would likely cause a later agent to make the wrong implementation judgment after context reset. Good candidates include:

- explicit user constraints
- selected libraries or frameworks that were agreed in the conversation
- user environment facts not obvious from the repo
- important investigation or web research findings
- relevant current-state facts that are not easy to infer later

Do not include transcripts, exhaustive investigation logs, low-value caveats, or facts the later agent can quickly rediscover from the code.

### Direction

Give the later agent the high-level direction for the work. Prefer short prose. Use bullets only when they make the direction clearer.

Do not prescribe an unnecessary step-by-step workflow. The plan should define the destination, completion conditions, important context, and direction while leaving room for the later agent to choose an efficient implementation path.
