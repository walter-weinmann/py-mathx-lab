# Makefile — task runner for the py-mathx-lab repository
#
# Usage examples:
#   make help
#   make conda-dev
#   make conda
#   make install-dev
#   make dev
#   make run EXP=e001_taylor_error_landscapes ARGS="--out out/e001 --seed 1"
#
# Notes:
# - Make cannot "activate" conda in your current shell; it will print next steps.
# - You can override variables, e.g.: make mypy MODULE=my_package

SHELL := /usr/bin/env bash
.ONESHELL:
.SHELLFLAGS := -euo pipefail -c

# ------------------------------------------------------------------------------
# Repo configuration (adjust if needed)
# ------------------------------------------------------------------------------
REPO_NAME := py-mathx-lab

# Your do.sh wrapper fixes MODULE=mathxlab; keep that as default. :contentReference[oaicite:2]{index=2}
MODULE ?= mathxlab

CFG_DIR := config
ENV_NAME_DEV := py-mathx-lab-dev
ENV_NAME_PROD := py-mathx-lab
ENV_FILE_DEV := $(CFG_DIR)/environment_dev.yml
ENV_FILE_PROD := $(CFG_DIR)/environment.yml

# For "run"
EXP ?=
ARGS ?=

# ------------------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------------------
define require_tool
command -v "$(1)" >/dev/null 2>&1 || { echo "Error: '$(1)' is required but not installed / not on PATH." >&2; exit 1; }
endef

# ------------------------------------------------------------------------------
# Targets
# ------------------------------------------------------------------------------
.PHONY: help conda-dev conda install-dev install format lint mypy pytest dev run

.DEFAULT_GOAL := help

help:
	@echo "===================================================================="
	@echo "$(REPO_NAME) — task runner"
	@echo "--------------------------------------------------------------------"
	@echo "help           Show this help."
	@echo "conda-dev      Create/update the dev conda env ($(ENV_NAME_DEV))."
	@echo "conda          Create/update the minimal conda env ($(ENV_NAME_PROD))."
	@echo "install-dev    pip install -e \".[dev]\""
	@echo "install        pip install -e ."
	@echo "format         ruff format ."
	@echo "lint           ruff check ."
	@echo "mypy           mypy $(MODULE)"
	@echo "pytest         pytest -q"
	@echo "dev            format + lint + mypy + pytest"
	@echo "run            Run an experiment: make run EXP=e001_... ARGS=\"--out out/e001 --seed 1\""
	@echo "--------------------------------------------------------------------"
	@echo "Variables you can override:"
	@echo "  MODULE=<pkg>   (default: $(MODULE))"
	@echo "  EXP=<module>   experiment module under experiments/"
	@echo "  ARGS=\"...\"   extra CLI args passed to the experiment"
	@echo "===================================================================="

conda-dev:
	@$(call require_tool,conda)
	@if [[ ! -f "$(ENV_FILE_DEV)" ]]; then \
		echo "Error: $(ENV_FILE_DEV) not found." >&2; \
		exit 1; \
	fi
	conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main || true
	conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r || true
	conda config --set always_yes true
	conda deactivate || true
	conda env create -f "$(ENV_FILE_DEV)" || conda env update --prune -f "$(ENV_FILE_DEV)"
	echo "--------------------------------------------------------------------"
	conda info --envs
	echo "===================================================================="
	echo "Next:"
	echo "  conda activate $(ENV_NAME_DEV)"
	echo "  make install-dev"
	echo "===================================================================="

conda:
	@$(call require_tool,conda)
	@if [[ ! -f "$(ENV_FILE_PROD)" ]]; then \
		echo "Error: $(ENV_FILE_PROD) not found." >&2; \
		exit 1; \
	fi
	conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main || true
	conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r || true
	conda config --set always_yes true
	conda deactivate || true
	conda env create -f "$(ENV_FILE_PROD)" || conda env update --prune -f "$(ENV_FILE_PROD)"
	echo "--------------------------------------------------------------------"
	conda info --envs
	echo "===================================================================="
	echo "Next:"
	echo "  conda activate $(ENV_NAME_PROD)"
	echo "  make install"
	echo "===================================================================="

install-dev:
	@$(call require_tool,python)
	@$(call require_tool,pip)
	pip install -U pip
	pip install -e ".[dev]"

install:
	@$(call require_tool,python)
	@$(call require_tool,pip)
	pip install -U pip
	pip install -e .

format:
	@$(call require_tool,ruff)
	ruff format .

lint:
	@$(call require_tool,ruff)
	ruff check .

mypy:
	@$(call require_tool,mypy)
	mypy "$(MODULE)"

pytest:
	@$(call require_tool,pytest)
	pytest -q

dev: format lint mypy pytest

run:
	@if [[ -z "$(EXP)" ]]; then \
		echo "Error: EXP is required."; \
		echo "Example: make run EXP=e001_taylor_error_landscapes ARGS=\"--out out/e001 --seed 1\""; \
		exit 1; \
	fi
	@$(call require_tool,python)
	python -m "experiments.$(EXP)" $(ARGS)
