# Contributing to py-mathx-lab

Thanks for your interest in contributing. This repository is maintained by a single maintainer and accepts contributions under a **strict, review-first workflow** to keep the project coherent and reproducible.

Please read this document before opening an issue or pull request.

---

## Table of contents

- [Ground rules](#ground-rules)
- [Ways to contribute](#ways-to-contribute)
- [Before you start](#before-you-start)
- [Development setup](#development-setup)
- [Project workflow (Makefile targets)](#project-workflow-makefile-targets)
- [Coding standards](#coding-standards)
- [Documentation standards](#documentation-standards)
- [Bibliography and citations](#bibliography-and-citations)
- [Experiments: adding or changing experiments](#experiments-adding-or-changing-experiments)
- [Dependencies and lockfiles](#dependencies-and-lockfiles)
- [Git workflow and pull requests](#git-workflow-and-pull-requests)
- [Review and merge policy](#review-and-merge-policy)
- [Labels (triage)](#labels-triage)
- [Security](#security)
- [License](#license)

---

## Ground rules

- **Be constructive and precise.** If something is unclear, propose wording or a concrete change.
- **Keep changes small.** Prefer narrowly-scoped PRs that are easy to review and easy to revert.
- **Reproducibility first.** If a change affects results, document it and keep outputs deterministic where possible.
- **No direct pushes to `main`.** All changes go through pull requests.

---

## Ways to contribute

You can contribute by:

- fixing bugs (especially reproducibility and portability issues)
- improving documentation (clarity, structure, examples)
- adding experiments (new experiment modules + write-up)
- adding tests (unit tests, regression tests, reproducibility checks)
- improving CI/workflows (while keeping them minimal and stable)

If you're unsure whether a change fits the scope, open an issue first with:
- the goal
- expected impact
- a small proposal

---

## Before you start

### Requirements

- Python **3.13**
- `uv` on PATH
- GNU `make`

Supported platforms:
- Windows
- Linux (native)
- Linux (WSL)
- macOS (best-effort)

### Line endings

This project aims to avoid CRLF/LF churn across Windows, WSL, and CI. Please keep line endings consistent (prefer LF unless a file type requires CRLF, e.g. `.bat/.cmd`).

---

## Development setup

From the repository root:

```bash
make uv-check
make python-check
make venv
make install-dev
```

For documentation work:

```bash
make install-docs
```

---

## Project workflow (Makefile targets)

Use Make targets instead of running tools directly.

Show available targets:

```bash
make help
```

Typical local checks:

```bash
make dev
```

Build documentation:

```bash
make docs
```

Run an experiment:

```bash
make run EXP=e001_taylor_error_landscapes ARGS="--out out/e001 --seed 1"
```

Clean caches and build artifacts:

```bash
make clean
```

---

## Coding standards

### Style

* Formatting: **Ruff formatter**
* Linting: **Ruff**
* Typing: **mypy**
* Tests: **pytest**

Run locally:

```bash
make dev
```

### General rules

* Prefer readable, explicit code over clever code.
* Add types for public functions and non-trivial internal functions.
* Keep functions small and testable.
* Use deterministic behavior by default (e.g., configurable `--seed`).

### Docstrings

* Use **Google-style docstrings** for public functions/classes.
* Explain *why* something exists, not just *what* it does.

---

## Documentation standards

Docs are built with **Sphinx + MyST**.

* Documentation changes should build locally:

```bash
make docs
```

* Prefer short sections, clear commands, and stable internal links.
* When adding an experiment, update the documentation entry in `docs/experiments.md`
  (and optionally add a dedicated page under `docs/experiments/`).

---

## Bibliography and citations

Bibliography entries live in:

* `docs/refs.bib`

A small style guide is included at the top of that file. Please follow it.

Key rules:

* Stable BibTeX keys (do not rename once used)
* Prefer DOI, otherwise URL + `urldate` (YYYY-MM-DD)
* Protect capitalization with braces (`{Python}`, `{NumPy}`, `{LaTeX}`)
* Use `--` for page ranges

If you cite references on an experiment page, add citations in the text like:

* `... as described in [knuth1997taocp1].`

---

## Experiments: adding or changing experiments

### File naming

* New experiments should use the naming scheme:

  * `experiments/e###_<short_name>.py`
* Keep experiment IDs stable (do not reuse IDs).

### CLI behavior (recommended)

Experiments should be runnable as a module:

```bash
uv run python -m experiments.e###_<short_name> --out out/e### --seed 1
```

Recommended arguments:

* `--out` output directory (required)
* `--seed` for deterministic behavior (if randomness involved)

### Output expectations

Write outputs into the `--out` folder only, for example:

* `report.md` (short narrative)
* `figures/*.png`
* `params.json` (inputs and configuration)
* `manifest.json` (stable snapshot: environment, versions, summary)

### Documentation update

Every experiment PR must include:

* an entry in `docs/experiments.md` (index entry: goal + how to run)
* optionally a dedicated page under `docs/experiments/e###.md` for longer write-ups

---

## Dependencies and lockfiles

### Adding dependencies

* Add runtime dependencies to `pyproject.toml` under `[project.dependencies]`.
* Add development tools to `[project.optional-dependencies].dev`.
* Add documentation dependencies to `[project.optional-dependencies].docs`.

### Lockfile policy

If the repository uses `uv.lock`, keep it consistent with `pyproject.toml`.

After dependency changes, run:

```bash
uv sync
```

and include any resulting lockfile updates in your PR.

---

## Git workflow and pull requests

### Branching model

* `main` is protected.
* Create feature branches from `main`:

```bash
git checkout -b <type>/<short-topic>
```

Recommended branch prefixes:

* `fix/...`
* `docs/...`
* `exp/...`
* `ci/...`
* `chore/...`

### Commit messages

Use clear, descriptive messages. Examples:

* `docs: clarify Sphinx build steps`
* `exp: add E002 prime gaps exploration`
* `fix: stabilize seed handling in E001`

### DCO / sign-off

If the repository uses Developer Certificate of Origin (DCO), sign your commits:

```bash
git commit -s -m "..."
```

(If you use the GitHub web UI, ensure you sign off where applicable.)

---

## Review and merge policy

This is a **solo-maintainer** repository.

* All PRs are reviewed by the maintainer.
* CI must pass before merge.
* The maintainer may request changes, restructure commits, or ask for smaller PRs.
* Preferred merge strategy: **Squash merge** (keeps `main` clean and linear).
* The maintainer may close PRs that are out of scope or too hard to maintain.

### PR checklist (required)

Your PR should:

* [ ] state the purpose and scope (1–5 sentences)
* [ ] include reproducible steps (commands, expected output) if relevant
* [ ] pass `make dev`
* [ ] build docs (`make docs`) if docs changed
* [ ] update `docs/experiments.md` if you add/change an experiment
* [ ] include tests when fixing a bug or adding non-trivial logic

---

## Labels (triage)

This repository uses a small label set to keep triage simple and consistent.

### Primary labels (one is usually enough)

- **bug**  
  Something is broken or incorrect (runtime errors, wrong results, failing tests, regressions).

- **feature**  
  New functionality or an improvement proposal that is not a bug.

- **docs**  
  Documentation changes or documentation issues (Sphinx/MyST, wording, structure, broken links).

- **experiment-request**  
  Proposal for a new experiment, or changes that primarily extend the experiments catalogue.

- **question**  
  Clarification requests that are not actionable work items yet.

### Triage/housekeeping labels

- **duplicate**  
  Already reported elsewhere (link to the original issue/PR).

- **invalid**  
  Not an issue for this project (wrong repo, misunderstanding, insufficient info even after request).

- **wontfix**  
  The issue is acknowledged but will not be addressed (out of scope, too costly, or not aligned with goals).

### Cross-cutting labels (add in addition to a primary label when applicable)

- **ci**  
  GitHub Actions, workflows, caches, Pages deployment, or CI-only failures.

- **tooling**  
  Local developer workflow: uv, Makefile targets, packaging, test/lint/type tooling.

- **reproducibility**  
  Anything that affects determinism, seeds, outputs, or “same results on CI”.

- **breaking-change**  
  Changes that affect users’ workflows, CLI/API behavior, output formats, or documented conventions.
  (This label is rare and should be used conservatively.)

---

## Security

Please do not open public issues for sensitive security problems.

Instead, contact the maintainer privately (GitHub Security Advisories if enabled, or via a private channel stated in the repo).

---

## License

By contributing, you agree that your contributions will be licensed under the repository’s license.
