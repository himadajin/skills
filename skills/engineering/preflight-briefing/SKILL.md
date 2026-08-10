---
name: preflight-briefing
description: Turn a task description (a GitHub issue link, a spec file, or a prompt) into a discussion-ready briefing before any implementation or implementation planning begins. Invoke only on the user's explicit request.
disable-model-invocation: true
---

# Preflight Briefing

Given a task description, verify it against the current state of the codebase and produce a briefing that lets the user decide the direction. The briefing comes before implementation, and also before an implementation plan.

## Scope and hard constraints

- The deliverable of this skill is the briefing itself. The skill is complete when the briefing has been presented and you have stopped to wait for the user's decision.
- Operate read-only. Do not edit files, create branches, commit, or change code in any way. Reading files and running read-only commands (git log, git diff, gh, grep, tests are NOT included — do not run tests) is fine.
- Do not produce an implementation plan. The briefing must not contain: code snippets, file-by-file change lists, ordered implementation steps, or effort estimates. Stay at the level of "what should be decided", not "how to build it". If you notice yourself describing concrete edits, you have gone one level too deep — pull back up.
- Implementation and planning are separate later phases. They begin only after the user has approved a direction in discussion. Do not start them yourself, even if the direction seems obvious or the user's tone seems eager.

## Workflow

### 1. Ingest the task description

The input may be a GitHub issue link, a spec or requirements file, or prose written directly in the prompt. Treat all of these the same way: as a task description.

- For an issue link, read the issue body, all comments, and any linked PRs or issues.
- For a file, read it in full.
- For prose, use it as-is.

Read the task description completely before touching the codebase.

### 2. Drift check

Task descriptions age. Before discussing direction, verify the description against the current main branch:

- Do the files, functions, and structures it references still exist in their assumed form?
- Are the premises it relies on still true?
- Has the problem been partially or fully solved since it was written? Check the git history from around the time the description was created, and look for related merged PRs.
- Have recent changes reshaped the task, made it easier, harder, or unnecessary?

Record concrete findings (what changed, where) — these are often the most valuable part of the briefing.

### 3. Explore direction

- Can the task be implemented as written? If not, what reinterpretation would be needed?
- Identify 2–3 candidate directions, at policy level only, each with its trade-offs. Include "do it as written" as a candidate when it is still viable.
- Form a recommendation and be explicit about why.

### 4. Present the briefing and stop

Present the briefing with this structure:

1. Task summary — the goal, not the method
2. Drift findings — gaps between the description and current main, with evidence
3. Feasibility as written
4. Candidate directions and trade-offs
5. Recommendation and reasoning
6. Open questions — the decisions you need the user to make

End the briefing with the open questions, then stop and wait for the user's reply. Do not continue into planning or implementation in the same turn under any circumstances.

## Output conventions

- Write the briefing in the language the user is using.
- Present the briefing in the chat by default. Write it to a file or post it as an issue comment only when the user explicitly asks.
- Keep it readable in one sitting. If the drift findings are extensive, summarize and offer to expand on request rather than dumping everything.
