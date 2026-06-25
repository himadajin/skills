# CLI Interface

Read this when writing `usage` and the option parsing section of `main`.

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

Use this shape:

```bash
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
```

## Option Parsing

Use `getopts` inside `main`. Do not create a separate `parse_args` function.

Use short options as the standard interface. Do not add long option aliases by
default. Support `-h` for help. Use `-o <path>` for file output when saving
primary output to a file is part of the script's behavior.

Use a leading `:` in the option string so missing values and unknown options are
handled explicitly.

Use this shape:

```bash
main() {
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

    process "$1" "${output_path}"
}
```

After `shift "$((OPTIND - 1))"`, validate positional arguments in `main` and
pass the resulting values explicitly to logic functions.
