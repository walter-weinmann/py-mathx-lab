# Makefile — py-mathx-lab (Windows + Linux/macOS) using uv (uv-only)
#
# Usage examples:
#   make help
#   make uv-check
#   make venv
#   make install-dev
#   make install-docs
#   make dev
#   make docs
#   make run EXP=e001_taylor_error_landscapes ARGS="--out out/e001 --seed 1"
#   make clean
#   make clean-venv

REPO_NAME := py-mathx-lab
MODULE ?= mathxlab

# Experiment runner variables
EXP ?=
ARGS ?=

# Detect OS
IS_WINDOWS := 0
ifeq ($(OS),Windows_NT)
IS_WINDOWS := 1
SHELL := cmd.exe
.SHELLFLAGS := /C
endif

.PHONY: \
	clean \
	clean-venv \
	dev \
	format \
	help \
	install \
	install-dev \
	install-docs \
	lint \
	mypy \
	pytest \
	docs \
	docs-clean \
	python-check \
	python-info \
	run \
	uv-check \
	venv

.DEFAULT_GOAL := help

clean:
ifeq ($(IS_WINDOWS),1)
	@echo Removing caches and build artifacts...
	@if exist ".mypy_cache" rmdir /s /q ".mypy_cache"
	@if exist ".pytest_cache" rmdir /s /q ".pytest_cache"
	@if exist ".ruff_cache" rmdir /s /q ".ruff_cache"
	@if exist "build" rmdir /s /q "build"
	@if exist "dist" rmdir /s /q "dist"
	@for /d %%D in (*.egg-info) do @rmdir /s /q "%%D"
	@echo Done.
else
	@echo "Removing caches and build artifacts..."
	@rm -rf .mypy_cache .pytest_cache .ruff_cache build dist *.egg-info
	@find . -maxdepth 1 -name "*.egg-info" -exec rm -rf {} +
	@echo "Done."
endif

clean-venv:
ifeq ($(IS_WINDOWS),1)
	@if exist ".venv" rmdir /s /q ".venv"
	@echo Removed .venv (if it existed).
else
	@rm -rf .venv
	@echo "Removed .venv (if it existed)."
endif

dev: install-all format lint type test docs

docs: install-docs
	@echo Building docs ...
	@uv run sphinx-build -b html docs docs/_build/html

docs-clean:
ifeq ($(IS_WINDOWS),1)
	@if exist "docs\_build" rmdir /s /q "docs\_build"
else
	@rm -rf docs/_build
endif

format: python-check
ifdef CI
	@uv run ruff format --check .
else
	@uv run ruff format .
endif

lint: python-check
	@uv run ruff check .

mypy: python-check
	@uv run mypy

pytest: python-check
	@uv run pytest -q

run: python-check
ifeq ($(IS_WINDOWS),1)
	@if "$(EXP)"=="" (echo Error: EXP is required. & echo Example: make run EXP=e001_taylor_error_landscapes ARGS="--out out/e001 --seed 1" & exit /b 1)
else
	@test -n "$(EXP)" || (echo "Error: EXP is required."; echo 'Example: make run EXP=e001_taylor_error_landscapes ARGS="--out out/e001 --seed 1"'; exit 1)
endif
	@uv run python -m experiments.$(EXP) $(ARGS)

install: venv
	@uv pip install -e .

install-all: venv
	@uv pip install -e ".[dev,docs]"

install-dev: venv
	@uv pip install -e ".[dev]"

install-docs: venv
	@uv pip install -e ".[docs]"

python-info: uv-check
	@uv run python -c "import sys, platform; print('Python:', platform.python_version()); print('Executable:', sys.executable); print('Prefix:', sys.prefix)"

python-check: uv-check
	@uv run python -c "import sys; assert sys.version_info[:2]==(3,13), f'Required Python 3.13, got {sys.version_info[0]}.{sys.version_info[1]}'"

uv-check:
ifeq ($(IS_WINDOWS),1)
	@where uv >NUL 2>&1 || (echo Error: uv is required but not on PATH. & exit /b 1)
else
	@command -v uv >/dev/null 2>&1 || (echo "Error: uv is required but not on PATH."; exit 1)
endif
	@uv --version

venv: python-check
ifeq ($(IS_WINDOWS),1)
	@if not exist ".venv" uv venv
else
	@test -d ".venv" || uv venv
endif

help:
	@$(info ====================================================================)
	@$(info $(REPO_NAME) - task runner (uv-only))
	@$(info --------------------------------------------------------------------)
	@$(info clean          Remove caches/build artifacts (keeps .venv).)
	@$(info clean-venv     Remove the .venv directory.)
	@$(info dev            format + lint + mypy + pytest + docs.)
	@$(info format         ruff format (CI uses --check).)
	@$(info lint           ruff check .)
	@$(info mypy           mypy (whole repo; configured in pyproject.toml).)
	@$(info pytest         pytest -q)
	@$(info docs           Build Sphinx HTML docs to docs/_build/html.)
	@$(info docs-clean     Remove docs/_build.)
	@$(info install        uv pip install -e .)
	@$(info install-dev    uv pip install -e ".[dev]")
	@$(info install-docs   uv pip install -e ".[docs]")
	@$(info python-check   Enforce Python 3.13 via uv.)
	@$(info run            Run experiment: make run EXP=e001_... ARGS="--out out/e001 --seed 1")
	@$(info uv-check       Verify uv is on PATH.)
	@$(info venv           Create/update .venv using uv.)
	@$(info ====================================================================)
