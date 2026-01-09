# Experiment suites (`mathxlab.experiments`)

The `mathxlab.experiments` package contains:

- many **runnable experiment scripts** (`e001...e999...`), documented in the Experiment Gallery
- a few **suite runner modules** intended for reuse (documented here)

```{admonition} Exclusion rule for API docs
:class: note

This API section documents only:

- `mathxlab.experiments.number_theory_suite`
- `mathxlab.experiments.prime_suite`
- `mathxlab.experiments.spiral_suite`

and **excludes** all modules matching:

- `mathxlab.experiments._*.py`
- `mathxlab.experiments.e[0-9][0-9][0-9]*.py`
```

## Suite runners

```{tab-set}

```{tab-item} number_theory_suite
```{automodule} mathxlab.experiments.number_theory_suite
:members:
:show-inheritance:
```
```

```{tab-item} prime_suite
```{automodule} mathxlab.experiments.prime_suite
:members:
:show-inheritance:
```
```

```{tab-item} spiral_suite
```{automodule} mathxlab.experiments.spiral_suite
:members:
:show-inheritance:
```
```

```

## Registry helpers

```{automodule} mathxlab.experiments
:members: ExperimentSpec, iter_experiments, list_experiment_ids, get_experiment_module
:show-inheritance:
```
