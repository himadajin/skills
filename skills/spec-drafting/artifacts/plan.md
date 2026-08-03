# Implementation Plan

A disposable prompt for the coding agent that builds the prototype, written
after `spec.md` is settled. It exists to be deleted: once the prototype is
built and the spec updated, removing `docs/plans/<topic>.md` must lose nothing
durable. No other file references it.

## Format

The plan does not use the shared artifact format. Write it as direct
instructions to a context-reset coding agent in the user's conversation
language, opening with:

- a note that this file is disposable and may be deleted once the prototype is
  built and the spec updated;
- the instruction to read `docs/specs/<topic>/spec.md` — and the companions
  its `Related Files` lists — as the source of truth.

Then include only prototype-specific content, such as:

- scope cuts: what to stub, fake, or skip for this prototype;
- throwaway choices made only to keep the prototype cheap;
- how to run and check the prototype;
- the feedback instruction: record what the prototype reveals by updating the
  spec — resolving `Open Questions` and correcting `Specification` — never by
  turning this file into documentation.

## Judgment

- Never restate spec content; reference it by path. If drafting the plan
  surfaces a decision that should hold beyond the prototype, return to the
  `spec.md` artifact and record it there.
- Treat as a marker any prototype-scoping decision — a cut, a stub, a
  throwaway choice — that would change what the prototype can teach if left to
  the implementation agent.
- Keep the plan as short as the prototype allows: it is a prompt, not
  documentation. Do not prescribe step-by-step tasks unless ordering genuinely
  matters.

## Closing

Close when the plan plus the spec would let a context-reset agent build the
prototype without guessing about scope. The default closing action is to write
the plan to `docs/plans/<topic>.md`, updating no other file.
