---
name: goal-definition
description: >-
  Interview the user to define software-development goals and draft handoff artifacts — purpose.md, design.md, and companion files such as ui.md or verification.md — before implementation. Use only when the user explicitly requests this skill or a goal-definition interview.
---

# Goal Definition

Define a software-development goal through an interview before implementation.
Keep the work in definition mode: clarify the purpose, shape the handoff
artifacts, and leave implementation work for a later task.

The interview is draft-driven: the active artifact draft is the shared working
state, shown and updated in conversation. Progress is a decision entering the
draft, not a question asked.

## Core Loop

1. Read enough context to draft: the user's request, any supplied artifact, and
   relevant repository docs/code/configs. Use external research only when
   outside knowledge would materially change the handoff.
2. As soon as the active artifact has enough content to draft — normally
   within one or two turns of its becoming active — show it as an
   in-conversation draft in the artifact format. Mark each undecided point
   inline with `[UNRESOLVED: <short question>]`, keeping the keyword in
   English and the question in the body language. Introduce your own interpretations and
   defaults as markers or named recommendations, never as silent decisions.
3. Ask one question per user turn, aimed at the unresolved marker whose answer
   would change the most of the draft; defer wording-level detail until no such
   marker remains. Resolve markers in `Purpose` and `Context` before markers in
   `Direction` and `Completion Conditions`.
4. Match the question to its kind:
   - A decision question chooses among alternatives. Include a recommended
     answer stating the text that would enter the draft if adopted, a concise
     reason, and room to choose, revise, or add an option.
   - An elicitation question asks for facts only the user can supply. Ask
     plainly; do not invent a recommendation.
   When investigation shaped the question, share the finding in one or two
   short sentences before asking. When no local signal grounds a
   recommendation, say it rests on general practice.
5. Do not ask when no plausible answer would change the draft: adopt the
   recommendation into the draft and note it.
6. After each answer, show the changed sections — or the whole draft when it is
   short — with the remaining markers.
7. Propose closing the artifact when the remaining markers could not change its
   `Direction` or `Completion Conditions`. A remaining marker that belongs to a
   later artifact moves into that artifact's first draft. When the user
   finishes early, convert remaining markers into decision-relevant unknowns in
   `Context` and use `Direction` to guide the later agent.

## Artifacts

The interview moves through up to three artifacts. Read the artifact file when
it becomes active, or before proposing it at a gate:

- Purpose brief — [artifacts/purpose.md](artifacts/purpose.md): what the user
  wants and why.
- `design.md` — [artifacts/design.md](artifacts/design.md): the self-contained
  implementation handoff.
- Companion files — [artifacts/companion.md](artifacts/companion.md): one file
  per decision area that would otherwise bloat `design.md`, such as `ui.md` or
  `verification.md`.

Choose the starting artifact from the user's input:

- No input artifact: start the purpose brief.
- An input supplied as settled groundwork starts the artifact it feeds: a
  confirmed purpose brief or `purpose.md` — or an issue, spec, or task list
  treated as one — starts `design.md`; a settled `design.md` starts a
  companion.
- An input supplied for refinement becomes the current draft of its own
  artifact and keeps its path.
- When the intent is unclear, make that the first question.

Move between artifacts only through the Confirmation Gate.

## Artifact Format

Every artifact uses these English headings in this order, dropping the sections
its artifact file excludes:

```md
# <Short Title>

## Purpose

## Context

## Related Files

## Direction

## Completion Conditions
```

Write the body in the user's conversation language unless they ask otherwise.
Keep filenames, headings, and the `<Short Title>` line in English.

- `Purpose`: the discovered target outcome, not merely the initial request.
- `Context`: only facts whose absence would likely cause a context-reset agent
  to misjudge the work — explicit constraints, agreed choices, environment
  facts, important investigation findings, relevant current state, and
  decision-relevant unknowns preserved at close.
- `Related Files`: bullet points only — companion handoff files that own
  separate decision areas, or `- None`.
- `Direction`: high-level judgment guidance that preserves agreed decisions,
  boundaries, and things to avoid. Prefer short prose; use bullets only when
  clearer. Do not prescribe unnecessary implementation means or step-by-step
  tasks.
- `Completion Conditions`: bullet points only — the observable state that
  should be true when the work is complete; if a later agent made all of them
  true, the target outcome should be achieved. Not a task list; do not describe
  how to verify them or add a separate testing section.

## Confirmation Gate

Gate before writing a file or moving to another artifact, with one short
message in the user's conversation language containing:

- the current draft or its delta since last shown — before writing a file,
  show in full any section the user has never seen in full;
- the recommended next action with a concise reason, and the proposed path when
  writing a file;
- an explicit invitation to correct the draft or choose another available
  action.

Offer only actions actually available from the current state. When an answer's
draft update and a gate fall on the same turn, one combined message showing the
delta serves both. Proceed after the user confirms the action and any path.

## Writing Artifacts

- Write only the artifact, action, and path confirmed through the gate, one
  artifact at a time, following its artifact file exactly.
- A written artifact contains no `[UNRESOLVED]` markers: each is resolved or
  converted into a decision-relevant unknown in `Context`.
- A file supplied for refinement is rewritten at its own path by default;
  confirm the overwrite — and the restructuring into the artifact format it
  implies — at the gate.
- Otherwise propose `docs/<filename>` where `<filename>` is the artifact
  filename. If the path would collide or multiple handoffs need separation,
  prefix a natural English kebab-case topic while keeping the artifact filename
  at the end.
- When writing a companion, also update `design.md` only to list the companion
  in `Related Files`.
