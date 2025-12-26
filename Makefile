# Makefile for py-mathx-lab
#
# Option A:
# - One command locally and in CI: `make final`
# - Uses `uv` for env + tool execution
# - Builds HTML docs always; PDF docs are optional (skips if latexmk is missing)

.PHONY: help sync sync-docs format format-check lint lint-fix type test \
        docs-html docs-pdf docs clean final

# Use a POSIX shell. Avoid bash-only constructs in recipes.
SHELL := /bin/sh

UV ?= uv

EXTRA_DEV  := --extra dev
EXTRA_DOCS := --extra docs

UV_RUN_DEV  := $(UV) run $(EXTRA_DEV)
UV_RUN_DOCS := $(UV) run $(EXTRA_DOCS)

DOCS_DIR        := docs
DOCS_BUILD_DIR  := $(DOCS_DIR)/_build
DOCS_HTML_DIR   := $(DOCS_BUILD_DIR)/html

help:
	@echo "Targets:"
	@echo "  sync          Install/update dev dependencies into .venv via uv"
	@echo "  sync-docs     Install/update docs dependencies into .venv via uv"
	@echo "  format        Auto-format code with ruff"
	@echo "  format-check  Check formatting (no changes)"
	@echo "  lint          Lint with ruff"
	@echo "  lint-fix      Lint and auto-fix with ruff"
	@echo "  type          Type-check with mypy"
	@echo "  test          Run tests with pytest"
	@echo "  docs-html     Build Sphinx HTML docs"
	@echo "  docs-pdf      Build Sphinx PDF docs (optional; skips if latexmk missing)"
	@echo "  docs          Build docs (HTML + optional PDF)"
	@echo "  clean         Remove caches and build artifacts"
	@echo "  final         Run full local/CI chain (format-check, lint, type, test, docs)"

sync:
	$(UV) sync $(EXTRA_DEV)

sync-docs:
	$(UV) sync $(EXTRA_DOCS)

format:
	$(UV_RUN_DEV) ruff format .

format-check:
	$(UV_RUN_DEV) ruff format --check .

lint:
	$(UV_RUN_DEV) ruff check .

lint-fix:
	$(UV_RUN_DEV) ruff check --fix .

type:
	$(UV_RUN_DEV) mypy .

test:
	$(UV_RUN_DEV) pytest -q

docs-html: sync-docs
	@echo "Building HTML docs..."
	$(UV_RUN_DOCS) sphinx-build -b html $(DOCS_DIR) $(DOCS_HTML_DIR)

docs-pdf: sync-docs
	@echo "Building PDF docs (optional; requires LaTeX toolchain + latexmk)..."
	$(UV_RUN_DOCS) python -m mathxlab.tools.docs_pdf --quiet

docs: docs-html docs-pdf

clean:
	@echo "Cleaning build artifacts and caches..."
	@rm -rf .venv
	@rm -rf .mypy_cache .pytest_cache .ruff_cache
	@rm -rf build dist *.egg-info
	@rm -rf $(DOCS_BUILD_DIR)

final:
	@echo "uv sync (dev)..."
	$(UV) sync $(EXTRA_DEV)
	@echo "format-check..."
	$(MAKE) format-check
	@echo "lint..."
	$(MAKE) lint
	@echo "type..."
	$(MAKE) type
	@echo "test..."
	$(MAKE) test
	@echo "docs..."
	$(MAKE) docs
