# `mathxlab.exp.cli`

Command-line helpers for experiments.

:::{admonition} Stability
:class: note

Status: **Experimental**.

This project treats the documented names as the *public surface*, but details may still evolve.
If you need strict API guarantees, add `__all__ = [...]` to each module and version releases accordingly.
:::

## Design notes
- Keep experiment scripts small: delegate I/O, seeding, and logging here.
- Aim for reproducible outputs (fixed seeds, stable file names).

## Examples

### Parse standard CLI arguments

```python
from mathxlab.exp.cli import parse_experiment_args
args = parse_experiment_args(argv=["--out", "out/e001", "--seed", "1"])
print(args.out_dir)
```

## Public API

:::{list-table}
:header-rows: 1
:widths: 22 10 68

* - Name
  - Kind
  - Summary
* - `ExperimentArgs`
  - class
  - Parsed command-line arguments for an experiment run.
* - `ExperimentArgsWithSize`
  - class
  - Parsed command-line arguments for an experiment run with a `size` parameter.
* - `parse_experiment_args_with_size`
  - function
  - Parse standard experiment CLI arguments plus a `--size` option.
* - `parse_experiment_args`
  - function
  - Parse standard experiment CLI arguments.
:::
## Reference

### Classes

:::{autoclass} mathxlab.exp.cli.ExperimentArgs
:members:
:member-order: bysource
:show-inheritance:
:::

:::{autoclass} mathxlab.exp.cli.ExperimentArgsWithSize
:members:
:member-order: bysource
:show-inheritance:
:::

### Functions

:::{autofunction} mathxlab.exp.cli.parse_experiment_args_with_size
:::

:::{autofunction} mathxlab.exp.cli.parse_experiment_args
:::

