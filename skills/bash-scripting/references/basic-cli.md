# Basic CLI Design

Read this when choosing or changing a script interface.

Default to the smallest interface that is easy to remember and hard to misuse.

## Decision Order

First choose what zero arguments mean:

- If the script has a natural zero-argument action, implement that action.
- If the script has no useful zero-argument action, show `usage()` and exit `0`.

This is part of the interface shape, not an error-handling special case.

Prefer these shapes, but do not treat the list as a rigid ladder:

1. Filter: read stdin and write stdout.
2. Single positional argument: `script <input>`.
3. Positional input and explicit output: `script <input> <output>`.
4. Repeated positional arguments: `script <file>...`.
5. Optional file or stdin: `script [<file>]`.
6. Subcommands for multiple modes: `script list <dir>` and `script show <file>`.
7. Environment variables for stable configuration that should not clutter the CLI.
8. Flags for optional behavior that would be awkward as a positional argument or subcommand.

If the script needs many flags, check whether it is doing too many jobs.

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
    "")
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

Unknown commands, unknown options, invalid argument values, and missing required arguments after a command, option, or mode has been selected are usage errors and exit with code `2`.

Do not automatically print usage on errors. Tell the user what is wrong and how to proceed:

```bash
die "missing input file for convert; pass <input> or use --help for usage" 2
die "unknown command: $1; use --help to see available commands" 2
```

## Flags

Use flags when they make the interface clearer.

Before adding several flags, ask:

- Can this be a positional argument?
- Can this be a subcommand?
- Can this be an environment variable?
- Is this feature making a disposable script too broad?

For one or two simple flags, a small `case` parser in `main()` is fine. For short options, `getopts` is fine. Read `advanced-option-parsing.md` when the parser starts to dominate the script.
