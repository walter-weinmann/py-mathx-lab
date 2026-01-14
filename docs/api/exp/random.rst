``mathxlab.exp.random``
========================

Randomness and seeding utilities for experiment runs.

.. admonition:: Stability
   :class: note

   Status: **Experimental**.

   This project treats the documented names as the *public surface*, but details may still evolve.
   If you need strict API guarantees, add ``__all__ = [...]`` to each module and version releases accordingly.

Design notes
------------

- Keep experiment scripts small: delegate I/O, seeding, and logging here.
- Aim for reproducible outputs (fixed seeds, stable file names).

Examples
--------

Set a deterministic seed
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from mathxlab.exp.random import set_global_seed
   set_global_seed(123)

Public API
----------

.. list-table::
   :header-rows: 1
   :widths: 22 10 68

   * - Name
     - Kind
     - Summary
   * - ``set_global_seed``
     - function
     - Set global seeds for deterministic experiment runs.

Reference
---------

Functions
~~~~~~~~~

.. autofunction:: mathxlab.exp.random.set_global_seed
