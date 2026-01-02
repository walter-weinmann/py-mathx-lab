# py-mathx-lab

Small, reproducible math experiments implemented in Python.

- **Audience:** curious engineers, students, and researchers
- **Idea:** each experiment is a self-contained runnable module with a short write-up
- **Goal:** a growing, searchable “lab notebook” of experiments

## Start here

- {doc}`background` - mathematical background for experiments
- {doc}`development` - Makefile workflow, CI, coding conventions
- {doc}`experiment_status` - document the processing status
- {doc}`experiments/experiments_gallery` - experiment gallery (IDs, tags, how to run)
- {doc}`getting-started` - install, setup, and run your first experiment
- {doc}`mathematical-experimentation` - what “experiments” in mathematics mean and how to read this repo
- {doc}`pdf` - download the PDF version of these docs
- {doc}`references` - bibliography and reading list
- {doc}`tags` - central directory of valid tags for experiments

## Run one experiment

```bash
make uv-check
make venv
make install-dev
make run EXP=e001 ARGS="--out out/e001 --seed 1"
````

## Latest

* * **E129** - {doc}`experiments/e129`

---

```{toctree}
:hidden:
:maxdepth: 2

mathematical-experimentation
tags
experiments/experiments_gallery
getting-started
development
background
pdf
experiment_status
references
```
