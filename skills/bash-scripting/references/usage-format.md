# Usage Format

Read this when help output is part of the request or the script will be shared with other users.

Keep the interface smaller before adding more notation.

## Core Rule

`usage()` documents the exact public interface.

- `Usage:` lists only supported invocation forms.
- `Commands:` lists only supported subcommands.
- `Arguments:` lists only placeholders that appear in `Usage:`.
- `Options:` lists only accepted options.
- `Examples:` shows representative successful commands, not extra behavior.

If these sections become hard to keep consistent, simplify the CLI.

## Section Order

Use concise language. Default to English unless the user asks for another language or the surrounding script already uses one.

Recommended section order:

1. One-line description.
2. `Usage:`
3. `Commands:` when the script has subcommands.
4. `Arguments:` when the script has positional arguments.
5. `Options:`
6. `Environment:` when environment variables affect behavior.
7. `Examples:`

Rules:

- The one-line description states what the script does.
- Do not use marketing words such as `simple`, `easy`, `powerful`, or `fast`.
- `Usage:` contains only supported invocation forms.
- `Commands:` lists every subcommand from `Usage:` and no others.
- `Arguments:` documents every placeholder from `Usage:` and no others.
- `Options:` documents every accepted option and no others.
- `Environment:` documents environment variables, not CLI options.
- `Examples:` contains 1 to 3 representative successful examples.
- Examples must be copyable commands.
- Do not include `--help` as an example.
- Do not introduce behavior in `Examples:` that is not already documented elsewhere in help.
- Keep descriptions short.
- Use consistent indentation.
- Use one blank line between sections.

## Usage Notation

Use one invocation form per line:

```text
Usage:
  script <input>
  script [<file>]
  script list <dir>
  script show <file>
  script [--json] <input>
```

Notation:

- `<name>` is a required value.
- `[<name>]` is an optional value.
- `<name>...` is one or more values.
- `[<name>...]` is zero or more values.
- `[--flag]` is an optional boolean flag.
- `--flag <value>` is an option with a required value.
- Bare words are subcommands.

Do not use `|`, `{}`, nested option groups, or EBNF-style grammar. If the notation needs that, redesign the CLI.

## Zero Arguments

Choose the zero-argument behavior before adding notation.

- If zero arguments perform a real action, include that invocation form in `Usage:`.
- If zero arguments only show help because no useful action exists, do not add a separate `Usage:` line for it.
- Do not include help-only invocations in `Examples:`.

## Options

`Options:` always contains `-h, --help` and any other accepted options.

Rules:

- List `-h, --help` first.
- Prefer long option names for shared scripts.
- Add short aliases when they are conventional or the user asks.
- Values use the form `--format <format>`.
- Boolean flags use the form `--json`.
- Put default values at the end of option descriptions, such as `Default: text.`
- Put small allowed value sets in the description, such as `Output format: text, json.`
- Keep parser order and `Options:` order aligned.
- Do not accept options that are not documented in `Options:`.

## Arguments

Rules:

- Document every placeholder from `Usage:`.
- Do not document placeholders that are not in `Usage:`.
- If the same placeholder appears in multiple `Usage:` lines, document it once.
- Use the same notation as `Usage:`, such as `<file>...` or `[<file>]`.
- Explain the argument's concrete role, such as `Markdown file to read.`
- When an argument is optional, document what happens when it is omitted.
- When a repeated argument is used, make the required count visible in `Usage:`.

## Commands

Rules:

- Write `Commands:` only when the script has subcommands.
- Document every subcommand from `Usage:`.
- Do not document subcommands that are not in `Usage:`.
- Explain command names only. Put command arguments in `Arguments:`.
- Start command descriptions with a verb.

## Single Positional Argument

Use this for one input with stdout output.

```text
Process a Markdown file and write HTML to stdout.

Usage:
  md-to-html <input>

Arguments:
  <input>  Markdown file to read.

Options:
  -h, --help  Show this help message.

Examples:
  md-to-html README.md > README.html
```

## Repeated Positional Arguments

Use this when the script requires at least one item.

```text
Print matching lines from files.

Usage:
  find-lines <file>...

Arguments:
  <file>...  Files to search.

Options:
  -h, --help  Show this help message.

Examples:
  find-lines src/*.txt
```

## Optional File Or Stdin

Use this for filter-like scripts that read stdin when no file is given.

```text
Normalize JSON and write it to stdout.

Usage:
  normalize-json [<file>]

Arguments:
  [<file>]  JSON file to read. Reads stdin when omitted.

Options:
  -h, --help  Show this help message.

Examples:
  normalize-json data.json
  cat data.json | normalize-json
```

## Subcommands

Use this when the script has multiple modes.

```text
Inspect saved entries.

Usage:
  entries list <dir>
  entries show <file>

Commands:
  list  List matching entries.
  show  Show one entry.

Arguments:
  <dir>   Directory to search.
  <file>  Entry file to show.

Options:
  -h, --help  Show this help message.

Examples:
  entries list notes
  entries show notes/today.txt
```

## One Leading Flag

Use this when one optional flag is clearer than another positional argument or subcommand.

```text
Read a data file and write selected fields to stdout.

Usage:
  select-fields [--json] <input>

Arguments:
  <input>  Data file to read.

Options:
  -h, --help  Show this help message.
  --json      Write JSON output.

Examples:
  select-fields data.txt
  select-fields --json data.txt
```

## Multiple Flags

Use this when multiple options are genuinely clearer than subcommands or smaller scripts.

```text
Render a report from an input file.

Usage:
  render-report [--format <format>] [--verbose] <input>

Arguments:
  <input>  Report source file to read.

Options:
  -h, --help         Show this help message.
  --format <format>  Output format: text, json. Default: text.
  --verbose          Write diagnostics to stderr.

Examples:
  render-report report.txt
  render-report --format json report.txt
```

Do not add this shape casually. First try positional arguments, subcommands, or a smaller interface.
