---
name: desire-articulation
description: >-
  Use only for an explicit interview-style clarification phase for a software development task whose output is a standalone desire.md or equivalent handoff brief for a later coding agent. Trigger when the user asks to be questioned, articulate an unclear development desire, or create/capture a desire file before implementation, and the request implies both unresolved intent and a written handoff artifact. First articulate the underlying desire, then refine how it should be realized without prescribing step-by-step implementation. Do NOT use for ordinary clarification, planning, plan.md creation, code review, issue execution, debugging, prompt writing, prose editing, brainstorming, non-development goals, or when an existing plan/desire/spec/issue/task list should be implemented, followed, reviewed, revised, or continued.
---

# Desire Articulation

Interview the user until their underlying development desire and its practical realization are clear enough to write a standalone `desire.md` for a later coding agent. Treat the initial request as a hypothesis; first discover the desired state or unresolved question behind it, then refine how that desire should be made real without locking in unnecessary step-by-step implementation.

## Activation Gate

Use only when all are true:

- Software development work.
- Intent is unresolved.
- User wants interview/guided clarification.
- Final output is `desire.md` or an equivalent handoff brief.

Do not activate merely because a request is vague, high-level, asks "what should we check?", or needs ordinary clarification. If a `plan.md`, `desire.md`, issue, PR, task list, spec, or implementation brief is already the source of truth, read that artifact and proceed with the ordinary implementation, review, revision, or debugging workflow instead of using Root/Branch/Leaf framing or creating a new handoff brief. Activate only if the user explicitly asks to restart desire articulation from scratch, replace the prior source of truth with a new desire brief, or be interviewed again before implementation.

## Conduct

- Investigate before asking: read relevant docs/code/configs and use web research only when outside knowledge would materially improve the brief. If investigation finds no relevant implementation context, say that briefly and ask the upstream desire question that would most change the eventual brief.
- Ask exactly one question per user turn.
- Maintain a lightweight Root/Branch hypothesis tree:
  - `Root`: the user's desired state or unresolved question.
  - `Branch`: an upstream decision or ambiguity that could change the Root or the final brief.
  - `Leaf`: wording or detail for the final `desire.md`.
- Ask about the most upstream unresolved Branch first. Do not follow a fixed checklist or phase order.
- Each question must include your recommended answer and the reason. Present the recommendation as a hypothesis, not as the user's conclusion.
- If the Root changes, revisit only the downstream Branches that the new Root invalidates.
- Respect explicit constraints; if a constraint conflicts with the Root, ask whether it is mandatory.
- Do not implement the articulated work.
- Do not maintain a separate memo or update `desire.md` incrementally. Write the final file once.
- If the user asks to write `desire.md` while ambiguity remains, allow an imperfect brief instead of forcing more questions. Preserve remaining decision-relevant unknowns in `Context`, do not invent specifics, and use `Direction` to guide the later agent away from premature implementation commitments.

When asking after investigation, first share one or two short sentences with the useful finding that frames the question. Do not dump research notes.

Branch examples include completion feeling, constraints, non-goals, audience, handoff boundaries, and direction-changing tradeoffs. These are examples, not a checklist; ask about them only when they could change the Root or the final brief. Avoid questions answerable from the repo/docs, implementation means before purpose, or low-value facts that are merely nice to record.

## Phases

Use the same Root/Branch/Leaf question model in both phases. The phases exist only to protect the boundary between understanding the desire and making it practical.

- `PHASE1`: Articulate the desire itself. Keep the existing behavior: avoid implementation means before purpose, do not steer the user toward an early technical shape, and stop when the Root is clear enough to preserve.
- `PHASE2`: Refine how the desire should be realized. Ask upstream Branch questions about what would make the work complete, which tools or libraries fit the user's environment, the minimum quality and testing expectations, architectural boundaries, and implementation directions to avoid. Prefer recommendations grounded in repo investigation and practical constraints. Decide tools and goals when they matter, but do not prescribe detailed implementation steps.

Do not enter `PHASE2` silently. When `PHASE1` appears complete, ask a narrow confirmation question before moving on. Do not draft or partially write `desire.md` during this confirmation. Use this shape:

> I think PHASE1 is ready to close: the desire itself is clear enough to preserve without turning it into implementation detail yet. My recommendation is to move to PHASE2 because the remaining important questions are about how to make this real. Should we continue refining the desire, or move to PHASE2?

## Finalization

Stop asking when the Root is articulated, no unresolved upstream Branch remains that would distort the Root or final brief, PHASE2 is complete enough to make the desire practical, and the user's own questions about what they want are resolved enough to proceed.

Before writing the file, ask one narrow confirmation question so the user controls when refinement stops, for example:

> I think this is ready to turn into `desire.md`: [brief direction]. My recommendation is to write it now because [reason]. Should I create the desire file?

If the user confirms or otherwise asks you to proceed, write the file.

## File Path

Use the user-specified path when provided. Otherwise write at the repository root:

- Use `desire.md` if it does not exist.
- If it exists, choose a short, meaningful English kebab-case filename such as `desire-refine-search-ui.md`.
- Do not ask the user to name the file.

## File Format

The file must contain exactly these English headings, in this order:

```md
# <Short Title>

## Purpose

## Context

## Direction

## Completion Conditions
```

Write the body in the user's conversation language unless they ask otherwise. Keep filenames and headings in English.

- `Purpose`: state the discovered desired outcome, not merely the initial request.
- `Context`: only facts whose absence would likely cause a later agent to make the wrong judgment after context reset, such as explicit constraints, agreed libraries/frameworks, environment facts, important investigation findings, and relevant current state.
- `Direction`: high-level judgment guidance for the later agent, such as agreed direction, important boundaries, and things to avoid. Prefer short prose; use bullets only when clearer. Do not prescribe unnecessary step-by-step implementation.
- `Completion Conditions`: bullet points only. Describe the observable state that should be true when the work is complete; if a later agent followed them until all are true, the desired outcome should be achieved. Do not turn them into a task list. Do not add a separate testing section.
