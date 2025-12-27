# Mersenne numbers and primes refresher

This page is a *beginner-friendly* refresher for experiments about **Mersenne numbers**
and **Mersenne primes**.

## Core definitions

The **Mersenne numbers** are the integers


$$
M_n = 2^n - 1 \quad (n \in \mathbb{N}).
$$


A **Mersenne prime** is a Mersenne number that is prime:


$$
M_p \text{ is a Mersenne prime } \iff \; 2^p-1 \text{ is prime}.
$$


A key (easy) fact is that if $2^n-1$ is prime, then $n$ must be prime.  
So, in experiments, you typically only test $M_p$ for *prime* exponents $p$. {cite:p}`WikipediaContributors2025MersennePrime`

## Key theorem / test: Lucas–Lehmer (why Mersenne primes are “computable”)

For an odd prime exponent $p$, define $M_p = 2^p-1$ and a sequence $\{s_k\}$ by


$$
s_0 = 4, \qquad s_{k+1} = s_k^2 - 2.
$$


Compute this sequence *modulo* $M_p$ at each step, and then:


$$
M_p \text{ is prime } \iff\; s_{p-2} \equiv 0 \pmod{M_p}.
$$


This is the **Lucas–Lehmer test**. It’s the workhorse behind most practical Mersenne-prime checks
(and historically central to GIMPS). {cite:p}`WikipediaContributors2025LucasLehmerPrimalityTest,MersenneResearchInc2024GIMPSMathPrimeNet`

## What experiments typically visualize

- **Growth with the exponent:** number of bits / digits of $M_p$ as $p$ grows.
- **Prime vs. composite behavior:** the Lucas–Lehmer residue $s_{p-2} \bmod M_p$ across many prime exponents.
- **Factor patterns for composites:** quickly finding small factors of $M_p$ (to avoid running LLT when a trivial factor exists).
- **Connections to perfect numbers:** if $M_p$ is prime, then
  $2^{p-1}(2^p-1)$ is an even perfect number (Euclid–Euler). {cite:p}`Caldwell2000EvenPerfectNumbersPrimePages`

For curated sequences (lists of exponents / known values), OEIS is a convenient “ground truth” reference. {cite:p}`OEIS2025A001348MersenneNumbers,OEIS2025A000043MersenneExponents`

## Practical numerical caveats

- **Always reduce modulo $M_p$ in Lucas–Lehmer.**  
  If you don’t, the intermediate values explode in size (each squaring roughly doubles the bit-length).
- **Test the exponent first.**  
  If $p$ is composite, $M_p$ is automatically composite, so there’s no point running LLT.
- **Huge integers are fine, but you must be intentional.**  
  Python’s big integers won’t overflow, but performance depends on bit-length and on the efficiency of modular squaring.
- **Separate “demo scale” from “real scale.”**  
  For educational experiments, keep $p$ modest (e.g., $p\le 10^5$ is already huge for pure Python LLT).
  For large exponents, you’d rely on specialized implementations and careful FFT-based multiplication.

## References

See {doc}`../references`.

{cite:p}`WikipediaContributors2025MersennePrime,WikipediaContributors2025LucasLehmerPrimalityTest,Caldwell2021MersennePrimesPrimePages,OEIS2025A001348MersenneNumbers,OEIS2025A000043MersenneExponents`
