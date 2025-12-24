# Minimal Makefile (Windows + Linux/macOS), same functionality

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

## Run logs and experiment runner

The `run` target writes a per-run log file under:

- `out/<exp>/logs/run_<exp>_YYYYMMDD_HHMMSS.log`

On Windows, the Makefile calls a small PowerShell helper script (`scripts/run_experiment.ps1`) so that:

- the Makefile stays readable,
- logs are written as UTF-8,
- both the dependency sync (`uv sync --extra dev`) and the experiment output end up in the same log.

To enable DEBUG output **only** from this repository’s code (`mathxlab.*`), run with `V=1`:

```bash
make run EXP=e001 ARGS="--seed 1" V=1
```


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
make run EXP=e001 ARGS="--seed 1"
```

Use `V=1` to enable DEBUG logs from `mathxlab.*` only:

```bash
make run EXP=e001 ARGS="--seed 1" V=1
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
