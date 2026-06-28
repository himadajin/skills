---
name: prompt-clarifying
description: Methodology for iteratively clarifying and improving agent-facing instructions (skills / slash commands / repository instruction files / code-gen prompts) via bias-free executor + two-sided evaluation (executor self-report + instruction-side metrics observable from delegated agents). Meta-skill, invoke ONLY when the user explicitly asks for an "empirical" eval, prompt tuning, prompt clarification, or the Iter-0 description / body consistency check. Do NOT auto-invoke after every instruction edit; this loop is operator-triggered by name.
---

# Prompt Clarifying

The author of a prompt cannot judge its quality. The clearer the writer thinks something is, the more likely another agent will stumble on it. The core of this skill is to **have a bias-free executor actually run the instruction, evaluate it two-sidedly, and iterate**. Do not stop until improvements plateau.

## When to use

- Right after creating or substantially revising a skill / slash command / task prompt
- When an agent does not behave as expected and you want to attribute the cause to ambiguity on the instruction side
- When hardening high-importance instructions (frequently used skills, automation-core prompts)

When not to use:

- One-off throwaway prompts (evaluation cost does not pay off)
- When the goal is not to improve success rate but merely to reflect the writer's subjective preferences

## Workflow

0. **Iteration 0 — description / body consistency check** (static, no dispatch needed)
   - Read the triggers / use cases claimed by the frontmatter `description`
   - Read the scope the body actually covers
   - If there is a gap, reconcile description or body before moving to iter 1
   - Example: description says "navigation / form filling / data extraction" but the body is only a CLI reference for `npx playwright test` — detect that kind of gap
   - If you skip this, the executor agent will "reinterpret" the body to match the description, and accuracy will come out high even though the skill does not actually meet the requirements (false positive)

1. **Baseline preparation**: Fix the target prompt and prepare the following two things.
   - **Evaluation scenarios**, 2 to 3 kinds (1 median + 1 to 2 edge). Realistic tasks that assume actual situations where the target prompt would apply.
   - **Requirements checklist** (for computing accuracy). For each scenario, enumerate 3 to 7 items the deliverable must satisfy. Accuracy % = items satisfied / total items. Fix this in advance (do not move it afterward).
2. **Bias-free read**: Have a "blank-slate" executor read the instruction. **Delegate to a fresh independent executor agent** using the host environment's available delegation mechanism (subagent, handoff, agent-as-tool, or equivalent). Do not substitute with a self-reread (it is structurally impossible to view text you just wrote objectively). When running multiple scenarios in parallel, dispatch multiple independent executor agents in the same round where possible. For how to handle environments where dispatch is unavailable, see the "Environment constraints" section.
3. **Execution**: Hand the executor agent a prompt that follows the **executor invocation contract** described below, and have it execute the scenario. The executor produces an implementation or output and returns a self-report at the end.
4. **Two-sided evaluation**: Record the following from the returned results.
   - **Executor self-report** (extracted from the body of the executor agent's report): unclear points / discretionary fill-ins / places where template application got stuck
   - **Trace interpretation**: each unclear point is tagged with the phase it originated in (Understanding / Planning / Execution / Formatting — see "Executor invocation contract"). Phase-local fixes land better than global "the prompt was unclear" fixes; a single Understanding-phase ambiguity often looks like a chain of Execution-phase failures.
   - **Structured reflection**: each unclear point must be returned as `Issue / Cause / General Fix Rule`. The `General Fix Rule` is the class-level abstraction that feeds the "Failure pattern ledger" — without it, fixes stay as one-off patches that rediscover the same mistake later.
   - **Instruction-side measurements** (the judgment rules are defined canonically in this section; refer to it from elsewhere):
     - Success/failure: counts as success (○) only when **all** requirements tagged `[critical]` are ○. If even one is × or partial, it is failure (×). The label is the binary ○ / × only.
     - Accuracy (achievement rate of the requirements checklist, %. ○ = full score, × = 0, partial = 0.5; sum and divide by total items)
     - Lookup footprint (number and categories of local / external references inspected beyond the target prompt. Extract from the executor agent's self-report; ask the executor to report it explicitly)
     - Unresolved judgment count (how many decisions the executor filled in because the instruction did not resolve them. Decisions that were explicitly routed to specs / acceptance criteria instead of filled in should be listed separately and count as 0 filled judgments)
     - Spec-gate / acceptance-gate compliance:
       - ○ only when the executor does not invent semantics for behavior the target prompt leaves unspecified, and instead routes them to specs, acceptance criteria, or user clarification.
       - Count a decision as "invented" when the deliverable silently chooses behavior that is not grounded in the target prompt, scenario, or inspected references.
       - Count it as "routed" when the executor names the missing decision and sends it to the proper spec / acceptance / clarification gate.
     - Retry count (how many times the executor agent redid the same decision. Extract from the executor agent's self-report; not measurable from the instruction side)
     - **On failure, add a one-line note to the "unclear points" section of the presentation format stating "which [critical] item dropped"** (for root cause tracing)
   - The requirements checklist must include **at least one** `[critical]`-tagged item (if there are zero, the success judgment becomes vacuous). Do not add or remove [critical] tags after the fact.
5. **Apply the diff**: Put the minimum fix into the prompt to eliminate the unclear points. One theme per iteration (multiple related fixes are OK, unrelated fixes go to next time).
   - **Before applying the fix, explicitly state "which item in the requirements checklist / judgment wording this fix satisfies"** (fixes inferred from axis names often do not land. See the "Fix propagation patterns" section below.)
   - **Consult the failure pattern ledger first**. If the structured reflection's `General Fix Rule` already matches a known pattern, the first question is "why didn't the existing fix prevent it?" — the fix may need to move closer to the top of the prompt, or be re-worded, before a new ledger entry is added.
6. **Re-evaluate**: Run 2 → 5 again with a new executor agent (do not reuse the same agent: it has learned the previous improvements). Increase parallelism if iterating further does not plateau improvements.
7. **Convergence check**: The rough rule is "stop when 2 consecutive iterations have zero new unclear points AND metric improvements fall below the thresholds (below)". Make it 3 consecutive for high-importance prompts.

## Evaluation axes

- Axis: Success/failure
  - How to capture: Did the executor produce the intended deliverable (binary)
  - Meaning: Minimum bar
- Axis: Accuracy
  - How to capture: What % of requirements the deliverable satisfies
  - Meaning: Degree of partial success
- Axis: Lookup footprint
  - How to capture: Count and categories of references inspected beyond the target prompt
  - Meaning: Indicator of instruction self-containment
- Axis: Unresolved judgment count
  - How to capture: Decisions filled in because the instruction did not resolve them
  - Meaning: Signal of implicit specification
- Axis: Spec-gate / acceptance-gate compliance
  - How to capture: Whether unspecified product behavior was explicitly routed to specs / acceptance criteria / user clarification instead of silently decided
  - Meaning: Signal of implementation discipline
- Axis: Retry count
  - How to capture: How many times the same decision was redone
  - Meaning: Signal of instruction ambiguity
- Axis: Unclear points (self-report)
  - How to capture: Executor enumerates as bullets
  - Meaning: Qualitative improvement material
- Axis: Discretionary fill-ins (self-report)
  - How to capture: Decisions not fixed by the instruction
  - Meaning: Surfaces implicit specification

**Weighting**: Qualitative (unclear points / discretionary fill-ins) is primary, quantitative (lookup footprint / unresolved judgment count) is auxiliary. Chasing only low lookup footprint makes the prompt too thin.

### Qualitative interpretation of lookup footprint

Looking only at accuracy hides skill problems. Using lookup footprint as a **relative value across scenarios** reveals structural defects:

- If one scenario inspects **3-5x or more** references vs the others, treat it as a suspicion threshold for **low self-containment**. The executor may be forced into references descent because the skill acts like an index of decisions rather than a usable recipe.
- Typical example: all scenarios inspect 1-3 relevant files but one scenario alone inspects 15+ → there is no recipe for that scenario in the skill itself, so it is cross-searching references/
- Countermeasure: adding an "inline minimum complete example" or "guidance on when to read references" at the top of SKILL.md in iter 2 significantly drops lookup footprint

Even at 100% accuracy, a skew in lookup footprint is grounds for triggering iter 2. "Cut off based on accuracy alone" tends to miss structural defects.

### Fix propagation patterns (conservative / overshoot / zero-shoot)

Fix → effect is not linear. Pre-estimation can play out in the following 3 patterns:

- **Conservative swing** (estimate > actual): one fix aimed at multiple axes but only moved one. "Aiming at multiple axes tends to miss."
- **Overshoot** (estimate < actual): one structural piece of information (e.g., a combination of command + config + expected output) satisfied judgment wording across multiple axes at once. "Combinations of information structurally hit multiple axes."
- **Zero-shoot** (estimate > 0, actual = 0): a fix inferred from the axis name did not reach any of the judgment wording. "Axis names and judgment wording are different things."

To stabilize this, **before applying the diff, have the executor agent verbalize "which judgment wording this fix satisfies"**. Estimation accuracy does not come out unless you tie things at the threshold-wording level. When adding a new evaluation axis, also concretize the judgment criteria for each point down to the threshold-wording level (at a granularity the executor can judge, such as "all explicit" or "full text of a minimum working configuration" — so it knows what constitutes 2 points).

## Executor invocation contract

The prompt given to the executor takes the following structure. This is the input contract for "two-sided evaluation".

```
You are an executor reading <target prompt name> with a blank slate.

## Target prompt
<Paste the full body of the target prompt, or specify a path for Read>

## Scenario
<One paragraph setting the scenario context>

## Requirements checklist (items the deliverable must satisfy)
1. [critical] <item that belongs to the minimum bar>
2. <normal item>
3. <normal item>
...
(Judgment rules are canonically defined in "Workflow 4. Two-sided evaluation / Instruction-side measurements". At least one [critical] is required.)

## Task
1. Follow the target prompt to execute the scenario and produce the deliverable.
2. On completion, respond with the report structure below.

## Report structure
- Deliverable: <artifact or execution summary>
- Requirement achievement: ○ / × / partial (with reason) for each item
- **Trace** (tag OK / stuck / skipped for each phase, one-line reason when not OK):
  - Understanding (reading the instruction and building a mental model)
  - Planning (deciding the approach / ordering)
  - Execution (actually doing the work)
  - Formatting (shaping the deliverable to the expected form)
  - *Collapsed form allowed*: when all four phases are OK, a single line `Trace: all OK` is sufficient. Emit phase-by-phase only when any phase is stuck or skipped. (This avoids happy-path boilerplate; the trace structure only earns its cost when something actually goes wrong.)
- **Unclear points (structured)**: for each issue, three lines:
  - Issue: <what observably happened>
  - Cause: <why, diagnosed at the instruction level>
  - General Fix Rule: <a class-level rule, not a spot fix, that would prevent this class of mistake>
- Discretionary fill-ins: places not fixed by the instruction and filled in by your own judgment (bullets)
- Retries: number of times you redid the same decision and why
- Lookup footprint: count, categories, and key referenced paths / sources
- Unresolved judgment count: number and bullets
- Spec-gate / acceptance-gate compliance: ○ / partial / × with reason
```

The caller extracts the self-report portion from the report and fills the evaluation-axis table from the executor's reported lookup footprint, unresolved judgment count, spec-gate compliance, and retries. Some host environments expose runtime or token metadata for delegated agents, but do not use elapsed time as an evaluation axis in this skill.

## Environment constraints

The full empirical loop requires dispatching a fresh independent executor agent. In environments where that is not possible (already running inside a delegated agent without access to a delegation mechanism, subagent / handoff tools are disabled, etc.), **do not run Workflow steps 2-7 as empirical evaluation**.

- Alternative 1: ask the parent session's user to start a separate agent session and delegate the evaluation there
- Alternative 2: give up on evaluation and explicitly report to the user "empirical evaluation skipped: dispatch unavailable"
- Static exception: Iteration 0 and structural review mode are text-only consistency checks. They may still be run, but label them as static / structural review and do not count them toward convergence.
- **NG**: substitute self-reread for the executor run (bias enters, so you must not trust the evaluation result)

**Structural review mode**: when you want to check only the **consistency and clarity of the description** of the skill / prompt rather than run empirical evaluation, carve it out explicitly as structural review mode. If using a delegated executor, note clearly in the request prompt "this round is structural review mode: text consistency check, not execution". Structural review is an aid to empirical, not a replacement (it cannot be used for consecutive-clear judgment).

## Iteration stopping criteria

- **Convergence (stop)**: 2 consecutive rounds satisfying **all** of the following:
  - New unclear points: 0
  - Accuracy improvement vs previous: +3 points or less (saturation such as 5% → 8%)
  - Lookup footprint variation vs previous: within ±20%, unless the difference is explained by intentionally routed spec/reference checks
  - Unresolved filled judgments: 0, or all remaining unresolved points are explicitly routed to specs / acceptance criteria without being filled in
  - Spec-gate / acceptance-gate compliance: ○
  - **Overfitting check**: at convergence judgment, add 1 hold-out scenario not used so far and evaluate. If accuracy drops 15 points or more from the recent average, overfitting. Go back to baseline scenario design and add edges.
- **Divergence (suspect the design)**: if new unclear points do not decrease across 3+ iterations → the design direction of the prompt itself may be wrong. Stop fixing by patches and rewrite the structure
- **Resource cutoff**: stop when importance and improvement cost no longer balance (the "ship at 80 points" call)

## Failure pattern ledger

Maintain a cumulative list of failure modes across iterations. Without it, each iteration re-discovers the same class of mistake, and accuracy improvements stall without the operator noticing that the same `General Fix Rule` keeps surfacing under different surface wording.

Entry format:

```
- **Pattern name**: short descriptive handle (not "ambiguous X"; prefer "over-eager template application when skip clause is absent")
  - Example: <representative Issue wording from some iter>
  - General Fix Rule: <the class-level rule from that iter's structured reflection>
  - Seen in: iter N, iter M, ...
```

Rules:

- Before generating a fix in Workflow step 5, scan the ledger. If the current `General Fix Rule` matches an existing entry, update `Seen in` and investigate why the existing fix did not prevent recurrence (wording ambiguity? position too late in the prompt? missing example?) before creating a new entry.
- A pattern that recurs 3+ times despite targeted fixes is a structural signal — escalate to the "Divergence" criterion above rather than continuing to patch.
- The ledger is per-target-prompt, not global across all prompt-clarifying runs. Keep it with the current run's iteration notes or review artifact; do not invent a new storage system just for the ledger.

## Variant exploration (optional, plateau-breaking)

When iterations approach a plateau but convergence criteria (2 consecutive clears) are not met, suspect local optimum and run a 2-variant round:

- **Conservative variant**: current prompt + next-best minor fix
- **Exploratory variant**: current prompt with one structural change — reorder sections, split a dense paragraph, drop a redundant section, or add a missing scaffolding (e.g., a worked example)

Dispatch fresh independent executor agents on the same scenarios in parallel through the host's delegation mechanism. Keep the variant with higher accuracy; on tie, prefer fewer unclear points; on further tie, prefer lower lookup footprint and fewer filled unresolved judgments.

Pairwise-comparison caveats:

- Do **not** ask an executor agent to rate "A vs B" directly. LLM position bias and self-preference bias make such judgments noisy at small n.
- Compare on the objective axes only (accuracy, lookup footprint, unresolved judgment count, unclear-points count, phase-weakness counts). Those are reproducible; "which prompt felt better" is not.
- If qualitative comparison is genuinely needed, counterbalance: run both orderings (A,B) and (B,A) and accept a verdict only if both orderings agree.

Cost: variant exploration doubles dispatch count per iteration. Use when plateau is suspected, not by default.

## Presentation format

Record and present to the user with the following form at each iteration:

```
## Iteration N

### Changes (diff from previous)
- <one-line fix content>
- Pattern applied: <pattern name from ledger, or "(new)">

### Execution results (per scenario)
| Scenario | Success/Failure | Accuracy | lookup footprint | unresolved judgments | spec gate | retries | Weak phase |
|---|---|---|---|---|---|---|---|
| A | ○ | 90% | 4 refs | 0 | ○ | 0 | — |
| B | × | 60% | 9 refs | 2 | partial | 2 | Execution |

### Structured reflection (newly surfaced this time)
- <Scenario B>: [critical] item N is × — <one-line reason for drop>
  - Issue: <what observably happened>
  - Cause: <why, at the instruction level>
  - General Fix Rule: <class-level abstraction>
- <Scenario A>: (nothing new)

### Discretionary fill-ins (newly surfaced this time)
- <Scenario B>: <fill-in content>

### Ledger updates
- Added: <pattern name> (from Scenario B)
- Re-seen: <pattern name> (originally iter K) — existing fix did not prevent recurrence because <reason>

### Next fix proposal
- <one-line minimum fix>

(Convergence check: X consecutive clears / Y rounds remaining to stop condition)
```

## Red flags (beware of rationalization)

- Rationalization: "Rereading it myself has the same effect"
  - Reality: You cannot view text you just wrote "objectively". Always dispatch a new executor agent.
- Rationalization: "One scenario is enough"
  - Reality: One scenario overfits. Minimum 2, ideally 3.
- Rationalization: "Zero unclear points once, so we're done"
  - Reality: Could be coincidence. Finalize with 2 consecutive rounds.
- Rationalization: "Let's knock out multiple unclear points at once"
  - Reality: You lose track of what worked. One theme per iteration.
- Rationalization: "Split each related micro-fix strictly into its own iter"
  - Reality: Trap in the opposite direction. "One theme" is a semantic unit. 2-3 related micro-fixes can be bundled into 1 iter. Splitting too far explodes the iter count.
- Rationalization: "Metrics are good, so ignore qualitative feedback"
  - Reality: Low lookup footprint can also be a sign of being too thin. Keep qualitative primary.
- Rationalization: "Rewriting from scratch is faster"
  - Reality: Correct if unclear points do not decrease across 3+ iterations. Before that stage, it is escape.
- Rationalization: "Let's reuse the same executor agent"
  - Reality: It has learned the previous improvements. Always dispatch a new one.

## Common failures

- **Scenario too easy / too hard**: neither produces signal. One at the median of real use, one edge
- **Only looking at metrics**: chasing only low lookup footprint strips important explanations and makes it fragile
- **Too many changes per iteration**: you can no longer trace "which fix back then worked". One theme per iteration
- **Tuning scenarios to match the fix**: making the scenario side easier just to make unclear points look eliminated → putting the cart before the horse

## Related

- `skill-creator` — the draft → test → review → improve loop for skill creation. Essentially the same as this skill's "baseline → fix → rerun with an executor agent"
- `retrospective-codify` — fixating learnings after a task. This skill is during prompt development, retrospective-codify is after a task ends; use them differently
- Delegation mechanisms such as subagents, handoffs, or agent-as-tool patterns are used for running multiple scenarios in parallel
- External eval CLIs such as `waxa-eval` can still cover persistence, CI repeatability, or external adoption gates. This skill (prompt-clarifying) covers the **methodology and the in-session delegated-agent flow**, including Iter 0 static check, `[critical]`-tagged checklists, lookup-footprint diagnosis, and spec-gate compliance.
