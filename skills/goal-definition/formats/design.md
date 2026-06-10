# design.md Format

Use this format for PHASE2 only. `design.md` must be self-contained: if it is handed to a context-reset coding agent without `purpose.md`, the agent should still have enough context to implement the work.

The file must contain exactly these English headings, in this order:

```md
# <Short Title>

## Purpose

## Context

## Direction

## Completion Conditions
```

Write the body in the user's conversation language unless they ask otherwise. Keep filenames and headings in English.

- `Purpose`: state the target outcome in implementation-facing terms, not merely the initial request.
- `Context`: only facts whose absence would likely cause a later agent to make the wrong judgment after context reset, such as explicit constraints, agreed libraries/frameworks, environment facts, important investigation findings, relevant current state, and unresolved but decision-relevant realization choices.
- `Direction`: high-level judgment guidance for the later agent, such as agreed realization choices, important boundaries, dependency choices, testability expectations, and things to avoid. Prefer short prose; use bullets only when clearer. Do not prescribe unnecessary step-by-step implementation. Put realization decisions here, not in `Completion Conditions`.
- `Completion Conditions`: bullet points only. Describe the observable state that should be true when the work is complete, including behavior that must be verified when that verification is central to the design; if a later agent followed them until all are true, the target outcome should be achieved. Do not turn them into a task list. Do not add a separate testing section.
