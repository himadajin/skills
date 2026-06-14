#!/usr/bin/env bash
set -euo pipefail

# = Script setup =
readonly tool_bin="${TOOL_BIN:-cat}"

# = Script interface =
usage() {
  local command_name=${0##*/}

  cat <<EOF
Process an input file and write the result to stdout.

Usage:
  ${command_name} <input>

Arguments:
  <input>  Input file to process.

Options:
  -h, --help  Show this help message.

Environment:
  TOOL_BIN  Command used to process the input. Default: cat

Examples:
  ${command_name} input.txt > output.txt
EOF
}

die() {
  local message=$1
  local code=${2:-1}

  printf 'Error: %s\n' "${message}" >&2
  exit "${code}"
}

validate() {
  command -v "${tool_bin}" >/dev/null 2>&1 || die "required command not found: ${tool_bin}" 127

  [[ $# -eq 1 ]] || die "expected exactly 1 argument, got $#; use --help for usage" 2
  [[ -f "$1" ]] || die "input file not found: $1; pass an existing file" 2
}

# = Script logic =
convert_file() {
  local input=$1

  "${tool_bin}" "${input}"
}

main() {
  if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
    usage
    exit 0
  fi

  if [[ $# -eq 0 ]]; then
    usage
    exit 0
  fi

  validate "$@"

  convert_file "$1"
}

main "$@"
