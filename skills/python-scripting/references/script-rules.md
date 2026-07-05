# Script Rules

Read this before implementation. These rules cover how to implement the agreed
specification; the public behavior comes from `SKILL.md` and the completed
interview.

## File Format

- Write one self-contained Python file.
- Start the file with `#!/usr/bin/env python3`.
- When the specification includes an approved non-standard-library dependency,
  put the PEP 723 metadata block directly below the shebang (see Dependencies).

## Command-Line Parsing

- Always use `argparse` for command-line argument parsing.
- Represent parsed command-line arguments with a frozen dataclass named `Args`.
- Parse command-line arguments in one function named `parse_args`.
- Build the `argparse.ArgumentParser` and construct `Args` inside `parse_args`.
- Treat `argparse.Namespace` as an intermediate value and convert it to `Args`.
- Validate argument shape inside `parse_args` with `parser.error`, which
  reports to stderr and exits with status 2.

## Structure

- Put the script's behavior in logic functions.
- Treat the interface section as the boundary from CLI concerns to script
  behavior. Keep `parse_args`, `-` interpretation, stdin/stdout/file wiring,
  diagnostics, and the entry-point code there.
- Keep logic functions focused on the script's operation. They should not know
  option names, interpret `-`, print CLI diagnostics, or exit the process.
- Adapt input and output at the interface boundary so each operation has one
  logic path instead of duplicated transformations for different input sources.
- Pass the parsed `Args` dataclass to `main`, and have `main` return the exit
  status as an `int`.
- Use `raise SystemExit(main(parse_args()))` as the entry point.

The skeleton below is the required frame, shown applied to a filter script with
one input and one output. Keep the frame in every script: the shebang, the
section comments, `Args`, `parse_args`, `main` returning an `int`, and the
`raise SystemExit` entry point. Adapt names, arguments, and options to the
agreed specification. The input and output helpers — the `-` checks and the
stdin/stdout wiring — are the standard pattern only when the script is such a
filter; for any other script shape, replace that wiring with what the agreed
specification needs and keep the rest of the frame.

```python
#!/usr/bin/env python3

import argparse
import sys
from collections.abc import Sequence
from dataclasses import dataclass

SCRIPT_NAME = "script-name"


# = Types =

@dataclass(frozen=True)
class Args:
    input_path: str
    output_path: str


# = Logic =

def process(text: str) -> str:
    ...


# = Interface =

def parse_args(argv: Sequence[str] | None = None) -> Args:
    parser = argparse.ArgumentParser(prog=SCRIPT_NAME)
    parser.add_argument("input", help="Input file to read, or - for stdin.")
    parser.add_argument(
        "-o", "--output", default="-", help="Write output to a file."
    )
    namespace = parser.parse_args(argv)
    return Args(input_path=namespace.input, output_path=namespace.output)


def fail(message: str) -> int:
    print(f"{SCRIPT_NAME}: {message}", file=sys.stderr)
    return 1


def read_input(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    with open(path, encoding="utf-8") as file:
        return file.read()


def write_output(path: str, text: str) -> None:
    if path == "-":
        sys.stdout.write(text)
        return
    with open(path, "w", encoding="utf-8") as file:
        file.write(text)


def main(args: Args) -> int:
    try:
        text = read_input(args.input_path)
        write_output(args.output_path, process(text))
    except OSError as error:
        return fail(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(parse_args()))
```

## Error Handling

- Command-line usage errors belong in `parse_args` via `parser.error` (exit
  status 2).
- Catch expected runtime failures (such as `OSError`) in `main`, report them to
  stderr as `<script name>: <message>`, and return 1. Do not let expected
  failures escape as tracebacks.
- Only `main` decides the exit status; logic functions raise exceptions instead
  of exiting.

## Dependencies

- Use only the Python standard library unless the specification names an
  approved library.
- Declare each approved non-standard-library dependency in a PEP 723 inline
  metadata block, and use `uv run <script>` to run and validate the script:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = ["example-package"]
# ///
```

## Style

- Follow PEP 8.
- Add type annotations to every function definition.
- Do not write explanatory comments.
- Use section comments from the required skeleton to keep top-level code grouped
  by role.
- Express behavior through types, names, functions, and simple control flow.

## Validation

After creating the script, run lightweight CLI checks when feasible:

- Confirm `python3 -m py_compile <script>` passes.
- Confirm `--help` works.
- Run at least one representative success command and one expected error case
  for the agreed behavior. Use `uv run <script>` for scripts that declare
  PEP 723 dependencies.
- Run `ruff check` when it is available, on PATH or via `uvx ruff check`.
- Create any test fixtures in the script's directory or a temporary location
  and remove them after validation.
- Report the checks you ran and their results when delivering the script.
