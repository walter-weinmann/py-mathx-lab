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
:end-before: "## Snapshots: syncing experiment outputs into docs"
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

### Report contract for algorithmic experiments (Phase 2 and later)

For experiments involving algorithms (primality tests, factorization, explicit bounds), the
`out/e###/report.md` file is part of the experiment's *scientific contract*.

It must state (when applicable):

- **Deterministic vs probabilistic.** Always label this explicitly.
- **Probability of error** for probabilistic methods (bases / repetitions).
- **Correctness cross-checks** against a trusted reference for CI-safe ranges.
- **Known counterexamples / failure modes** (e.g., Carmichael numbers for Fermat).
- **Finite-range behavior** vs asymptotics (do not oversell small N).

Use this drop-in template for report sections (copy/paste into `report.md` or generate it in code):

```{include} experiments/report_section_template.md
:start-after: "<!-- TEMPLATE:BEGIN -->"
:end-before: "<!-- TEMPLATE:END -->"
```

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
