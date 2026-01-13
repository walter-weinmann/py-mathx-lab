``mathxlab.exp.run_logging``
============================

Utilities for run log file discovery.

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

Infer the run log file path
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from pathlib import Path
   from mathxlab.exp.run_logging import infer_run_log_file
   print(infer_run_log_file(out_dir=Path("out/e001"), experiment_slug="e001"))

Public API
----------

.. list-table::
   :header-rows: 1
   :widths: 22 10 68

   * - Name
     - Kind
     - Summary
   * - ``RunLogDiscovery``
     - class
     - Result of run log discovery.
   * - ``infer_run_log_file``
     - function
     - Infer the run log file for an experiment.

Reference
---------

Classes
~~~~~~~

.. autoclass:: mathxlab.exp.run_logging.RunLogDiscovery
   :members:
   :show-inheritance:

Functions
~~~~~~~~~

.. autofunction:: mathxlab.exp.run_logging.infer_run_log_file
