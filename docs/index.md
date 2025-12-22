# py-mathx-lab

Small, reproducible math experiments implemented in Python.

- **Audience:** curious engineers, students, and researchers
- **Idea:** each experiment is a self-contained runnable module with a short write-up
- **Goal:** a growing, searchable “lab notebook” of experiments

## Start here

- {doc}`getting-started` — install, setup, and run your first experiment
- {doc}`mathematical-experimentation` — what “experiments” in mathematics mean and how to read this repo
- {doc}`experiments` — experiment gallery (IDs, tags, how to run)
- {doc}`development` — Makefile workflow, CI, coding conventions
- {doc}`references` — bibliography and reading list

## Run one experiment

```bash
make uv-check
make venv
make install-dev
make run EXP=e001_taylor_error_landscapes ARGS="--out out/e001 --seed 1"
````

## Latest

* **E001** — {ref}`e001-taylor-error-landscapes`

---

```{toctree}
:hidden:
:maxdepth: 2

getting-started
mathematical-experimentation
experiments
development
references
```
