# `mathxlab.exp.reporting`

Paths to standard artifacts produced by an experiment run.

:::{contents} On this page
:local:
:depth: 2
:::

## Quickstart

```python
from mathxlab.exp.reporting import prepare_out_dir, save_figure, RunArtifacts
```

:::{list-table} Public API
:header-rows: 1
:widths: 20 10 70

* - Name
  - Kind
  - Summary
* - `JsonPayload`
  - data
  - 
* - `RunArtifacts`
  - class
  - Paths to standard artifacts produced by an experiment run.
* - `prepare_out_dir`
  - function
  - Create the output directory and return standard artifact paths.
* - `save_figure`
  - function
  - Save the current Matplotlib figure to disk.
* - `write_json`
  - function
  - Write a JSON file with stable formatting.
:::

## Reference
### Classes
::{autoclass} mathxlab.exp.reporting.RunArtifacts:members::member-order: bysource:show-inheritance::::

### Functions
::{autofunction} mathxlab.exp.reporting.prepare_out_dir:::
::{autofunction} mathxlab.exp.reporting.save_figure:::
::{autofunction} mathxlab.exp.reporting.write_json:::

### Data
::{autodata} mathxlab.exp.reporting.JsonPayload:::
