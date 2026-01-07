# Makefile

This repository uses a **Makefile** as a simple command launcher for common tasks.
Think of it as a “one command per workflow” shortcut (similar to `npm run …` in JS).

It wraps these tools:

- **uv**: creates `.venv` and installs dependencies
- **ruff**: formatting + linting
- **mypy**: type checking
- **pytest**: tests (fast / slow / perf)
- **Sphinx**: builds documentation (HTML + optional PDF)

:::{note}
**Windows detail:** Make recipes run under `cmd.exe` (`SHELL := cmd.exe` in the Makefile).  
You can still *invoke* `make …` from PowerShell, but the recipe lines execute in `cmd.exe`.
A few targets intentionally call PowerShell (mainly experiment loops) because it is more robust there.
:::

---

## Quick start

### First-time setup (all platforms)

```bash
make install-dev
````

This will:

1. check that `uv` exists
2. check you have a recent enough Python (default minimum is 3.14)
3. create `.venv` if missing
4. install dependencies (runtime + dev tools)

### Day-to-day workflow (most common)

When you changed code and want quick confidence:

```bash
make fmt
make pytest
```

When you want “as close to CI as possible”:

```bash
make final
```

### Documentation (HTML)

```bash
make docs-html
```

If you don’t have LaTeX installed, prefer `docs-html` over `docs` (see “Docs” section below).

---

## How to think about the Make targets (junior-friendly)

The targets fall into **two big buckets**:

### 1) Quality checks (keep code correct and consistent)

* **Formatting**: makes code look consistent (indentation, line breaks, etc.)
* **Linting**: catches common mistakes and style issues
* **Typing**: catches type errors before runtime
* **Testing**: ensures behaviour stays correct

### 2) Productive targets (produce outputs)

* run experiments and produce files under `out/…`
* sync experiment outputs into `docs/…` (for the gallery/docs)
* build documentation

If you are unsure which command to run: **use `make final`**.

---

## Dependency groups (pyproject.toml)

`uv` installs dependencies from your `pyproject.toml`. This project uses “extras”:

* **default**: runtime dependencies (needed to run the package)
* **dev**: developer tools (ruff, mypy, pytest, …)
* **docs**: documentation tools (sphinx, theme, myst, bibtex, …)

### What the Makefile uses

* Most developer commands run via:

  ```bash
  uv run --extra dev ...
  ```

* Documentation build runs via:

  ```bash
  uv run --extra docs ...
  ```

### Why `docs-deps` uses `--all-extras`

`make docs-deps` runs:

```bash
uv sync --all-extras
```

because the docs pipeline also runs a small helper under the **dev** extra before invoking Sphinx.

---

## Virtual environment behavior

### Where is the venv?

The venv is always created at:

* `.venv/`

### Minimum Python version

The Makefile checks `PYTHON_MIN` (default is `3.14`). If your Python is older, `make python-check` fails.

### Why `UV_LINK_MODE=copy` exists

On Windows, hardlinks can fail or warn on multi-drive setups (e.g. repo on `D:` but cache on `C:`).
So the Makefile defaults to:

* `UV_LINK_MODE=copy`

You *can* override it, but the default is chosen to reduce Windows pain.

### Common “reset” if your venv is broken

```bash
make clean-venv
make install-dev
```

---

## Formatting (ruff)

Formatting is purely about **how code looks**, not what it does.

### Targets

| Target              | What it does                                      | When to use it                            |
| ------------------- | ------------------------------------------------- | ----------------------------------------- |
| `make format`       | formats selected repo paths                       | normal formatting                         |
| `make format-check` | checks formatting only (no changes)               | CI-like check                             |
| `make fmt`          | “broad auto-fix”: ruff fixes + formats everything | when you want the repo cleaned up quickly |

### Typical usage

Before committing:

```bash
make fmt
```

If CI says “formatting changed”:

```bash
make format
```

---

## Linting (ruff)

Linting looks for **potential bugs and bad patterns**, for example:

* unused imports
* variables shadowing names
* common correctness issues ruff knows how to detect

### Targets

| Target          | What it does       | Does it edit files? |
| --------------- | ------------------ | ------------------- |
| `make lint`     | ruff check-only    | no                  |
| `make lint-fix` | ruff with auto-fix | yes                 |

### Typical usage

* Use `make lint` when you only want to see problems.
* Use `make lint-fix` when you want ruff to fix safe issues automatically.

---

## Typing (mypy)

Typing checks help catch issues like:

* calling functions with wrong argument types
* returning the wrong types
* forgetting to handle `None`

### Target

```bash
make mypy
```

It runs:

* `mypy mathxlab tests experiments`

### Common tip for juniors

If mypy errors look scary, start with the first error in the output.
Many later errors are “follow-up noise” caused by an earlier wrong type.

---

## Tests (pytest): fast / slow / perf

This repo separates tests using **pytest markers**:

* **fast tests**: `not slow and not perf`
* **slow tests**: `slow and not perf`
* **perf tests**: `perf`

Markers are set in tests like:

```python
import pytest

@pytest.mark.slow
def test_big_case():
    ...
```

### Coverage and threshold

Tests collect coverage for the library packages (not for experiment scripts).
Coverage fails the target if it drops below **80%**.

### Stable temp paths

pytest is invoked with stable temp directories:

* `temp_pytest_cache`
* `temp_pytest`

They are cleaned by `make clean`.

---

### `pytest` (fast tests)

```bash
make pytest
```

What it does:

* runs only **fast** tests (`not slow and not perf`)
* runs with coverage
* fails if coverage < 80%

This is the main “developer loop” test target.

---

### `pytest-xdist` (fast tests in parallel)

```bash
make pytest-xdist
```

Runs fast tests using xdist:

* `-n auto --dist=load`

Use this when the test suite gets bigger and you want faster local feedback.

---

### `pytest-slow` (two-phase: fast then slow)

```bash
make pytest-slow
```

What it does (important detail):

1. deletes `.coverage`
2. runs **fast tests** first *in best-effort mode*
   (failures in this phase do **not** fail the target — this is intentional in the Makefile)
3. runs **slow tests** with:

   * xdist by default (`PYTEST_XDIST_SLOW=-n auto --dist=load`)
   * `--cov-append` to combine coverage from both phases
   * coverage threshold (80%)

:::{warning}
If you want “fast tests must pass”, run `make pytest` separately.
`make pytest-slow` is designed to always get through the slow suite even if fast tests are currently failing.
:::

---

## Performance tests (pytest-perf): what they are and how to use them

Performance tests are still **pytest tests**, but marked with `@pytest.mark.perf`.
They exist to catch **accidental slowdowns** (e.g. a function becomes 10× slower).

### Why the Makefile forces thread counts to 1

Math/scientific libraries sometimes use multiple CPU threads automatically (BLAS/OpenMP/etc.).
That makes timings noisy and hard to compare.

So perf targets set:

* `OMP_NUM_THREADS=1`
* `MKL_NUM_THREADS=1`
* `OPENBLAS_NUM_THREADS=1`
* `NUMEXPR_NUM_THREADS=1`

This makes timings **more reproducible** across machines and runs.

---

### `pytest-perf` (run perf-marked tests)

```bash
make pytest-perf
```

Runs only:

* `-m "perf"`

and shows progress output.

Use this when:

* you changed a performance-sensitive function
* you want to ensure you didn’t introduce an obvious regression

### `pytest-perf-baseline` (update accepted baseline numbers)

```bash
make pytest-perf-baseline
```

Same as `pytest-perf`, but also passes:

* `--perf-update-baseline`

Use this **only** when:

* you intentionally changed performance (e.g. algorithm changed)
* and you want to accept the new timings as the baseline

:::{warning}
Baseline updates should be done on a reasonably idle machine.
If you run baseline updates while your system is busy, you may “bake in” slow/noisy numbers.
:::

---

## Performance suite (non-pytest): snapshots and comparisons

In addition to `pytest-perf`, the Makefile also provides a small “perf runner” pipeline:

### `perf` (dev snapshot)

```bash
make perf
```

Runs:

* `python mathxlab/tools/run_perf.py --mode dev --overwrite`

This is typically used during development to write/update a **performance snapshot**.

### `perf-release` (release snapshot)

```bash
make perf-release
```

Runs:

* `python mathxlab/tools/run_perf.py --mode release --overwrite`

This is usually for “release-ish” measurements (more stable, fewer surprises).

### `perf-compare` (compare two snapshots)

```bash
make perf-compare A=v0.1.0 B=v0.2.0
```

Runs:

* `python mathxlab/tools/compare_perf.py --a … --b …`

Use this when you want a readable report of “what got faster/slower” between two saved snapshots.

:::{tip}
If you’re not sure what valid values for `A` and `B` are, run `make perf` once and look at the output written by the script.
It usually prints the snapshot identifiers/paths it created.
:::

---

## Run logs and experiment runner

Experiments are Python modules like:

* `mathxlab/experiments/e001.py`
* `mathxlab/experiments/e002.py`
* …

### Run one experiment (recommended: via Make)

```bash
make run EXP=e001
```

This:

* creates `out/e001/` (if missing)
* creates `out/e001/logs/`
* writes a log file:

  * `out/e001/logs/run_e001.log`
* runs the experiment with:

  * `python -m mathxlab.experiments.e001 --out out/e001 -v`

### Forward CLI arguments

```bash
make run EXP=e001 ARGS="--seed 123 --n 200000"
```

:::{note}
On Windows, always quote `ARGS="..."` if it contains spaces.
:::

### Run all experiments

```bash
make out
```

This finds all `mathxlab/experiments/e???.py` files and runs them sequentially.

---

## Snapshots: syncing experiment outputs into docs

After experiments run, you typically want to publish their outputs into `docs/…`
so the gallery/docs can include them.

### `snapshots`

```bash
make snapshots
```

Runs a sync helper that copies the “published artifacts” from:

* `out/...`

into:

* `docs/...`

You can limit what is synced:

```bash
make snapshots IDS="e001 e002 e010"
```

Or redirect roots:

```bash
make snapshots OUT_ROOT=out DOCS_ROOT=docs
```

---

## Documentation builds: HTML and optional PDF

### `docs-html` (recommended)

```bash
make docs-html
```

What it does:

1. installs docs dependencies (`make docs-deps`)
2. runs the snapshot sync helper (so docs see the latest experiment artifacts)
3. builds Sphinx HTML into `docs/_build/html`

Important: it uses Sphinx `-W`, so **warnings become errors** (this is intentional for CI cleanliness).

### `docs-pdf` (optional; requires LaTeX)

```bash
make docs-pdf
```

Requires a working LaTeX toolchain (including `latexmk`).

### `docs`

```bash
make docs
```

Runs the full chain:

* `status → tags-check → docs-html → docs-pdf`

:::{note}
If you don’t have LaTeX installed locally, use `make docs-html`.
:::

---

## Target overview (what each target does)

Targets are defined in the repository `Makefile`.
This table explains what each one is for.

| Target                 | Purpose                                                                            |
| ---------------------- | ---------------------------------------------------------------------------------- |
| `clean`                | Remove caches/build artifacts (docs build, mypy/pytest/ruff caches, temp dirs, …). |
| `clean-venv`           | Remove the virtual environment `.venv`.                                            |
| `docs`                 | Build docs: `status` + `tags-check` + `docs-html` + `docs-pdf`.                    |
| `docs-clean`           | Remove `docs/_build`.                                                              |
| `docs-deps`            | Install/update dependencies needed for docs builds (`uv sync --all-extras`).       |
| `docs-html`            | Build Sphinx HTML into `docs/_build/html` (strict warnings).                       |
| `docs-pdf`             | Build PDF docs (optional): requires LaTeX toolchain + `latexmk`.                   |
| `final`                | Full chain: `format` + `lint-fix` + `mypy` + `pytest` + `docs`.                    |
| `final-slow`           | Strict chain: `format-check` + `lint` + `mypy` + `pytest-slow` + `docs`.           |
| `fmt`                  | Broad auto-fix helper: `ruff check --fix .` and `ruff format .`.                   |
| `format`               | Apply formatting (`ruff format`) to selected paths.                                |
| `format-check`         | Check formatting only (`ruff format --check`) on selected paths.                   |
| `help`                 | Print the complete list of targets and short descriptions.                         |
| `install`              | Editable install: `uv pip install -e .` (after venv exists).                       |
| `install-all`          | Install default dependencies (`uv sync`).                                          |
| `install-dev`          | Install default + dev dependencies (`uv sync --extra dev`).                        |
| `install-docs`         | Install default + docs dependencies (`uv sync --extra docs`).                      |
| `lint`                 | Ruff lint (check-only): `ruff check .`.                                            |
| `lint-fix`             | Ruff lint with auto-fix: `ruff check --fix .`.                                     |
| `mypy`                 | Type-check: `mypy mathxlab tests experiments`.                                     |
| `out`                  | Run all experiments sequentially (`mathxlab/experiments/e###.py`).                 |
| `perf`                 | Run perf suite in “dev” mode (writes snapshot).                                    |
| `perf-compare`         | Compare two perf snapshots (`A=... B=...`).                                        |
| `perf-release`         | Run perf suite in “release” mode (writes snapshot).                                |
| `pytest`               | Run fast tests (`not slow and not perf`) with coverage + threshold.                |
| `pytest-perf`          | Run perf-marked tests (`perf`) with reproducible threading env vars.               |
| `pytest-perf-baseline` | Same as `pytest-perf`, but updates stored baselines.                               |
| `pytest-slow`          | Run fast then slow tests with coverage aggregation.                                |
| `pytest-xdist`         | Run fast tests with xdist (`-n auto --dist=load`).                                 |
| `python-check`         | Verify Python >= `PYTHON_MIN`.                                                     |
| `run`                  | Run a single experiment: `make run EXP=e001 [ARGS=...]`.                           |
| `snapshots`            | Sync `out/*` snapshots into `docs/*` (optionally `IDS=...`).                       |
| `status`               | Update `docs/experiment_status.md`.                                                |
| `tags-check`           | Validate docs tags against `docs/tags.md`.                                         |
| `uv-check`             | Verify `uv` is available on PATH.                                                  |
| `venv`                 | Create `.venv` if missing (does not install deps by itself).                       |
| `venv-recreate`        | Remove and recreate `.venv` from scratch.                                          |

---

## Variables you can override

Make lets you pass variables like:

```bash
make <target> NAME=value
```

Common variables:

| Variable            | Meaning                                                    | Example                                               |
| ------------------- | ---------------------------------------------------------- | ----------------------------------------------------- |
| `EXP`               | experiment id (used by `run`)                              | `make run EXP=e001`                                   |
| `ARGS`              | forwarded CLI args for experiments                         | `make run EXP=e001 ARGS="--seed 1 --n 200000"`        |
| `OUT_ROOT`          | snapshot input root                                        | `make snapshots OUT_ROOT=out`                         |
| `DOCS_ROOT`         | snapshot docs root                                         | `make snapshots DOCS_ROOT=docs`                       |
| `IDS`               | experiment id filter for snapshots                         | `make snapshots IDS="e001 e002"`                      |
| `A` / `B`           | perf snapshot identifiers for `perf-compare`               | `make perf-compare A=v0.1.0 B=v0.2.0`                 |
| `PYTEST_XDIST_FAST` | extra xdist args for fast tests                            | `make pytest PYTEST_XDIST_FAST="-n auto --dist=load"` |
| `PYTEST_XDIST_SLOW` | xdist args for slow tests (default: `-n auto --dist=load`) | `make pytest-slow PYTEST_XDIST_SLOW=`                 |
| `PYTHON_MIN`        | minimum Python version                                     | `make venv PYTHON_MIN=3.14`                           |
| `UV_LINK_MODE`      | uv link mode (default: `copy`)                             | `make install-dev UV_LINK_MODE=hardlink`              |

---

## Troubleshooting

### `make uv-check` fails (“uv is not installed”)

Install `uv` and ensure it is on PATH, then rerun:

```bash
make uv-check
make install-dev
```

### `make python-check` fails (Python too old / not found)

Reset sequence:

```bash
make clean-venv
make install-dev
```

### `docs-html` fails with include marker errors

This happens when `docs/development.md` uses `include` with `start-after` / `end-before`
and the marker headings are missing or renamed.

This file intentionally contains these headings **exactly**:

* `## Dependency groups (pyproject.toml)`
* `## Run logs and experiment runner`
* `## Target overview (what each target does)`

If you rename them, the include markers in other docs may break.

### Windows quoting problems for `ARGS`

If `ARGS` contains spaces, always quote:

```powershell
make run EXP=e001 ARGS="--seed 1 --n 200000"
```

If you need nested quotes, prefer single quotes inside double quotes:

```powershell
make run EXP=e001 ARGS="--title 'My Title With Spaces'"
```
