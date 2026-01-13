``mathxlab.nt.convolution``
===========================

Dirichlet convolution helpers.

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

Dirichlet convolution on a prefix
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from mathxlab.nt.convolution import ones, identity, dirichlet_convolution
   res = dirichlet_convolution(ones(10), identity(10), n_max=10)
   print(res.values[1:6])

Public API
----------

.. list-table::
   :header-rows: 1
   :widths: 22 10 68

   * - Name
     - Kind
     - Summary
   * - ``ConvolutionResult``
     - class
     - Result of a Dirichlet convolution computed on a prefix.
   * - ``dirichlet_convolution``
     - function
     - Compute the Dirichlet convolution (f*g)(n) for n <= n_max.
   * - ``epsilon``
     - function
     - Return the identity element ε for Dirichlet convolution on [0..n_max].
   * - ``ones``
     - function
     - Return the constant-one function 1(n)=1 for n>=1.
   * - ``identity``
     - function
     - Return the identity arithmetic function id(n)=n.

Reference
---------

Classes
~~~~~~~

.. autoclass:: mathxlab.nt.convolution.ConvolutionResult
   :members:
   :member-order: bysource
   :show-inheritance:

Functions
~~~~~~~~~

.. autofunction:: mathxlab.nt.convolution.dirichlet_convolution

.. autofunction:: mathxlab.nt.convolution.epsilon

.. autofunction:: mathxlab.nt.convolution.ones

.. autofunction:: mathxlab.nt.convolution.identity
