# Makefile

This project uses a Makefile as a thin, cross-platform command interface around
[`uv`](https://github.com/astral-sh/uv) and common developer workflows:

- formatting + linting (`ruff`)
- typing (`mypy`)
- tests (`pytest`)
- documentation build (Sphinx HTML and optional PDF via LaTeX)

The Makefile is designed to work on:

- **Windows** (PowerShell / cmd) for local development
- **Linux** (e.g., GitHub Actions runners) for CI

---

## Quick start

### Create the venv and install dev dependencies

```bash
make install-dev
````

### Run the full local “confidence chain” (checks and auto-fixes)

```bash
make final
```

### Build documentation (HTML + optional PDF)

```bash
make docs
```

### See all targets

```bash
make help
```

---

## Dependency groups (pyproject.toml)

Dependencies are organized via `pyproject.toml` extras:

* **default**: runtime dependencies needed to run the package
* **dev** (`--extra dev`): developer tooling (ruff, mypy, pytest, etc.)
* **docs** (`--extra docs`): documentation tooling (sphinx, furo, myst-parser, sphinx-design, bibtex, ...)

### What the Makefile does

* Dev / QA targets run via:

  ```bash
  uv run --extra dev ...
  ```

* Documentation targets run via:

  ```bash
  uv run --extra docs ...
  ```

* The docs dependency target uses:

  ```bash
  uv sync --all-extras
  ```

  (because `docs-html` also runs a small helper under the `dev` extra).

---

## Run logs and experiment runner

Experiments live under `mathxlab/experiments/` and can be run either directly
with Python or through Make targets.

### Run an experiment module directly

```bash
uv run --extra dev python -m mathxlab.experiments.e001
```

### Run an experiment via Make (with logs)

```bash
make run EXP=e001
```

Optional arguments:

```bash
make run EXP=e001 ARGS="--seed 123 --n 200000"
```

### Typical output locations (convention)

Depending on the experiment runner implementation, outputs are usually placed in:

* `out/e###/` (generated artifacts, figures, manifests, logs)
* `docs/reports/`, `docs/params/`, `docs/gallery/` (published snapshots)

If you add new experiments, keep the numbering stable (`e001`, `e002`, …) so the
gallery and documentation can remain consistent.

---

## Common workflows

| Task                                | Command                                     |
| ----------------------------------- | ------------------------------------------- |
| Install dev dependencies            | `make install-dev`                          |
| Complete quality check              | `make final`                                |
| Apply auto-fixes (lint + format)    | `make fmt`                                  |
| Build HTML docs                     | `make docs-html`                            |
| Build HTML + optional PDF docs      | `make docs`                                 |
| Run fast tests with coverage        | `make pytest`                               |
| Run fast + slow tests with coverage | `make pytest-slow`                          |
| Clean build artifacts               | `make clean`                                |
| Reset environment                   | `make clean clean-venv && make install-dev` |

---

## Target overview (what each target does)

> The exact set of targets is defined in the repository `Makefile`.
> This page documents the intent of the targets used in this repo.

Targets are listed in **alphabetical order**.

| Target          | Purpose                                                                             |
| --------------- |-------------------------------------------------------------------------------------|
| `clean`         | Remove caches/build artifacts (docs build, mypy/pytest/ruff caches, etc.).          |
| `clean-venv`    | Remove the virtual environment directory `.venv`.                                   |
| `docs`          | Build docs: `status` + `tags-check` + `docs-html` + `docs-pdf`.                     |
| `docs-clean`    | Remove `docs/_build`.                                                               |
| `docs-deps`     | Install/update dependencies needed for docs builds (`uv sync --all-extras`).        |
| `docs-html`     | Build Sphinx HTML into `docs/_build/html` (also syncs docs snapshots first).        |
| `docs-pdf`      | Build PDF docs (optional): requires external LaTeX toolchain + `latexmk`.           |
| `final`         | Full check chain: `format` + `lint-fix` + `mypy` + `pytest` + `docs`.               |
| `final-slow`    | Full check chain: `format-check` + `lint` + `mypy` + `pytest` + `docs`.             |
| `fmt`           | Developer helper: run `ruff check --fix .` and `ruff format .` (broad auto-fix).    |
| `format`        | Apply formatting (`ruff format`) to selected paths.                                 |
| `format-check`  | Check formatting only (`ruff format --check`) on selected paths.                    |
| `help`          | Print the complete list of targets and short descriptions.                          |
| `install`       | `pip install -e .` (editable install) after venv exists.                            |
| `install-all`   | Install default dependencies (`uv sync`).                                           |
| `install-dev`   | Install default + dev dependencies (`uv sync --extra dev`).                         |
| `install-docs`  | Install default + docs dependencies (`uv sync --extra docs`).                       |
| `lint`          | Ruff lint (check-only): `ruff check .`.                                             |
| `lint-fix`      | Ruff lint with auto-fix: `ruff check --fix .`.                                      |
| `mypy`          | Type-check: `mypy mathxlab tests experiments`.                                      |
| `out`           | Run all experiments sequentially (`mathxlab/experiments/e###.py`).                  |
| `perf`          | Run performance suite in “dev” mode.                                                |
| `perf-compare`  | Compare two perf snapshots (`A=... B=...`).                                         |
| `perf-release`  | Run performance suite in “release” mode.                                            |
| `pytest`        | Run fast tests (`not slow`) with coverage.                                          |
| `pytest-slow`   | Run fast tests then slow tests (`slow`) with coverage aggregation.                  |
| `pytest-xdist`  | Run fast tests with xdist (`-n auto`).                                              |
| `python-check`  | Verify `python` is at least `PYTHON_MIN`.                                           |
| `run`           | Run a single experiment by id: `make run EXP=e001 [ARGS=...]`.                      |
| `snapshots`     | Sync `out/*` snapshots (params/report/assets) into `docs/*` (optionally `IDS=...`). |
| `status`        | Update `docs/experiment_status.md`.                                                 |
| `tags-check`    | Validate doc tags against `docs/tags.md`.                                           |
| `uv-check`      | Verify `uv` is installed and available on PATH.                                     |
| `venv`          | Create `.venv` if missing (does not install deps by itself).                        |
| `venv-recreate` | Remove and recreate `.venv` from scratch.                                           |

---

## Variables and parameters

These are the most common knobs you can pass on the command line:

* `EXP`: experiment id, e.g. `e001` (used by `run`)
* `ARGS`: forwarded to the experiment module, e.g. `ARGS="--seed 1 --n 200000"`
* `OUT_ROOT`: defaults to `out` (used by `snapshots`)
* `DOCS_ROOT`: defaults to `docs` (used by `snapshots`)
* `IDS`: optional list for `snapshots`, e.g. `IDS="e001 e002 e003"`
* `A`, `B`: perf snapshot identifiers for `perf-compare`
* `PYTHON_MIN`: minimum Python version required by `python-check`

---

## Notes on documentation targets

* `docs-html` should work if `docs-deps` (or `install-dev` + `install-docs`) succeeds.
* `docs-pdf` requires an external LaTeX toolchain:

  * `latexmk`
  * a LaTeX distribution (MiKTeX on Windows, TeX Live on Linux)
  * recommended engine: `xelatex` (works well with Unicode fonts)

If LaTeX is not installed, `docs-pdf` should be treated as “best effort”.

---

## Troubleshooting

### Sphinx “include start-after/end-before text not found”

This means an `{include}` directive is looking for a marker string that does not
exist in the included file. Ensure this `docs/makefile.md` contains the headings
exactly as expected (including capitalization and parentheses).

### CI shell errors in Make recipes

GitHub Actions uses `/bin/sh` by default. Any recipe text containing shell
metacharacters must be valid for POSIX shells.

```
