---
name: preflight-briefing
description: >-
  Turn a task description such as a GitHub issue link, a spec file,
  or a prompt into a briefing that verifies it against the current
  codebase, then discuss direction with the user.
  Do not start implementing until the user explicitly asks.
  Invoke only on the user's explicit request.
disable-model-invocation: true
---

# preflight-briefing

## Goal

Task descriptions age.
By the time work starts, the description may reference code that has moved,
rely on premises that are no longer true, or ask for something already partially solved.
Verify the task description against the current state of the codebase
and give the user the material to decide the direction.

## Deliverable: the briefing

Present the briefing in the chat, in the user's language.
Write it to a file or post it as an issue comment only when the user asks.
Keep it readable in one sitting;
if drift findings are extensive, summarize and offer to expand.

The briefing has three parts, in this order:

1. **Situation**
  — what is true now.
    The goal of the task (not the method),
    the gaps between the description and the current main branch
    with evidence (commits, merged PRs, moved or removed code),
    and whether the task can be implemented as described.
    Cover: whether the files and structures it references still exist in their assumed form,
    whether its premises still hold, and whether the problem has been partially or fully solved since it was written.
2. **Decision**
  — what could be done.
    Name the primary decision in one sentence,
    then give 2–3 candidate directions at policy level.
    Include "do it as written" when it is still viable.
    Attach each candidate's preconditions, costs, and consequences to that candidate;
    do not float them as standalone questions.
3. **Proposal**
  — what you suggest. End the briefing here.
    One complete package as an itemized list:
    the candidate you recommend plus a default for every remaining sub-decision,
    so the user can override single items.
    Accepting the proposal as-is must leave nothing undecided.
    A sub-decision may stay open only when you cannot form a default,
    and then state why the call is the user's.
    Close by saying that "as proposed" settles everything
    and that individual items can be swapped in the reply.

## Boundaries

Until the user explicitly asks for implementation or an implementation plan:

- Stay at "what should be decided", not "how to build it".
  Do not go into code snippets, file-by-file change lists, ordered
  implementation steps, or effort estimates —
  in the briefing or in the discussion that follows it.
- Work read-only.
  Reading files and running read-only commands (git log, git diff, gh, grep) is fine;
  do not edit files, run tests, or change any state.

Agreement with a direction — "sounds good", "let's go with B" — is a decision within the discussion, not that ask.
