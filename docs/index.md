# py-mathx-lab

Welcome to **py-mathx-lab** — a repository for small, reproducible math experiments
implemented in Python.

```{toctree}
:maxdepth: 2
:caption: Contents

getting-started
experiments
development
references

---

## 3) `docs/getting-started.md`

Create `docs/getting-started.md`:

```markdown
# Getting started

## Prerequisites

- Python **3.13**
- `uv`
- GNU `make`

## Setup

```bash
make uv-check
make venv
make install-dev
make install-docs
