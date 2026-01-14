``mathxlab.experiments.prime_suite``
====================================

Prime Numbers experiment suite (E014–E046).

.. contents:: On this page
   :local:
   :depth: 2

Quickstart
----------


.. code-block:: python

   from mathxlab.experiments.prime_suite import run_e014, run_e015, CommonParams



.. list-table:: Public API
   :header-rows: 1
   :widths: 20 10 70



   * - Name
     - Kind
     - Summary
   * - ``CommonParams``
     - class
     - Shared parameters.
   * - ``ParamsE014``
     - class
     - Parameters for E014.
   * - ``run_e014``
     - function
     - E014: Primorial ± 1: "Euclid numbers are prime" fails quickly.
   * - ``ParamsE015``
     - class
     - Parameters for E015.
   * - ``run_e015``
     - function
     - E015: Wilson's theorem is true, but the naive 'test' is unusable at scale.
   * - ``ParamsE016``
     - class
     - Parameters for E016.
   * - ``run_e016``
     - function
     - E016: Trial division collapses with size; MR stays fast (counterexample to 'simple is fine').
   * - ``ParamsE017``
     - class
     - Parameters for E017.
   * - ``run_e017``
     - function
     - E017: Full sieve memory vs segmented sieve (counterexample to 'O(N) is fine').
   * - ``ParamsE018``
     - class
     - Parameters for E018.
   * - ``run_e018``
     - function
     - E018: Strong pseudoprimes: too few MR bases yields false positives (counterexample).
   * - ``ParamsE019``
     - class
     - Parameters for E019.
   * - ``run_e019``
     - function
     - E019: Prime density: pi(x) vs x/log x and error curve.
   * - ``ParamsE020``
     - class
     - Parameters for E020.
   * - ``run_e020``
     - function
     - E020: li(x) is often a better approximation than x/log x (visual counterexample).
   * - ``ParamsE021``
     - class
     - Parameters for E021.
   * - ``run_e021``
     - function
     - E021: Explicit inequality sanity checks (conditions matter).
   * - ``ParamsE022``
     - class
     - Parameters for E022.
   * - ``run_e022``
     - function
     - E022: Prime race: pi(x;4,1) vs pi(x;4,3).
   * - ``ParamsE023``
     - class
     - Parameters for E023.
   * - ``run_e023``
     - function
     - E023: Distribution of primes across residue classes mod q (finite-range bias).
   * - ``ParamsE024``
     - class
     - Parameters for E024.
   * - ``run_e024``
     - function
     - E024: Ulam spiral: primes in a spiral show diagonal structure.
   * - ``ParamsE025``
     - class
     - Parameters for E025.
   * - ``run_e025``
     - function
     - E025: Prime gaps are not monotone (counterexample to naive 'gaps always grow').
   * - ``ParamsE026``
     - class
     - Parameters for E026.
   * - ``run_e026``
     - function
     - E026: Gap normalization: g/log p helps compare scales.
   * - ``ParamsE027``
     - class
     - Parameters for E027.
   * - ``run_e027``
     - function
     - E027: Record prime gaps vs log^2 heuristic (Cramér-style scaling).
   * - ``ParamsE028``
     - class
     - Parameters for E028.
   * - ``run_e028``
     - function
     - E028: Jumping champions: most frequent gap in sliding windows.
   * - ``ParamsE029``
     - class
     - Parameters for E029.
   * - ``run_e029``
     - function
     - E029: Twin prime counts vs simple Hardy–Littlewood-style heuristic.
   * - ``ParamsE030``
     - class
     - Parameters for E030.
   * - ``run_e030``
     - function
     - E030: Cousin and sexy primes: compare counts of prime pairs.
   * - ``ParamsE031``
     - class
     - Parameters for E031.
   * - ``run_e031``
     - function
     - E031: Prime k-tuple admissibility: mod obstructions are real counterexamples.
   * - ``ParamsE032``
     - class
     - Parameters for E032.
   * - ``run_e032``
     - function
     - E032: Count small prime constellations (triplets/quadruplets) up to N.
   * - ``ParamsE033``
     - class
     - Parameters for E033.
   * - ``run_e033``
     - function
     - E033: Small gaps exist often, but that doesn't make them twins (data-only counterexample).
   * - ``ParamsE034``
     - class
     - Parameters for E034.
   * - ``run_e034``
     - function
     - E034: Twin prime counts vary strongly across windows (variance counterexample).
   * - ``ParamsE035``
     - class
     - Parameters for E035.
   * - ``run_e035``
     - function
     - E035: Primes in arithmetic progressions: empirical counts in reduced residues.
   * - ``ParamsE036``
     - class
     - Parameters for E036.
   * - ``run_e036``
     - function
     - E036: Small arithmetic progressions of primes (3-term and 4-term) in ranges.
   * - ``ParamsE037``
     - class
     - Parameters for E037.
   * - ``run_e037``
     - function
     - E037: Prime-free intervals exist: n!+2,...,n!+n are all composite.
   * - ``ParamsE038``
     - class
     - Parameters for E038.
   * - ``run_e038``
     - function
     - E038: Bertrand's postulate: for n>1 there is a prime in (n, 2n).
   * - ``ParamsE039``
     - class
     - Parameters for E039.
   * - ``run_e039``
     - function
     - E039: Sophie Germain primes and safe primes (counts in range).
   * - ``ParamsE040``
     - class
     - Parameters for E040.
   * - ``run_e040``
     - function
     - E040: Palindromic primes: even-length palindromes are divisible by 11 (counterexample).
   * - ``ParamsE041``
     - class
     - Parameters for E041.
   * - ``run_e041``
     - function
     - E041: Fermat numbers: not all are prime (counterexample at F5).
   * - ``ParamsE042``
     - class
     - Parameters for E042.
   * - ``run_e042``
     - function
     - E042: Repunit primes: many k are forced composite (counterexamples).
   * - ``ParamsE043``
     - class
     - Parameters for E043.
   * - ``run_e043``
     - function
     - E043: Pollard rho runtime varies wildly (counterexample to 'same size => same effort').
   * - ``ParamsE044``
     - class
     - Parameters for E044.
   * - ``run_e044``
     - function
     - E044: Solovay–Strassen vs Miller–Rabin (liar rates on random composites).
   * - ``ParamsE045``
     - class
     - Parameters for E045.
   * - ``run_e045``
     - function
     - E045: Deterministic 64-bit MR: 12 bases vs small subsets (counterexample).
   * - ``ParamsE046``
     - class
     - Parameters for E046.
   * - ``run_e124``
     - class
     - Parameters for E124.
   * - ``run_e124``
     - function
     - E124: Klauber triangle: prime patterns on a triangular array.
   * - ``ParamsE125``
     - class
     - Parameters for E125.
   * - ``run_e125``
     - function
     - E125: Sacks spiral: primes on an Archimedean spiral (one square per turn).
   * - ``ParamsE126``
     - class
     - Parameters for E126.
   * - ``run_e126``
     - function
     - E126: Hexagonal number spiral: primes on a hexagonal lattice spiral.

Reference
---------

Classes
~~~~~~~



.. autoclass::  mathxlab.experiments.prime_suite.CommonParams
   :members:
   :member-order: bysource
   :show-inheritance:



.. autoclass:: mathxlab.experiments.prime_suite.ParamsE014
   :members:
   :member-order: bysource
   :show-inheritance:





.. autoclass:: mathxlab.experiments.prime_suite.ParamsE015
   :members:
   :member-order: bysource
   :show-inheritance:





.. autoclass:: mathxlab.experiments.prime_suite.ParamsE016
   :members:
   :member-order: bysource
   :show-inheritance:





.. autoclass:: mathxlab.experiments.prime_suite.ParamsE017
   :members:
   :member-order: bysource
   :show-inheritance:





.. autoclass:: mathxlab.experiments.prime_suite.ParamsE018
   :members:
   :member-order: bysource
   :show-inheritance:





.. autoclass:: mathxlab.experiments.prime_suite.ParamsE019
   :members:
   :member-order: bysource
   :show-inheritance:





.. autoclass:: mathxlab.experiments.prime_suite.ParamsE020
   :members:
   :member-order: bysource
   :show-inheritance:





.. autoclass:: mathxlab.experiments.prime_suite.ParamsE021
   :members:
   :member-order: bysource
   :show-inheritance:





.. autoclass:: mathxlab.experiments.prime_suite.ParamsE022
   :members:
   :member-order: bysource
   :show-inheritance:





.. autoclass:: mathxlab.experiments.prime_suite.ParamsE023
   :members:
   :member-order: bysource
   :show-inheritance:





.. autoclass:: mathxlab.experiments.prime_suite.ParamsE024
   :members:
   :member-order: bysource
   :show-inheritance:





.. autoclass:: mathxlab.experiments.prime_suite.ParamsE025
   :members:
   :member-order: bysource
   :show-inheritance:





.. autoclass:: mathxlab.experiments.prime_suite.ParamsE026
   :members:
   :member-order: bysource
   :show-inheritance:





.. autoclass:: mathxlab.experiments.prime_suite.ParamsE027
   :members:
   :member-order: bysource
   :show-inheritance:





.. autoclass:: mathxlab.experiments.prime_suite.ParamsE028
   :members:
   :member-order: bysource
   :show-inheritance:





.. autoclass:: mathxlab.experiments.prime_suite.ParamsE029
   :members:
   :member-order: bysource
   :show-inheritance:





.. autoclass:: mathxlab.experiments.prime_suite.ParamsE030
   :members:
   :member-order: bysource
   :show-inheritance:





.. autoclass:: mathxlab.experiments.prime_suite.ParamsE031
   :members:
   :member-order: bysource
   :show-inheritance:





.. autoclass:: mathxlab.experiments.prime_suite.ParamsE032
   :members:
   :member-order: bysource
   :show-inheritance:





.. autoclass:: mathxlab.experiments.prime_suite.ParamsE033
   :members:
   :member-order: bysource
   :show-inheritance:





.. autoclass:: mathxlab.experiments.prime_suite.ParamsE034
   :members:
   :member-order: bysource
   :show-inheritance:





.. autoclass:: mathxlab.experiments.prime_suite.ParamsE035
   :members:
   :member-order: bysource
   :show-inheritance:





.. autoclass:: mathxlab.experiments.prime_suite.ParamsE036
   :members:
   :member-order: bysource
   :show-inheritance:





.. autoclass:: mathxlab.experiments.prime_suite.ParamsE037
   :members:
   :member-order: bysource
   :show-inheritance:





.. autoclass:: mathxlab.experiments.prime_suite.ParamsE038
   :members:
   :member-order: bysource
   :show-inheritance:





.. autoclass:: mathxlab.experiments.prime_suite.ParamsE039
   :members:
   :member-order: bysource
   :show-inheritance:





.. autoclass:: mathxlab.experiments.prime_suite.ParamsE040
   :members:
   :member-order: bysource
   :show-inheritance:





.. autoclass:: mathxlab.experiments.prime_suite.ParamsE041
   :members:
   :member-order: bysource
   :show-inheritance:





.. autoclass:: mathxlab.experiments.prime_suite.ParamsE042
   :members:
   :member-order: bysource
   :show-inheritance:





.. autoclass:: mathxlab.experiments.prime_suite.ParamsE043
   :members:
   :member-order: bysource
   :show-inheritance:





.. autoclass:: mathxlab.experiments.prime_suite.ParamsE044
   :members:
   :member-order: bysource
   :show-inheritance:





.. autoclass:: mathxlab.experiments.prime_suite.ParamsE045
   :members:
   :member-order: bysource
   :show-inheritance:





.. autoclass:: mathxlab.experiments.prime_suite.ParamsE046
   :members:
   :member-order: bysource
   :show-inheritance:





.. autoclass:: mathxlab.experiments.prime_suite.ParamsE124
   :members:
   :member-order: bysource
   :show-inheritance:





.. autoclass:: mathxlab.experiments.prime_suite.ParamsE125
   :members:
   :member-order: bysource
   :show-inheritance:





.. autoclass:: mathxlab.experiments.prime_suite.ParamsE126
   :members:
   :member-order: bysource
   :show-inheritance:



Functions
~~~~~~~~~



.. autofunction:: mathxlab.experiments.prime_suite.run_e014





.. autofunction:: mathxlab.experiments.prime_suite.run_e015

   .. autofunction:: mathxlab.experiments.prime_suite.run_e016





.. autofunction::  mathxlab.experiments.prime_suite.run_e017





.. autofunction:: mathxlab.experiments.prime_suite.run_e018





.. autofunction:: mathxlab.experiments.prime_suite.run_e019

   .. autofunction:: mathxlab.experiments.prime_suite.run_e020





.. autofunction::  mathxlab.experiments.prime_suite.run_e021





.. autofunction:: mathxlab.experiments.prime_suite.run_e022





.. autofunction:: mathxlab.experiments.prime_suite.run_e023

   .. autofunction:: mathxlab.experiments.prime_suite.run_e024





.. autofunction::  mathxlab.experiments.prime_suite.run_e025





.. autofunction:: mathxlab.experiments.prime_suite.run_e026





.. autofunction:: mathxlab.experiments.prime_suite.run_e027

   .. autofunction:: mathxlab.experiments.prime_suite.run_e028





.. autofunction::  mathxlab.experiments.prime_suite.run_e029





.. autofunction:: mathxlab.experiments.prime_suite.run_e030





.. autofunction:: mathxlab.experiments.prime_suite.run_e031

   .. autofunction:: mathxlab.experiments.prime_suite.run_e032





.. autofunction::  mathxlab.experiments.prime_suite.run_e033





.. autofunction:: mathxlab.experiments.prime_suite.run_e034





.. autofunction:: mathxlab.experiments.prime_suite.run_e035

   .. autofunction:: mathxlab.experiments.prime_suite.run_e036





.. autofunction::  mathxlab.experiments.prime_suite.run_e037





.. autofunction:: mathxlab.experiments.prime_suite.run_e038





.. autofunction:: mathxlab.experiments.prime_suite.run_e039

   .. autofunction:: mathxlab.experiments.prime_suite.run_e040





.. autofunction::  mathxlab.experiments.prime_suite.run_e041





.. autofunction:: mathxlab.experiments.prime_suite.run_e042





.. autofunction:: mathxlab.experiments.prime_suite.run_e043

   .. autofunction:: mathxlab.experiments.prime_suite.run_e044





.. autofunction::  mathxlab.experiments.prime_suite.run_e045





.. autofunction:: mathxlab.experiments.prime_suite.run_e046





.. autofunction:: mathxlab.experiments.prime_suite.run_e124

   .. autofunction:: mathxlab.experiments.prime_suite.run_e125



.. autofunction::  mathxlab.experiments.prime_suite.run_e126
