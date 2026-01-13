``mathxlab.nt.zeta``
=====================

Riemann zeta function and related numerical helpers.

.. admonition:: Stability
   :class: note

   Status: **Experimental**.

   This project treats the documented names as the *public surface*, but details may still evolve.
   If you need strict API guarantees, add ``__all__ = [...]`` to each module and version releases accordingly.

Design notes
------------
- Functions are designed for experiment-scale inputs (not cryptographic workloads).
- Prefer explicit parameters (e.g., ``n_max``) for reproducibility.

Examples
--------

Approximate ζ(2) via a partial series
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from mathxlab.nt.zeta import zeta_series_partial
   print(zeta_series_partial(2, 10_000))

Public API
----------

.. list-table::
   :header-rows: 1
   :widths: 22 10 68

   * - Name
     - Kind
     - Summary
   * - ``ZetaEvalSettings``
     - class
     - Settings for zeta-related numerical evaluations.
   * - ``mp_workdps``
     - function
     - Temporarily set the mpmath precision (decimal digits).
   * - ``zeta_series_partial``
     - function
     - Compute the partial Dirichlet series for the Riemann zeta function.
   * - ``eta_series_partial``
     - function
     - Compute the partial Dirichlet eta series.
   * - ``zeta_via_eta``
     - function
     - Recover zeta(s) from eta(s) via the identity.
   * - ``euler_product_partial``
     - function
     - Compute a partial Euler product approximation of zeta(s).
   * - ``chi_factor``
     - function
     - Compute the factor chi(s) in the functional equation of zeta.
   * - ``hardy_Z``
     - function
     - Compute Hardy's Z-function at height t.
   * - ``riemann_von_mangoldt_count``
     - function
     - Return the Riemann--von Mangoldt main term for N(T).

Reference
---------

Classes
~~~~~~~

.. autoclass:: mathxlab.nt.zeta.ZetaEvalSettings
   :members:
   :member-order: bysource
   :show-inheritance:

Functions
~~~~~~~~~

.. autofunction:: mathxlab.nt.zeta.mp_workdps

.. autofunction:: mathxlab.nt.zeta.zeta_series_partial

.. autofunction:: mathxlab.nt.zeta.eta_series_partial

.. autofunction:: mathxlab.nt.zeta.zeta_via_eta

.. autofunction:: mathxlab.nt.zeta.euler_product_partial

.. autofunction:: mathxlab.nt.zeta.chi_factor

.. autofunction:: mathxlab.nt.zeta.hardy_Z

.. autofunction:: mathxlab.nt.zeta.riemann_von_mangoldt_count
