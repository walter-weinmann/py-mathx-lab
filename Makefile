# Minimal Makefile (Windows + Linux/macOS), same functionality

.DEFAULT_GOAL := help
.PHONY: _run_core \
        clean \
        clean-venv \
        docs \
        docs-clean \
        docs-deps \
        docs-html \
        docs-pdf \
        final \
        final-slow \
        fmt \
        format \
        format-check \
        help \
        install \
        install-all \
        install-dev \
        install-docs \
        lint \
        mypy \
        out \
        perf \
        perf-compare \
        perf-release \
        pytest \
        pytest-slow \
        python-check \
        run \
        status \
        tags-check \
        uv-check \
        venv \
        venv-recreate

PYTHON_MIN := 3.14
CLEAN_DIRS := .mypy_cache .pytest_cache .ruff_cache build dist docs/_build temp_pytest temp_pytest_cache
VENV_DIR   := .venv

DOCS_DIR        := docs
DOCS_BUILD_DIR  := $(DOCS_DIR)/_build
DOCS_HTML_DIR   := $(DOCS_BUILD_DIR)/html

UV         ?= uv
UV_RUN      = $(UV) run
UV_RUN_DEV  = $(UV) run --extra dev
UV_RUN_DOCS = $(UV) run --extra docs

PYTEST   = $(UV_RUN_DEV) pytest -o "cache_dir=temp_pytest_cache" --basetemp=temp_pytest
PYTEST_XDIST_FAST ?=
PYTEST_XDIST_SLOW ?= -n auto --dist=load
# Coverage focuses on library code. Experiment scripts are excluded via
# [tool.coverage.run].omit in pyproject.toml.
COV_PKGS = --cov=mathxlab.exp --cov=mathxlab.nt --cov=mathxlab.num --cov=mathxlab.plots --cov=mathxlab.viz
COV_OPTS = $(COV_PKGS) --cov-report=term-missing --cov-fail-under=80

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
_run_core:
ifeq ($(IS_WINDOWS),1)
	@if "$(EXP)"=="" (echo ERROR: Please provide EXP, e.g. make run EXP=e001 & exit /b 1)
else
	@test -n "$(EXP)" || (echo "ERROR: Please provide EXP, e.g. make run EXP=e001" && exit 1)
endif
ifeq ($(IS_WINDOWS),1)
	@powershell -NoProfile -ExecutionPolicy Bypass -Command "$$ErrorActionPreference = 'Stop'; $$exp='$(EXP)'; $$out=Join-Path 'out' $$exp; $$logDir=Join-Path $$out 'logs'; New-Item -ItemType Directory -Force -Path $$logDir | Out-Null; $$log=Join-Path $$logDir ('run_' + $$exp + '.log'); Write-Host ('Logging to: ' + $$log); & $(UV_RUN_DEV) python -m mathxlab.experiments.$$exp --out $$out -v $(ARGS); exit $$LASTEXITCODE"
else
	@bash -lc 'set -euo pipefail; mkdir -p "out/$(EXP)/logs"; log="out/$(EXP)/logs/run_$(EXP).log"; echo "Logging to: $${log}"; $(UV_RUN_DEV) python -m mathxlab.experiments.$(EXP) --out out/$(EXP) -v $(ARGS)'
endif

clean:
	$(call clean_artifacts)

clean-venv:
	$(call rm_venv)

docs: status tags-check docs-html docs-pdf

docs-clean:
	$(call rmdir_if_exists,$(DOCS_BUILD_DIR))

docs-deps:
ifeq ($(IS_WINDOWS),1)
	@if exist "$(VENV_DIR)\lib64" ( \
		echo Detected stale lib64 symlink, cleaning to avoid Access Denied... & \
		rmdir /s /q "$(VENV_DIR)\lib64" \
	)
endif
	@echo Syncing docs dependencies...
	@uv sync --all-extras

docs-html: docs-deps
	@echo Building HTML docs...
	@$(UV_RUN_DOCS) python -m sphinx -q -W -b html $(DOCS_DIR) $(DOCS_HTML_DIR)

docs-pdf: docs-deps
	@echo "Building PDF docs (optional; requires LaTeX toolchain + latexmk)..."
	@$(UV_RUN_DOCS) python -m mathxlab.tools.docs_pdf --quiet

final: format lint-fix mypy pytest docs

final-slow: format lint mypy pytest-slow docs

fmt: install-dev
	$(UV_RUN_DEV) ruff check --fix .
	$(UV_RUN_DEV) ruff format .

# Check-only formatting (used by CI and by final)
format: install-dev
	$(UV_RUN_DEV) ruff format mathxlab tests experiments scripts pyproject.toml

format-check:
	$(UV_RUN_DEV) ruff format --check mathxlab tests experiments scripts pyproject.toml

help:
	@echo Targets:
	@echo   make clean         - remove caches/build artifacts
	@echo   make clean-venv    - remove .venv
	@echo   make docs          - build Sphinx HTML docs
	@echo   make docs-clean    - remove docs/_build
	@echo   make final         - run format-check + lint + mypy + pytest      + docs
	@echo   make final-slow    - run format-check + lint + mypy + pytest-slow + docs
	@echo   make fmt           - apply ruff fixes + format (local developer helper)
	@echo   make format        - check formatting (ruff format --check)
	@echo   make install       - install package editable
	@echo   make install-all   - sync default        deps
	@echo   make install-dev   - sync default + dev  deps
	@echo   make install-docs  - sync default + docs deps
	@echo   make lint          - ruff lint (check-only)
	@echo   make lint-fix      - ruff lint
	@echo   make mypy          - check typing
	@echo   make out           - run all experiments (sequential)
	@echo   make perf          - run performance suite for all experiments (dev snapshot)
	@echo   make perf-compare  - compare two snapshots (make perf-compare A=vX B=vY)
	@echo   make perf-release  - run performance suite and store results for current MVERSION
	@echo   make pytest        - run fast tests with coverage
	@echo   make pytest-slow   - run slow tests with coverage
	@echo   make run EXP=e001  - run an experiment by id
	@echo   make status        - update docs/experiment_status.md (append new experiments)
	@echo   make tags-check    - validate docs tags against docs/tags.md
	@echo   make venv          - create/update virtual environment

install: venv
	$(UV) pip install -e .

install-all: uv-check python-check venv
	$(UV) sync

install-dev: uv-check python-check venv
	$(UV) sync --extra dev

install-docs: uv-check python-check venv
	$(UV) sync --extra docs

# Check-only lint (used by CI and by final)
lint: install-dev
	$(UV_RUN_DEV) ruff check .

# Check-only lint (used by final)
lint-fix: install-dev
	$(UV_RUN_DEV) ruff check --fix .

mypy: install-dev
	$(UV_RUN_DEV) mypy mathxlab tests experiments

out: install-dev
ifeq ($(IS_WINDOWS),1)
	@powershell -NoProfile -ExecutionPolicy Bypass -Command "$$ErrorActionPreference = 'Stop'; $$files = Get-ChildItem -Path 'mathxlab/experiments' -Filter 'e???.py' | Sort-Object Name; foreach ($$f in $$files) { $$exp = $$f.BaseName; if ($$exp -match '^e\d{3}$$') { Write-Host ('== RUN ' + $$exp + ' =='); & $(MAKE) _run_core EXP=$$exp ARGS=\"$(ARGS)\"; if ($$LASTEXITCODE -ne 0) { exit $$LASTEXITCODE } } }"
else
	@bash -lc 'set -euo pipefail; for f in mathxlab/experiments/e[0-9][0-9][0-9].py; do exp="$$(basename "$$f" .py)"; echo "== RUN $$exp =="; $(MAKE) _run_core EXP="$$exp" ARGS="$(ARGS)"; done'
endif

perf: install-dev
	$(UV_RUN_DEV) python mathxlab/tools/run_perf.py --mode dev --overwrite

perf-compare: install-dev
ifeq ($(IS_WINDOWS),1)
	@if "$(A)"=="" (echo ERROR: Provide A, e.g. make perf-compare A=v0.1.0 B=v0.2.0 & exit /b 1)
	@if "$(B)"=="" (echo ERROR: Provide B, e.g. make perf-compare A=v0.1.0 B=v0.2.0 & exit /b 1)
else
	@test -n "$(A)" || (echo "ERROR: Provide A, e.g. make perf-compare A=v0.1.0 B=v0.2.0" && exit 1)
	@test -n "$(B)" || (echo "ERROR: Provide B, e.g. make perf-compare A=v0.1.0 B=v0.2.0" && exit 1)
endif
	$(UV_RUN_DEV) python mathxlab/tools/compare_perf.py --a $(A) --b $(B)

perf-release: install-dev
	$(UV_RUN_DEV) python mathxlab/tools/run_perf.py --mode release --overwrite

pytest: install-dev
	$(PYTEST) -q $(PYTEST_XDIST_FAST) -m "not slow" \
		$(COV_PKGS) --cov-report=term-missing --cov-fail-under=80

pytest-slow: install-dev
ifeq ($(IS_WINDOWS),1)
	@if exist .coverage del /f .coverage
else
	@rm -f .coverage
endif
ifeq ($(IS_WINDOWS),1)
	$(PYTEST) -q -m "not slow" \
		$(COV_PKGS) --cov-report=term || exit /b 0
else
	$(PYTEST) -q -m "not slow" \
		$(COV_PKGS) --cov-report=term || true
endif
	$(PYTEST) -q $(PYTEST_XDIST_SLOW) -m "slow" \
		$(COV_PKGS) --cov-append --cov-report=term-missing --cov-fail-under=80 \
		--progress --progress-every=1

pytest-xdist: install-dev
	$(PYTEST) -q -n auto --dist=load -m "not slow" \
		$(COV_PKGS) --cov-report=term-missing --cov-fail-under=80

python-check:
	@python -c "import sys; req='$(PYTHON_MIN)'.split('.'); req=(int(req[0]), int(req[1])); v=sys.version_info; assert v[:2] >= req, f'Need Python >= {req[0]}.{req[1]}, got {v.major}.{v.minor}'"

run: install-dev _run_core

status: install-dev
	$(UV_RUN_DEV) python mathxlab/tools/generate_experiment_status.py

tags-check: install-dev
	$(UV_RUN_DEV) python -m mathxlab.tools.validate_doc_tags

uv-check:
	$(call assert_uv)

venv: python-check uv-check
ifeq ($(IS_WINDOWS),1)
	@if exist "$(VENV_DIR)\Scripts\python.exe" (echo Using existing venv at $(VENV_DIR)) else ($(UV) venv --python $(PYTHON_MIN))
else
	@test -d "$(VENV_DIR)" || $(UV) venv --python $(PYTHON_MIN)
endif

venv-recreate: clean-venv
	$(UV) venv --python $(PYTHON_MIN) --clear
