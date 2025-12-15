#!/usr/bin/env bash

set -euo pipefail

# ------------------------------------------------------------------------------
# run_prep_bash_scripts.sh: Normalize EOL + execution rights for bash scripts.
#
# Intended for: py-mathx-lab
# - makes relevant *.sh files executable
# - converts CRLF -> LF (Windows -> Unix) using dos2unix if available
# - prefers git-tracked files to avoid touching venv/out/build artifacts
# ------------------------------------------------------------------------------

echo "=========================================================================="
echo "Start $0"
echo "--------------------------------------------------------------------------"
echo "Normalize EOL and execution rights (Ubuntu/Linux)."
echo "--------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "=========================================================================="

ensure_dos2unix() {
  if command -v dos2unix >/dev/null 2>&1; then
    echo "dos2unix is already installed."
    return 0
  fi

  echo "Installing dos2unix..."
  if command -v apt >/dev/null 2>&1; then
    sudo apt update
    sudo apt install -y dos2unix
    return 0
  fi

  echo "Warning: apt not found; skipping dos2unix install."
  return 1
}

list_sh_files() {
  # Prefer git-tracked scripts (safer), but fall back to find if none are tracked yet.
  if command -v git >/dev/null 2>&1 && git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    local tracked
    tracked="$(git ls-files '*.sh' || true)"
    if [[ -n "${tracked}" ]]; then
      printf '%s\n' "${tracked}"
      return 0
    fi
  fi

  find . -type f -name '*.sh' \
    -not -path './.venv/*' \
    -not -path './out/*' \
    -not -path './build/*' \
    -not -path './dist/*' \
    -not -path './.git/*'
}

echo "Collecting bash scripts..."
mapfile -t SH_FILES < <(list_sh_files)

if [[ ${#SH_FILES[@]} -eq 0 ]]; then
  echo "No .sh files found."
  exit 0
fi

echo "--------------------------------------------------------------------------"
echo "Found ${#SH_FILES[@]} script(s)."
printf '%s\n' "${SH_FILES[@]}"
echo "--------------------------------------------------------------------------"

echo "=========================================================================="
echo "Setting execute bits..."
chmod +x "${SH_FILES[@]}"
echo "=========================================================================="

if ensure_dos2unix; then
  echo "=========================================================================="
  echo "Converting CRLF -> LF..."
  dos2unix "${SH_FILES[@]}"
  echo "=========================================================================="
else
  echo "=========================================================================="
  echo "Skipping CRLF conversion (dos2unix not available)."
  echo "=========================================================================="
fi

echo "--------------------------------------------------------------------------"
date +"DATE TIME : %d.%m.%Y %H:%M:%S"
echo "--------------------------------------------------------------------------"
echo "End   $0"
echo "=========================================================================="
