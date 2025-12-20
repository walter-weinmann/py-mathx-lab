# Developer Guide: Using the Makefile (uv-only) in `py-mathx-lab`

This repository uses a **uv-based** workflow to manage:

- virtual environment creation (`.venv/`)
- dependency installation (editable + extras)
- formatting, linting, typing, tests
- Sphinx documentation build
- running experiments

Supported platforms:

- **Windows** (GNU Make, `cmd.exe` recipes for Windows parts)
- **Linux/macOS** (POSIX shell recipes)

No shell activation is required: everything is executed via `uv run ...`.

---

## Prerequisites

### Required tools

You need:

1. **GNU Make**
   - Windows: install GNU Make (e.g. via Chocolatey or Git for Windows tooling)
   - Linux/macOS: typically already available (or install via package manager)
2. **uv** on your `PATH`
3. **Python 3.13** installed on the machine (uv will select an interpreter)

### Verify your setup

Run from the repo root:

```bat
make uv-check
make python-check
make python-info
````

Expected output includes your `uv` version, and `python-check` must confirm **Python 3.13**.

---

## Conceptual model

### What uv does here

* `uv venv` creates the virtual environment in `.venv/`
* `uv pip install ...` installs packages into `.venv/`
* `uv run <command>` runs a command inside `.venv/` **without activating it**

So you do **not** need:

* `.\.venv\Scripts\activate`
* `source .venv/bin/activate`

---

## Quick start (first-time setup)

From the repository root:

```bat
make uv-check
make venv
make install-dev
make install-docs
```

Then run the full pipeline:

```bat
make dev
```

Notes:

* `install-dev` installs the project in editable mode plus dev tools (ruff/mypy/pytest).
* `install-docs` installs the Sphinx toolchain (so `sphinx-build` exists).
* `dev` runs **format + lint + mypy + pytest + docs** (see below).

---

## The development loop

Typical edit → check → test flow:

```bat
make format
make lint
make mypy
make pytest
```

Or run everything (including docs build) in one go:

```bat
make dev
```

### CI behavior for formatting

In CI (GitHub Actions sets `CI=1` automatically):

* `make format` runs `ruff format --check .`
* locally, `make format` runs `ruff format .` (in-place formatting)

This means CI fails if formatting is not already correct.

---

## Documentation (Sphinx)

### Install docs dependencies

You must install the docs toolchain once:

```bat
make install-docs
```

### Build docs

```bat
make docs
```

Output directory:

* `docs/_build/html`

### Clean docs build output

```bat
make docs-clean
```

---

## Running experiments

Experiments are run via module execution:

```bat
make run EXP=<experiment_module> ARGS="<arguments>"
```

Example:

```bat
make run EXP=e001_taylor_error_landscapes ARGS="--out out/e001 --seed 1"
```

This runs:

```text
uv run python -m experiments.e001_taylor_error_landscapes --out out/e001 --seed 1
```

Rules:

* `EXP` is required and must be the module name under `experiments/` (without `.py`)
* `ARGS` is optional and passed verbatim

If `EXP` is missing, the Makefile fails early with an example invocation.

---

## Cleaning build artifacts and caches

### `make clean`

Removes typical caches and build outputs (keeps `.venv`):

* `.mypy_cache`
* `.pytest_cache`
* `.ruff_cache`
* `build`
* `dist`
* `*.egg-info` directories

```bat
make clean
```

### `make clean-venv`

Removes `.venv`:

```bat
make clean-venv
```

Recommended “full reset” sequence:

```bat
make clean
make clean-venv
make venv
make install-dev
make install-docs
```

---

## Typical workflows

### 1) Day-to-day development

```bat
make dev
```

### 2) Before creating a PR / merging change

```bat
make clean
make dev
```

### 3) Fresh checkout setup

```bat
make uv-check
make venv
make install-dev
make install-docs
make dev
```

### 4) Iterate on one experiment

```bat
make run EXP=e001_taylor_error_landscapes ARGS="--out out/e001 --seed 1"
```

Then after changes:

```bat
make format
make run EXP=e001_taylor_error_landscapes ARGS="--out out/e001 --seed 2"
```

---

## Troubleshooting

### `error: Failed to spawn: sphinx-build` / `program not found`

Cause: Sphinx is not installed into the environment used by `uv run`.

Fix:

```bat
make install-docs
make docs
```

### `Error: uv is required but not on PATH.`

Windows:

```bat
where uv
uv --version
```

Linux/macOS:

```sh
command -v uv
uv --version
```

Open a new terminal after installing uv (PATH changes may require it).

### `make python-check` fails (wrong Python version)

The Makefile enforces **Python 3.13**. If it fails:

1. Install Python 3.13.
2. Recreate the environment:

```bat
make clean-venv
make venv
make install-dev
make install-docs
```

### `make` not found on Windows

Install GNU Make, e.g. with Chocolatey:

```bat
choco install make -y
```

Then open a new terminal and retry.

---

## Reference: available targets

Run:

```bat
make help
```

Targets:

* `clean` – remove caches and build artifacts (keep `.venv`)
* `clean-venv` – remove `.venv`
* `dev` – format + lint + mypy + pytest + docs
* `format` – ruff format (CI uses `--check`)
* `lint` – ruff check
* `mypy` – mypy (scope configured in `pyproject.toml`)
* `pytest` – pytest -q
* `docs` – build Sphinx HTML docs to `docs/_build/html`
* `docs-clean` – remove `docs/_build`
* `install` – `uv pip install -e .`
* `install-dev` – `uv pip install -e ".[dev]"`
* `install-docs` – `uv pip install -e ".[docs]"`
* `python-check` – enforce Python 3.13 via uv
* `python-info` – print interpreter details uv is using
* `run` – run an experiment module (`EXP=...`, optional `ARGS=...`)
* `uv-check` – verify uv availability
* `venv` – create/update `.venv` using uv

---

## Contributor recommendations

* Always use `make` targets instead of calling tools directly.
* Prefer `make dev` before committing.
* Use `make clean` periodically to keep the working tree tidy.
* Use `make clean-venv` only when you need a fully fresh environment.

```

If you also want, I can provide a matching **`docs/` Sphinx scaffold** (`docs/conf.py`, `docs/index.md`, theme config) so `make docs` works immediately after `make install-docs`.
```
