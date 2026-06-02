# Option Parsing

Avoid option parsing by default.

First try one of these interfaces:

```text
script <input>
script <input> <output>
script list <dir>
script show <file>
script convert <input> <output>
```

Flags make small scripts grow quickly. Prefer positional arguments for single-purpose scripts and subcommands for multiple modes.

Do not use `getopts`.

Do not switch to another language unless the user explicitly asks for it. If option parsing becomes complex, first simplify the CLI. If it still does not fit Bash, explain the tradeoff and ask the user before changing languages.

## Small Command Dispatch

Use this when a script has subcommands but no flags beyond `-h` and `--help`.

```bash
main() {
  case "${1:-}" in
    -h|--help)
      usage
      exit 0
      ;;
    list)
      shift
      validate_list "$@"
      list_items "$@"
      ;;
    show)
      shift
      validate_show "$@"
      show_item "$@"
      ;;
    "")
      die "missing command; use --help to see available commands" 2
      ;;
    -*)
      die "unknown option: $1; use --help to see available options" 2
      ;;
    *)
      die "unknown command: $1; use --help to see available commands" 2
      ;;
  esac
}
```

Prefer separate validation functions only when each command has meaningfully different arguments. Otherwise, keep one `validate()`.

## Minimal Flag Handling

Use this only when a small number of flags is clearly better than subcommands or positional arguments.

```bash
main() {
  local mode='text'

  case "${1:-}" in
    -h|--help)
      usage
      exit 0
      ;;
    --json)
      mode='json'
      shift
      ;;
    -*)
      die "unknown option: $1; use --help to see available options" 2
      ;;
  esac

  validate "$@"
  run_task "${mode}" "$@"
}
```

This permits at most one simple leading flag. If more flexibility is needed, reconsider the CLI before adding a loop.

## Last-Resort Flag Loop

Use `while` plus `case` only when all of these are true:

- The script genuinely needs more than one optional flag.
- Subcommands would make the interface less clear.
- The flag set is small and stable.
- The user asked for this interface or accepted the tradeoff.

```bash
main() {
  local format='text'
  local verbose=0
  local args=()

  while (($# > 0)); do
    case "$1" in
      -h|--help)
        usage
        exit 0
        ;;
      --format)
        [[ $# -ge 2 ]] || die "missing value for --format; use --help for usage" 2
        format=$2
        shift 2
        ;;
      --verbose)
        verbose=1
        shift
        ;;
      --)
        shift
        args+=("$@")
        break
        ;;
      -*)
        die "unknown option: $1; use --help to see available options" 2
        ;;
      *)
        args+=("$1")
        shift
        ;;
    esac
  done

  validate "${args[@]}"
  run_task "${format}" "${verbose}" "${args[@]}"
}
```

Keep this form out of ordinary scripts. Its purpose is to make the exceptional case consistent, not to make flags easy to add.
