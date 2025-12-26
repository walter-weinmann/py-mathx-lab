# py-mathx-lab

Small, reproducible math experiments implemented in Python.

- **Audience:** curious engineers, students, and researchers
- **Idea:** each experiment is a self-contained runnable module with a short write-up
- **Goal:** a growing, searchable “lab notebook” of experiments

## Start here

- {doc}`mathematical-experimentation` - what “experiments” in mathematics mean and how to read this repo
- {doc}`experiments/experiments_gallery` - experiment gallery (IDs, tags, how to run)
- {doc}`tags` - central directory of valid tags for experiments
- {doc}`background` - mathematical background for experiments
- {doc}`getting-started` - install, setup, and run your first experiment
- {doc}`development` - Makefile workflow, CI, coding conventions
- {doc}`references` - bibliography and reading list
- {doc}`pdf` - download the PDF version of these docs

## Run one experiment

```bash
make uv-check
make venv
make install-dev
make run EXP=e001 ARGS="--out out/e001 --seed 1"
````

## Latest

* * **E006** - {doc}`experiments/e006`

---

```{toctree}
:hidden:
:maxdepth: 2

mathematical-experimentation
tags
experiments/experiments_gallery
background
getting-started
development
references
pdf
```
