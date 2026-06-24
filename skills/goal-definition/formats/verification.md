# verification.md Format

Use this format for PHASE3 only. `verification.md` complements `design.md`: it
owns verification strategy so those details are not duplicated in `design.md`.

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

- `Purpose`: state the verification outcome in quality-facing terms, not the
  implementation design or a test implementation task.
- `Context`: only facts whose absence would likely cause a later agent to make
  the wrong verification judgment after context reset, such as important risks,
  existing tests, external dependencies, fixture needs, deterministic controls,
  CI constraints, manual-check constraints, and unresolved but decision-relevant
  verification choices.
- `Direction`: high-level verification judgment guidance for the later agent,
  such as what to verify, which boundaries to verify at, important cases,
  reproducibility expectations, and how to balance automated tests, manual
  checks, CI, or evaluation. Prefer short prose; use bullets only when clearer.
  Do not duplicate product completion conditions from `design.md` or prescribe
  test implementation steps.
- `Completion Conditions`: bullet points only. Describe the observable
  verification strategy state that should be true when the work is complete,
  including behavior that must be verified when that verification is central to
  the handoff; if a later agent followed them until all are true, the target
  verification outcome should be achieved. Do not turn them into a task list. Do
  not add a separate testing section.
