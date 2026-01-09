# `mathxlab.utils.plotting`

Shared plotting utilities for py-mathx-lab.

:::{contents} On this page
:local:
:depth: 2
:::

## Quickstart

```python
from mathxlab.utils.plotting import detect_latex_toolchain, configure_matplotlib, LatexToolchainStatus
```

:::{list-table} Public API
:header-rows: 1
:widths: 20 10 70

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
::{autoclass} mathxlab.utils.plotting.LatexToolchainStatus:members::member-order: bysource:show-inheritance::::

### Functions
::{autofunction} mathxlab.utils.plotting.detect_latex_toolchain:::
::{autofunction} mathxlab.utils.plotting.configure_matplotlib:::
::{autofunction} mathxlab.utils.plotting.make_math_label:::
