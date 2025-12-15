#!/usr/bin/env bash

# Simple wrapper for scripts/do_python.sh (fixed MODULE=mathxlab).

set -euo pipefail

MODULE="mathxlab"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUNNER="${SCRIPT_DIR}/scripts/do_python.sh"

if [[ ! -x "${RUNNER}" ]]; then
  echo "Error: ${RUNNER} not found or not executable."
  echo "Hint: chmod +x scripts/do_python.sh"
  exit 1
fi

if [[ $# -eq 0 ]]; then
  "${RUNNER}" "${MODULE}" help
else
  "${RUNNER}" "${MODULE}" "$@"
fi
