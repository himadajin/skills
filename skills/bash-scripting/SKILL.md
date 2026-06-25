---
name: bash-scripting
description: Use only when the user explicitly asks to use this skill. Create a single-file Bash command-line script after interviewing the user to decide its script specification.
---

# bash-scripting

Use this skill to create a single-file Bash command-line tool.

## Workflow

Interview the user until you and the user share the same expected script
behavior. Do not treat the required decisions below as a checklist whose
completion automatically ends the interview.

Break down the user's request into the decisions that affect the implementation.
Resolve decisions in dependency order, asking about the most constraining
unresolved behavior first. Defer naming and other derived decisions until the
behavior they describe is stable. If multiple reasonable implementations remain,
ask another question instead of guessing.

Ask one question at a time and wait for the user's answer before continuing. For
each question, provide a recommended answer as a concrete proposal the user can
accept or revise.

Resolve at least these decisions before implementation:

- Purpose
- Input
- Output
- Command-line options
- Commands and dependencies
- Script name

After the decisions are clear, summarize the agreed specification briefly.

Then ask for explicit permission to create the script from that specification.
Phrase the confirmation naturally for the current conversation and make it clear
that implementation will start only after approval.

Create the script only after the user approves.

## Script Rules

### File Format

- Write one self-contained Bash file.
- Start the file with `#!/usr/bin/env bash`.
- Use `set -euo pipefail`.

### Bash and Dependencies

- Write Bash, not POSIX `sh`.
- Use Bash builtins and agreed command-line tools.
- Resolve required external commands during the interview.
- Do not embed substantial Python, Node, or other language programs inside Bash.
- Do not hand-roll parsers for structured data formats in Bash; use an agreed
  purpose-built command or choose another language.

### Command-Line Parsing

- Always support `-h` and `--help`.
- Document the actual public interface in `usage`.
- Parse command-line arguments in one function named `parse_args`.
- Use a short `case` loop in `parse_args`.
- Treat variables set by `parse_args` as interface state only; pass values
  explicitly from `main` into logic functions.

### Required Structure

- Put script behavior in logic functions.
- Keep command-line parsing and entry-point code in the interface section.
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

input_path=""
output_path=""

usage() {
    cat <<'USAGE'
Usage: script-name [options] input
USAGE
}

parse_args() {
    while (($#)); do
        case "$1" in
            -h|--help)
                usage
                exit 0
                ;;
            -o|--output)
                output_path="${2:?missing value for $1}"
                shift 2
                ;;
            --)
                shift
                break
                ;;
            -*)
                printf 'Error: unknown option: %s\n' "$1" >&2
                usage >&2
                return 2
                ;;
            *)
                input_path="$1"
                shift
                ;;
        esac
    done
}

main() {
    parse_args "$@"
    process "$input_path" "$output_path"
}

main "$@"
```

### Code Style

- Write ShellCheck-friendly Bash.
- Quote variable expansions.
- Use arrays for lists of arguments or paths.
- Use `local` for function-local variables.
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
- Treat `-o` / `--output` as the standard option for saving primary output to a
  file when file output is part of the script's behavior.
- Write diagnostics and errors to stderr.
- Do not print success messages by default.
- Do not add extra features unless they are needed for the agreed specification.

## Validation

After creating the script, run lightweight CLI checks when feasible:

- Confirm `bash -n` passes.
- Confirm `--help` works.
- Run at least one representative command for the agreed behavior.
- Run `shellcheck` when it is available.
