# Makefile usage (Windows + Ubuntu)

This repository uses a small `Makefile` as a thin wrapper around:

- **Python** (requires `>= 3.13`)
- **uv** (virtual environment + dependency management via `uv.lock`)
- **ruff / mypy / pytest** (dev toolchain)
- **Sphinx** (docs build)

The goals are:

- one consistent command set for Windows and Ubuntu
- reproducible installs via `uv.lock`
- simple CI entrypoints (`make final`)

---

## Prerequisites

### Required on both Windows and Ubuntu

- **Python 3.13+** available on `PATH` (used by `make python-check`)
- **uv** installed and available on `PATH`
- **GNU Make**
  - Ubuntu: `sudo apt-get install make`
  - Windows: install a `make` compatible with GNU Make (e.g., via Git for Windows / MSYS2 / Chocolatey)

### Notes for Windows

- Run `make` from **PowerShell** or **cmd.exe**.
- The Makefile supports Windows command shell behavior.
- The warning `CRLF will be replaced by LF` is normal and controlled by `.gitattributes`.

---

## System Python vs `.venv` Python (important)

This repo intentionally uses **two “Python contexts”**:

1) **System Python (or whatever `python` on PATH points to)**  
   Used only for `make python-check` to verify you *can* run Python 3.13+ at all.

2) **Project virtual environment `.venv` managed by uv**  
   Used for *all tooling and project commands* via `uv run ...`.

### What this means in practice

- You **do not need to activate** `.venv` to run Make targets.
- Targets like `format`, `lint`, `mypy`, `pytest`, `docs`, and `run` execute inside `.venv` because they call `uv run ...`.
- If you have multiple Python installs on Windows, `python-check` can succeed (or fail) based on what `python` resolves to.  
  The actual `.venv` interpreter is selected by:

```bash
make venv
```

which runs:

```bash
uv venv --python <PYTHON_MIN>
```

So: **`python-check` validates PATH**, while **`venv` selects the interpreter for `.venv`**.

### Quick sanity checks

* Show which Python is used for the *system check*:

```bash
python --version
where python   # Windows
which python   # Ubuntu
```

* Show which Python is used inside the project environment:

```bash
uv run python --version
```

---

## Dependency groups (pyproject.toml)

Your `pyproject.toml` defines dependency sets:

* Base runtime dependencies: `project.dependencies`
* Dev tools: `project.optional-dependencies.dev` (e.g. `ruff`, `mypy`, `pytest`)
* Docs tools: `project.optional-dependencies.docs` (e.g. `sphinx`, `sphinxcontrib-bibtex`)

The Makefile maps to these groups like this:

* `make install-all` → `uv sync` (base set from `uv.lock`)
* `make install-dev` → `uv sync --extra dev`
* `make install-docs` → `uv sync --extra docs`
* `make install` → `uv pip install -e .` (editable install)

> Recommendation: keep `uv.lock` committed. It is the reproducibility anchor for `uv sync`.

---

## Common workflows

### First-time setup (dev machine)

```bash
make uv-check
make python-check
make venv
make install-dev
```

### Run checks locally (like CI)

```bash
make final
```

### Build docs only

```bash
make docs
```

### Run an experiment

```bash
make run EXP=e001
```

---

## Target overview (what each target does)

### Environment and installs

* `uv-check`
  Verifies that `uv` is installed.

* `python-check`
  Verifies that your current `python` is at least the configured minimum version.

* `venv`
  Creates/updates `.venv` using uv (`uv venv --python <PYTHON_MIN>`).

* `install-all`
  Installs base dependencies from `uv.lock` (`uv sync`).

* `install-dev`
  Installs base + dev tools (`uv sync --extra dev`).

* `install-docs`
  Installs base + docs tools (`uv sync --extra docs`).

* `install`
  Editable install of the package (`uv pip install -e .`).

### Quality / verification

* `format`
  Runs `ruff format` (in CI mode `CI=1`, runs `ruff format --check`).

* `lint`
  Runs `ruff check`.

* `mypy`
  Runs `mypy .`.

* `pytest`
  Runs tests (`pytest -q`).

### Documentation

* `docs`
  Builds HTML docs with Sphinx into `docs/_build/html`.

* `docs-clean`
  Removes `docs/_build`.

### Cleanup

* `clean`
  Removes caches/build artifacts (`.mypy_cache`, `.pytest_cache`, `.ruff_cache`, `dist`, `build`, `docs/_build`, etc.).

* `clean-venv`
  Removes `.venv`.

### Aggregation

* `final`
  Runs: `format + lint + mypy + pytest + docs`.

> Note: `format/lint/mypy/pytest` depend on dev tools; `docs` depends on docs tools.
> The Makefile ensures this by making those targets run after `install-dev` / `install-docs`.

---

## Troubleshooting

### 1) `Need Python >= 3.13.0, got 3.13`

This happens if the check compares incompatible types (e.g. a float like `3.13` vs `(3, 13)`).
The correct approach is to parse the version string into integer `(major, minor)` and compare that.

The Makefile uses this correct pattern in `python-check`:

```make
@python -c "import sys; req='$(PYTHON_MIN)'.split('.'); req=(int(req[0]), int(req[1])); v=sys.version_info; assert v[:2] >= req, f'Need Python >= {req[0]}.{req[1]}, got {v.major}.{v.minor}'"
```

### 2) `error: Failed to spawn: ruff (program not found)`

`ruff` is a **dev extra**. Fix:

```bash
make install-dev
```

Then rerun:

```bash
make format
# or
make final
```

### 3) `Failed to hardlink files; falling back to full copy`

This is a performance warning from uv (common on Windows when cache and target are on different filesystems).
You can silence it by forcing copy mode:

* PowerShell:

```powershell
$env:UV_LINK_MODE="copy"
```

* cmd.exe:

```bat
set UV_LINK_MODE=copy
```

(Optionally, the Makefile can export `UV_LINK_MODE=copy` by default.)

### 4) CRLF/LF warnings on Windows

Example:

```
warning: CRLF will be replaced by LF ...
```

This is expected when `.gitattributes` enforces LF for consistency.

---

## CI notes

* In CI, use:

```bash
CI=1 make final
```

This makes `format` run in check mode.

* Ensure CI installs Python 3.13+ and has `uv` available.
* Keep `uv.lock` committed so `uv sync` is deterministic.
