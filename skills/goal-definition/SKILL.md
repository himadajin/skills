---
name: goal-definition
description: >-
  Interview the user to define the purpose behind a software development goal before implementation and prepare handoff documents. Use only when the user explicitly requests this skill or a goal-definition interview.
---

# Goal Definition

Interview the user until the purpose behind their development goal is clear enough to preserve as a purpose brief, refine that brief into a practical, self-contained `design.md` only when PHASE2 is explicitly requested, then refine selected design companions one at a time only when PHASE3 is explicitly requested or accepted. Treat the initial request as a hypothesis and preserve the user's real intent without locking in unnecessary step-by-step implementation.

PHASE1 is mandatory for this skill, but `purpose.md` is not mandatory by default. Keep the confirmed purpose as an in-conversation purpose brief when continuing directly into PHASE2, and write `purpose.md` only when the user asks for it, PHASE1 is the stopping point, or a separate handoff/context reset needs a persistent purpose file.

## Activation Gate

Use only when all are true:

- Software development work.
- Intent or realization is unresolved.
- User wants interview/guided clarification.
- Final output is a purpose brief or `purpose.md` in PHASE1, `design.md` in PHASE2, or a selected companion file such as `ui.md` or `verification.md` in PHASE3.

Do not activate merely because a request is vague, high-level, asks "what should we check?", or needs ordinary clarification. If a `plan.md`, `purpose.md`, `design.md`, `ui.md`, `verification.md`, issue, PR, task list, spec, or implementation brief is already the source of truth, read that artifact and proceed with the ordinary implementation, review, revision, or debugging workflow instead of using Root/Branch/Leaf framing or creating a new handoff brief. Activate only if the user explicitly asks to restart goal definition from scratch, replace the prior source of truth with a new purpose brief, be interviewed again before implementation, create/refine `design.md` from an existing `purpose.md`, or create/refine a companion file from an existing `design.md`.

## Conduct

- Investigate before asking: read relevant docs/code/configs and use web research only when outside knowledge would materially improve the brief. If investigation finds no relevant implementation context, say that briefly and ask the upstream purpose question that would most change the eventual brief.
- Ask exactly one question per user turn.
- Maintain a lightweight Root/Branch hypothesis tree:
  - `Root`: the user's target state or unresolved question.
  - `Branch`: an upstream decision or ambiguity that could change the Root or the active output.
  - `Leaf`: wording or detail for the active output.
- Ask about the most upstream unresolved Branch first. Do not follow a fixed checklist or phase order.
- Each question must include your recommended answer and the reason. Present the recommendation as a hypothesis, not as the user's conclusion.
- If the Root changes, revisit only the downstream Branches that the new Root invalidates.
- Respect explicit constraints; if a constraint conflicts with the Root, ask whether it is mandatory.
- Do not implement the defined work.
- During PHASE1, preserve the agreed purpose as a purpose brief. Write only `purpose.md` when the user asks for it, PHASE1 ends without continuing, or a separate handoff/context reset is needed. During PHASE2, write only `design.md`. During PHASE3, write only the selected companion file; you may edit `design.md` only to add or update that companion file's reference in `Related Files`.
- If the user asks to write the active file while ambiguity remains, allow an imperfect brief instead of forcing more questions. Preserve remaining decision-relevant unknowns in `Context`, do not invent specifics, and use `Direction` to guide the later agent away from premature implementation commitments.
- Before stopping, closing a phase, or writing a file, ask a narrow confirmation question so the user explicitly chooses whether to continue or finish.

When asking after investigation, first share one or two short sentences with the useful finding that frames the question. Do not dump research notes.

Branch examples include completion feeling, constraints, non-goals, audience, handoff boundaries, and direction-changing tradeoffs. These are examples, not a checklist; ask about them only when they could change the Root or the active output. Avoid questions answerable from the repo/docs, implementation means before purpose, or low-value facts that are merely nice to record.

## Phases

Use the same Root/Branch/Leaf question model in every phase. The phases exist only to protect the boundary between defining the purpose, making it practical, and defining selected companion concerns without duplicating them in the implementation design.

- `PHASE1`: define the purpose itself as a purpose brief; follow [phases/phase1.md](phases/phase1.md) and [formats/purpose.md](formats/purpose.md).
- `PHASE2`: refine a purpose brief or written `purpose.md` into a self-contained `design.md`; follow [phases/phase2.md](phases/phase2.md) and [formats/design.md](formats/design.md).
- `PHASE3`: refine a design into one selected companion file; follow [phases/phase3.md](phases/phase3.md) and the matching format file.

Load only the phase file and matching format file needed for the current interview:

- Start with `phases/phase1.md` by default.
- Start with PHASE2 only when the user provides or points to an existing `purpose.md`, or when PHASE1 in the same conversation has produced a confirmed purpose brief and the user explicitly asks to begin PHASE2 or create/refine `design.md`.
- Start with PHASE3 only when the user provides or points to an existing `design.md` and explicitly asks to begin PHASE3, create/refine a companion file, or accepts the recommendation to continue into a selected companion definition.
- If the user chooses to continue from PHASE1 to PHASE2 in the same conversation, do not write `purpose.md` by default. Carry the confirmed purpose brief forward, then load PHASE2 and its format.
- If the user asks to persist PHASE1 before continuing, write `purpose.md` first, then load PHASE2 and its format.
- If the user chooses to continue from PHASE2 to PHASE3, write `design.md` first. Load PHASE3 and its format only after that.

## Finalization

Stop asking only when the active phase's rule file says the interview is ready to close and the user's own questions about what they want are resolved enough to proceed.

Before closing the active phase or writing the active file, ask one narrow confirmation question in the user's conversation language so the user controls when refinement stops. Do not copy a fixed template verbatim.

The question must briefly convey:

- The active phase is ready to close or the active file is ready to be written, with a brief direction.
- The recommended next step, with a concise reason.
- The user can choose either to continue refining or to close/write now.

If the user confirms or otherwise asks you to proceed from PHASE1, continue directly to PHASE2 without writing `purpose.md` when the user wants a design handoff in the same conversation. Write `purpose.md` instead when the user asks for it, PHASE1 is the stopping point, or a persistent handoff is needed.

If the user confirms or otherwise asks you to proceed from PHASE2 or PHASE3, write the active file.

When writing `design.md`, always include its `Related Files` section. After writing `design.md`, consider whether `ui.md` or `verification.md` should be created as companion files. Recommend continuing into PHASE3 only for companion files that would materially reduce downstream guesswork; do not reference companion files that are not created.

## File Path

Use the user-specified path when provided. Otherwise write under the repository `docs/` directory. If `docs/` does not exist, create it without asking.

- In PHASE1, when writing `purpose.md`, use `docs/purpose.md` if it does not exist.
- In PHASE2, use `docs/design.md` if it does not exist.
- In PHASE3, use the matching default path such as `docs/ui.md` or `docs/verification.md` if it does not exist.
- If the target file exists, choose a short, meaningful English kebab-case filename under `docs/`, such as `docs/purpose-refine-search-ui.md`, `docs/design-refine-search-ui.md`, `docs/ui-refine-search-ui.md`, or `docs/verification-refine-search-ui.md`.
- Do not ask the user to name the file.

## File Format

Follow only the matching format file for the active phase or selected companion:

- PHASE1: [formats/purpose.md](formats/purpose.md)
- PHASE2: [formats/design.md](formats/design.md)
- PHASE3 `ui.md`: [formats/ui.md](formats/ui.md)
- PHASE3 `verification.md`: [formats/verification.md](formats/verification.md)
