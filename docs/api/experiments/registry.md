# `mathxlab.experiments`

Experiment package.

:::{admonition} Stability
:class: note

Status: **Experimental**.

This project treats the documented names as the *public surface*, but details may still evolve.
If you need strict API guarantees, add `__all__ = [...]` to each module and version releases accordingly.
:::

## Design notes
- Keep helpers small, explicit, and reproducible.

## Examples

### Resolve experiment metadata

```python
from mathxlab.experiments import get_experiment_module, list_experiment_ids
print(list_experiment_ids()[:5])
print(get_experiment_module("e001"))
```

## Public API

:::{list-table}
:header-rows: 1
:widths: 22 10 68

* - Name
  - Kind
  - Summary
* - `ExperimentSpec`
  - class
  - Lightweight metadata about an experiment.
* - `iter_experiments`
  - function
  - Iterate over known experiments.
* - `list_experiment_ids`
  - function
  - Return all known experiment ids.
* - `get_experiment_module`
  - function
  - Return the module import path for a given experiment id.
:::
## Reference

### Classes

:::{autoclass} mathxlab.experiments.ExperimentSpec
:members:
:member-order: bysource
:show-inheritance:
:::

### Functions

:::{autofunction} mathxlab.experiments.iter_experiments
:::

:::{autofunction} mathxlab.experiments.list_experiment_ids
:::

:::{autofunction} mathxlab.experiments.get_experiment_module
:::

