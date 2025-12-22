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

UV      ?= uv
UV_RUN   = $(UV) run
UV_RUN_DEV  = $(UV) run --extra dev
UV_RUN_DOCS = $(UV) run --extra docs

# Optional: silence uv "Failed to hardlink files" warning on multi-drive setups (common on Windows).
# You can also set this globally via environment instead of here.
export UV_LINK_MODE ?= copy

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
	$(UV_RUN_DOCS) python -m sphinx -b html docs docs/_build/html

docs-clean:
	$(call rmdir_if_exists,docs/_build)

final: format lint mypy pytest docs

format: install-dev
ifdef CI
	$(UV_RUN_DEV) ruff format --check .
else
	$(UV_RUN_DEV) ruff format .
endif

help:
	@echo Targets:
	@echo   make clean         - remove caches/build artifacts
	@echo   make clean-venv    - remove .venv
	@echo   make docs          - build Sphinx HTML docs
	@echo   make docs-clean    - remove docs/_build
	@echo   make final         - run format + lint + mypy + pytest + docs
	@echo   make format        - format with ruff
	@echo   make install       - install package editable
	@echo   make install-all   - sync default deps
	@echo   make install-dev   - sync default + dev deps
	@echo   make install-docs  - sync default + docs deps
	@echo   make lint          - ruff lint
	@echo   make mypy          - check typing
	@echo   make pytest        - run tests
	@echo   make run EXP=e001  - run an experiment by id
	@echo   make venv          - create/update virtual environment

install: venv
	$(UV) pip install -e .

install-all: uv-check python-check venv
	$(UV) sync

install-dev: uv-check python-check venv
	$(UV) sync --extra dev

install-docs: uv-check python-check venv
	$(UV) sync --extra docs

lint: install-dev
	$(UV_RUN_DEV) ruff check .

mypy: install-dev
	$(UV_RUN_DEV) mypy .

pytest: install-dev
	$(UV_RUN_DEV) pytest -q

python-check:
	@python -c "import sys; req='$(PYTHON_MIN)'.split('.'); req=(int(req[0]), int(req[1])); v=sys.version_info; assert v[:2] >= req, f'Need Python >= {req[0]}.{req[1]}, got {v.major}.{v.minor}'"

run:
ifeq ($(IS_WINDOWS),1)
	@if "$(EXP)"=="" (echo ERROR: Please provide EXP, e.g. make run EXP=e001 & exit /b 1)
else
	@test -n "$(EXP)" || (echo "ERROR: Please provide EXP, e.g. make run EXP=e001" && exit 1)
endif
	$(UV_RUN) python -m experiments.$(EXP) $(ARGS)

uv-check:
	$(call assert_uv)

venv: python-check uv-check
	$(UV) venv --python $(PYTHON_MIN)

venv-recreate: clean-venv
	$(UV) venv --python $(PYTHON_MIN) --clear
