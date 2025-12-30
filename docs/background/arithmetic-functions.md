# Arithmetic functions refresher

This page is a *beginner-friendly* refresher for experiments about **arithmetic functions**
(i.e. functions $f:\mathbb{N}\to\mathbb{C}$ that encode number-theoretic structure).

For deeper treatments, see {cite:p}`apostol1976introanalyticnumbertheory`,
{cite:p}`nivenzuckermanmontgomery1991introductiontheorynumbers`,
and {cite:p}`tenenbaum2015introanalyticprobabilisticnumbertheory`.

## What “arithmetic function” usually means

An **arithmetic function** is any function of a positive integer $n$.
Common themes:

- prime factorization drives the behavior of many functions
- *multiplicativity* lets you reduce to prime powers
- *averages* and *summatory functions* reveal global structure

Examples you will meet often:

- Euler’s totient $\varphi(n)$ (coprime residues)
- Möbius $\mu(n)$ and Mertens $M(x)=\sum_{n\le x}\mu(n)$
- divisor counts $d(n)$ and sums $\sigma_k(n)$
- prime-factor counting $\omega(n),\Omega(n)$
- von Mangoldt $\Lambda(n)$ (prime powers)
- Carmichael’s $\lambda(n)$ (group exponent mod $n$)

## Multiplicative vs. additive

### Multiplicative

An arithmetic function $f$ is **multiplicative** if

$$
f(1)=1,\qquad f(ab)=f(a)f(b)\;\; \text{whenever }\gcd(a,b)=1.
$$

If $n=\prod p_i^{\alpha_i}$ then multiplicativity gives

$$
f(n)=\prod f(p_i^{\alpha_i}).
$$

Typical: $\varphi,\mu,\sigma_k,d,J_k,\lambda$.

### Additive

A function $g$ is **additive** if

$$
g(ab)=g(a)+g(b)\;\; \text{whenever }\gcd(a,b)=1,
$$

and **completely additive** if the relation holds for all $a,b$ (no gcd condition).
Typical: $\Omega(n)$ is completely additive; $\omega(n)$ is additive.

## Why averages matter

Many experiments compare:

- pointwise behavior of $f(n)$
- cumulative behavior $\sum_{k\le n} f(k)$
- distribution of $f(n)$ over ranges

Analytic/probabilistic number theory focuses on these averages; see
{cite:p}`montgomeryvaughan2006multiplicativenumbertheoryi` and {cite:p}`tenenbaum2015introanalyticprobabilisticnumbertheory`.

## Common experiment patterns

- **Value distribution:** histograms of $f(n)$ for $n\le N$
- **Scatter vs. factorization features:** compare $f(n)$ with $\log n$, $\omega(n)$, etc.
- **Normal order:** show “typical size” vs. rare extremes (e.g. Erdős–Kac behavior)
- **Summatory oscillations:** $M(x)$, $\sum_{n\le x}\lambda(n)$, etc.
- **Extremal orders:** highly composite numbers maximize $d(n)$ (see {cite:p}`ramanujan1915highlycompositenumbers`)

## Experiments in this repository

- **E121** — Multiplicativity stress tests across core arithmetic functions.
- **E123** — Correlation matrix of arithmetic functions on 1..N (empirical relationships).
