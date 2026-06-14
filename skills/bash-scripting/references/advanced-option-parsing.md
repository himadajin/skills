# Advanced Option Parsing

Read this when a script needs more than one or two flags or the parser is becoming the largest part of the script.

Before adding a larger parser, check whether a smaller interface would be clearer:

- Positional arguments for required inputs.
- Subcommands for modes.
- Environment variables for stable configuration.
- A separate script for a separate job.

Use `getopts` for short options. Use hand-written `while` plus `case` for long options. If option parsing becomes complex, consider a language with a real argument parser.

Keep `Options:` order and parser order aligned.

The examples call `validate()` because larger CLIs usually benefit from a separate precondition function. Replace that with inline checks when the script stays small.

## One Leading Flag

Use this when one optional flag is clearly better than another positional argument or subcommand.

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

This keeps single-flag scripts readable without a full parser.

## Short Options With getopts

Use `getopts` when the script has conventional short options.

```bash
main() {
  local format='text'
  local verbose=0

  while getopts ':f:vh' option; do
    case "${option}" in
      f)
        format=${OPTARG}
        ;;
      v)
        verbose=1
        ;;
      h)
        usage
        exit 0
        ;;
      :)
        die "missing value for -${OPTARG}; use --help for usage" 2
        ;;
      \?)
        die "unknown option: -${OPTARG}; use --help for usage" 2
        ;;
    esac
  done
  shift $((OPTIND - 1))

  run_task "${format}" "${verbose}" "$@"
}
```

`getopts` does not handle GNU-style long options. If the public interface needs long options such as `--format`, use a `while` plus `case` parser.

## Long Options With while/case

Use `while` plus `case` when the script needs long options.

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

Keep this form compact. If this parser keeps growing, the script likely needs a smaller interface or a different implementation language.
