# Script Rules

Read this before implementing the Bash script.

## File Format

- Write one self-contained Bash file.
- Start the file with `#!/usr/bin/env bash`.
- Use `set -euo pipefail`.

## Dependencies

- Write Bash, not POSIX `sh`.
- Use Bash builtins and agreed command-line tools.
- Do not embed substantial Python, Node, or other language programs inside Bash.
- Do not hand-roll parsers for structured data formats in Bash; use an agreed
  purpose-built command or choose another language.

## Structure

- Put script behavior in logic functions.
- Keep `usage`, option parsing, positional argument validation, and entry-point
  code in the interface section.
- Use `getopts` inside `main` for option parsing.
- Do not define `parse_args`.
- Pass values explicitly from `main` into logic functions.
- Use `main "$@"` as the entry point.

Use this structure as the required skeleton:

```bash
#!/usr/bin/env bash
set -euo pipefail


# = Logic =

process() {
    :
}


# = Interface =

usage() {
    cat <<'USAGE'
Usage: script-name [-o output] input

Arguments:
  input       Input file to read.

Options:
  -h          Show this help.
  -o output   Write output to file.
USAGE
}

main() {
    local input_path=""
    local output_path=""
    local option

    while getopts ":ho:" option; do
        case "${option}" in
            h)
                usage
                return 0
                ;;
            o)
                output_path="${OPTARG}"
                ;;
            :)
                printf 'Error: missing value for -%s\n' "${OPTARG}" >&2
                return 2
                ;;
            \?)
                printf 'Error: unknown option: -%s\n' "${OPTARG}" >&2
                return 2
                ;;
        esac
    done
    shift "$((OPTIND - 1))"

    [[ $# -eq 1 ]] || {
        printf 'Error: expected 1 argument, got %s\n' "$#" >&2
        return 2
    }

    input_path="$1"
    process "$input_path" "$output_path"
}

main "$@"
```

## Usage

`usage` documents the exact public interface implemented by the script.

Use `Usage:` and `Options:` by default. Add `Arguments:` when positional
arguments need explanation. Add `Examples:` only when an example prevents
ambiguity.

Keep `usage` synchronized with `main`:

- Every option accepted by `main` appears in `Options:`.
- Every placeholder in `Usage:` is accepted and validated by `main`.
- `Examples:` shows only behavior already documented by `Usage:`, `Arguments:`,
  or `Options:`.

## Options

- Use short options as the standard interface.
- Do not add long option aliases by default.
- Always support `-h`.
- Use `-o <path>` for file output when saving primary output to a file is part
  of the script's behavior.
- Use a leading `:` in the `getopts` option string so missing values and unknown
  options are handled explicitly.
- After `shift "$((OPTIND - 1))"`, validate positional arguments in `main`.

## Style

- Write ShellCheck-friendly Bash.
- Do not write explanatory comments.
- Use section comments from the required skeleton to keep top-level code grouped
  by role.
- Express behavior through names, functions, and simple control flow.

## CLI Design

- Follow Unix command-line conventions.
- Keep the interface small.
- Prefer positional arguments for primary inputs.
- Prefer `-` to mean stdin or stdout when that fits the task.
- Write primary output to stdout by default.
- Write diagnostics and errors to stderr.
- Do not print success messages by default.
- Do not add extra features unless they are needed for the agreed specification.

## Validation

After creating the script, run lightweight CLI checks when feasible:

- Confirm `bash -n` passes.
- Confirm `-h` works.
- Run at least one representative command for the agreed behavior.
- Run `shellcheck` when it is available.
