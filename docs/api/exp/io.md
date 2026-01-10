# `mathxlab.exp.io`

Reusable helpers for the `mathxlab` project.

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

### Create standard output paths

```python
from pathlib import Path
from mathxlab.exp.io import prepare_out_dir
paths = prepare_out_dir(out_dir=Path("out/e001"))
```

## Public API

:::{list-table}
:header-rows: 1
:widths: 22 10 68

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

:::{autoclass} mathxlab.exp.io.RunPaths
:members:
:member-order: bysource
:show-inheritance:
:::

### Functions

:::{autofunction} mathxlab.exp.io.prepare_out_dir
:::

:::{autofunction} mathxlab.exp.io.save_figure
:::

:::{autofunction} mathxlab.exp.io.json_default
:::

:::{autofunction} mathxlab.exp.io.write_json
:::

:::{autofunction} mathxlab.exp.io.write_text
:::

### Data

:::{autodata} mathxlab.exp.io.JsonDict
:::

