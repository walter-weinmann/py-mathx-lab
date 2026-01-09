# `mathxlab.exp.cli`

Command-line helpers for experiments.

:::{contents} On this page
:local:
:depth: 2
:::

## Quickstart

```python
from mathxlab.exp.cli import parse_experiment_args_with_size, parse_experiment_args, ExperimentArgs
```

:::{list-table} Public API
:header-rows: 1
:widths: 20 10 70

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
::{autoclass} mathxlab.exp.cli.ExperimentArgs:members::member-order: bysource:show-inheritance::::
::{autoclass} mathxlab.exp.cli.ExperimentArgsWithSize:members::member-order: bysource:show-inheritance::::

### Functions
::{autofunction} mathxlab.exp.cli.parse_experiment_args_with_size:::
::{autofunction} mathxlab.exp.cli.parse_experiment_args:::
