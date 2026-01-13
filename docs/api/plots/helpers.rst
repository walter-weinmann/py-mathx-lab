``mathxlab.plots.helpers``
==========================

Matplotlib styling and layout helpers.

.. admonition:: Stability
   :class: note

   Status: **Experimental**.

   This project treats the documented names as the *public surface*, but details may still evolve.
   If you need strict API guarantees, add ``__all__ = [...]`` to each module and version releases accordingly.

Design notes
------------
- Keep figure styling consistent across experiments.
- Prefer small helpers over copy/pasted plotting code.

Examples
--------

Finalize a Matplotlib figure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import matplotlib.pyplot as plt
   from mathxlab.plots.helpers import finalize_figure
   finalize_figure(plt.figure())

Public API
----------

.. list-table::
   :header-rows: 1
   :widths: 22 10 68

   * - Name
     - Kind
     - Summary
   * - ``apply_axis_style``
     - function
     - Apply common axis styling.
   * - ``configure_mathtext``
     - function
     - Configure Matplotlib MathText to look more LaTeX-like.
   * - ``finalize_figure``
     - function
     - Finalize a Matplotlib figure (layout + MathText config).

Reference
---------

Functions
~~~~~~~~~

.. autofunction:: mathxlab.plots.helpers.apply_axis_style

.. autofunction:: mathxlab.plots.helpers.configure_mathtext

.. autofunction:: mathxlab.plots.helpers.finalize_figure
