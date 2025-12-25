# Perfect numbers refresher

This page is a *beginner-friendly* refresher for experiments about **perfect numbers**.
You only need basic number theory facts (divisors, primes) to follow it.

## Core definitions

For a positive integer $n$, let

- $d \mid n$ mean “$d$ divides $n$”,
- $\sigma(n) = \sum_{d\mid n} d$ be the **sum-of-divisors function**,
- $s(n) = \sum_{d\mid n,\; d<n} d = \sigma(n) - n$ be the sum of **proper** divisors.

A number $n$ is **perfect** iff its proper divisors sum to itself:

$$

n \text{ is perfect } \iff s(n)=n \iff \sigma(n)=2n .

$$

Examples:

- $6$ is perfect because $1+2+3=6$.
- $28$ is perfect because $1+2+4+7+14=28$.

## Key theorem: all even perfect numbers (Euclid–Euler)

A classic result completely characterizes **even** perfect numbers:

**Euclid–Euler theorem.**  
An integer $n$ is an even perfect number **iff**

$$

n = 2^{p-1}(2^p-1)

$$

where $2^p-1$ is prime (a **Mersenne prime**).

So every known perfect number is generated from a Mersenne prime exponent $p$.
This is the main “generator” you’ll use in experiments. {cite:p}`Caldwell2000EvenPerfectNumbersPrimePages,Voight1998PerfectNumbersElementaryIntroduction`

### Why $\sigma$ matters (multiplicativity)

If $n$ factors as

$$

n = \prod_{i=1}^k p_i^{a_i},

$$

then

$$

\sigma(n) = \prod_{i=1}^k \sigma\left(p_i^{a_i}\right)
= \prod_{i=1}^k \frac{p_i^{a_i+1}-1}{p_i-1}.

$$

This formula turns “sum all divisors” into a fast computation once you know the prime factorization.

## The big open question: odd perfect numbers

It is **unknown** whether any **odd** perfect numbers exist.
A large literature proves *constraints* (congruences, size bounds, number of prime factors, etc.).
Experiments can explore these constraints (and why they make brute-force search unrealistic). {cite:p}`Stone2024ImprovedUpperBoundsOddPerfectNumbersPartI,OchemRao2014LowerBoundsOddPerfectNumbersSlides,Guy2004UnsolvedProblemsInNumberTheory`

## What experiments typically visualize

Typical “lab” questions you can turn into plots and tables:

- **Verification by computation:** compute $\sigma(n)$ (via factorization) and check $\sigma(n)=2n$ for candidates.
- **Generator experiment:** produce even perfect numbers from known Mersenne exponents $p$ and confirm perfection.
- **Growth:** number of digits / bit length of $2^{p-1}(2^p-1)$ as a function of $p$.
- **Divisor-function behavior:** compare $\sigma(n)/n$ (abundancy index) for random $n$ vs. perfect numbers.
- **Odd constraints (toy models):** test necessary conditions on odd $n$ and see how restrictive they are.

For data (lists of perfect numbers and exponents), OEIS is a convenient reference. {cite:p}`OEIS2025A000396PerfectNumbers`

## Practical numerical caveats

Even with correct math, computation has a few traps:

- **Factorization dominates.** Computing $\sigma(n)$ via divisors is slow unless you factor $n$.
  For large $n$, factorization becomes infeasible; prefer the Euclid–Euler generator for even perfect numbers.
- **Big integers are fine, but expensive.** Python integers won’t overflow, but operations on huge numbers scale with
  the number of bits (so be mindful in loops and plotting).
- **Prime testing vs. proof.** Testing that $2^p-1$ is prime is nontrivial for large $p$.
  For experiments, use a curated list of known Mersenne prime exponents (e.g., from OEIS / GIMPS) rather than
  trying to discover new ones from scratch. {cite:p}`GIMPS2024M136279841PressRelease,GIMPS2025MilestonesReport`
- **Be explicit about definitions.** Some sources define “perfect” via $\sigma(n)=2n$; others via proper divisors.
  Use one convention consistently in code and docs.

## References

See {doc}`../references`.

{cite:p}`Voight1998PerfectNumbersElementaryIntroduction,Caldwell2000EvenPerfectNumbersPrimePages,Stone2024ImprovedUpperBoundsOddPerfectNumbersPartI,OEIS2025A000396PerfectNumbers`
