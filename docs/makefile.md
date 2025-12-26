# Makefile

This project uses a Makefile as a thin, cross-platform command interface around
[`uv`](https://github.com/astral-sh/uv) and common developer workflows:

- formatting + linting (`ruff`)
- typing (`mypy`)
- tests (`pytest`)
- documentation build (Sphinx HTML + optional PDF via LaTeX)

The Makefile is designed to work on:

- **Windows** (PowerShell / cmd) for local development
- **Linux** (e.g., GitHub Actions runners) for CI

---

## Quick start

### Create / sync the venv
```bash
make venv
````

### Run the full local “confidence chain”

```bash
make final
```

### Build documentation

```bash
make docs
```

---

## Dependency groups (pyproject.toml)

Dependencies are organized via `pyproject.toml` extras:

* **default**: runtime dependencies needed to run the package
* **dev** (`--extra dev`): developer tooling (ruff, mypy, pytest, etc.)
* **docs** (`--extra docs`): documentation tooling (sphinx, furo, myst-parser, sphinx-design, bibtex, ...)

### What the Makefile does

* Most dev targets run via:

  ```bash
  uv run --extra dev ...
  ```
* Documentation targets run via:

  ```bash
  uv run --extra docs ...
  ```

### Why this matters

CI and local development can install only what they need:

* fast “dev chain” (no docs):

  ```bash
  uv sync --extra dev
  ```
* docs build:

  ```bash
  uv sync --extra docs
  ```

---

## Run logs and experiment runner

Experiments live under `mathxlab/experiments/` and can be run either directly
with Python or through Make targets (if available in your Makefile).

### Run an experiment module directly

```bash
uv run python -m mathxlab.experiments.e001
```

### Typical output locations (convention)

Depending on the experiment runner implementation, outputs are usually placed in:

* `out/e###/` (generated artifacts, figures, manifests)
* `docs/gallery/`, `docs/reports/`, `docs/manifests/` (published snapshots)

If you add new experiments, keep the numbering stable (`e001`, `e002`, …) so the
gallery and documentation can remain consistent.

---

## Common workflows

| Task                   | Command                     |
| ---------------------- | --------------------------- |
| Complete quality check | `make final`                |
| Build HTML docs        | `make docs-html`            |
| Run tests              | `make test`                 |
| Clean all artifacts    | `make clean`                |
| Reset environment      | `make clean && make venv`   |

---

## Target overview (what each target does)

> The exact set of targets is defined in the repository `Makefile`.
> This page documents the intent of the standard targets used in this repo.

| Target      | Purpose                                                                               |
| ----------- | ------------------------------------------------------------------------------------- |
| `venv`      | Create / reuse `.venv` (via `uv venv` / `uv sync`) and install required dependencies. |
| `docs`      | Build docs HTML and then attempt PDF generation (if the toolchain is installed).      |
| `docs-html` | Build Sphinx HTML into `docs/_build/html`.                                            |
| `docs-pdf`  | Build Sphinx LaTeX + compile to PDF using `latexmk` (optional).                       |
| `format`    | Run `ruff format` (may include `--check` in CI).                                      |
| `lint`      | Run `ruff check`.                                                                     |
| `type`      | Run `mypy`.                                                                           |
| `test`      | Run `pytest`.                                                                         |
| `final`     | Run the full chain: sync dev deps, format check, lint, type, tests, docs.             |
| `clean`     | Remove build artifacts (e.g., `docs/_build`).                                         |

### Notes on documentation targets

* `docs-html` should always work if `--extra docs` installs successfully.
* `docs-pdf` requires an external LaTeX toolchain:

  * `latexmk`
  * a LaTeX distribution (MiKTeX on Windows, TeX Live on Linux)
  * recommended engine: `xelatex` (works well with Unicode fonts)

If LaTeX is not installed, `docs-pdf` should be treated as “best effort”.

---

## Troubleshooting

### Sphinx “include start-after/end-before text not found”

This means a `{include}` directive is looking for a marker string that does not
exist in the included file. Ensure this `docs/makefile.md` contains the headings
exactly as expected (including capitalization and parentheses).

### CI shell errors in Make recipes

GitHub Actions uses `/bin/sh` by default. Any recipe text containing shell
metacharacters (e.g., `;`) must be quoted.
