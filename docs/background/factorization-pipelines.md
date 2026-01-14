# Factorization pipelines (trial division + Pollard rho)

Phase 2 includes experiments that do not only test primality but also attempt to **factor** integers.
In practice you rarely use a single algorithm; you build a pipeline:

1. Cheap deterministic filters (small primes, gcd checks).
2. A fast primality test for the remaining cofactor (often Miller-Rabin).
3. A randomized factor finder for hard cases (Pollard rho), with retries.

This page describes a practical, experiment-friendly pipeline and how to report it.

## What is being computed

Given an integer $n \ge 2$, factorization aims to write

$$n = p_1^{e_1} p_2^{e_2} \cdots p_k^{e_k}$$

with distinct primes $p_i$ and exponents $e_i \ge 1$.

## Deterministic front-end: trial division

Trial division tries to find small prime factors by dividing by primes $p \le B$.

- It is **deterministic**.
- It is extremely effective as a first stage.
- It gives you natural runtime knobs (`B`, number of primes).

Implementation notes:

- Precompute primes up to $B$ with a sieve.
- Divide repeatedly to capture multiplicities.
- After removing small primes, the remaining cofactor can be 1, prime, or composite.

## Probabilistic core: Pollard rho

Pollard's rho is a randomized method that often finds a nontrivial factor quickly.
It is the standard next step after trial division for medium-size integers.
See {cite}`pollard1975montecarlofactorization` and the practical improvements in {cite}`brent1980improvedmontecarlofactorization`.

### Idea (high level)

Work modulo $n$ and iterate a polynomial map, commonly

$$f(x) = x^2 + c \pmod n.$$

The sequence $x_{i+1} = f(x_i)$ eventually cycles modulo a hidden prime divisor $p$ of $n$.
Using gcd computations on differences, you can often extract a factor:

$$d = \gcd(|x_i - x_j|, n).$$

If $1 < d < n$ you found a nontrivial factor.

### Why it is probabilistic

- The runtime depends on the chosen function parameter $c$, the start value, and luck.
- For some choices, the method can stall; you must retry with different parameters.

Because of this, Pollard rho is **probabilistic / heuristic**. You must report it that way.

## A practical pipeline

A good experiment pipeline is:

1. **Handle trivial cases:** $n < 2$, even numbers, perfect powers if you want.
2. **Trial division:** divide by primes up to $B$.
3. **Primality check on the cofactor:** if the remaining cofactor is 1 or prime, stop.
4. **Pollard rho for the remaining composite cofactor:** find a factor $d$.
5. **Recurse:** factor $d$ and $n/d$ using the same pipeline.
6. **Normalize:** sort factors, combine multiplicities.
7. **Verify:** multiply the result back and check you recover the original $n$.

The key property for correctness is the final verification step: it turns implementation bugs into test failures.

## Reporting checklist

In your report, always include:

- **Deterministic vs probabilistic:**
  - Trial division: deterministic.
  - Pollard rho: probabilistic / heuristic.
- **Runtime knobs:**
  - trial division bound $B$,
  - max rho iterations per attempt,
  - number of rho restarts,
  - random seed (if used).
- **Correctness cross-check:**
  - for small $n$ compare against a trusted reference (full trial division or a library factorization),
  - verify the product of returned factors equals the original input.

## Common pitfalls

- **Repeated factors:** always divide repeatedly (e.g. $n=12$ has factor 2 twice).
- **Prime cofactors:** do not feed a prime into rho without checking; you can loop unnecessarily.
- **gcd edge cases:** rho can return $d = n$ (failure); treat as "retry".
- **Non-reproducible results:** randomized algorithms should record a seed or a full parameter list.

## How this connects to experiments

- Semiprimes and factorization difficulty: {doc}`semiprimes`
- Primality tests used inside pipelines: {doc}`primality-testing`
- Modular arithmetic building blocks: {doc}`divisibility-and-modular-arithmetic`

## References

See {doc}`../references`.

