---
orphan: true
---

# py-mathx-lab

<!-- This is the PDF / LaTeX root document. It is intentionally not linked from the HTML navigation. -->

```{toctree}
:caption: Guide
:maxdepth: 2

mathematical-experimentation
getting-started
development
```

```{toctree}
:caption: Experiments
:maxdepth: 2

tags
experiments/experiments_gallery
experiment_status
```

```{toctree}
:caption: Background
:maxdepth: 2

background
```

## API Reference and Bibliography 

```{bibliography} refs.bib
:all:
:style: plain
```

The full API reference with auto-generated documentation is available in the **HTML version** of this documentation.

For the PDF, we provide a brief overview of the main modules:

- **mathxlab.exp** — CLI helpers, seeding, logging, and report writing for experiments.
- **mathxlab.experiments** — Stable registry for enumerating and running experiments.
- **mathxlab.nt** — Arithmetic functions, Dirichlet machinery, and zeta/L-related utilities.
- **mathxlab.num** — Numerical series helpers.
- **mathxlab.plots** — Plotting helpers used across experiments and reports.
- **mathxlab.utils** — Shared utilities.
- **mathxlab.viz** — Visualization backend wrappers (Matplotlib).
