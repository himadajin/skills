---
name: bash-scripting
description: Use only when the user explicitly asks to use this skill. Create a single-file Bash command-line script after interviewing the user to decide its script specification.
---

# bash-scripting

Use this skill to create a single-file Bash command-line tool.

## Workflow

Interview the user until you and the user share the same expected script
behavior. Do not treat the required decisions below as a checklist whose
completion automatically ends the interview.

Break down the user's request into the decisions that affect the implementation.
Resolve decisions in dependency order, asking about the most constraining
unresolved behavior first. Defer naming and other derived decisions until the
behavior they describe is stable. If multiple reasonable implementations remain,
ask another question instead of guessing.

Ask one question at a time and wait for the user's answer before continuing. For
each question, provide a recommended answer as a concrete proposal the user can
accept or revise.

Resolve at least these decisions before implementation:

- Purpose
- Input
- Output
- Command-line options
- Commands and dependencies
- Script name

After the decisions are clear, summarize the agreed specification briefly.

Then ask for explicit permission to create the script from that specification.
Phrase the confirmation naturally for the current conversation and make it clear
that implementation will start only after approval.

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
