#!/usr/bin/env bash

# =============================================================================
# do_python.sh  Task runner for the py-mathx-lab repository.
#
# Usage:
#   ./do.sh help
#   ./do.sh conda-dev
#   ./do.sh conda
#   ./do.sh install-dev
#   ./do.sh dev
#   ./do.sh run e001_taylor_error_landscapes --out out/e001 --seed 1
# =============================================================================

set -euo pipefail

# -----------------------------------------------------------------------------
# Args
# -----------------------------------------------------------------------------
if [[ $# -lt 1 ]]; then
  echo "Error: Missing MODULE argument."
  echo "Usage: $0 <MODULE> <target> [args...]"
  exit 1
fi

MODULE="$1"
TARGET="${2:-help}"
shift || true
shift || true

# -----------------------------------------------------------------------------
# Repo settings
# -----------------------------------------------------------------------------
REPO_NAME="py-mathx-lab"
ENV_NAME_DEV="py-mathx-lab-dev"
ENV_NAME_PROD="py-mathx-lab"

CFG_DIR="config"
ENV_FILE_DEV="${CFG_DIR}/environment_dev.yml"
ENV_FILE_PROD="${CFG_DIR}/environment.yml"

# -----------------------------------------------------------------------------
# Colors
# -----------------------------------------------------------------------------
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

check_tool() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo -e "${RED}Error: '$1' is required but not installed / not on PATH.${NC}" >&2
    exit 1
  fi
}

help_menu() {
  echo "===================================================================="
  echo "${REPO_NAME} — task runner"
  echo "--------------------------------------------------------------------"
  echo -e "${CYAN}help${NC}           Show this help."
  echo -e "${CYAN}conda-dev${NC}      Create/update the dev conda env (${ENV_NAME_DEV})."
  echo -e "${CYAN}conda${NC}          Create/update the minimal conda env (${ENV_NAME_PROD})."
  echo -e "${CYAN}install-dev${NC}    pip install -e \".[dev]\""
  echo -e "${CYAN}install${NC}        pip install -e ."
  echo -e "${CYAN}format${NC}         ruff format ."
  echo -e "${CYAN}lint${NC}           ruff check ."
  echo -e "${CYAN}mypy${NC}           mypy ${MODULE}"
  echo -e "${CYAN}pytest${NC}         pytest -q"
  echo -e "${CYAN}dev${NC}            format + lint + mypy + pytest"
  echo -e "${CYAN}run${NC}            Run an experiment module (e.g. run e001_... --out ... --seed ...)"
  echo "===================================================================="
}

conda_dev() {
  check_tool conda
  if [[ ! -f "${ENV_FILE_DEV}" ]]; then
    echo -e "${RED}Error: ${ENV_FILE_DEV} not found.${NC}" >&2
    exit 1
  fi

  conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main || true
  conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r || true
  conda config --set always_yes true

  conda deactivate || true
  conda env create -f "${ENV_FILE_DEV}" || conda env update --prune -f "${ENV_FILE_DEV}"

  echo "--------------------------------------------------------------------"
  conda info --envs
  echo "===================================================================="
  echo "Next:"
  echo "  conda activate ${ENV_NAME_DEV}"
  echo "  ./do.sh install-dev"
  echo "===================================================================="
}

conda_prod() {
  check_tool conda
  if [[ ! -f "${ENV_FILE_PROD}" ]]; then
    echo -e "${RED}Error: ${ENV_FILE_PROD} not found.${NC}" >&2
    exit 1
  fi

  conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main || true
  conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r || true
  conda config --set always_yes true

  conda deactivate || true
  conda env create -f "${ENV_FILE_PROD}" || conda env update --prune -f "${ENV_FILE_PROD}"

  echo "--------------------------------------------------------------------"
  conda info --envs
  echo "===================================================================="
  echo "Next:"
  echo "  conda activate ${ENV_NAME_PROD}"
  echo "  ./do.sh install"
  echo "===================================================================="
}

install_dev() {
  check_tool python
  check_tool pip
  pip install -U pip
  pip install -e ".[dev]"
}

install_pkg() {
  check_tool python
  check_tool pip
  pip install -U pip
  pip install -e .
}

format_target() {
  check_tool ruff
  ruff format .
}

lint_target() {
  check_tool ruff
  ruff check .
}

mypy_target() {
  check_tool mypy
  mypy "${MODULE}"
}

pytest_target() {
  check_tool pytest
  pytest -q
}

dev_target() {
  format_target
  lint_target
  mypy_target
  pytest_target
}

run_experiment() {
  if [[ $# -lt 1 ]]; then
    echo -e "${RED}Error: 'run' requires an experiment module, e.g. e001_taylor_error_landscapes${NC}" >&2
    exit 1
  fi
  local exp_mod="$1"
  shift || true

  check_tool python
  python -m "experiments.${exp_mod}" "$@"
}

case "${TARGET}" in
  help) help_menu ;;
  conda-dev) conda_dev ;;
  conda) conda_prod ;;
  install-dev) install_dev ;;
  install) install_pkg ;;
  format) format_target ;;
  lint) lint_target ;;
  mypy) mypy_target ;;
  pytest) pytest_target ;;
  dev) dev_target ;;
  run) run_experiment "$@" ;;
  *)
    echo -e "${RED}Error: Unknown target '${TARGET}'. Use: ./do.sh help${NC}" >&2
    exit 1
    ;;
esac
