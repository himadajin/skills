# Bash Style

Read this before creating scripts, editing Bash code, or reviewing Bash implementation.

## Structure

Keep this order:

```bash
#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly script_dir
readonly color_red=$'\033[31m'
readonly color_cyan=$'\033[36m'
readonly color_reset=$'\033[0m'

# Script interface

usage() { ... }
die() { ... }
color_enabled() { ... }
validate() { ... }

# Task functions

task_function() { ... }

# Entry point

main() { ... }

main "$@"
```

Rules:

- Do not place task-specific functions between `usage()`, `die()`, `color_enabled()`, `validate()`, and `cleanup()` when `cleanup()` is present.
- `# Task functions` may be removed when there are no task-specific functions.
- Order task-specific functions by the order in which `main()` calls them.
- Keep `script_dir` and color support in the template unless the user explicitly asks to remove them.
- Add `tmp_dir`, `cleanup()`, and `trap cleanup EXIT` together only when the script creates temporary files or directories.
- Do not create a dummy temporary directory just to keep `cleanup()` or `trap cleanup EXIT` in the script.

## Variables

- Use lowercase `snake_case` for internal variables.
- Use uppercase names only for environment variables or exported values.
- Global variables are normally readonly configuration values or constants.
- Environment overrides map from uppercase environment names to lowercase internal names:

```bash
readonly tool_bin="${TOOL_BIN:-tool}"
```

- Put stable literal constants that would otherwise clutter functions, including ANSI escape codes, in top-level readonly variables:

```bash
readonly color_red=$'\033[31m'
readonly color_cyan=$'\033[36m'
readonly color_yellow=$'\033[33m'
readonly color_reset=$'\033[0m'
```

- Runtime state belongs in `main()` or local function variables.
- Do not store derived state that depends on arguments, output file descriptors, terminal state, command results, or user input in globals.
- The only standard mutable global is temporary resource state used by `cleanup()`, such as `tmp_dir=""`.
- Function-local working variables should normally be `local`.
- More detailed `local` declaration rules are intentionally not fixed.

## Quoting And Expansion

- Quote command arguments, paths, and user input.
- Use braces for normal variable expansions, such as `"${dir}"`.
- Omit braces for simple special parameters such as `"$0"`, `"$1"`, `"$@"`, and `"$?"`.
- Do not quote where Bash syntax changes meaning:
  - Arithmetic contexts: `(( count > 0 ))`.
  - Pattern right-hand sides: `[[ "${file}" == *.md ]]`.
  - Regex right-hand sides: `[[ "${value}" =~ ^[0-9]+$ ]]`.
- Pass arrays as `"${array[@]}"`.
- Use intentional word splitting or glob expansion only when the reason is clear.

## Conditions And Loops

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
- Use only these color roles: `red`, `cyan`, `yellow`, and `reset`.
- Define only the color constants used by the script.
- Keep ANSI escape codes in readonly globals such as `color_red`; use local `red`, `cyan`, `yellow`, and `reset` variables only for fd-gated output inside functions.
- Do not store enabled color state in globals because color depends on the output file descriptor and `NO_COLOR` at call time.
- Do not use bold.
- Do not add dedicated color helper functions beyond `color_enabled()`.
- `red`: `Error:` prefix only.
- `yellow`: `Warning:` prefix only.
- `cyan`: help headings, command names, paths, environment variable names, and placeholders.
- `reset`: immediately after each colored segment.
- Do not use color for success, completion, or progress.
- Do not make color the only carrier of meaning.
- Never color machine-readable stdout.

## Comments

- Keep section comments: `# Script interface`, `# Task functions`, and `# Entry point`.
- Do not add line-by-line explanation comments.
- Use `usage()` to document the interface instead of comments.
- Add comments only to explain non-obvious reasons, not what the code already says.
- If code needs comments to be readable, refactor it first.
- Do not add `TODO` comments unless the user explicitly asks for them.
