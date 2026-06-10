#!/usr/bin/env bash
set -euo pipefail

# = Script setup =
readonly color_red=$'\033[31m'
readonly color_cyan=$'\033[36m'
readonly color_reset=$'\033[0m'
readonly tool_bin="${TOOL_BIN:-cat}"

help_cyan=''
help_reset=''
error_red=''
error_reset=''

if [[ -t 1 && -z "${NO_COLOR:-}" ]]; then
  help_cyan=${color_cyan}
  help_reset=${color_reset}
fi

if [[ -t 2 && -z "${NO_COLOR:-}" ]]; then
  error_red=${color_red}
  error_reset=${color_reset}
fi

readonly help_cyan help_reset error_red error_reset

# = Script interface =
usage() {
  local command_name=${0##*/}

  cat <<EOF
Process an input file and write the result to stdout.

${help_cyan}Usage:${help_reset}
  ${command_name} <input>

${help_cyan}Arguments:${help_reset}
  ${help_cyan}<input>${help_reset}  Input file to process.

${help_cyan}Options:${help_reset}
  ${help_cyan}-h, --help${help_reset}  Show this help message.

${help_cyan}Environment:${help_reset}
  ${help_cyan}TOOL_BIN${help_reset}  Command used to process the input. Default: cat

${help_cyan}Examples:${help_reset}
  ${command_name} input.txt > output.txt
EOF
}

die() {
  local message=$1
  local code=${2:-1}

  printf '%sError:%s %s\n' "${error_red}" "${error_reset}" "${message}" >&2
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
