# Euler’s prime-generating polynomial refresher

One of the most famous “too good to be true” examples in experimental number theory is Euler’s quadratic

$$
f(n)=n^2+n+41.
$$

For integers $n=0,1,\dots,39$ it produces **prime numbers**.
This is an unusually long initial run for such a simple polynomial, and it is a classic motivation for prime-value experiments. {cite:p}`WikipediaContributors2025LuckyNumbersOfEuler,Weisstein2025EulerPrimeMathWorld`

## The basic facts

- For $0\le n\le 39$, $f(n)$ is prime.
- At $n=40$,
  $$
  f(40)=40^2+40+41=1681=41^2,
  $$
  so the prime streak must stop.
- At $n=41$,
  $$
  f(41)=41^2+41+41 = 41\cdot 43,
  $$
  again composite.

A neat way to see the “divisibility by 41” phenomenon is to write

$$
f(n) = n(n+1)+41.
$$

Working modulo 41, if $n\equiv -1 \pmod{41}$ then $n(n+1)\equiv 0$ and $f(n)\equiv 0 \pmod{41}$.
So infinitely many inputs force a factor 41.

## Why this doesn’t contradict “no prime polynomial”

A standard (and important) observation:

> No non-constant polynomial with integer coefficients can take prime values for *all* integers $n$.

Reason: if $f(0)=m$, then for $n=m$ we get $f(m)\equiv f(0)\equiv m \pmod m$, so $m\mid f(m)$, and $f(m)$ is composite once it is larger than $|m|$.

Euler’s example is still interesting because it shows that **long prime runs can happen**, even though a “prime for all $n$” polynomial is impossible.

## What to experiment with

Good experiment patterns:

- **Prime-streak length:** for a family $n^2+an+b$, measure the longest initial segment $n=0,1,\dots,L$ where values are prime.
- **Modular obstructions:** for each prime $p$, count how many residues $n\bmod p$ make $f(n)\equiv 0\pmod p$.
  (If there are many such residues, prime values should be rarer.)
- **Heuristic growth:** count primes among $f(0),\dots,f(N)$ and compare against a rough $N/\log N$ scale.
- **Visualization:** plot $f(n)$ and mark prime/composite values; or show a heatmap over $(a,b)$ for streak lengths.

## Practical numerical caveats

- **Big integers:** $f(n)$ grows like $n^2$; primality testing dominates runtime quickly.
- **Avoid accidental float conversion:** keep $n$ and $f(n)$ as Python integers throughout.
- **Sampling bias:** focusing only on “nice-looking” polynomials can be misleading; compare against random $(a,b)$ baselines.

## References

See {doc}`../references`.

{cite:p}`WikipediaContributors2025LuckyNumbersOfEuler,Weisstein2025EulerPrimeMathWorld,HardyWright2008AnIntroductionToTheTheoryOfNumbers`
