# Minimal Makefile (Windows + Linux/macOS), same functionality

.DEFAULT_GOAL := help

.PHONY: clean \
        clean-venv \
        docs \
        docs-clean \
        final \
        format \
        help \
        install \
        install-all \
        install-dev \
        install-docs \
        lint \
        mypy \
        pytest \
        python-check \
        run \
        uv-check \
        venv

PYTHON_MIN := 3.13
CLEAN_DIRS := .mypy_cache .pytest_cache .ruff_cache build dist docs/_build
VENV_DIR   := .venv

UV     := uv
UV_RUN := $(UV) run

# --- OS detection ------------------------------------------------------------
ifeq ($(OS),Windows_NT)
  IS_WINDOWS := 1
  SHELL := cmd.exe
  .SHELLFLAGS := /C
else
  IS_WINDOWS := 0
endif

# --- small helpers -----------------------------------------------------------
ifeq ($(IS_WINDOWS),1)

define assert_uv
@where uv >NUL 2>&1 || (echo ERROR: uv is not installed. & exit /b 1)
endef

define rmdir_if_exists
@if exist "$(1)" rmdir /s /q "$(1)"
endef

define rm_venv
@if exist "$(VENV_DIR)" rmdir /s /q "$(VENV_DIR)"
endef

define clean_artifacts
@for %%D in ($(CLEAN_DIRS)) do @if exist "%%D" rmdir /s /q "%%D"
@for /d %%D in (*.egg-info) do @rmdir /s /q "%%D"
endef

else  # POSIX

define assert_uv
@command -v uv >/dev/null 2>&1 || (echo "ERROR: uv is not installed." && exit 1)
endef

define rmdir_if_exists
@rm -rf "$(1)"
endef

define rm_venv
@rm -rf "$(VENV_DIR)"
endef

define clean_artifacts
@rm -rf $(CLEAN_DIRS) *.egg-info
endef

endif

# --- targets -----------------------------------------------------------------
clean:
	$(call clean_artifacts)

clean-venv:
	$(call rm_venv)

docs: install-docs
	$(UV_RUN) python -m sphinx -b html docs docs/_build/html

docs-clean:
	$(call rmdir_if_exists,docs/_build)

final: format lint mypy pytest docs

format: install-dev
ifdef CI
	$(UV_RUN) ruff format --check .
else
	$(UV_RUN) ruff format .
endif

help:
	@echo Targets:
	@echo   make clean         - remove caches/build artifacts
	@echo   make clean-venv    - remove .venv
	@echo   make docs          - build Sphinx HTML docs
	@echo   make docs-clean    - remove docs/_build
	@echo   make final         - run format, lint, mypy, pytest, docs
	@echo   make format        - format with ruff
	@echo   make install       - install package editable
	@echo   make install-all   - install dev + docs tools
	@echo   make install-dev   - install dev tools
	@echo   make install-docs  - install docs tools
	@echo   make lint          - ruff lint
	@echo   make mypy          - check typing
	@echo   make pytest        - run tests
	@echo   make run EXP=e001  - run an experiment by id
	@echo   make venv          - create/update virtual environment

install: uv-check python-check venv
	$(UV) pip install -e .

# "all" means dev+docs (matches your help text)
install-all: uv-check python-check venv
	$(UV) sync --extra dev --extra docs

install-dev: uv-check python-check venv
	$(UV) sync --extra dev

install-docs: uv-check python-check venv
	$(UV) sync --extra docs

lint: install-dev
	$(UV_RUN) ruff check .

mypy: install-dev
	$(UV_RUN) mypy .

pytest: install-dev
	$(UV_RUN) pytest -q

python-check:
	@python -c "import sys; s='$(PYTHON_MIN)'; parts=s.split('.'); major=int(parts[0]); minor=int(parts[1]); v=sys.version_info; assert (v.major, v.minor) >= (major, minor), f'Need Python >= {major}.{minor}, got {v.major}.{v.minor}'"

run: python-check uv-check
ifeq ($(IS_WINDOWS),1)
	@if "$(EXP)"=="" (echo ERROR: Please provide EXP, e.g. make run EXP=e001 & exit /b 1)
else
	@test -n "$(EXP)" || (echo "ERROR: Please provide EXP, e.g. make run EXP=e001" && exit 1)
endif
	$(UV_RUN) python -m experiments.$(EXP)

uv-check:
	$(call assert_uv)

venv: python-check uv-check
	$(UV) venv --python $(PYTHON_MIN) --clear
