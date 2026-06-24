# purpose.md Format

Use this format for PHASE1 only. `purpose.md` preserves what the user wants
without turning it into implementation design.

The file must contain exactly these English headings, in this order:

```md
# <Short Title>

## Purpose

## Context

## Direction
```

Write the body in the user's conversation language unless they ask otherwise.
Keep filenames and headings in English.

- `Purpose`: state the discovered target outcome, not merely the initial
  request.
- `Context`: only facts whose absence would likely cause a later agent to
  misunderstand the purpose after context reset, such as explicit constraints,
  non-goals, audience, handoff boundaries, important investigation findings,
  relevant current state, and unresolved but decision-relevant purpose-level
  unknowns.
- `Direction`: high-level guidance that preserves the purpose, such as the
  intended direction, boundaries, and things to avoid. Prefer short prose; use
  bullets only when clearer. Do not prescribe unnecessary implementation means,
  step-by-step tasks, or completion conditions.
