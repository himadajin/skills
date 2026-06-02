#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly script_dir
readonly tool_bin="${TOOL_BIN:-cat}"
tmp_dir=""

# Script interface

usage() {
  local fd=${1:-1}
  local command_name=${0##*/}
  local red=''
  local cyan=''
  local yellow=''
  local reset=''

  if color_enabled "${fd}"; then
    red=$'\033[31m'
    cyan=$'\033[36m'
    yellow=$'\033[33m'
    reset=$'\033[0m'
  fi

  cat >&"${fd}" <<EOF
Process an input file and write the result to stdout.

${cyan}Usage:${reset}
  ${command_name} <input>

${cyan}Arguments:${reset}
  ${cyan}<input>${reset}  Input file to process.

${cyan}Options:${reset}
  ${cyan}-h, --help${reset}  Show this help message.

${cyan}Environment:${reset}
  ${cyan}TOOL_BIN${reset}  Command used to process the input. Default: cat

${cyan}Examples:${reset}
  ${command_name} input.txt > output.txt
EOF
}

die() {
  local message=$1
  local code=${2:-1}
  local red=''
  local reset=''

  if color_enabled 2; then
    red=$'\033[31m'
    reset=$'\033[0m'
  fi

  printf '%sError:%s %s\n' "${red}" "${reset}" "${message}" >&2
  exit "${code}"
}

color_enabled() {
  local fd=${1:-1}
  [[ -t "${fd}" && -z "${NO_COLOR:-}" ]]
}

validate() {
  command -v "${tool_bin}" >/dev/null 2>&1 || die "required command not found: ${tool_bin}" 127

  [[ $# -eq 1 ]] || die "expected exactly 1 argument, got $#; use --help for usage" 2
  [[ -f "$1" ]] || die "input file not found: $1"
}

cleanup() {
  [[ -n "${tmp_dir}" && -d "${tmp_dir}" ]] || return 0
  rm -rf -- "${tmp_dir}"
}

# Task functions

convert_file() {
  local input=$1

  "${tool_bin}" "${input}"
}

# Entry point

main() {
  if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
    usage
    exit 0
  fi

  validate "$@"

  tmp_dir=$(mktemp -d)
  trap cleanup EXIT

  convert_file "$1"
}

main "$@"
