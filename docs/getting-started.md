# Getting started

This project uses an **uv-only** workflow and a small Makefile wrapper to run everything consistently.

## Prerequisites

You need:

- **Python 3.13**
- **uv** on your PATH
- **GNU Make**

### Windows notes

- Install GNU Make (e.g., via Chocolatey).
- You can run everything from `cmd.exe`, PowerShell, or from WSL.

## Verify tools

From the repository root:

```bash
make uv-check
make python-check
make python-info
````

## First-time setup

Create a virtual environment and install dependencies:

```bash
make venv
make install-dev
make install-docs
```

## Run the full development chain

```bash
make final
```

`make final` runs:

* formatting (Ruff)
* linting (Ruff)
* type checking (mypy)
* tests (pytest)
* documentation (sphinx)

Documentation can be built separately via:

```bash
make docs
```

## Run an experiment

Example (E001):

```bash
make run EXP=e001 ARGS="--seed 1"
```

See the experiment overview here: {doc}`experiments/experiments_gallery`.

## Build documentation locally

```bash
make docs
```

Output:

* `docs/_build/html`

## Troubleshooting

### `error: Failed to spawn: sphinx-build`

Sphinx is not installed in the uv environment.

Fix:

```bash
make install-docs
make docs
```

### `make python-check` fails

The repo enforces Python **3.13**. Install Python 3.13, then recreate the environment:

```bash
make clean-venv
make venv
make install-dev
make install-docs
```
