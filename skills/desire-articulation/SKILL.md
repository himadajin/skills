---
name: desire-articulation
description: >-
  Use only for an explicit interview-style clarification phase for a software development task whose output is a standalone desire.md or equivalent handoff brief for a later coding agent. Trigger when the user asks to be questioned, articulate an unclear development desire, create/capture a desire file before implementation, or refine an existing desire.md through an explicit PHASE2 interview. First articulate the underlying desire, then refine how it should be realized without prescribing step-by-step implementation. Do NOT use for ordinary clarification, planning, plan.md creation, code review, issue execution, debugging, prompt writing, prose editing, brainstorming, non-development goals, or when an existing plan/desire/spec/issue/task list should simply be implemented, followed, reviewed, revised, or continued.
---

# Desire Articulation

Interview the user until their underlying development desire and its practical realization are clear enough to write a standalone `desire.md` for a later coding agent. Treat the initial request as a hypothesis and preserve the user's real intent without locking in unnecessary step-by-step implementation.

## Activation Gate

Use only when all are true:

- Software development work.
- Intent is unresolved.
- User wants interview/guided clarification.
- Final output is `desire.md` or an equivalent handoff brief.

Do not activate merely because a request is vague, high-level, asks "what should we check?", or needs ordinary clarification. If a `plan.md`, `desire.md`, issue, PR, task list, spec, or implementation brief is already the source of truth, read that artifact and proceed with the ordinary implementation, review, revision, or debugging workflow instead of using Root/Branch/Leaf framing or creating a new handoff brief. Activate only if the user explicitly asks to restart desire articulation from scratch, replace the prior source of truth with a new desire brief, be interviewed again before implementation, or refine a provided `desire.md` from `PHASE2`.

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
- Before stopping, switching phase, or writing the file, ask a narrow confirmation question so the user explicitly chooses whether to continue or finish.

When asking after investigation, first share one or two short sentences with the useful finding that frames the question. Do not dump research notes.

Branch examples include completion feeling, constraints, non-goals, audience, handoff boundaries, and direction-changing tradeoffs. These are examples, not a checklist; ask about them only when they could change the Root or the final brief. Avoid questions answerable from the repo/docs, implementation means before purpose, or low-value facts that are merely nice to record.

## Phases

Use the same Root/Branch/Leaf question model in both phases. The phases exist only to protect the boundary between understanding the desire and making it practical.

- `PHASE1`: articulate the desire itself; follow [phases/phase1.md](phases/phase1.md).
- `PHASE2`: refine how the desire should be realized; follow [phases/phase2.md](phases/phase2.md).

Load only the phase file needed for the current interview:

- Start with `phases/phase1.md` by default.
- Start with `phases/phase2.md` only when the user provides an existing `desire.md` and explicitly asks to begin from `PHASE2`.
- If the user chooses to continue from `PHASE1` to `PHASE2`, load `phases/phase2.md` then.

## Finalization

Stop asking only when the active phase's rule file says the interview is ready to close and the user's own questions about what they want are resolved enough to proceed.

Before writing the file, ask one narrow confirmation question so the user controls when refinement stops. For example:

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
- `Context`: only facts whose absence would likely cause a later agent to make the wrong judgment after context reset, such as explicit constraints, agreed libraries/frameworks, environment facts, important investigation findings, relevant current state, and unresolved but decision-relevant realization choices.
- `Direction`: high-level judgment guidance for the later agent, such as agreed direction, important boundaries, concrete realization choices, and things to avoid. Prefer short prose; use bullets only when clearer. Do not prescribe unnecessary step-by-step implementation.
- `Completion Conditions`: bullet points only. Describe the observable state that should be true when the work is complete, including behavior that must be verified when that verification is central to the desire; if a later agent followed them until all are true, the desired outcome should be achieved. Do not turn them into a task list. Do not add a separate testing section.
