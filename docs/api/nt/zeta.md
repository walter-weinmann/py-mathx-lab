# `mathxlab.nt.zeta`

Settings for zeta-related numerical evaluations.

:::{contents} On this page
:local:
:depth: 2
:::

## Quickstart

```python
from mathxlab.nt.zeta import mp_workdps, zeta_series_partial, ZetaEvalSettings
```

:::{list-table} Public API
:header-rows: 1
:widths: 20 10 70

* - Name
  - Kind
  - Summary
* - `ZetaEvalSettings`
  - class
  - Settings for zeta-related numerical evaluations.
* - `mp_workdps`
  - function
  - Temporarily set the mpmath precision (decimal digits).
* - `zeta_series_partial`
  - function
  - Compute the partial Dirichlet series for the Riemann zeta function.
* - `eta_series_partial`
  - function
  - Compute the partial Dirichlet eta series.
* - `zeta_via_eta`
  - function
  - Recover zeta(s) from eta(s) via the identity.
* - `euler_product_partial`
  - function
  - Compute a partial Euler product approximation of zeta(s).
* - `chi_factor`
  - function
  - Compute the factor chi(s) in the functional equation of zeta.
* - `hardy_Z`
  - function
  - Compute Hardy's Z-function at height t.
* - `riemann_von_mangoldt_count`
  - function
  - Return the Riemann--von Mangoldt main term for N(T).
:::

## Reference
### Classes
::{autoclass} mathxlab.nt.zeta.ZetaEvalSettings:members::member-order: bysource:show-inheritance::::

### Functions
::{autofunction} mathxlab.nt.zeta.mp_workdps:::
::{autofunction} mathxlab.nt.zeta.zeta_series_partial:::
::{autofunction} mathxlab.nt.zeta.eta_series_partial:::
::{autofunction} mathxlab.nt.zeta.zeta_via_eta:::
::{autofunction} mathxlab.nt.zeta.euler_product_partial:::
::{autofunction} mathxlab.nt.zeta.chi_factor:::
::{autofunction} mathxlab.nt.zeta.hardy_Z:::
::{autofunction} mathxlab.nt.zeta.riemann_von_mangoldt_count:::
