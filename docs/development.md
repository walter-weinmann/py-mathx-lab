# Development

This page describes the development workflow and the conventions used in this repository.

## Workflow overview

Use the Makefile targets for everything. They wrap `uv run ...` so you do not need to activate a virtual environment manually.

Typical day-to-day:

```bash
make final
```

Documentation-only build:

```bash
make docs
```

Clean caches and build artifacts:

```bash
make clean
```

Remove the virtual environment (full reset):

```bash
make clean-venv
```
## Makefile workflow

The Makefile is the **single entry point** for development tasks (env setup, quality checks, docs builds, and running experiments).

- Prefer `make final` before pushing.
- Prefer `make docs` to validate documentation changes.
- Use `make run EXP=<id>` to execute an experiment and write artifacts to `out/<id>/`.

### Dependency groups

This summary is included from the Makefile documentation:

```{include} makefile.md
:start-after: "## Dependency groups (pyproject.toml)"
:end-before: "## Run logs and experiment runner"
```

### Run logs

```{include} makefile.md
:start-after: "## Run logs and experiment runner"
:end-before: "## Common workflows"
```

### Common workflows

```{include} makefile.md
:start-after: "## Common workflows"
:end-before: "## Target overview (what each target does)"
```

### Full reference

For the complete target-by-target reference and troubleshooting, see {doc}`makefile`.

## Formatting, linting, typing, tests

* Formatting: **Ruff formatter**
* Linting: **Ruff**
* Typing: **mypy**
* Tests: **pytest**

### CI formatting behavior

In CI, formatting runs in check mode (`ruff format --check`). Locally it formats in place.

## Experiment authoring guidelines

When adding a new experiment:

1. Add a new module under `mathxlab/experiments/`, e.g. `e002_...py`.
2. Prefer deterministic outputs:

   * `--seed` argument if randomness is involved
   * write results to a single `--out` directory
3. Keep the experiment runnable as a module:

   * `python -m mathxlab.experiments.e002`
4. Update the docs:

   * add a short entry to {doc}`experiments/experiments_gallery`
   * optionally add a dedicated page under `docs/experiments/` later

## Documentation

Docs are built with Sphinx + MyST.

Build locally:

```bash
make install-docs
make docs
```

Deployed website:

* GitHub Pages from the `docs` workflow

## Contributing (high-level)

* Create a feature branch.
* Open a PR against `main`.
* CI must pass before merge.
* Keep PRs small and well-scoped.
