# Makefile usage (Windows + Ubuntu)

This repository uses a small `Makefile` as a thin wrapper around:

- **Python** (requires `>= 3.13`)
- **uv** (environment + dependency management)
- **ruff / mypy / pytest** (dev toolchain)
- **Sphinx** (docs build)

The goal is:

- one consistent command set for Windows and Ubuntu
- reproducible installs via `uv.lock`
- simple CI entrypoints (`make final`)

---

## Prerequisites

### Required on both Windows and Ubuntu

- **Python 3.13+** available on `PATH` (for `make python-check`)
- **uv** installed and available on `PATH`
- **GNU Make**
  - Ubuntu: `sudo apt-get install make`
  - Windows: install a `make` compatible with GNU Make (e.g. via Git for Windows / MSYS2 / Chocolatey)

### Notes for Windows

- Run `make` from **PowerShell** or **cmd.exe**.
- The Makefile is written to be compatible with Windows’ command shell behavior.
- The warning `CRLF will be replaced by LF` is normal and controlled by `.gitattributes`.

---

## Dependency groups (pyproject.toml)

Your `pyproject.toml` defines extras:

- Base runtime dependencies: `project.dependencies`
- Dev tools: `project.optional-dependencies.dev` (e.g. `ruff`, `mypy`, `pytest`)
- Docs tools: `project.optional-dependencies.docs` (e.g. `sphinx`)

The Makefile targets map to these groups:

- `make install` → editable install of the package (runtime deps only)
- `make install-dev` → installs runtime + **dev** tools
- `make install-docs` → installs runtime + **docs** tools
- `make install-all` → installs from `uv.lock` (reproducible base; extras are handled by the dedicated targets)

> Recommendation: keep `uv.lock` committed. It is the reproducibility anchor for `uv sync`.

---

## Common workflows

### First-time setup (dev machine)

```bash
make uv-check
make python-check
make venv
make install-dev
````

### Run checks locally (like CI)

```bash
make final
```

### Build docs

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
  Creates/updates `.venv` using uv.

* `install`
  Editable install of the package (runtime deps).

* `install-dev`
  Ensures dev dependencies are installed (ruff/mypy/pytest, etc.), plus editable install.

* `install-docs`
  Ensures docs dependencies are installed (Sphinx, etc.), plus editable install.

* `install-all`
  Installs dependencies from `uv.lock` (base reproducible set).

### Quality / verification

* `format`
  Runs `ruff format`. In CI mode (`CI=1`), uses `--check`.

* `lint`
  Runs `ruff check`.

* `mypy`
  Runs mypy type checks.

* `pytest`
  Runs the test suite.

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
  Runs the “everything should be green” sequence (format + lint + mypy + tests + docs).

---

## Troubleshooting

### 1) `Need Python >= 3.13.0, got 3.13`

This happens if the Makefile constructs `req=(3.13, 0)` (a float) and compares it to `(3, 13)`.
The fix is to **parse the version string into integers** inside `python-check`.

**Correct pattern** inside `python-check`:

```make
@python -c "import sys; req='$(PYTHON_MIN)'; major,minor=(int(x) for x in req.split('.')[:2]); v=sys.version_info; assert (v.major,v.minor)>=(major,minor), f'Need Python >= {req}, got {v.major}.{v.minor}'"
```

### 2) `error: Failed to spawn: ruff (program not found)`

`ruff` is a **dev dependency** (extra). Fix:

```bash
make install-dev
```

Then rerun:

```bash
make format
# or
make final
```

If you want `make final` to always work from a clean checkout, ensure that `final`
runs `install-dev` before `format/lint/mypy/pytest`.

### 3) `Failed to hardlink files; falling back to full copy`

This is a performance warning from uv on Windows when cache and target are on different filesystems.
You can silence it by setting:

* PowerShell:

```powershell
$env:UV_LINK_MODE="copy"
```

* cmd.exe:

```bat
set UV_LINK_MODE=copy
```

### 4) CRLF/LF warnings on Windows

Example:

```
warning: CRLF will be replaced by LF ...
```

This is expected when `.gitattributes` enforces LF for consistency.

---

## CI notes

* In CI, you usually want:

  * `CI=1 make final` (so `format` becomes `ruff format --check`)
* Ensure CI installs Python 3.13+ and has `uv` available.
* Keep `uv.lock` committed so `uv sync` is deterministic.

---
