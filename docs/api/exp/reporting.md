# `mathxlab.exp.reporting`

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

### Prepare artifacts for a run

```python
from pathlib import Path
from mathxlab.exp.reporting import prepare_out_dir
artifacts = prepare_out_dir(out_dir=Path("out/e001"))
```

## Public API

:::{list-table}
:header-rows: 1
:widths: 22 10 68

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

:::{autoclass} mathxlab.exp.reporting.RunArtifacts
:members:
:member-order: bysource
:show-inheritance:
:::

### Functions

:::{autofunction} mathxlab.exp.reporting.prepare_out_dir
:::

:::{autofunction} mathxlab.exp.reporting.save_figure
:::

:::{autofunction} mathxlab.exp.reporting.write_json
:::

### Data

:::{autodata} mathxlab.exp.reporting.JsonPayload
:::

