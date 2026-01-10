# `mathxlab.utils.plotting`

Shared plotting utilities for py-mathx-lab.

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

### Configure Matplotlib and build math labels

```python
from mathxlab.utils.plotting import configure_matplotlib, make_math_label
configure_matplotlib()
print(make_math_label(r"\pi(x) \sim x/\log x"))
```

## Public API

:::{list-table}
:header-rows: 1
:widths: 22 10 68

* - Name
  - Kind
  - Summary
* - `LatexToolchainStatus`
  - class
  - Represents the availability of an external LaTeX toolchain.
* - `detect_latex_toolchain`
  - function
  - Detect whether an external LaTeX toolchain is available.
* - `configure_matplotlib`
  - function
  - Configure Matplotlib defaults for experiments.
* - `make_math_label`
  - function
  - Wrap an expression in `$...$` for math rendering.
:::
## Reference

### Classes

:::{autoclass} mathxlab.utils.plotting.LatexToolchainStatus
:members:
:member-order: bysource
:show-inheritance:
:::

### Functions

:::{autofunction} mathxlab.utils.plotting.detect_latex_toolchain
:::

:::{autofunction} mathxlab.utils.plotting.configure_matplotlib
:::

:::{autofunction} mathxlab.utils.plotting.make_math_label
:::

