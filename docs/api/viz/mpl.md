# `mathxlab.viz.mpl`

Reusable helpers for the `mathxlab` project.

:::{admonition} Stability
:class: note

Status: **Experimental**.

This project treats the documented names as the *public surface*, but details may still evolve.
If you need strict API guarantees, add `__all__ = [...]` to each module and version releases accordingly.
:::

## Design notes
- Keep figure styling consistent across experiments.
- Prefer small helpers over copy/pasted plotting code.

## Examples

### Apply consistent styling to the current figure

```python
from mathxlab.viz.mpl import finalize_figure
finalize_figure("Prime density", "x", "y")
```

## Public API

:::{list-table}
:header-rows: 1
:widths: 22 10 68

* - Name
  - Kind
  - Summary
* - `finalize_figure`
  - function
  - Apply consistent Matplotlib styling to the current figure.
:::
## Reference

### Functions

:::{autofunction} mathxlab.viz.mpl.finalize_figure
:::

