# ui.md Format

Use this format for PHASE3 only. `ui.md` complements `design.md`: it owns
UI-specific decisions so those details are not duplicated in `design.md`.

The file must contain exactly these English headings, in this order:

```md
# <Short Title>

## Purpose

## Context

## Direction

## Completion Conditions
```

Write the body in the user's conversation language unless they ask otherwise.
Keep filenames and headings in English.

- `Purpose`: state the UI outcome in user-facing terms, not the implementation
  design or the initial request.
- `Context`: only facts whose absence would likely cause a later agent to make
  the wrong UI judgment after context reset, such as target users, surfaces,
  workflows, existing design conventions, brand constraints, content
  constraints, and unresolved but decision-relevant UI choices.
- `Direction`: high-level UI judgment guidance for the later agent, such as
  screen structure, information hierarchy, interaction model, visual tone,
  density, color behavior, component expectations, responsive behavior,
  accessibility expectations, and things to avoid. Prefer short prose; use
  bullets only when clearer. Do not duplicate non-UI implementation decisions
  from `design.md`.
- `Completion Conditions`: bullet points only. Describe the observable UI state
  that should be true when the work is complete, including behavior that must be
  verified when that verification is central to the UI definition; if a later
  agent followed them until all are true, the target UI outcome should be
  achieved. Do not turn them into a task list. Do not add a separate testing
  section.
