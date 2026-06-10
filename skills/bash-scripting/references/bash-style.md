# Bash Style

Read this before creating scripts, editing Bash code, or reviewing Bash implementation.

## Structure

Keep this order:

```bash
#!/usr/bin/env bash
set -euo pipefail

# = Script setup =
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC2034
readonly script_dir
readonly color_red=$'\033[31m'
readonly color_cyan=$'\033[36m'
readonly color_reset=$'\033[0m'
readonly tool_bin="${TOOL_BIN:-tool}"

help_cyan=''
help_reset=''
error_red=''
error_reset=''

if [[ -t 1 && -z "${NO_COLOR:-}" ]]; then
  help_cyan=${color_cyan}
  help_reset=${color_reset}
fi

if [[ -t 2 && -z "${NO_COLOR:-}" ]]; then
  error_red=${color_red}
  error_reset=${color_reset}
fi

readonly help_cyan help_reset error_red error_reset

# = Script interface =
usage() { ... }
die() { ... }
validate() { ... }

# = Script logic =
task_function() { ... }

main() { ... }

main "$@"
```

Rules:

- Do not place task-specific functions between `usage()`, `die()`, `validate()`, and `cleanup()` when `cleanup()` is present.
- Keep exactly these top-level section comments: `# = Script setup =`, `# = Script interface =`, and `# = Script logic =`.
- Do not leave a blank line between a section comment and the first line in that section.
- Put task-specific functions and `main()` in `# = Script logic =`; order task-specific functions by the order in which `main()` calls them, then define `main()`.
- Keep `script_dir` and help/error color support in the template unless the user explicitly asks to remove them.
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
readonly color_reset=$'\033[0m'
```

- Top-level readonly variables may also cache simple startup decisions for fixed script output channels, such as whether help on stdout or errors on stderr should be colored.
- Runtime state belongs in `main()` or local function variables.
- Do not store derived state that depends on arguments, command results, or user input in globals.
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

Color is included to make help and errors quick to scan, not as a general output styling system.

- Respect `NO_COLOR`.
- Decide help and error color once near the top of the script.
- Help color is based on stdout: `[[ -t 1 && -z "${NO_COLOR:-}" ]]`.
- Error color is based on stderr: `[[ -t 2 && -z "${NO_COLOR:-}" ]]`.
- Use `cyan` for help headings, command names, paths, environment variable names, and placeholders.
- Use `red` for the `Error:` prefix only.
- Use `reset` immediately after each colored segment.
- Do not add color to task output by default.
- Do not add bold, warning colors, progress colors, success colors, or color helper functions by default.
- Never color machine-readable stdout.

## Comments

- Keep only the standard section comments: `# = Script setup =`, `# = Script interface =`, and `# = Script logic =`.
- Do not add line-by-line explanation comments.
- Use `usage()` to document the interface instead of comments.
- Add comments only to explain non-obvious reasons, not what the code already says.
- If code needs comments to be readable, refactor it first.
- Do not add `TODO` comments unless the user explicitly asks for them.
