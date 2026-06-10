# Advanced Option Parsing

This is a last-resort reference. Do not read or use it during first-pass CLI design.

Read this only when all of these are true:

- Positional arguments and subcommands make the interface worse.
- A flag-based interface is still necessary.
- The flag set is small and stable.
- The user accepted the tradeoff.

`getopts` is forbidden. Use hand-written `case` parsing only.

Do not switch to another language unless the user explicitly asks for it. If option parsing becomes complex, explain the tradeoff and ask the user before changing languages.

Keep `Options:` order and parser order aligned.

## One Leading Flag

Use this only when one optional flag is clearly better than another positional argument or subcommand.

```bash
main() {
  local mode='text'

  case "${1:-}" in
    -h|--help)
      usage
      exit 0
      ;;
    "")
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

Use `while` plus `case` only when all conditions at the top of this file are satisfied and the script genuinely needs more than one optional flag.

```bash
main() {
  local format='text'
  local verbose=0
  local args=()

  if [[ $# -eq 0 ]]; then
    usage
    exit 0
  fi

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
