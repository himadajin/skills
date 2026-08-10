# design.md

Refine a purpose brief or `purpose.md` into a self-contained `design.md`:
handed to a context-reset coding agent without the conversation, it should be
enough to implement the work without guessing about purpose, shape,
verification, dependencies, or boundaries — without becoming step-by-step
implementation instructions.

## Sections

Use all five sections.

- `Purpose`: the target outcome in implementation-facing terms.
- `Context`: explicit constraints, agreed libraries and frameworks, environment
  facts, important investigation findings, relevant current state, and
  unresolved but decision-relevant realization choices.
- `Related Files`: companion handoff files that own separate decision areas, or
  `- None`. Keep companion-owned decisions out of `design.md`.
- `Direction`: agreed realization choices, important boundaries, dependency
  choices, testability expectations, and things to avoid. Realization decisions
  live here, not in `Completion Conditions`.
- `Completion Conditions`: the observable state that should be true when the
  work is complete, including behavior whose presence is central to the design.

## Judgment

- Treat as a marker any realization decision that would change the
  deliverable's shape, verifiability, dependencies, or separation boundaries if
  left to the implementation agent.
- Ask only when the answer would materially reduce downstream guesswork. Ground
  recommendations in repo investigation, existing project conventions, and
  practical constraints.
- Preserve concrete realization decisions when they matter, but do not convert
  them into a task list.
- Leave details undecided when deciding them now would add little value or
  narrow the user's intent prematurely.

Prompts for finding markers — not a checklist; use one only when it reveals a
high-impact undecided point:

- Would a concrete tool or library choice change the dependency surface or
  implementation shape?
- Which behavior must be verified for the work to count as complete?
- Does randomness, time, ordering, or external input need deterministic control
  to make the result testable?
- Should reusable core logic be separated from UI, CLI, or external-service
  wrappers?
- Is there processing that should be testable directly instead of only through
  an end-to-end surface?
- Should formatter, linter, or automated-test expectations be part of the
  handoff for this kind of work?

## Closing

Close when the remaining markers could not change `Direction` or `Completion
Conditions`, or are preserved as decision-relevant unknowns in `Context`. The
default closing action is to write `design.md` to the proposed path. After
writing, offer a companion for a decision area that would still materially
reduce downstream guesswork.
