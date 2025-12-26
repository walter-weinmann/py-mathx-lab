# Makefile

This repository ships a small, cross-platform `Makefile` that standardizes the common developer and CI workflows:

- create/manage a local virtual environment via **uv**
- install dependencies via **uv sync**
- format/lint/typecheck/test
- build Sphinx docs (HTML + optional PDF)

The Makefile is designed to work on **Windows** (via `cmd.exe` + PowerShell for logging) and **POSIX** shells (Linux/macOS).

---

## Prerequisites

- **Python ≥ 3.14** (see `PYTHON_MIN` in the Makefile)
- **uv** installed and on `PATH`
- **GNU make** available (`make`)

Notes:

- The virtual environment is created in `.venv/`.
- On Windows with multi-drive setups, the Makefile exports `UV_LINK_MODE=copy` to avoid uv hardlink warnings.

---

## Quick start

Create the venv and install dev dependencies:

```bash
make install-dev
````

Run all CI-style checks locally:

```bash
make final
```

Build docs:

```bash
make docs
```

---

## Common workflows

### 1) Create/update the virtual environment

```bash
make venv
```

Recreate it from scratch:

```bash
make venv-recreate
```

Remove it:

```bash
make clean-venv
```

### 2) Install dependencies

Editable install of the package:

```bash
make install
```

Sync default dependencies:

```bash
make install-all
```

Sync default + dev extras:

```bash
make install-dev
```

Sync default + docs extras:

```bash
make install-docs
```

### 3) Quality gates

Apply autofixes and format (local dev helper):

```bash
make fmt
```

Check formatting only (CI-style):

```bash
make format
```

Lint only (CI-style):

```bash
make lint
```

Typecheck:

```bash
make mypy
```

Run tests:

```bash
make pytest
```

Run *everything* (what CI should run):

```bash
make final
```

### 4) Run an experiment

Run experiment `e001` and write output into `out/e001/`:

```bash
make run EXP=e001
```

Pass extra CLI args to the experiment via `ARGS`:

```bash
make run EXP=e001 ARGS="--seed 123 --max-n 20000"
```

Logging:

* logs are written to `out/<EXP>/logs/run_<EXP>_<timestamp>.log`
* Windows uses PowerShell `Tee-Object`, POSIX uses `tee`

### 5) Documentation

Build HTML + PDF:

```bash
make docs
```

Build only HTML:

```bash
make docs-html
```

Build only PDF:

```bash
make docs-pdf
```

Clean docs output:

```bash
make docs-clean
```

Outputs:

* HTML: `docs/_build/html/`
* LaTeX build dir: `docs/_build/latex/`
* PDF generation is handled by `mathxlab/tools/docs_pdf.py`

---

## Targets reference

| Target          | What it does                                   |
| --------------- | ---------------------------------------------- |
| `help`          | Print a short help text                        |
| `venv`          | Create or reuse `.venv` (checks Python and uv) |
| `venv-recreate` | Remove and recreate `.venv`                    |
| `clean-venv`    | Remove `.venv`                                 |
| `install`       | `uv pip install -e .`                          |
| `install-all`   | `uv sync` (default deps)                       |
| `install-dev`   | `uv sync --extra dev`                          |
| `install-docs`  | `uv sync --extra docs`                         |
| `fmt`           | Apply `ruff check --fix` + `ruff format`       |
| `format`        | Check formatting (`ruff format --check`)       |
| `lint`          | Check lint (`ruff check`)                      |
| `mypy`          | Run `mypy .`                                   |
| `pytest`        | Run tests (`pytest -q`)                        |
| `run`           | Run an experiment (`EXP=e001`) with logging    |
| `docs-deps`     | Ensure docs dependencies are installed         |
| `docs-html`     | Build Sphinx HTML docs                         |
| `docs-pdf`      | Build PDF via `mathxlab/tools/docs_pdf.py`     |
| `docs-clean`    | Remove `docs/_build/`                          |
| `docs`          | `docs-html` + `docs-pdf`                       |
| `clean`         | Remove caches/build artifacts                  |
| `final`         | `format` + `lint` + `mypy` + `pytest` + `docs` |

---

## Variables you’ll likely use

* `EXP` (required for `make run`)
  Example: `make run EXP=e003`

* `ARGS` (optional extra CLI args passed to the experiment)
  Example: `make run EXP=e003 ARGS="--out out/e003 --max-n 100000"`

---

## Implementation notes

### Why `final` is check-only

`final` is meant to mimic CI behavior: it must never silently modify code. That’s why:

* `format` uses `ruff format --check`
* `lint` uses `ruff check` (no `--fix`)

Use `fmt` locally to apply fixes.

### Docs runner extras

The Makefile defines:

* `UV_RUN_DEV  = uv run --extra dev`
* `UV_RUN_DOCS = uv run --extra docs`

`docs-deps` installs the `docs` extra via `uv sync --extra docs`.

If you ever notice docs builds pulling in/removing unexpected packages, the most stable pattern is:

* run Sphinx via `$(UV_RUN_DOCS)` (docs extra), not via the dev extra

(Your Makefile can enforce that by using `$(UV_RUN_DOCS)` in `docs-html` as well.)

---

## Troubleshooting

### “uv is not installed”

Run:

```bash
make uv-check
```

and install uv if needed.

### “Need Python >= …”

Update your Python installation or lower `PYTHON_MIN` in the Makefile (only if the project supports it).

### Docs look outdated

Clean and rebuild:

```bash
make docs-clean
make docs
```
