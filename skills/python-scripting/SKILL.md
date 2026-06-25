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

- Write one self-contained Python file.
- Start the file with `#!/usr/bin/env python3`.
- Target Python 3.11+.
- Follow PEP 8.
- Use only the Python standard library unless the user explicitly approves
  another library.
- Prefer standard-library-only implementations.
- Always use `argparse` for command-line option parsing.
- Represent parsed command-line options with a frozen dataclass.
- Parse command-line options in one function named `parse_options`.
- `parse_options` should accept `argv: Sequence[str] | None = None` and return
  the options dataclass.
- Build the `argparse.ArgumentParser` and construct the options dataclass inside
  `parse_options`.
- Pass the parsed options dataclass to `main`.
- Use `raise SystemExit(main(parse_options()))` in the entry point.
- Add type annotations to every function definition.
- Do not write comments.
- Express behavior through types, names, functions, and simple control flow.

Use this structure:

```python
#!/usr/bin/env python3

import argparse
from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class Options:
    ...


def parse_options(argv: Sequence[str] | None = None) -> Options:
    parser = argparse.ArgumentParser()
    ...
    args = parser.parse_args(argv)
    return Options(...)


def main(options: Options) -> int:
    ...


if __name__ == "__main__":
    raise SystemExit(main(parse_options()))
```

## CLI Design

- Follow Unix command-line conventions.
- Keep the interface small.
- Prefer positional arguments for primary inputs.
- Prefer `-` to mean stdin or stdout when that fits the task.
- Write primary output to stdout.
- Write diagnostics and errors to stderr.
- Do not print success messages by default.
- Do not add extra features unless they are needed for the agreed specification.

## Validation

After creating the script, run lightweight CLI checks when feasible:

- Confirm the script starts.
- Confirm `--help` works.
- Run at least one representative command for the agreed behavior.
