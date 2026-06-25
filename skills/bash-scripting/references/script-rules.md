# Script Rules

Read this before implementation. These rules cover how to implement the agreed
specification; the public behavior comes from `SKILL.md` and the completed
interview.

## File Format

- Start the file with `#!/usr/bin/env bash`.
- Use `set -euo pipefail`.
- Write Bash, not POSIX `sh`.

## Commands

- Use Bash builtins and agreed command-line tools.
- Do not embed substantial Python, Node, or other language programs inside Bash.

## Structure

- Put the script's behavior in logic functions.
- Treat the interface section as the boundary from CLI concerns to script
  behavior. Keep `usage`, option parsing, positional argument validation,
  stdin/stdout/file wiring, diagnostics, and entry-point code there.
- Keep logic functions focused on the script's operation. They should not know
  option names, interpret `-`, validate CLI arguments, or print CLI diagnostics.
- Adapt input and output at the interface boundary so each operation has one
  logic path instead of duplicated transformations for different input sources.
- Use `main "$@"` as the entry point.

Use this structure as the required skeleton, adapting names, arguments, and
option cases to the agreed specification:

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
    local output_path="-"
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

    if [[ "${input_path}" != "-" ]]; then
        [[ -f "${input_path}" ]] || {
            printf 'Error: input is not a file: %s\n' "${input_path}" >&2
            return 1
        }
        [[ -r "${input_path}" ]] || {
            printf 'Error: input is not readable: %s\n' "${input_path}" >&2
            return 1
        }
    fi

    if [[ "${input_path}" == "-" && "${output_path}" == "-" ]]; then
        process
    elif [[ "${input_path}" == "-" ]]; then
        process >"${output_path}"
    elif [[ "${output_path}" == "-" ]]; then
        process <"${input_path}"
    else
        process <"${input_path}" >"${output_path}"
    fi
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

## Option Parsing

- Implement accepted options with `getopts` inside `main`.
- Use a leading `:` in the `getopts` option string so missing values and unknown
  options are handled explicitly.
- After `shift "$((OPTIND - 1))"`, validate positional arguments in `main`.

## Style

- Write ShellCheck-friendly Bash.
- Do not write explanatory comments.
- Use section comments from the required skeleton to keep top-level code grouped
  by role.
- Express behavior through names, functions, and simple control flow.

## Validation

After creating the script, run lightweight CLI checks when feasible:

- Confirm `bash -n` passes.
- Confirm `-h` works.
- Run at least one representative command for the agreed behavior.
- Run `shellcheck` when it is available.
