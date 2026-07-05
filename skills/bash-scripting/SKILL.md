---
name: bash-scripting
description: Use only when the user explicitly asks to use this skill. Create a single-file Bash command-line script after interviewing the user to decide its script specification.
---

# bash-scripting

Use this skill to create a single-file Bash command-line tool.

## Workflow

Interview the user to agree on the expected script behavior before
implementation.

Break down the user's request into the decisions that affect the
implementation, and classify each decision:

- Decided: the request already fixes it.
- Defaulted: the rules in this skill fix it.
- Open: neither fixes it.

Ask only about open decisions; carry decided and defaulted values into the
specification summary instead of asking about them. If no decisions are open,
skip the questions and present the specification summary directly.

Resolve open decisions in dependency order, asking about the most constraining
unresolved behavior first. Defer naming and other derived decisions until the
behavior they describe is stable.

Ask one question at a time and wait for the user's answer before continuing. For
each question, provide a recommended answer as a concrete proposal the user can
accept or revise.

Resolve at least these decisions before implementation:

- Purpose
- Input
- Output
- Command-line options
- Error behavior
- Commands and dependencies
- Script name

End the interview only when every required decision has a value and you can
describe the script's normal and error behavior without guessing. If multiple
reasonable implementations remain, ask another question instead of guessing.

Then present the specification summary: one entry per required decision with
its value, marking each value the user did not explicitly state or confirm as
assumed. The summary is where the user reviews assumed values, so make it
complete rather than brief.

After presenting the summary, ask for explicit permission to create the script
from that specification. Phrase the confirmation naturally for the current
conversation and make it clear that implementation will start only after
approval.

Create the script only after the user approves.

## Bash CLI Rules

Use these rules while interviewing so the proposed specification already fits
the Bash script that will be implemented.

### Scope

- Follow Unix command-line conventions.
- Keep the interface small.
- Create one self-contained Bash command-line tool.
- Do not add extra features unless they are needed for the agreed specification.

### Inputs and Outputs

- Prefer positional arguments for primary inputs.
- Prefer `-` to mean stdin or stdout when that fits the task.
- Write primary output to stdout by default.
- Treat `-o <path>` as the standard option for saving primary output to a file
  when file output is part of the script's behavior.
- Write diagnostics and errors to stderr.
- Use exit status 2 for command-line usage errors and 1 for runtime failures.
- Do not print success messages by default.

### Options

- Use short options as the standard Bash interface.
- Do not add long option aliases by default.
- Always support `-h`.

### Commands

- Resolve required external commands during the interview.
- Do not hand-roll parsers for structured data formats in Bash; use an agreed
  purpose-built command or choose another language.

## Implementation Rules

Before implementing, read `references/script-rules.md` and follow it.

## Validation

After creating the script, run the lightweight CLI checks from
`references/script-rules.md` when feasible.
