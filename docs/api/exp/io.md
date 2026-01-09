# `mathxlab.exp.io`

Standard output paths for an experiment run.

:::{contents} On this page
:local:
:depth: 2
:::

## Quickstart

```python
from mathxlab.exp.io import prepare_out_dir, save_figure, RunPaths
```

:::{list-table} Public API
:header-rows: 1
:widths: 20 10 70

* - Name
  - Kind
  - Summary
* - `JsonDict`
  - data
  - 
* - `RunPaths`
  - class
  - Standard output paths for an experiment run.
* - `prepare_out_dir`
  - function
  - Prepare the output directory structure.
* - `save_figure`
  - function
  - Save a Matplotlib figure to disk.
* - `json_default`
  - function
  - Default JSON encoder for math objects.
* - `write_json`
  - function
  - Write a dictionary to a JSON file with stable formatting.
* - `write_text`
  - function
  - Write text to a file.
:::

## Reference
### Classes
::{autoclass} mathxlab.exp.io.RunPaths:members::member-order: bysource:show-inheritance::::

### Functions
::{autofunction} mathxlab.exp.io.prepare_out_dir:::
::{autofunction} mathxlab.exp.io.save_figure:::
::{autofunction} mathxlab.exp.io.json_default:::
::{autofunction} mathxlab.exp.io.write_json:::
::{autofunction} mathxlab.exp.io.write_text:::

### Data
::{autodata} mathxlab.exp.io.JsonDict:::
