[![CI](https://github.com/walter-weinmann/py-mathx-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/walter-weinmann/py-mathx-lab/actions/workflows/ci.yml)
[![Docs](https://github.com/walter-weinmann/py-mathx-lab/actions/workflows/docs.yml/badge.svg)](https://github.com/walter-weinmann/py-mathx-lab/actions/workflows/docs.yml)

# py-mathx-lab

A curated gallery of small, reproducible math experiments implemented in Python.

Each experiment is runnable with one command and produces an output folder containing a short report and figures.

## Website (documentation)

Documentation (GitHub Pages):

- https://walter-weinmann.github.io/py-mathx-lab/

The docs include: **Experiments**, **Getting started**, **Development**, **References**.  
As the project grows, experiment write-ups can scale under `docs/experiments/`.

## Quickstart

### Prerequisites

- Python **3.14**
- `uv`
- GNU `make`

### Setup

```bash
make uv-check
make python-check
make venv
make install-dev
````

### Run the development chain (format + lint + typing + tests + documentation)

```bash
make final
```

### Build documentation only (Sphinx)

```bash
make install-docs
make docs
```

Docs output is written to:

* `docs/_build/html`

### Run an experiment

Example (E001):

```bash
make run EXP=e001 ARGS="--seed 1"
```

Outputs will appear in `out/e001/` (report, figures, parameters).

Logs are written to `out/e001/logs/` for each run. Use `V=1` to enable DEBUG logs from `mathxlab.*` only:

```bash
make run EXP=e001 ARGS="--seed 1" V=1
```

Outputs will appear in `out/e001/` (report, figures, parameters).

## Experiments

See the experiment overview in the docs:

* `docs/experiments.md`

As the number of experiments grows, individual pages live under:

* `docs/experiments/e###.md`

### Naming convention

* `experiments/e###_<short_name>.py` (IDs are stable, do not reuse)

### Reproducibility expectations

Each experiment should be:

* deterministic given `--seed` (if randomness is involved)
* self-contained: all artifacts go into the `--out` directory
* runnable as a module (recommended), e.g.:

```bash
uv run python -m mathxlab.experiments.e001_taylor_error_landscapes --out out/e001 --seed 1
```

## Contributing

This is a **solo-maintainer** repository with a strict PR workflow.

* Read: `CONTRIBUTING.md`
* Security: `SECURITY.md`

Highlights:

* No direct pushes to `main`
* Small, reviewable PRs
* CI must pass before merge

## License

* **Code**: MIT License (see `LICENSE`)
* **Documentation & media** (Markdown, images, figures): CC BY 4.0 (see `LICENSE-CC-BY-4.0`)

## Citation

If you reference this work, please cite:

* the repository link
* the experiment ID (e.g., E001)
* ideally a commit hash or tag for reproducibility
