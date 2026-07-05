# Purpose Brief

Define what the user wants and why before deciding how it should be realized.
The draft lives in conversation; `purpose.md` is written only when the user
asks for it, the brief is the stopping point, or a separate handoff or context
reset needs a persistent file.

## Sections

Use `Purpose`, `Context`, and `Direction`. Exclude `Related Files` and
`Completion Conditions`.

- `Purpose`: the discovered target outcome, including whom it serves when that
  shapes it.
- `Context`: explicit constraints, non-goals, audience, handoff boundaries,
  important investigation findings, relevant current state, and unresolved but
  decision-relevant purpose-level unknowns.
- `Direction`: the intended direction, boundaries, and things to avoid —
  without implementation means, step-by-step tasks, or completion conditions.

## Judgment

- Keep the draft about the user's target state, not the initial wording of the
  request.
- Do not steer toward an early technical shape, framework, library,
  architecture, verification method, or task sequence. In the first draft, mark
  every interpretive leap beyond the user's words as `[UNRESOLVED]`.
- If the user names an implementation detail early, capture the purpose or
  constraint it represents before accepting it as direction.
- Treat constraints, non-goals, audience, and handoff boundaries as unresolved
  markers only when they could change the purpose itself.

## Closing

Close when no remaining marker could change what the purpose is — only how it
might be realized. The default closing action is to keep the brief in
conversation and move to `design.md`. When writing `purpose.md`, propose the
path at the gate.
