# Basic CLI Design

Read this before choosing or changing a script interface. This is the normal path.

Do not start with flags. Do not read `advanced-option-parsing.md` during first-pass CLI design.

## Decision Order

Stop at the first shape that fits the task:

1. Filter: read stdin and write stdout.
2. Single positional argument: `script <input>`.
3. Positional input and explicit output: `script <input> <output>`.
4. Repeated positional arguments: `script <file>...`.
5. Optional file or stdin: `script [<file>]`.
6. Subcommands for multiple modes: `script list <dir>` and `script show <file>`.
7. Environment variables for stable configuration that should not clutter the CLI.
8. Flags only when the simpler shapes make the interface worse.

If flags still look necessary, explain the tradeoff to the user. Read `advanced-option-parsing.md` only after the user accepts that tradeoff.

## Positional Arguments

Use positional arguments for single-purpose scripts.

Good shapes:

```text
script <input>
script <input> <output>
script <file>...
script [<file>]
```

Keep positional arguments few and meaningful. If the order becomes hard to remember, prefer subcommands or a smaller script.

## Subcommands

Use subcommands when the script has multiple modes.

Good shapes:

```text
script list <dir>
script show <file>
script convert <input> <output>
```

Use a small `case` dispatch in `main()`:

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

## Environment Variables

Use environment variables for stable configuration, not for ordinary positional inputs.

Good uses:

- Selecting a specific command binary.
- Providing a base URL, cache directory, or default format.
- Supplying configuration that should remain out of the CLI.

Map uppercase environment variables to lowercase internal readonly variables:

```bash
readonly tool_bin="${TOOL_BIN:-tool}"
```

Document environment variables in `Environment:`, not in `Options:`.

## Usage Errors

Unknown commands, unknown options, missing arguments, and invalid argument values are usage errors and exit with code `2`.

Do not automatically print usage on errors. Tell the user what is wrong and how to proceed:

```bash
die "missing input file; pass <input> or use --help for usage" 2
die "unknown command: $1; use --help to see available commands" 2
```

## Flags

Flags are a last resort for this skill.

Before adding a flag, ask:

- Can this be a positional argument?
- Can this be a subcommand?
- Can this be an environment variable?
- Is this feature making a disposable script too broad?

If a flag is still necessary, do not invent a parser from memory. Read `advanced-option-parsing.md` only after the user accepts the tradeoff.
