# Developer Guide: Using the Makefile (uv-only) in `py-mathx-lab`

This repository uses a **uv-based** workflow on Windows (GNU Make 3.81 / mingw32) to manage the Python virtual environment, install dependencies, run quality checks, execute tests, and run experiments.

The Makefile is intentionally small and predictable:
- no conda support
- no shell activation required
- all developer actions go through `make <target>`

---

## Prerequisites

### Required tools

You need:

1. **GNU Make** (Windows build, e.g. `i386-pc-mingw32`)
2. **uv** on your `PATH`
3. A working **Python interpreter** installed on the machine (uv will choose one)

Verify:

```bat
make uv-check
make python-check
````

Expected output resembles:

```text
uv 0.9.18 (...)
```

If `uv` is missing, `make uv-check` will fail with a clear message.

---

## Project standards (Python 3.13 + strict typing)

This repo targets **Python 3.13**. The configuration is centralized in `pyproject.toml`:

- **Ruff**
  - `target-version = "py313"`
  - `line-length = 100`
  - `ruff format` is the canonical formatter
  - `ruff check` provides linting and import sorting rules
- **mypy**
  - `strict = true`
  - `python_version = "3.13"`
  - checks the entire repository (configured in pyproject.toml)

Practical implications:

- Run `make format` before committing (keeps diffs small and consistent).
- Expect mypy to be opinionated; add annotations early and prefer explicit types at module boundaries.
- If a third‑party dependency lacks type info, mypy is configured to silence missing-import noise while staying strict for your own code.

---

## Conceptual model

### What uv does here

* `uv venv` creates a virtual environment in `.venv/`
* `uv pip install ...` installs packages into that `.venv`
* `uv run <command>` runs a command using the `.venv` environment **without activating it**

This means:

* you do **not** need `.\.venv\Scripts\activate`
* all commands run reproducibly as long as you use `make`

---

## Quick start (first-time setup)

From the repository root:

```bat
make uv-check
make venv
make install-dev
```

What this does:

* `uv-check`: confirms `uv` is available
* `venv`: creates `.venv` (or updates it)
* `install-dev`: installs the project in editable mode plus developer dependencies

After that, you can run the full developer pipeline:

```bat
make dev
```

---

## The development loop

A typical edit → check → test cycle:

```bat
make format
make lint
make mypy
make pytest
```

Or, run them all at once:

```bat
make dev
```

### Target details

#### `make format`

Formats the codebase:

```bat
make format
```

Equivalent to:

```text
uv run ruff format .
```

Use this before committing.

#### `make lint`

Runs lint checks:

```bat
make lint
```

Equivalent to:

```text
uv run ruff check .
```

Use this to catch style and correctness issues.

#### `make mypy`

Runs static type checks (configured as **strict**) against the default module (configurable):

```bat
make mypy
```

Equivalent to:

```text
uv run mypy
```

You can override the module to type-check:

```bat
make mypy MODULE=some_package
```

#### `make pytest`

Runs tests:

```bat
make pytest
```

Equivalent to:

```text
uv run pytest -q
```

---

## Running experiments

Experiments are run via a Python module invocation:

```bat
make run EXP=<experiment_module> ARGS="<arguments>"
```

### Example

```bat
make run EXP=e001_taylor_error_landscapes ARGS="--out out/e001 --seed 1"
```

This translates to:

```text
uv run python -m experiments.e001_taylor_error_landscapes --out out/e001 --seed 1
```

### Notes / conventions

* `EXP` should be the module name under the `experiments/` package (without `.py`)
* `ARGS` is optional and passed verbatim to the module

If `EXP` is missing, the Makefile fails early with an example invocation.

---

## Cleaning build artifacts and caches

### `make clean`

Removes typical cache and build directories (but **keeps** `.venv`):

```bat
make clean
```

Removes (if present):

* `.mypy_cache`
* `.pytest_cache`
* `.ruff_cache`
* `build`
* `dist`
* `*.egg-info` directories

### `make clean-venv`

Removes the `.venv` directory:

```bat
make clean-venv
```

Use this if:

* your environment got corrupted
* you want to force a clean reinstalling
* you changed Python versions and wanted a fresh venv

Recommended rebuild sequence:

```bat
make clean
make clean-venv
make venv
make install-dev
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
make dev
```

### 4) Run one experiment repeatedly while iterating

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

### `Error: uv is required but not on PATH.`

* Confirm `uv` is installed and accessible:

  ```bat
  where uv
  uv --version
  ```
* Open a new terminal after installing (PATH updates often require it).

### `make venv` prompts to replace `.venv`

uv may prompt if `.venv` already exists, and it decides it needs replacement.

If you want fully non-interactive behavior, adjust the `venv` target in the Makefile:

* keep existing venv and avoid prompt:

  * only create if missing

### `mypy`, `ruff`, or `pytest` not found

This usually means dependencies were not installed.

Fix:

```bat
make install-dev
```

### Python version changes

The Makefile enforces Python **3.13**. If `make python-check` fails, ensure Python 3.13 is installed and that uv is selecting it.

If uv keeps selecting a different interpreter, remove and recreate the environment:

```bat
make clean-venv
make venv
make install-dev
```


If you installed a new Python version and want uv to rebuild the environment:

```bat
make clean-venv
make venv
make install-dev
```

---

## Reference: available targets

Run:

```bat
make help
```

Targets:

* `clean` – remove caches and build artifacts (keep `.venv`)
* `clean-venv` – remove `.venv`
* `dev` – format + lint + mypy + pytest
* `format` – code formatting
* `help` – show help
* `install` – install package editable
* `install-dev` – install editable + dev extras
* `lint` – lint checks
* `mypy` – type checking
* `pytest` – test runner
* `run` – run an experiment module
* `uv-check` – verify uv availability
* `venv` – create/update `.venv`

---

## Recommendations for contributors

* Always use `make` targets instead of calling tools directly.
* Prefer `make dev` before committing.
* Use `make clean` periodically to keep your working tree tidy.
* Use `make clean-venv` only when you need a fully fresh environment.

---


## Inspecting the interpreter uv is using

Run:

```bat
make python-info
```

This prints the Python version, the executable path (`sys.executable`), and the environment prefix.
