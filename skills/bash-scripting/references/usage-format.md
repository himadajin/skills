# Usage Format

Use this reference when the template is not enough. Keep the interface smaller before adding more notation.

## Core Rule

`usage()` documents the exact public interface.

- `Usage:` lists only supported invocation forms.
- `Commands:` lists only supported subcommands.
- `Arguments:` lists only placeholders that appear in `Usage:`.
- `Options:` lists only accepted options.
- `Examples:` shows representative successful commands, not extra behavior.

If these sections become hard to keep consistent, simplify the CLI.

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

Use this only when one optional flag is clearer than another positional argument or subcommand.

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

## Last-Resort Multiple Flags

Use this only with the parser pattern in `option-parsing.md`.

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
