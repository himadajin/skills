---
name: bash-scripting
description: >-
  Coding conventions for small, single-file Bash command-line scripts.
  Use when creating or modifying standalone scripts for small tasks or builds.
  Not for shell libraries or scripts organized across multiple source files.
---

# bash-scripting

## CLI

- Prefer positional arguments for primary inputs.
- Use `-` for stdin or stdout when appropriate.
- Write primary output to stdout by default, and diagnostics to stderr.
- Use `-o <path>` for primary file output when applicable.
- Do not print success messages by default.
- Use short options parsed with `getopts` as the standard interface.
- Provide `-h` and keep the help consistent with the implementation.

## Structure

- Put the script’s execution flow in `main()` and call it with `main "$@"`
  at the end of the file.
- Keep CLI argument parsing and validation in `main()`.
- Extract functions when naming a distinct operation makes the flow easier
  to follow.

## Strings and variable expansion

- Quote strings and expansions unless shell interpretation is intended.
- Use braces when expanding variable names of two or more characters,
  as in `"${directory}"`.
