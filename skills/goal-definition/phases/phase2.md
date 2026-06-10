# PHASE2

Refine a written `purpose.md` into a practical, self-contained `design.md` without turning it into step-by-step implementation instructions.

## Judgment

- Treat as an upstream Branch any realization decision that would change the later deliverable's shape, verifiability, dependencies, or separation boundaries if left to the implementation agent.
- Ask only when the answer would materially reduce downstream guesswork.
- Prefer recommendations grounded in repo investigation, existing project conventions, and practical constraints.
- Preserve concrete realization decisions when they matter, but do not convert them into a task list.
- Leave details undecided when deciding them now would add little value or narrow the user's intent prematurely.

Useful prompts for judgment:

- Would a concrete tool or library choice change the dependency surface or implementation shape?
- Would an established library, framework, or development environment materially reduce risk compared with leaving the choice to the implementation agent?
- Which behavior must be verified for the work to count as complete?
- Does randomness, time, ordering, or external input need deterministic control to make the result testable?
- Should reusable core logic be separated from UI, CLI, or external-service wrappers?
- Would Unix-style composition, pure-function boundaries, or explicit separation between logic and presentation make important behavior easier to test or reason about?
- Is there processing that should be explicitly testable instead of only exercised through an end-to-end surface?
- Should formatter, linter, or automated test expectations be part of the handoff for this kind of work?

These prompts are not a checklist. Use them only when they reveal the most upstream unresolved Branch.

## Closing PHASE2

Close this phase only when `design.md` would be self-contained enough for a later coding agent to act without guessing about shape, verification, dependencies, or boundaries, or when remaining unknowns are explicitly preserved as decision-relevant context.

Before writing `design.md`, apply the Finalization rule. The choice must be between continuing to refine the handoff and writing `design.md` now.
