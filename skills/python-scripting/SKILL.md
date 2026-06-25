---
name: python-scripting
description: Use only when the user explicitly asks to use this skill. Create a single-file Python command-line script after interviewing the user to decide its script specification.
---

# python-scripting

Use this skill to create a single-file Python command-line tool.

## Workflow

Interview the user until you and the user share the same expected script
behavior. Do not treat the required decisions below as a checklist whose
completion automatically ends the interview.

Break down the user's request into the decisions that affect the implementation.
Resolve the decisions in dependency order, asking about the most constraining
unresolved point first. If multiple reasonable implementations remain, ask
another question instead of guessing.

Ask one question at a time and wait for the user's answer before continuing. For
each question, provide a recommended answer as a concrete proposal the user can
accept or revise.

Resolve at least these decisions before implementation:

- Purpose
- Script name
- Input
- Output
- Command-line options
- Libraries

After the decisions are clear, summarize the agreed specification briefly.

Then ask for explicit permission to create the script from that specification.
Phrase the confirmation naturally for the current conversation and make it clear
that implementation will start only after approval.

Create the script only after the user approves.

## Script Rules

### File Format

- Write one self-contained Python file.
- Start the file with `#!/usr/bin/env python3`.

### Python and Dependencies

- Target Python 3.11+.
- Use only the Python standard library unless the user explicitly approves
  another library.
- Prefer standard-library-only implementations.

### Command-Line Parsing

- Always use `argparse` for command-line argument parsing.
- Represent parsed command-line arguments with a frozen dataclass named `Args`.
- Parse command-line arguments in one function named `parse_args`.
- Build the `argparse.ArgumentParser` and construct `Args` inside `parse_args`.
- Treat `argparse.Namespace` as an intermediate value and convert it to `Args`.

### Required Structure

- Pass the parsed `Args` dataclass to `main`.
- Use `raise SystemExit(main(parse_args()))` in the entry point.

Use this structure as the required skeleton:

```python
#!/usr/bin/env python3

import argparse
from collections.abc import Sequence
from dataclasses import dataclass


# = Types =

@dataclass(frozen=True)
class Args:
    ...


# = Logic =

def process(...) -> ...:
    ...


# = Interface =

def parse_args(argv: Sequence[str] | None = None) -> Args:
    parser = argparse.ArgumentParser()
    ...
    namespace = parser.parse_args(argv)
    return Args(...)


def main(args: Args) -> int:
    ...


if __name__ == "__main__":
    raise SystemExit(main(parse_args()))
```

### Code Style

- Follow PEP 8.
- Add type annotations to every function definition.
- Do not write explanatory comments.
- Use section comments from the required skeleton to keep top-level code grouped
  by role.
- Express behavior through types, names, functions, and simple control flow.

## CLI Design

- Follow Unix command-line conventions.
- Keep the interface small.
- Prefer positional arguments for primary inputs.
- Prefer `-` to mean stdin or stdout when that fits the task.
- Write primary output to stdout by default.
- Treat `-o` / `--output` as the standard option for saving primary output to a
  file when file output is part of the script's behavior.
- Write diagnostics and errors to stderr.
- Do not print success messages by default.
- Do not add extra features unless they are needed for the agreed specification.

## Validation

After creating the script, run lightweight CLI checks when feasible:

- Confirm the script starts.
- Confirm `--help` works.
- Run at least one representative command for the agreed behavior.
