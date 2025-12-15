# py-mathx-lab

Reproducible mathematical experiments in Python — with a focus on **analysis** and **number theory**.

This repo is a curated **gallery**: each experiment is runnable in one command and produces a short report + figures.

## Quickstart

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate

pip install -U pip
pip install -e ".[dev]"

python -m experiments.e001_taylor_error_landscapes --out out/e001 --seed 1
````

Outputs will appear in `out/e001/` (report + figures + parameters).

## Experiment gallery

| ID   | Experiment              | What you’ll see                                                          |
| ---- | ----------------------- | ------------------------------------------------------------------------ |
| E001 | Taylor error landscapes | How approximation error depends on interval, degree, and expansion point |

As you add experiments, include **one representative image** per row and link to the output report.

## How to run an experiment

All experiments follow the same interface:

```bash
python -m experiments.eNNN_slug --out out/eNNN --seed 1
```

Each run must be:

* deterministic given the seed
* self-contained (write everything needed to reproduce the outputs)

## How to add a new experiment

* Copy the structure of `experiments/e001_taylor_error_landscapes.py`
* Use helpers in `mathxlab.exp.*`
* Ensure it produces:

  * `report.md`
  * `params.json`
  * at least one `fig_*.png`

## Design principles

* Experiment → observation → conjecture → falsification attempt
* Strong separation of concerns:

  * `experiments/` = questions + runs
  * `mathxlab/` = reusable utilities (sampling, metrics, plotting, reporting)
  * `posts/` = public writing derived from experiment outputs

## Development

```bash
ruff check .
pytest -q
mypy mathxlab
```

## License

* **Code**: MIT License (see `LICENSE`)
* **Documentation & media** (Markdown, images, figures): CC BY 4.0 (see `LICENSE-docs`)

## Citation

If you reference this work, please link to the repository and the specific experiment ID.

```
```
