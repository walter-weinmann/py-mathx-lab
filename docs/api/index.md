# API Reference

This section documents the **reusable library code** in `mathxlab` (the parts you would import and build upon).
It intentionally keeps the **runnable experiment scripts** out of the API surface.

```{grid} 2
:gutter: 2

```{grid-item-card} Experiment framework
:link: exp
:link-type: doc

CLI helpers, deterministic seeding, logging, reporting, and experiment I/O.
```

```{grid-item-card} Number theory
:link: nt
:link-type: doc

Reusable number-theory building blocks (arithmetic, Dirichlet, zeta, …).
```

```{grid-item-card} Numerics
:link: num
:link-type: doc

Numerical series helpers and small numerical utilities.
```

```{grid-item-card} Plotting
:link: plots
:link-type: doc

Plotting helpers used by experiments and reports.
```

```{grid-item-card} Utilities
:link: utils
:link-type: doc

Shared utility modules.
```

```{grid-item-card} Visualization backends
:link: viz
:link-type: doc

Visualization backend wrappers (Matplotlib).
```

```{grid-item-card} Experiment registry & suites
:link: experiments
:link-type: doc

Registry helpers and suite-style runners (excludes e001–e999 scripts and private `_*.py` helpers).
```

```

```{toctree}
:hidden:
:maxdepth: 2

exp
nt
num
plots
utils
viz
experiments
```
