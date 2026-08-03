---
name: spec-drafting
description: >-
  Interview the user to draft a first-draft specification
  and a disposable prototype implementation plan before implementation.
  Invoke only on the user's explicit request.
disable-model-invocation: true
---

# Spec Drafting

Draft a durable first-draft specification
and a disposable prototype implementation plan
through an interview, before implementation.
Keep the work in definition mode:
clarify the purpose, shape the artifacts,
and leave implementation work for a later task.

The interview is draft-driven:
the active artifact draft is the shared working state,
shown and updated in conversation.
Progress is a decision entering the draft, not a question asked.

## Core Loop

1. Read enough context to draft:
   the user's request, any supplied artifact,
   and relevant repository docs/code/configs.
   Use external research only when outside knowledge
   would materially change the artifacts.
2. As soon as the active artifact has enough content to draft —
   normally within one or two turns of its becoming active —
   show it as an in-conversation draft in the artifact format.
   Mark each undecided point inline with `[UNRESOLVED: <short question>]`,
   keeping the keyword in English and the question in the body language.
   Introduce your own interpretations and defaults
   as markers or named recommendations, never as silent decisions.
3. Ask one question per user turn,
   aimed at the unresolved marker whose answer would change the most of the draft;
   defer wording-level detail until no such marker remains.
   Resolve markers in `Purpose` and `Context` before markers in later sections.
4. Match the question to its kind:
   - A decision question chooses among alternatives.
     Include a recommended answer
     stating the text that would enter the draft if adopted,
     a concise reason, and room to choose, revise, or add an option.
   - An elicitation question asks for facts only the user can supply.
     Ask plainly; do not invent a recommendation.
   When investigation shaped the question,
   share the finding in one or two short sentences before asking.
   When no local signal grounds a recommendation,
   say it rests on general practice.
5. Do not ask when no plausible answer would change the draft:
   adopt the recommendation into the draft and note it.
6. After each answer, show the changed sections —
   or the whole draft when it is short — with the remaining markers.
7. Propose closing the artifact when its artifact file's closing condition holds.
   A remaining marker that belongs to a later artifact
   moves into that artifact's first draft.
   When the user finishes early,
   preserve remaining markers as `Open Questions` entries
   or decision-relevant unknowns in `Context`.

## Artifacts

The interview moves through these artifacts in order.
Read the artifact file when it becomes active,
or before proposing it at a gate:

- Purpose brief — [artifacts/purpose.md](artifacts/purpose.md):
  what the user wants and why.
  Lives only in conversation; never written to a file.
- `spec.md` — [artifacts/spec.md](artifacts/spec.md):
  the durable first-draft specification.
- Companion files — [artifacts/companion.md](artifacts/companion.md):
  one file per spec-side decision area that would otherwise bloat `spec.md`,
  such as `ui.md` or `verification.md`.
- Implementation plan — [artifacts/plan.md](artifacts/plan.md):
  the disposable prototype prompt, drafted last.

Two lifecycles, one dependency direction:
everything under `docs/specs/` is durable and outlives the prototype;
`docs/plans/` is disposable and deleted once the prototype is built.
The plan reads the spec;
the spec and its companions never reference the plan.
Deleting a plan must lose nothing durable.

Choose the starting artifact from the user's input:

- No input artifact: start the purpose brief.
- An input supplied as settled groundwork starts the artifact it feeds:
  a settled purpose — or an issue, spec sketch, or task list treated as one —
  starts `spec.md`;
  a settled `spec.md` starts a companion or the implementation plan.
- An input supplied for refinement
  becomes the current draft of its own artifact and keeps its path.
- When the intent is unclear, make that the first question.

Move between artifacts only through the Confirmation Gate.
Propose the implementation plan only after `spec.md` is written.

## Artifact Format

Every artifact except the implementation plan
uses these English headings in this order,
dropping the sections its artifact file excludes;
the plan uses the prompt format in its artifact file:

```md
# <Short Title>

## Purpose

## Context

## Direction

## Related Files

## Specification

## Open Questions
```

Write the body in the user's conversation language unless they ask otherwise.
Keep filenames, headings, and the `<Short Title>` line in English.

- `Purpose`: the discovered target outcome, not merely the initial request.
- `Context`: only facts whose absence would likely cause
  a context-reset agent to misjudge the work —
  explicit constraints, agreed choices, environment facts,
  important investigation findings, relevant current state;
  in artifacts without `Open Questions`,
  also decision-relevant unknowns preserved at close.
- `Direction`: high-level judgment guidance —
  intended direction, boundaries, and things to avoid.
  Prefer short prose; use bullets only when clearer.
- `Related Files`: bullet points only —
  companion files in the same directory, or `- None`.
  Never the implementation plan.
- `Specification`: what the software is and how it behaves,
  written in present tense as durable fact —
  observable behavior, interfaces, data, and boundaries.
  Not a task list and not completion criteria.
- `Open Questions`: bullet points only —
  undecided points that later work must resolve,
  especially those the prototype exists to answer.

## Confirmation Gate

Gate before writing a file or moving to another artifact,
with one short message in the user's conversation language containing:

- the current draft or its delta since last shown —
  before writing a file,
  show in full any section the user has never seen in full;
- the recommended next action with a concise reason,
  and the proposed path when writing a file;
- an explicit invitation to correct the draft
  or choose another available action.

Offer only actions actually available from the current state.
When an answer's draft update and a gate fall on the same turn,
one combined message showing the delta serves both.
Proceed after the user confirms the action and any path.

## Writing Artifacts

- Write only the artifact, action, and path confirmed through the gate,
  one artifact at a time, following its artifact file exactly.
  The purpose brief is never written to a file.
- A written artifact contains no `[UNRESOLVED]` markers:
  each is resolved or preserved as an `Open Questions` entry.
- Default paths: `spec.md` at `docs/specs/<topic>/spec.md`,
  companions beside it in the same directory,
  and the implementation plan at `docs/plans/<topic>.md`,
  where `<topic>` is a natural English kebab-case topic proposed at the gate.
- A file supplied for refinement is rewritten at its own path by default;
  the gate confirms the overwrite
  and the restructuring into the artifact format it implies.
- When writing a companion,
  also update `spec.md` only to list the companion in `Related Files`.
  When writing the plan, update no other file.
