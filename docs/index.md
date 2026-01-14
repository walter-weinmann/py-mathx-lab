# py-mathx-lab

Small, reproducible math experiments implemented in Python.

```{toctree}
:hidden:
:caption: Guide
:maxdepth: 2

mathematical-experimentation
getting-started
development
```

```{toctree}
:hidden:
:caption: Experiments
:maxdepth: 2

tags
experiments/experiments_gallery
experiment_status
```

```{toctree}
:hidden:
:caption: Background
:maxdepth: 2

background
references
```

```{toctree}
:hidden:
:caption: Downloads
:maxdepth: 1

pdf
```

```{toctree}
:hidden:
:caption: API
:maxdepth: 2

api/index
api/exp
api/experiments
api/nt
api/num
api/plots
api/utils
api/viz
```

```{only} html

## Start here

- {doc}`mathematical-experimentation` — what “experiments” in mathematics mean and how to read this repo
- {doc}`tags` — central directory of valid tags for experiments
- {doc}`experiments/experiments_gallery` — experiment gallery (IDs, tags, how to run)
- {doc}`getting-started` — install, setup, and run your first experiment
- {doc}`development` — Makefile workflow, CI, coding conventions
- {doc}`background` — mathematical background for experiments
- {doc}`api/index` — library-style API reference (excludes runnable experiments/tools)
- {doc}`pdf` — download the PDF version of these docs
- {doc}`experiment_status` — processing status / maintenance
- {doc}`references` — bibliography and reading list

## Run one experiment

```text
make uv-check
make venv
make install-dev
make run EXP=e001 ARGS="--out out/e001 --seed 1"
```

## Latest

**E129** — Euler lucky constants for $n^2 + n + b$ — {doc}`open <experiments/e129>`

Check the {doc}`experiments/experiments_gallery` for new experiments.
