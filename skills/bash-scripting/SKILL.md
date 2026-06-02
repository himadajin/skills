---
name: bash-scripting
description: Create, review, and revise Bash scripts using a fixed style for small disposable utilities, UNIX-style composability, predictable help output, safe Bash idioms, and the reference template.
---

# bash-scripting

Use this skill when creating, reviewing, or revising Bash scripts.

This skill is for small disposable utilities. Prefer a simple command line interface, predictable behavior, and readable Bash over broad configurability.

## Scope

- Use Bash only. Start scripts with `#!/usr/bin/env bash`.
- Do not write POSIX `sh` unless the user explicitly asks for it.
- Do not switch to another language unless the user explicitly asks for it.
- Do not embed another language inside Bash with heredocs or generated files, such as `python - <<'PY'`, `node - <<'JS'`, or `cat <<EOF > script.py`.
- Short `sed`, `awk`, and `jq` expressions passed as CLI arguments are allowed.
- If Bash becomes a poor fit, explain the tradeoff and ask the user before changing languages.

## Reference Files

- For new scripts, start from `references/template.sh`.
- For option parsing, do not invent a new parser. First simplify the CLI. If flags are still necessary, read `references/option-parsing.md`.
- `getopts` is forbidden.

## Core Principles

- Follow UNIX philosophy: do one thing, compose with pipes, and avoid hidden side effects.
- Write the primary result to stdout.
- Write errors, diagnostics, warnings, and optional verbose output to stderr.
- Do not print success chatter such as `Done`, `Success`, or `Generated ...`.
- Do not print decorative characters, emoji, or box drawing.
- Do not color machine-readable stdout.
- For filter-like scripts, consider accepting stdin when it keeps the interface simple.
- Prefer external CLI tools for their domains: `rg` for search, `jq` for JSON, `curl` for URLs and APIs, and `git` for Git operations.
- Do not hand-roll parsers for JSON, CSV, YAML, or other structured formats in Bash.

## Standard Structure

Use this order:

```bash
#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly script_dir
tmp_dir=""

# Script interface

usage() { ... }

die() { ... }

color_enabled() { ... }

validate() { ... }

cleanup() { ... }

# Task functions

task_function() { ... }

# Entry point

main() { ... }

main "$@"
```

Rules:

- `usage()`, `die()`, `color_enabled()`, `validate()`, `main()`, and `main "$@"` are required.
- `cleanup()` and `trap cleanup EXIT` may be removed only when the script does not create temporary files or directories.
- `# Task functions` may be removed when there are no task-specific functions.
- Additional task-specific functions go between `validate()` and `main()`, under `# Task functions`.
- Order task-specific functions by the order in which `main()` calls them.
- Do not place task-specific functions between `usage()`, `die()`, `color_enabled()`, and `validate()`.
- Keep `script_dir`, `tmp_dir`, and color support in the template unless the user explicitly asks to remove them.

## Help Output

`usage()` is part of the interface and acts as the maintained documentation for the script.

Use English and ASCII only. Use this section order:

1. One-line description.
2. `Usage:`
3. `Commands:` when the script has subcommands.
4. `Arguments:` when the script has positional arguments.
5. `Options:`
6. `Environment:` when environment variables affect behavior.
7. `Examples:`

Rules:

- The one-line description states what the script does. Do not use marketing words such as `simple`, `easy`, `powerful`, or `fast`.
- `Usage:` contains only supported invocation forms.
- Use lowercase placeholders such as `<input>`, `<output>`, and `<dir>`.
- Use `<file>...` for repeated arguments.
- Use `[<file>]` for optional arguments.
- Use bare words for subcommands, such as `script list <dir>`.
- `Options:` normally contains only `-h, --help`.
- `Environment:` documents environment variables, not CLI options.
- `Examples:` contains 1 to 3 representative successful examples.
- Examples must be copyable commands.
- Do not include `--help` as an example.
- End descriptions with periods.
- Keep item descriptions to one line; if they need wrapping, simplify the text.
- Use 2 spaces of indentation for item lines.
- Align descriptions within the same section with at least 2 spaces between the item and the description.
- Use one blank line between sections.

## CLI Design

- Do not add flags by default.
- For a single-purpose script, use positional arguments.
- For multiple modes, use subcommands such as `script list <dir>` or `script convert <input> <output>`.
- Use flags only when positional arguments and subcommands make the interface worse.
- Keep option parsing with `case`; use `while` plus `case` only as a last resort.
- Do not use `getopts`.
- Unknown commands, unknown options, and invalid arguments are usage errors and exit with code `2`.
- Do not automatically print usage on errors. Give a clear error message and tell the user to use `--help` if needed.

## Exit Codes

- `0`: success.
- `1`: general runtime error.
- `2`: usage error, such as missing arguments, unknown commands, or invalid argument values.
- `127`: required command not found.

## Error Handling

- Use `set -euo pipefail`.
- Use `die()` for errors.
- `die()` prints `Error:` to stderr and exits.
- Error messages must say what is wrong and what the user should do next.
- Do not hide failing external commands behind unclear command substitutions.
- For important command substitutions, add context:

```bash
if ! output=$(some_command); then
  die "failed to run some_command"
fi
```

- Do not use `local var=$(command)`. Declare and assign separately when command status matters.

## Validation

`validate()` checks preconditions only. It must not perform the task.

Use `validate()` for:

- Required command checks.
- Required argument checks.
- Input file and directory checks.
- Output destination sanity checks when needed.
- Preconditions for destructive operations.

Missing commands should exit with code `127`:

```bash
command -v jq >/dev/null 2>&1 || die "required command not found: jq" 127
```

## Paths

- Do not depend on the caller's current directory unless that is the explicit interface.
- Use `script_dir` for files that live next to the script.
- Do not force all user-provided paths to absolute paths.
- Quote user-provided paths.
- Validate input paths in `validate()`.
- Do not write code that relies on `cd` and later returning to the previous directory.
- If a temporary directory change is needed, use a subshell such as `(cd "${dir}" && command ...)`.

## Variables

- Use lowercase `snake_case` for internal variables.
- Use uppercase names only for environment variables or exported values.
- Global variables are normally read-only configuration values.
- Environment overrides should map from uppercase environment names to lowercase internal names:

```bash
readonly tool_bin="${TOOL_BIN:-tool}"
```

- Runtime state belongs in `main()` or local function variables.
- The only standard mutable global is temporary resource state used by `cleanup()`, such as `tmp_dir=""`.
- Function-local working variables should normally be `local`.
- More detailed `local` declaration rules are intentionally not fixed here.

## Quoting and Expansion

- Quote command arguments, paths, and user input.
- Use braces for normal variable expansions, such as `"${dir}"`.
- Omit braces for simple special parameters such as `"$0"`, `"$1"`, `"$@"`, and `"$?"`.
- Do not quote where Bash syntax changes meaning:
  - Arithmetic contexts: `(( count > 0 ))`.
  - Pattern right-hand sides: `[[ "${file}" == *.md ]]`.
  - Regex right-hand sides: `[[ "${value}" =~ ^[0-9]+$ ]]`.
- Pass arrays as `"${array[@]}"`.
- Use intentional word splitting or glob expansion only when the reason is clear.

## Conditions and Loops

- Use `[[ ... ]]` for tests.
- Use `(( ... ))` for arithmetic.
- Do not use `test` or `[ ... ]`.
- Use `IFS= read -r line` when reading lines.
- Read files with:

```bash
while IFS= read -r line; do
  ...
done < "${file}"
```

- Do not use `for item in $(command)`.
- Iterate arrays with `for item in "${items[@]}"`.
- Simple globs are allowed:

```bash
for file in ./*.md; do
  [[ -e "${file}" ]] || continue
  ...
done
```

- For paths from `find`, prefer null delimiters:

```bash
while IFS= read -r -d '' path; do
  ...
done < <(find . -name '*.md' -print0)
```

- If output is line-oriented by definition, use `while IFS= read -r line`.
- Use `mapfile -t array < <(command)` only when collecting the full output is appropriate.

## Color

Color is allowed when it improves human-readable output, but it must not break pipelines.

- Use `color_enabled()` to check the output file descriptor.
- Respect `NO_COLOR`.
- Use only `red`, `cyan`, `yellow`, and `reset`.
- Do not use bold.
- `red`: `Error:` prefix only.
- `yellow`: `Warning:` prefix only.
- `cyan`: help headings, command names, paths, environment variable names, and placeholders.
- `reset`: immediately after each colored segment.
- Do not use color for success, completion, or progress.
- Do not make color the only carrier of meaning.
- Never color machine-readable stdout.

## Temporary Files

- Use `mktemp` or `mktemp -d`.
- Use `cleanup()` and `trap cleanup EXIT`.
- Do not use fixed paths such as `/tmp/script-name`.
- `tmp_dir` starts as an empty global variable so `cleanup()` is safe under `set -u`.
- `trap cleanup EXIT` goes in `main()` near the temporary resource creation.
- `cleanup()` must validate the target before `rm -rf`.

## File Modification and Deletion

- Filter-style scripts should read input and write transformed output to stdout.
- Let the caller redirect stdout to a file when they want a file output.
- If stdout cannot represent the result, accept an explicit output path or output directory.
- Do not modify input files in place by default.
- Do not overwrite existing files unless the interface clearly says so.
- Deletion scripts are allowed, but the command name, subcommand, and usage must make the destructive action obvious.
- Do not use `rm -rf` outside `cleanup()` without a strong reason and immediate validation of the target.
- Do not add confirmation prompts by default; prompts make scripts harder to compose and automate.
- Add `--dry-run` only when the user asks for it or the destructive scope makes it necessary.

## Comments

- Keep section comments: `# Script interface`, `# Task functions`, and `# Entry point`.
- Do not add line-by-line explanation comments.
- Use `usage()` to document the interface instead of comments.
- Add comments only to explain non-obvious reasons, not what the code already says.
- If code needs comments to be readable, refactor it first.
- Do not add `TODO` comments unless the user explicitly asks for them.
