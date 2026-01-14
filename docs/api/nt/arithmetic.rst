``mathxlab.nt.arithmetic``
===========================

Arithmetic functions and factor-sieve helpers.

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

Factorize using a smallest-prime-factor sieve
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from mathxlab.nt.arithmetic import build_factor_sieve, factorize
   sieve = build_factor_sieve(100)
   print(factorize(84, sieve=sieve))

Public API
----------

.. list-table::
   :header-rows: 1
   :widths: 22 10 68

   * - Name
     - Kind
     - Summary
   * - ``FactorSieve``
     - class
     - Factor-sieve data for fast integer arithmetic.
   * - ``build_factor_sieve``
     - function
     - Build a linear-time smallest-prime-factor sieve.
   * - ``factorize``
     - function
     - Factorize n into prime powers using the SPF sieve.
   * - ``lcm``
     - function
     - Compute the least common multiple.
   * - ``compute_phi``
     - function
     - Compute φ(n) for 0..n_max via dynamic SPF recurrence.
   * - ``compute_mobius``
     - function
     - Compute μ(n) for 0..n_max using SPF recurrence.
   * - ``compute_omega``
     - function
     - Compute ω(n): number of distinct prime factors of n.
   * - ``compute_big_omega``
     - function
     - Compute Ω(n): number of prime factors of n with multiplicity.
   * - ``compute_tau_sigma``
     - function
     - Compute τ(n) and σ(n) for 0..n_max using SPF recurrences.
   * - ``liouville``
     - function
     - Compute Liouville function λ(n) from Ω(n).
   * - ``carmichael_lambda_for_prime_power``
     - function
     - Compute Carmichael's λ(p^e).
   * - ``carmichael_lambda``
     - function
     - Compute Carmichael's lambda function λ(n).
   * - ``jordan_totient``
     - function
     - Compute Jordan's totient function J_k(n).
   * - ``compute_von_mangoldt``
     - function
     - Compute Λ(n) for n=0..n_max.
   * - ``von_mangoldt``
     - function
     - Compute the von Mangoldt function Λ(n).
   * - ``chebyshev_psi``
     - function
     - Compute Chebyshev's ψ(x) for x=0..n_max.

Reference
---------

Classes
~~~~~~~

.. autoclass:: mathxlab.nt.arithmetic.FactorSieve
   :members:
   :member-order: bysource
   :show-inheritance:

Functions
~~~~~~~~~

.. autofunction:: mathxlab.nt.arithmetic.build_factor_sieve

.. autofunction:: mathxlab.nt.arithmetic.factorize

.. autofunction:: mathxlab.nt.arithmetic.lcm

.. autofunction:: mathxlab.nt.arithmetic.compute_phi

.. autofunction:: mathxlab.nt.arithmetic.compute_mobius

.. autofunction:: mathxlab.nt.arithmetic.compute_omega

.. autofunction:: mathxlab.nt.arithmetic.compute_big_omega

.. autofunction:: mathxlab.nt.arithmetic.compute_tau_sigma

.. autofunction:: mathxlab.nt.arithmetic.liouville

.. autofunction:: mathxlab.nt.arithmetic.carmichael_lambda_for_prime_power

.. autofunction:: mathxlab.nt.arithmetic.carmichael_lambda

.. autofunction:: mathxlab.nt.arithmetic.jordan_totient

.. autofunction:: mathxlab.nt.arithmetic.compute_von_mangoldt

.. autofunction:: mathxlab.nt.arithmetic.von_mangoldt

.. autofunction:: mathxlab.nt.arithmetic.chebyshev_psi
