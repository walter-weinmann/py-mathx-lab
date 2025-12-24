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
        venv \
        venv-recreate

PYTHON_MIN := 3.14
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
ifdef CI
	$(UV_RUN_DEV) ruff check .
else
	$(UV_RUN_DEV) ruff check --fix .
endif

mypy: install-dev
	$(UV_RUN_DEV) mypy .

pytest: install-dev
	$(UV_RUN_DEV) pytest -q

python-check:
	@python -c "import sys; req='$(PYTHON_MIN)'.split('.'); req=(int(req[0]), int(req[1])); v=sys.version_info; assert v[:2] >= req, f'Need Python >= {req[0]}.{req[1]}, got {v.major}.{v.minor}'"

run: install-dev
ifeq ($(IS_WINDOWS),1)
	@if "$(EXP)"=="" (echo ERROR: Please provide EXP, e.g. make run EXP=e001 & exit /b 1)
else
	@test -n "$(EXP)" || (echo "ERROR: Please provide EXP, e.g. make run EXP=e001" && exit 1)
endif
ifeq ($(IS_WINDOWS),1)
	@powershell -NoProfile -ExecutionPolicy Bypass -Command "$$exp='$(EXP)'; $$out='out/$(EXP)'; $$logDir=Join-Path $$out 'logs'; New-Item -ItemType Directory -Force -Path $$logDir | Out-Null; $$ts=Get-Date -Format 'yyyyMMdd_HHmmss'; $$log=Join-Path $$logDir ('run_'+$$exp+'_'+$$ts+'.log'); $$cmd='$(UV_RUN_DEV) python -m mathxlab.experiments.'+$$exp+' --out '+$$out+' -v $(ARGS)'; 'COMMAND: ' + $$cmd | Out-File -FilePath $$log -Encoding utf8; 'START: ' + (Get-Date -Format o) | Out-File -FilePath $$log -Append -Encoding utf8; Write-Host ('Logging to: ' + $$log); & $(UV) run --extra dev python -m mathxlab.experiments.$(EXP) --out out/$(EXP) -v $(ARGS) 2>&1 | Tee-Object -FilePath $$log -Append; exit $$LASTEXITCODE"
else
	@bash -lc 'set -euo pipefail; \
		mkdir -p "out/$(EXP)/logs"; \
		ts="$$(date +%Y%m%d_%H%M%S)"; \
		log="out/$(EXP)/logs/run_$(EXP)_$${ts}.log"; \
		echo "COMMAND: $(UV_RUN_DEV) python -m mathxlab.experiments.$(EXP) --out out/$(EXP) -v $(ARGS)" | tee "$${log}"; \
		echo "START: $$(date -Iseconds)" | tee -a "$${log}"; \
		echo "Logging to: $${log}"; \
		$(UV_RUN_DEV) python -m mathxlab.experiments.$(EXP) --out out/$(EXP) -v $(ARGS) 2>&1 | tee -a "$${log}"'
endif

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
