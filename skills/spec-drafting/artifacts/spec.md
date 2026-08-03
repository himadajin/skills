# spec.md

Refine the purpose brief into a first-draft specification:
a durable, present-tense description of what the software is and how it behaves.
It is the source of truth that outlives the prototype —
later work updates it as the prototype teaches —
and it must stand alone:
it never references the implementation plan.

## Sections

Use `Purpose`, `Context`, `Related Files`, `Specification`, and `Open Questions`.
Exclude `Direction`.

- `Purpose`: the target outcome and whom it serves.
- `Context`: explicit constraints, environment facts,
  important investigation findings, relevant current state,
  and realization decisions meant to hold beyond the prototype.
- `Related Files`: companion files in the same directory, or `- None`.
  Keep companion-owned decisions out of `spec.md`;
  never list the implementation plan.
- `Specification`: the software's observable behavior, interfaces,
  data shapes, and boundaries,
  stated in present tense as fact about the target software.
  A first draft is expected to be incomplete;
  prefer an honest open question over invented detail.
- `Open Questions`: undecided points later work must resolve —
  above all the uncertainties the prototype exists to answer.

## Judgment

- Treat as a marker any decision that would change what the software is —
  its behavior, interfaces, data, or boundaries —
  if left to the implementation agent.
- Sort realization decisions by lifetime:
  a decision that should still hold after the prototype belongs here;
  a decision made only to keep the prototype cheap
  belongs in the implementation plan.
- Ask only when the answer would materially reduce downstream guesswork.
  Ground recommendations in repo investigation,
  existing project conventions, and practical constraints.
- Leave details undecided when deciding them now would add little value
  or narrow the user's intent prematurely;
  record the valuable ones as `Open Questions`.

Prompts for finding markers — not a checklist;
use one only when it reveals a high-impact undecided point:

- Which observable behavior defines the software —
  what would a user see it do?
- Which interface or data shape would be costly to change after the prototype?
- Is a tool or library choice part of the software's identity,
  or only prototype convenience that belongs in the plan?
- Should reusable core logic be separated
  from UI, CLI, or external-service wrappers?
- Which uncertainty should the prototype answer,
  and is it recorded as an open question?

## Closing

Close when the remaining markers could not change `Specification`,
or are preserved as `Open Questions`.
The default closing action is to write `spec.md` to `docs/specs/<topic>/spec.md`.
After writing,
offer a companion for a decision area that would otherwise bloat `spec.md`,
or move to the implementation plan.
