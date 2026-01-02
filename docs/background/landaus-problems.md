# Landau’s problems refresher

At the 1912 International Congress of Mathematicians (Cambridge), Edmund Landau highlighted four “basic” open problems about prime numbers. They became known as **Landau’s problems**. {cite:p}`WikipediaContributors2026LandauProblems,Pintz2009LandauProblemsOnPrimes`

The striking aspect is that the statements are easy to explain to a beginner, but none of them has been proved so far.

## The four problems (informal statements)

Landau’s list is usually presented as:

1. **Goldbach (binary):** Every even integer $\ge 4$ is a sum of two primes.
2. **Twin primes:** There are infinitely many primes $p$ such that $p+2$ is also prime.
3. **Legendre’s conjecture:** For every $n\ge 1$, there is a prime between $n^2$ and $(n+1)^2$.
4. **Primes of the form $n^2+1$:** There are infinitely many primes among $n^2+1$.

Landau’s original phrasing and historical context are discussed nicely in Pintz’s survey. {cite:p}`Pintz2009LandauProblemsOnPrimes`

## Why these problems are “simple but hard”

A recurring theme is that **primes behave like random numbers in many respects**, but not enough is known to turn probabilistic intuition into proofs.

Two typical obstacles:

- **Parity barrier:** Many sieve methods can show “almost primes” (numbers with few prime factors), but they struggle to force *exactly one* prime factor.
- **Correlation control:** Conjectures like “twin primes” require proving that primality events at two nearby integers are correlated often enough.

## What experiments often do

Landau’s problems are perfect targets for “experimental math” because you can explore the *shape* of the evidence:

- **Goldbach:** empirical coverage, number of representations, typical smallest prime in a representation.
- **Twin primes:** counts up to $x$, normalized by $x/(\log x)^2$ (heuristics).
- **Legendre:** check prime gaps near squares; visualize primes in intervals $[n^2,(n+1)^2]$.
- **$n^2+1$ primes:** count prime values of $n^2+1$ for $n\le N$; compare against heuristic $\sim C\,N/\log N$ (Bateman–Horn-style intuition).

## Practical numerical caveats

- **Cost growth:** naive primality tests become slow as ranges grow; use a fast deterministic/probabilistic test (e.g. Miller–Rabin) and cache/sieve where possible.
- **Bias in small ranges:** for small $N$, “constants” in asymptotics are hard to see; show uncertainty bands or multiple scales.
- **Overflow:** $n^2$ grows quickly; use Python integers and avoid intermediate floats.

## References

See {doc}`../references`.

{cite:p}`WikipediaContributors2026LandauProblems,Pintz2009LandauProblemsOnPrimes,Guy2004UnsolvedProblemsInNumberTheory`
