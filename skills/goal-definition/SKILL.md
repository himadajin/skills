---
name: goal-definition
description: >-
  Interview the user to define software-development goals and handoff artifacts such as purpose.md, design.md, or one companion file before implementation. Use only when the user explicitly requests this skill or a goal-definition interview.
---

# Goal Definition

Define a software-development goal through an interview before implementation.
Keep the work in definition mode: clarify the purpose, shape the selected
handoff artifact, and leave implementation work for a later task.

The essential work is the interview loop and the phase artifact contract.

## Core Loop

- Read enough existing context to ask a better next question: the user's linked
  artifact, relevant repository docs/code/configs, and current phase artifacts.
  Use external research when outside knowledge materially changes the handoff.
- Treat a user-provided `plan.md`, `purpose.md`, `design.md`, `ui.md`,
  `verification.md`, issue, task list, spec, or implementation brief as the
  current source for the definition work.
- Maintain `Root` / `Branch` / `Leaf` as an internal model for choosing the next
  question:
  - `Root`: the target state or unresolved question the user is trying to
    define.
  - `Branch`: an upstream decision or ambiguity that could change the Root or
    the active artifact.
  - `Leaf`: wording or detail inside the active artifact.
- Ask about the most upstream unresolved Branch whose answer could change the
  active artifact.
- Ask one question per user turn. Include a recommended answer and a concise
  reason. Frame the recommendation as a hypothesis for the user to accept,
  reject, or revise.
- When investigation frames the question, share the useful finding in one or two
  short sentences before asking.
- If the user wants to finish with remaining ambiguity, preserve
  decision-relevant unknowns in the artifact's `Context` and use `Direction` to
  guide the later agent.

## Phases

Each phase defines one artifact contract. Choose the active phase from the
current user request and available artifact:

- `PHASE1`: define the purpose brief. Read [phases/phase1.md](phases/phase1.md)
  and [formats/purpose.md](formats/purpose.md).
- `PHASE2`: refine a confirmed purpose brief or `purpose.md` into self-contained
  `design.md`. Read [phases/phase2.md](phases/phase2.md) and
  [formats/design.md](formats/design.md).
- `PHASE3`: refine `design.md` into one selected companion file. Read
  [phases/phase3.md](phases/phase3.md) and the selected companion format:
  [formats/ui.md](formats/ui.md) or
  [formats/verification.md](formats/verification.md).

Begin with `PHASE1` when the current phase is unclear. Begin from `PHASE2` or
`PHASE3` when the user supplies the artifact that phase needs. Move from one
phase to the next through the Confirmation Gate.

## Confirmation Gate

Use a confirmation gate before closing a phase, moving to the next phase, or
writing an artifact. Ask one narrow question in the user's conversation
language. The question must include:

- what the current phase has defined;
- the recommended next action and reason;
- an explicit choice to continue refining, close the phase, move to the next
  phase, or write the active artifact.

Proceed after the user confirms the chosen action.

## Writing Artifacts

- Write one active artifact at a time.
- Follow the active format file exactly.
- Use a user-specified path when provided. Otherwise create `docs/` as needed
  and write a natural English kebab-case filename that identifies the phase and
  topic.
- Choose the filename yourself from the artifact purpose.
- Keep a PHASE1 purpose brief in conversation when the user continues directly
  to PHASE2. Persist `purpose.md` when the user asks for it, PHASE1 closes as
  the stopping point, or a handoff/context reset needs a file.
- Write `design.md` before entering PHASE3.
- In PHASE3, write the selected companion file and update `design.md` only to
  reference the companion in `Related Files`.
- After writing `design.md`, recommend PHASE3 for a companion concern that would
  materially reduce downstream guesswork. List created companion files in
  `Related Files`; use `- None` when none exist.
