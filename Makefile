# Makefile — py-mathx-lab (Windows cmd.exe + GNU Make 3.81) using uv (uv-only)
#
# Usage examples:
#   make help
#   make uv-check
#   make venv
#   make install-dev
#   make dev
#   make run EXP=e001_taylor_error_landscapes ARGS="--out out/e001 --seed 1"
#   make clean
#   make clean-venv

REPO_NAME := py-mathx-lab
MODULE ?= mathxlab

# Experiment runner variables
EXP ?=
ARGS ?=

.PHONY: \
	clean \
	clean-venv \
	dev \
	format \
	help \
	install \
	install-dev \
	lint \
	mypy \
	pytest \
	python-check \
	python-info \
	run \
	uv-check \
	venv


.DEFAULT_GOAL := help

clean:
	@echo Removing caches and build artifacts...
	@if exist ".mypy_cache" rmdir /s /q ".mypy_cache"
	@if exist ".pytest_cache" rmdir /s /q ".pytest_cache"
	@if exist ".ruff_cache" rmdir /s /q ".ruff_cache"
	@if exist "build" rmdir /s /q "build"
	@if exist "dist" rmdir /s /q "dist"
	@for /d %%D in (*.egg-info) do @rmdir /s /q "%%D"
	@echo Done.

clean-venv:
	@if exist ".venv" rmdir /s /q ".venv"
	@echo Removed .venv (if it existed).

dev: format lint mypy pytest

format: python-check
	@uv run ruff format .

help:
	@$(info ====================================================================)
	@$(info $(REPO_NAME) - task runner (uv-only))
	@$(info --------------------------------------------------------------------)
	@$(info clean          Remove caches/build artifacts (keeps .venv).)
	@$(info clean-venv     Remove the .venv directory.)
	@$(info dev            format + lint + mypy + pytest.)
	@$(info format         uv run ruff format .)
	@$(info help           Show this help.)
	@$(info install        uv pip install -e .)
	@$(info install-dev    uv pip install -e ".[dev]")
	@$(info lint           uv run ruff check .)
	@$(info mypy           uv run mypy (whole repo; configured in pyproject.toml))
	@$(info pytest         uv run pytest -q)
	@$(info python-check   Enforce Python 3.13 via uv.)
	@$(info run            Run experiment: make run EXP=e001_... ARGS="--out out/e001 --seed 1")
	@$(info uv-check       Verify uv is on PATH.)
	@$(info venv           Create/update .venv using uv.)
	@$(info --------------------------------------------------------------------)
	@$(info Variables you can customize:)
	@$(info   Python is enforced to 3.13 via python-check.)
	@$(info   MODULE=<pkg>   (default: $(MODULE)))
	@$(info   EXP=<module>   experiment module under experiments/)
	@$(info   ARGS="..."     extra CLI args passed to the experiment)
	@$(info ====================================================================)

install: python-check
	@uv pip install -e .

install-dev: python-check
	@uv pip install -e ".[dev]"

lint: python-check
	@uv run ruff check .

mypy: python-check
	@uv run mypy

pytest: python-check
	@uv run pytest -q

run: python-check
	@if "$(EXP)"=="" (echo Error: EXP is required. & echo Example: make run EXP=e001_taylor_error_landscapes ARGS="--out out/e001 --seed 1" & exit /b 1)
	@uv run python -m experiments.$(EXP) $(ARGS)


python-info: uv-check
	@uv run python -c "import sys, platform; print('Python:', platform.python_version()); print('Executable:', sys.executable); print('Prefix:', sys.prefix)"

python-check: uv-check
	@uv run python -c "import sys; assert sys.version_info[:2]==(3,13), f'Expected Python 3.13, got {sys.version_info[0]}.{sys.version_info[1]}'"

uv-check:
	@where uv >NUL 2>&1 || (echo Error: uv is required but not on PATH. & exit /b 1)
	@uv --version

venv: python-check
	@if not exist ".venv" uv venv
