# `mathxlab.exp.seeding`

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

### Set a deterministic seed

```python
from mathxlab.exp.seeding import set_global_seed
set_global_seed(123)
```

## Public API

:::{list-table}
:header-rows: 1
:widths: 22 10 68

* - Name
  - Kind
  - Summary
* - `set_global_seed`
  - function
  - Set global seeds for deterministic experiment runs.
:::
## Reference

### Functions

:::{autofunction} mathxlab.exp.seeding.set_global_seed
:::

