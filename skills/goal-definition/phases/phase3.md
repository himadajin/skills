# PHASE3

Refine a `design.md` into one selected companion file without duplicating
implementation design.

## Judgment

- Treat as an upstream Branch any companion-owned decision that would change the
  later deliverable's quality, boundaries, or implementation outcome if left to
  the implementation agent.
- Ask only when the answer would materially reduce downstream guesswork for the
  selected companion file.
- Prefer recommendations grounded in repo investigation, existing conventions,
  product context, and practical implementation constraints.
- Keep implementation design decisions in `design.md`; if companion exploration
  invalidates the implementation design, return to PHASE2 instead of rewriting
  `design.md` during PHASE3.
- Preserve concrete companion decisions when they matter, but do not convert
  them into a task list.
- Leave details undecided when deciding them now would add little value or
  narrow the user's intent prematurely.

Useful prompts for judgment:

- Which concern does the selected companion own, and what must stay out of
  `design.md` to avoid duplication?
- What decisions would materially improve handoff quality if captured
  separately?
- Which existing project conventions or constraints should shape this companion
  file?
- Which observable completion conditions belong in this companion rather than in
  `design.md`?

These prompts are not a checklist. Use them only when they reveal the most
upstream unresolved Branch.

## Closing PHASE3

Close this phase only when the selected companion file would be self-contained
enough for a later coding agent to act without guessing about that companion's
owned concern, or when remaining unknowns are explicitly preserved as
decision-relevant context.

Before writing the companion file, apply the Confirmation Gate. The choice must
be between continuing to refine the companion definition and writing the
companion file now.

When writing a companion file, also update `design.md` only to reference that
file in `Related Files`. Do not edit the implementation design body during
PHASE3.
