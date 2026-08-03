# Companion Files

A companion file owns one spec-side decision area that would otherwise bloat
`spec.md`. Refine a settled `spec.md` into one companion at a time. Companions
live in the spec's directory and share its lifecycle: durable, and never
referencing the implementation plan. `ui.md` and `verification.md` are the
provided companions; for another separable decision area, reuse this same
contract with a natural English kebab-case filename, for example `api.md` or
`data-model.md`.

## Sections

Use `Purpose`, `Context`, `Specification`, and `Open Questions`. Exclude
`Direction` and `Related Files`.

- `Purpose`: the companion's outcome in its own terms — user-facing for
  `ui.md`, quality-facing for `verification.md` — not implementation design.
- `Context`: facts that shape judgment in the owned decision area.
- `Specification`: the owned decision area stated in present tense — for
  `ui.md`, the screens, hierarchy, and interaction behavior; for
  `verification.md`, what is verified and how trust is established. Do not
  duplicate decisions from `spec.md`.
- `Open Questions`: undecided points in the owned decision area, especially
  those the prototype should answer.

## Judgment

- Treat as a marker any companion-owned decision that would change the later
  deliverable's quality, boundaries, or outcome if left to the implementation
  agent.
- Ask only when the answer would materially reduce downstream guesswork for
  this companion. Ground recommendations in repo investigation, existing
  conventions, product context, and practical constraints.
- Keep whole-software decisions in `spec.md`. If companion exploration
  invalidates part of the spec, return to the `spec.md` artifact instead of
  rewriting it here.
- Leave details undecided when deciding them now would add little value;
  record the valuable ones as `Open Questions`.

Prompts for finding markers — not a checklist; use one only when it reveals a
high-impact undecided point:

- Which concern does this companion own, and what must stay out of `spec.md`
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
  which parts of its area does the prototype exist to answer?

## Closing

Close when the remaining markers could not change the companion's
`Specification`, or are preserved as `Open Questions`. The default closing
action is to write the companion beside `spec.md` in `docs/specs/<topic>/` and
update `spec.md` only to list it in `Related Files`. At the gate, offer
another companion while a separate decision area would still materially reduce
downstream guesswork, or move to the implementation plan.
