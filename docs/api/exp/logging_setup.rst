``mathxlab.exp.logging_setup``
==============================

Backwards-compatible logging setup for experiment runs.

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

Backwards-compatible logging setup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from mathxlab.exp.logging_setup import configure_logging
   configure_logging()

Public API
----------

.. list-table::
   :header-rows: 1
   :widths: 22 10 68

   * - Name
     - Kind
     - Summary
   * - ``configure_logging``
     - function
     - Backward-compatible wrapper around :func:`mathxlab.exp.logging.setup_logging`.

Reference
---------

Functions
~~~~~~~~~

.. autofunction:: mathxlab.exp.logging_setup.configure_logging
