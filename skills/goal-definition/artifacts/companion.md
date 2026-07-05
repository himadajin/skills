# Companion Files

A companion file owns one decision area that would otherwise bloat `design.md`.
Refine a settled `design.md` into one companion at a time. `ui.md` and
`verification.md` are the provided companions; for another separable decision
area, reuse this same contract with a natural English kebab-case filename, for
example `api.md` or `data-model.md`.

## Sections

Use `Purpose`, `Context`, `Direction`, and `Completion Conditions`. Exclude
`Related Files`.

- `Purpose`: the companion's outcome in its own terms — user-facing for
  `ui.md`, quality-facing for `verification.md` — not implementation design.
- `Context`: facts that shape judgment in the owned decision area. Name the
  `design.md` this companion complements.
- `Direction`: high-level judgment guidance for the owned decision area only.
  Do not duplicate decisions from `design.md`.
- `Completion Conditions`: the observable state for the owned decision area,
  including behavior that must be verified when that verification is central to
  the companion.

## Judgment

- Treat as a marker any companion-owned decision that would change the later
  deliverable's quality, boundaries, or outcome if left to the implementation
  agent.
- Ask only when the answer would materially reduce downstream guesswork for
  this companion. Ground recommendations in repo investigation, existing
  conventions, product context, and practical constraints.
- Keep implementation design decisions in `design.md`. If companion exploration
  invalidates the implementation design, return to the `design.md` artifact
  instead of rewriting it here.
- Preserve concrete companion decisions when they matter, but do not convert
  them into a task list. Leave details undecided when deciding them now would
  add little value.

Prompts for finding markers — not a checklist; use one only when it reveals a
high-impact undecided point:

- Which concern does this companion own, and what must stay out of `design.md`
  to avoid duplication?
- For `ui.md`: would screen structure, information hierarchy, visual tone,
  density, color behavior, component library or design-system convention,
  interaction priority, or responsive and accessibility expectations change
  whether the result is judged correct? Target users, surfaces, workflows, and
  brand or content constraints belong in `Context`.
- For `verification.md`: would the verification boundary, deterministic
  controls, fixture shape, CI/manual balance, or evaluation criteria change
  whether the result can be trusted? Important risks, existing tests, external
  dependencies, and CI constraints belong in `Context`.
- For any companion: which existing project conventions should shape it, and
  which observable completion conditions belong here rather than in
  `design.md`?

## Closing

Close when the remaining markers could not change the companion's `Direction`
or `Completion Conditions`, or are preserved as decision-relevant unknowns in
`Context`. The default closing action is to write the companion to the proposed
path and update `design.md` only to list it in `Related Files`. At the gate,
offer another companion while a separate decision area would still materially
reduce downstream guesswork.
