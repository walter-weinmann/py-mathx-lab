# `mathxlab.num.series`

Reusable helpers for the `mathxlab` project.

:::{admonition} Stability
:class: note

Status: **Experimental**.

This project treats the documented names as the *public surface*, but details may still evolve.
If you need strict API guarantees, add `__all__ = [...]` to each module and version releases accordingly.
:::

## Design notes
- Keep helpers small, explicit, and reproducible.

## Examples

### Taylor polynomial approximation of sin(x)

```python
import numpy as np
from mathxlab.num.series import taylor_sin
print(taylor_sin(np.array([0.0, 1.0]), x0=0.0, degree=7))
```

## Public API

:::{list-table}
:header-rows: 1
:widths: 22 10 68

* - Name
  - Kind
  - Summary
* - `taylor_sin`
  - function
  - Compute the Taylor polynomial approximation of sin(x) around x0.
:::
## Reference

### Functions

:::{autofunction} mathxlab.num.series.taylor_sin
:::

