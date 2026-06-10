---
name: goal-definition
description: >-
  Use only for an explicit interview-style goal-definition phase for a software development task before implementation. In PHASE1, interview to define the user's purpose and write purpose.md. In PHASE2, start only from an existing purpose.md when the user explicitly asks to refine realization into a self-contained design.md. In PHASE3, start only from an existing design.md for work with a GUI and write ui.md. Trigger when the user asks to be questioned, define/capture a purpose file, create/refine a design handoff from purpose.md, or create/refine a UI handoff from design.md. Do NOT use for ordinary clarification, planning, plan.md creation, code review, issue execution, debugging, prompt writing, prose editing, brainstorming, non-development goals, or when an existing plan/purpose/design/ui/spec/issue/task list should simply be implemented, followed, reviewed, revised, or continued.
---

# Goal Definition

Interview the user until the purpose behind their development goal is clear enough to write `purpose.md`, refine a written purpose into a practical, self-contained `design.md` only when PHASE2 is explicitly requested, then refine a GUI design into `ui.md` only when PHASE3 is explicitly requested or accepted. Treat the initial request as a hypothesis and preserve the user's real intent without locking in unnecessary step-by-step implementation.

## Activation Gate

Use only when all are true:

- Software development work.
- Intent or realization is unresolved.
- User wants interview/guided clarification.
- Final output is `purpose.md` in PHASE1, `design.md` in PHASE2, or `ui.md` in PHASE3.

Do not activate merely because a request is vague, high-level, asks "what should we check?", or needs ordinary clarification. If a `plan.md`, `purpose.md`, `design.md`, `ui.md`, issue, PR, task list, spec, or implementation brief is already the source of truth, read that artifact and proceed with the ordinary implementation, review, revision, or debugging workflow instead of using Root/Branch/Leaf framing or creating a new handoff brief. Activate only if the user explicitly asks to restart goal definition from scratch, replace the prior source of truth with a new purpose brief, be interviewed again before implementation, create/refine `design.md` from an existing `purpose.md`, or create/refine `ui.md` from an existing `design.md`.

## Conduct

- Investigate before asking: read relevant docs/code/configs and use web research only when outside knowledge would materially improve the brief. If investigation finds no relevant implementation context, say that briefly and ask the upstream purpose question that would most change the eventual brief.
- Ask exactly one question per user turn.
- Maintain a lightweight Root/Branch hypothesis tree:
  - `Root`: the user's target state or unresolved question.
  - `Branch`: an upstream decision or ambiguity that could change the Root or the active output file.
  - `Leaf`: wording or detail for the active output file.
- Ask about the most upstream unresolved Branch first. Do not follow a fixed checklist or phase order.
- Each question must include your recommended answer and the reason. Present the recommendation as a hypothesis, not as the user's conclusion.
- If the Root changes, revisit only the downstream Branches that the new Root invalidates.
- Respect explicit constraints; if a constraint conflicts with the Root, ask whether it is mandatory.
- Do not implement the defined work.
- Do not maintain a separate memo or update the active output file incrementally. Write the final file once.
- During PHASE1, write only `purpose.md`. During PHASE2, write only `design.md`. During PHASE3, write `ui.md`; you may edit `design.md` only to add or update the `ui.md` reference in `Related Files`.
- If the user asks to write the active file while ambiguity remains, allow an imperfect brief instead of forcing more questions. Preserve remaining decision-relevant unknowns in `Context`, do not invent specifics, and use `Direction` to guide the later agent away from premature implementation commitments.
- Before stopping or writing the file, ask a narrow confirmation question so the user explicitly chooses whether to continue or finish.

When asking after investigation, first share one or two short sentences with the useful finding that frames the question. Do not dump research notes.

Branch examples include completion feeling, constraints, non-goals, audience, handoff boundaries, and direction-changing tradeoffs. These are examples, not a checklist; ask about them only when they could change the Root or the active output file. Avoid questions answerable from the repo/docs, implementation means before purpose, or low-value facts that are merely nice to record.

## Phases

Use the same Root/Branch/Leaf question model in every phase. The phases exist only to protect the boundary between defining the purpose, making it practical, and defining important UI decisions without duplicating them in the implementation design.

- `PHASE1`: define the purpose itself and write `purpose.md`; follow [phases/phase1.md](phases/phase1.md) and [formats/purpose.md](formats/purpose.md).
- `PHASE2`: refine a written purpose into a self-contained `design.md`; follow [phases/phase2.md](phases/phase2.md) and [formats/design.md](formats/design.md).
- `PHASE3`: refine a GUI design into a self-contained `ui.md`; follow [phases/phase3.md](phases/phase3.md) and [formats/ui.md](formats/ui.md).

Load only the phase file and matching format file needed for the current interview:

- Start with `phases/phase1.md` by default.
- Start with PHASE2 only when the user provides or points to an existing `purpose.md` and explicitly asks to begin PHASE2 or create/refine `design.md`.
- Start with PHASE3 only when the user provides or points to an existing `design.md` for work with a GUI and explicitly asks to begin PHASE3, create/refine `ui.md`, or accepts the recommendation to continue into UI definition.
- If the user chooses to continue from PHASE1 to PHASE2, write `purpose.md` first. Load PHASE2 and its format only after that.
- If the user chooses to continue from PHASE2 to PHASE3, write `design.md` first. Load PHASE3 and its format only after that.

## Finalization

Stop asking only when the active phase's rule file says the interview is ready to close and the user's own questions about what they want are resolved enough to proceed.

Before writing the active file, ask one narrow confirmation question in the user's conversation language so the user controls when refinement stops. Do not copy a fixed template verbatim.

The question must briefly convey:

- The active file is ready to be written, with a brief direction.
- Writing it now is the recommended next step, with a concise reason.
- The user can choose either to continue refining or to write the active file now.

If the user confirms or otherwise asks you to proceed, write the file.

When writing `design.md`, always include its `Related Files` section. If the design includes a GUI or could reasonably require user-facing screens, ask whether to continue into PHASE3 after writing `design.md`; recommend continuing so UI decisions are captured in `ui.md` instead of duplicated in `design.md`.

## File Path

Use the user-specified path when provided. Otherwise write under the repository `docs/` directory. If `docs/` does not exist, create it without asking.

- In PHASE1, use `docs/purpose.md` if it does not exist.
- In PHASE2, use `docs/design.md` if it does not exist.
- In PHASE3, use `docs/ui.md` if it does not exist.
- If the target file exists, choose a short, meaningful English kebab-case filename under `docs/`, such as `docs/purpose-refine-search-ui.md`, `docs/design-refine-search-ui.md`, or `docs/ui-refine-search-ui.md`.
- Do not ask the user to name the file.

## File Format

Follow only the matching format file for the active phase:

- PHASE1: [formats/purpose.md](formats/purpose.md)
- PHASE2: [formats/design.md](formats/design.md)
- PHASE3: [formats/ui.md](formats/ui.md)
