---
name: bash-scripting
description: Use when creating, reviewing, or revising Bash scripts that must follow a fixed small-utility style: Bash-only implementation, UNIX-style composability, predictable usage() output, simple CLI design, and safe shell idioms.
---

# bash-scripting

Use this skill for Bash scripts that should be small, predictable, and composable.

## Non-Negotiable Rules

- Use Bash only. Start scripts with `#!/usr/bin/env bash` and `set -euo pipefail`.
- Do not write POSIX `sh` unless the user explicitly asks for it.
- Do not switch to another language unless the user explicitly asks for it.
- Do not embed another language inside Bash with heredocs or generated files, such as `python - <<'PY'`, `node - <<'JS'`, or `cat <<EOF > script.py`.
- Short `sed`, `awk`, and `jq` expressions passed as CLI arguments are allowed.
- Start new scripts from `references/template.sh`.
- Keep the template structure unless the user asks for a smaller final script.
- `usage()`, `die()`, `color_enabled()`, `validate()`, `main()`, and `main "$@"` are required.
- `cleanup()` and `trap cleanup EXIT` may be removed only when the script does not create temporary files or directories.
- Additional task functions go under `# Task functions`, ordered by the order in which `main()` calls them.
- Follow UNIX philosophy: write the primary result to stdout, and write errors, diagnostics, warnings, and optional verbose output to stderr.
- Do not print success chatter such as `Done`, `Success`, or `Generated ...`.
- Do not add `--verbose` by default. Add it only when the user asks.
- Do not print decorative characters, emoji, or box drawing.
- Do not color machine-readable stdout.
- `usage()` is required, English-only, ASCII-only, and documents the exact public interface.
- `-h, --help` is required.
- Do not automatically print usage on errors. Error messages must say what is wrong and what the user should do next.
- Default CLI design uses no flags. Use positional arguments for single-purpose scripts and subcommands for multiple modes.
- Use flags only when positional arguments and subcommands make the interface worse.
- `getopts` is forbidden.
- Do not read or use advanced option parsing during first-pass CLI design.
- `validate()` checks preconditions only. It must not perform the task.
- Do not modify input files in place by default. Prefer stdout and let callers redirect output.
- Deletion, overwrite, and other destructive behavior must be obvious from the interface and validated before execution.
- Prefer established CLI tools for their domains: `rg` for search, `jq` for JSON, `curl` for URLs and APIs, and `git` for Git operations.
- Do not hand-roll parsers for JSON, CSV, YAML, or other structured formats in Bash.

## Read Gates

These reference reads are part of this skill. Do not skip a required reference and rely on memory.

### New Scripts

Before writing code, read these files in order:

1. `references/template.sh`
2. `references/basic-cli.md`
3. `references/usage-format.md`
4. `references/bash-style.md`
5. `references/safety.md`

### Existing Script Changes

- Read `references/bash-style.md` before editing Bash code.
- Read `references/usage-format.md` when changing `usage()`, help output, arguments, commands, options, examples, or environment documentation.
- Read `references/basic-cli.md` when changing the CLI shape, positional arguments, subcommands, options, or environment overrides.
- Read `references/safety.md` when changing `validate()`, `die()`, `cleanup()`, temporary files, command dependencies, path handling, stdout/stderr behavior, output files, overwrites, deletion, or exit behavior.
- Read `references/template.sh` when adding the standard structure to a script or restoring missing required functions.
- If multiple triggers apply, read all triggered references before editing.

### Reviews

- Read `references/bash-style.md` before reviewing Bash style or implementation.
- Read `references/safety.md` unless the review is explicitly limited to formatting or help text.
- Read `references/usage-format.md` when reviewing help output or the public interface.
- Read `references/basic-cli.md` when reviewing CLI design.

### Flags And Option Parsing

- First read `references/basic-cli.md` and try positional arguments or subcommands.
- Do not read `references/advanced-option-parsing.md` during first-pass CLI design.
- Read `references/advanced-option-parsing.md` only when flags remain necessary after simpler CLI shapes fail and the user accepts that tradeoff.
- If `advanced-option-parsing.md` is not allowed by these gates, do not implement `while`/`case` option parsing.
