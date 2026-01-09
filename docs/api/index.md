# API Reference

This section documents the **reusable library code** in `mathxlab` (the parts you would import and build upon).

It intentionally excludes:

- `mathxlab/tools/**` (repo tooling scripts)
- `mathxlab/experiments/_*.py` (private helper modules)
- `mathxlab/experiments/e001*.py` … `mathxlab/experiments/e999*.py` (runnable experiment scripts)

The runnable experiments are documented in the **Experiment Gallery**; the API reference focuses on stable, reusable modules.

```{grid} 2
:gutter: 2

```{grid-item-card} Experiment framework
:link: exp
:link-type: doc

`mathxlab.exp` — CLI helpers, seeding, logging, and report writing.
```

```{grid-item-card} Experiment suites
:link: experiments
:link-type: doc

`mathxlab.experiments` — suite runners and registry helpers (excluding `e###` scripts).
```

```{grid-item-card} Number theory
:link: nt
:link-type: doc

`mathxlab.nt` — arithmetic, Dirichlet machinery, and zeta/L-related utilities.
```

```{grid-item-card} Numerics
:link: num
:link-type: doc

`mathxlab.num` — numerical series helpers.
```

```{grid-item-card} Plotting
:link: plots
:link-type: doc

`mathxlab.plots` — plotting helpers used across experiments and reports.
```

```{grid-item-card} Utilities
:link: utils
:link-type: doc

`mathxlab.utils` — shared utilities.
```

```{grid-item-card} Visualization backends
:link: viz
:link-type: doc

`mathxlab.viz` — visualization backend wrappers (Matplotlib).
```

```

```{toctree}
:hidden:
:maxdepth: 2

exp
experiments
nt
num
plots
utils
viz
```
