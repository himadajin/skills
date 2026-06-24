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
- Ask one question per user turn. Prefer a question that helps the user expand,
  correct, or sharpen the active Branch.
- Include a recommended answer that states the decision content that would enter
  the active artifact if adopted. Give a concise reason explaining what the
  answer would settle in the Root or active artifact.
- When asking the user to decide, expose the choice surface: the current read,
  the meaningful tradeoff or alternative space, and room for the user to choose,
  revise, or add an option.
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
`PHASE3` when the user supplies the artifact that phase needs. A phase that
names an input artifact begins only from that artifact. Move from one phase to
the next through the Confirmation Gate.

## Confirmation Gate

Use a confirmation gate before closing a phase, moving to the next phase, or
writing an artifact. Ask one narrow question in the user's conversation
language. The question must include:

- what the current phase has defined;
- the recommended next action and reason;
- how the active artifact will be handled;
- the proposed path when writing a file;
- an explicit choice to continue refining, close the phase, move to the next
  phase, or write the active artifact.

When proposing a path without a user-specified destination, use
`docs/<filename>` where `<filename>` is the active artifact filename:
`purpose.md`, `design.md`, `ui.md`, or `verification.md`. If that path would
collide with an existing file or multiple handoffs need separation, prefix the
filename with a natural English kebab-case topic while keeping the artifact
filename at the end.

Proceed after the user confirms the chosen action and any proposed path.

## Writing Artifacts

- Write only the active artifact and path confirmed through the Confirmation
  Gate.
- Write one active artifact at a time.
- Follow the active format file exactly.
- In PHASE3, when writing the selected companion file, also update `design.md`
  only to reference the companion in `Related Files`.
