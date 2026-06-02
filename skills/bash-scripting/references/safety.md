# Runtime Safety

Read this before creating scripts, reviewing runtime behavior, or changing validation, errors, paths, temp files, output files, overwrites, deletion, or exit behavior.

## Output Contract

- Follow UNIX philosophy: do one thing, compose with pipes, and avoid hidden side effects.
- Write the primary result to stdout.
- Write errors, diagnostics, warnings, and optional verbose output to stderr.
- Do not print success chatter such as `Done`, `Success`, or `Generated ...`.
- Do not add confirmation prompts by default. Prompts make scripts harder to compose and automate.
- For filter-like scripts, consider accepting stdin when it keeps the interface simple.

## Exit Codes

- `0`: success.
- `1`: general runtime error.
- `2`: usage error, such as missing arguments, unknown commands, or invalid argument values.
- `127`: required command not found.

## Error Handling

- Use `set -euo pipefail`.
- Use `die()` for errors.
- `die()` prints `Error:` to stderr and exits.
- Error messages must say what is wrong and what the user should do next.
- Do not automatically print usage on errors.
- Do not hide failing external commands behind unclear command substitutions.
- For important command substitutions, add context:

```bash
if ! output=$(some_command); then
  die "failed to run some_command"
fi
```

- Do not use `local var=$(command)`. Declare and assign separately when command status matters.

## Validation

`validate()` checks preconditions only. It must not perform the task.

Use `validate()` for:

- Required command checks.
- Required argument checks.
- Input file and directory checks.
- Output destination sanity checks when needed.
- Preconditions for destructive operations.

User-supplied precondition failures, such as missing arguments, invalid argument values, and missing input paths, are usage errors and should exit with code `2`.

Missing commands should exit with code `127`:

```bash
command -v jq >/dev/null 2>&1 || die "required command not found: jq" 127
```

## Paths

- Do not depend on the caller's current directory unless that is the explicit interface.
- Use `script_dir` for files that live next to the script.
- Do not force all user-provided paths to absolute paths.
- Quote user-provided paths.
- Validate input paths in `validate()`.
- Do not write code that relies on `cd` and later returning to the previous directory.
- If a temporary directory change is needed, use a subshell such as `(cd "${dir}" && command ...)`.

## Temporary Files

When a script creates temporary files or directories:

- Use `mktemp` or `mktemp -d`.
- Prefer `tmp_dir=$(mktemp -d)` for temporary directories; do not pass a literal `/tmp/...` template unless the script's public interface explicitly requires that location.
- Add `tmp_dir`, `cleanup()`, and `trap cleanup EXIT` together.
- Do not use fixed paths such as `/tmp/script-name`.
- `tmp_dir` starts as an empty global variable so `cleanup()` is safe under `set -u`.
- `trap cleanup EXIT` goes in `main()` near the temporary resource creation.
- `cleanup()` must validate the target before `rm -rf`.

Minimum directory cleanup pattern:

```bash
tmp_dir=""

cleanup() {
  [[ -n "${tmp_dir}" && -d "${tmp_dir}" ]] || return 0
  rm -rf -- "${tmp_dir}"
}

main() {
  tmp_dir=$(mktemp -d)
  trap cleanup EXIT
}
```

When a script does not create temporary files or directories, do not define `tmp_dir`, `cleanup()`, or `trap cleanup EXIT`.

## File Modification And Deletion

- Filter-style scripts should read input and write transformed output to stdout.
- Let the caller redirect stdout to a file when they want a file output.
- If stdout cannot represent the result, accept an explicit output path or output directory.
- Do not modify input files in place by default.
- Do not overwrite existing files unless the interface clearly says so.
- Deletion scripts are allowed, but the command name, subcommand, and usage must make the destructive action obvious.
- Do not use `rm -rf` outside `cleanup()` without a strong reason and immediate validation of the target.
- Add `--dry-run` only when the user asks for it or the destructive scope makes it necessary.

## External Commands And Structured Data

- Prefer external CLI tools for their domains: `rg` for search, `jq` for JSON, `curl` for URLs and APIs, and `git` for Git operations.
- Do not hand-roll parsers for JSON, CSV, YAML, or other structured formats in Bash.
- If a required command is missing, fail during `validate()` with exit code `127`.
