# PHASE3

Refine a GUI-bearing `design.md` into a self-contained `ui.md` without duplicating implementation design.

## Judgment

- Treat as an upstream Branch any UI decision that would change the later deliverable's information architecture, visual direction, interaction model, responsive behavior, state handling, or accessibility expectations if left to the implementation agent.
- Ask only when the answer would materially reduce downstream UI guesswork.
- Prefer recommendations grounded in repo investigation, existing UI conventions, design systems, product context, and practical implementation constraints.
- Keep non-UI implementation decisions in `design.md`; if UI exploration invalidates the implementation design, return to PHASE2 instead of rewriting `design.md` during PHASE3.
- Preserve concrete UI decisions when they matter, but do not convert them into a task list.
- Leave details undecided when deciding them now would add little value or narrow the user's intent prematurely.

Useful prompts for judgment:

- Which screens, panels, or surfaces must exist for the core workflow to make sense?
- What should the user see first, compare, edit, confirm, or recover from?
- Which states matter: empty, loading, partial, error, success, disabled, selected, focused, or destructive?
- What visual tone, density, color behavior, and component style would fit the product and audience?
- Which layout changes are required across mobile, tablet, desktop, or constrained containers?
- Which accessibility expectations would materially affect structure, semantics, focus, contrast, or input behavior?

These prompts are not a checklist. Use them only when they reveal the most upstream unresolved Branch.

## Closing PHASE3

Close this phase only when `ui.md` would be self-contained enough for a later coding agent to act without guessing about UI structure, visual direction, interaction states, responsive behavior, accessibility expectations, or completion quality, or when remaining unknowns are explicitly preserved as decision-relevant context.

Before writing `ui.md`, apply the Finalization rule. The choice must be between continuing to refine the UI definition and writing `ui.md` now.

When writing `ui.md`, also update `design.md` only to reference `ui.md` in `Related Files`. Do not edit the implementation design body during PHASE3.
