---
name: desire-articulation
description: >-
  Use only for an explicit interview-style clarification phase for a software development task before implementation. In PHASE1, interview to articulate an unclear development desire and write desire.md. In PHASE2, start only from an existing desire.md when the user explicitly asks to refine realization into a self-contained design.md. Trigger when the user asks to be questioned, articulate/capture a desire file, or create/refine a design handoff from desire.md. Do NOT use for ordinary clarification, planning, plan.md creation, code review, issue execution, debugging, prompt writing, prose editing, brainstorming, non-development goals, or when an existing plan/desire/design/spec/issue/task list should simply be implemented, followed, reviewed, revised, or continued.
---

# Desire Articulation

Interview the user until their underlying development desire is clear enough to write `desire.md`, then refine a written desire into a practical, self-contained `design.md` only when PHASE2 is explicitly requested. Treat the initial request as a hypothesis and preserve the user's real intent without locking in unnecessary step-by-step implementation.

## Activation Gate

Use only when all are true:

- Software development work.
- Intent or realization is unresolved.
- User wants interview/guided clarification.
- Final output is `desire.md` in PHASE1 or `design.md` in PHASE2.

Do not activate merely because a request is vague, high-level, asks "what should we check?", or needs ordinary clarification. If a `plan.md`, `desire.md`, `design.md`, issue, PR, task list, spec, or implementation brief is already the source of truth, read that artifact and proceed with the ordinary implementation, review, revision, or debugging workflow instead of using Root/Branch/Leaf framing or creating a new handoff brief. Activate only if the user explicitly asks to restart desire articulation from scratch, replace the prior source of truth with a new desire brief, be interviewed again before implementation, or create/refine `design.md` from an existing `desire.md`.

## Conduct

- Investigate before asking: read relevant docs/code/configs and use web research only when outside knowledge would materially improve the brief. If investigation finds no relevant implementation context, say that briefly and ask the upstream desire question that would most change the eventual brief.
- Ask exactly one question per user turn.
- Maintain a lightweight Root/Branch hypothesis tree:
  - `Root`: the user's desired state or unresolved question.
  - `Branch`: an upstream decision or ambiguity that could change the Root or the active output file.
  - `Leaf`: wording or detail for the active output file.
- Ask about the most upstream unresolved Branch first. Do not follow a fixed checklist or phase order.
- Each question must include your recommended answer and the reason. Present the recommendation as a hypothesis, not as the user's conclusion.
- If the Root changes, revisit only the downstream Branches that the new Root invalidates.
- Respect explicit constraints; if a constraint conflicts with the Root, ask whether it is mandatory.
- Do not implement the articulated work.
- Do not maintain a separate memo or update the active output file incrementally. Write the final file once.
- During PHASE1, write only `desire.md`. During PHASE2, write only `design.md`. You may reference the other phase's file, but do not edit it.
- If the user asks to write the active file while ambiguity remains, allow an imperfect brief instead of forcing more questions. Preserve remaining decision-relevant unknowns in `Context`, do not invent specifics, and use `Direction` to guide the later agent away from premature implementation commitments.
- Before stopping or writing the file, ask a narrow confirmation question so the user explicitly chooses whether to continue or finish.

When asking after investigation, first share one or two short sentences with the useful finding that frames the question. Do not dump research notes.

Branch examples include completion feeling, constraints, non-goals, audience, handoff boundaries, and direction-changing tradeoffs. These are examples, not a checklist; ask about them only when they could change the Root or the active output file. Avoid questions answerable from the repo/docs, implementation means before purpose, or low-value facts that are merely nice to record.

## Phases

Use the same Root/Branch/Leaf question model in both phases. The phases exist only to protect the boundary between understanding the desire and making it practical.

- `PHASE1`: articulate the desire itself and write `desire.md`; follow [phases/phase1.md](phases/phase1.md) and [formats/desire.md](formats/desire.md).
- `PHASE2`: refine a written desire into a self-contained `design.md`; follow [phases/phase2.md](phases/phase2.md) and [formats/design.md](formats/design.md).

Load only the phase file and matching format file needed for the current interview:

- Start with `phases/phase1.md` by default.
- Start with PHASE2 only when the user provides or points to an existing `desire.md` and explicitly asks to begin PHASE2 or create/refine `design.md`.
- If the user chooses to continue from PHASE1 to PHASE2, write `desire.md` first. Load PHASE2 and its format only after that.

## Finalization

Stop asking only when the active phase's rule file says the interview is ready to close and the user's own questions about what they want are resolved enough to proceed.

Before writing the active file, ask one narrow confirmation question in the user's conversation language so the user controls when refinement stops. Do not copy a fixed template verbatim.

The question must briefly convey:

- The active file is ready to be written, with a brief direction.
- Writing it now is the recommended next step, with a concise reason.
- The user can choose either to continue refining or to write the active file now.

If the user confirms or otherwise asks you to proceed, write the file.

## File Path

Use the user-specified path when provided. Otherwise write under the repository `docs/` directory. If `docs/` does not exist, create it without asking.

- In PHASE1, use `docs/desire.md` if it does not exist.
- In PHASE2, use `docs/design.md` if it does not exist.
- If the target file exists, choose a short, meaningful English kebab-case filename under `docs/`, such as `docs/desire-refine-search-ui.md` or `docs/design-refine-search-ui.md`.
- Do not ask the user to name the file.

## File Format

Follow only the matching format file for the active phase:

- PHASE1: [formats/desire.md](formats/desire.md)
- PHASE2: [formats/design.md](formats/design.md)
