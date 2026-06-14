---
name: bash-scripting
description: 'Use when the user asks to create, refactor, review, or revise a shell script artifact, or to turn commands, steps, or existing code into a shell script. Use for Bash scripts ranging from disposable personal utilities to reusable command-line tools. This skill implements shell scripts as Bash by default, but trigger on requests like "write a shell script to...", "refactor this .sh", "review this shell script", or requested edits to shell script files even when the user does not name Bash or this skill. Do not trigger for general shell questions, one-off command help, pipeline debugging, POSIX/zsh/PowerShell discussions, or narrow shell syntax/option questions unless the user is creating or revising a script artifact.'
---

# bash-scripting

Use this skill for Bash scripts that should be small, readable, predictable, and easy to delete or reuse.

Default to the smallest script that clearly does the job. Raise the structure only when the script is public, reused, destructive, or has a non-trivial CLI.

## Core Rules

- Use Bash by default. Start new scripts with `#!/usr/bin/env bash` and usually `set -euo pipefail`.
- Do not write POSIX `sh` unless the user explicitly asks for it.
- Do not switch to another language unless Bash is a poor fit or the user asks for another language.
- Do not embed substantial Python, Node, or other language programs inside Bash heredocs or generated files. If that language is doing the real work, write that script directly. Short `python -c`, `sed`, `awk`, and `jq` snippets are fine when they keep the script simpler.
- `usage()`, `die()`, `main()`, and `main "$@"` are required.
- `usage()` documents the actual public interface. Support `-h` and `--help`.
- `die()` writes errors to stderr and exits non-zero. Keep messages short; mention `--help` when it helps the user recover.
- `validate()` is optional. Use it when there are several preconditions, command checks, path checks, or destructive-operation checks; otherwise validate inline in `main()`.
- Use functions when they clarify steps or isolate repeated logic. Do not split every two-line operation into a function.
- Keep comments sparse. Use comments for non-obvious reasons, not for restating code.
- Write the primary result to stdout. Write errors, diagnostics, warnings, and optional verbose output to stderr.
- Do not print success chatter such as `Done`, `Success`, or `Generated ...` unless the user asked for human-oriented progress output.
- Do not add color, `--verbose`, `--dry-run`, or confirmation prompts by default. Add them only when requested or when the operation's risk makes the extra interface worthwhile.
- Do not color machine-readable stdout.
- Prefer positional arguments for one-purpose scripts, subcommands for multiple modes, and a small number of flags when flags make the interface clearer.
- For option parsing, use a short `case` parser or `getopts` as appropriate. If parsing becomes large, reduce the CLI or consider a language with a real argument parser.
- Do not modify input files in place by default. Prefer stdout, or accept an explicit output path when stdout cannot represent the result.
- Make deletion, overwrite, and other destructive behavior obvious from the command name, subcommand, usage text, and validation.
- Prefer established CLI tools for their domains: `rg` for search, `jq` for JSON, `curl` for URLs and APIs, and `git` for Git operations.
- Do not hand-roll parsers for JSON, CSV, YAML, or other structured formats in Bash.

## Reference Use

Most small scripts can be written from this file alone. Read references only when the task needs their detail:

- `references/template.sh`: when starting a reusable/public script or when the user wants a template.
- `references/basic-cli.md`: when choosing or revising positional arguments, subcommands, flags, or environment overrides.
- `references/usage-format.md`: when help output is part of the request or the script will be shared with other users.
- `references/bash-style.md`: when editing non-trivial Bash logic, reviewing Bash implementation, or adding color.
- `references/safety.md`: when handling temporary files, output files, overwrites, deletion, path-sensitive behavior, command dependencies, or exit behavior.
- `references/advanced-option-parsing.md`: when the script needs more than one or two flags or the parser is becoming the largest part of the script.
