# Euler’s totient function $\varphi(n)$ refresher

Euler’s totient function $\varphi(n)$ counts reduced residues modulo $n$.
Standard references: {cite:p}`apostol1976introanalyticnumbertheory`, {cite:p}`nivenzuckermanmontgomery1991introductiontheorynumbers`.

## Definition

For $n\ge 1$,

$$
\varphi(n) = \#\{\,1\le k\le n : \gcd(k,n)=1\,\}.
$$

Equivalently: $\varphi(n)$ is the size of the multiplicative group $(\mathbb{Z}/n\mathbb{Z})^\times$.

## Prime power formula

If $p$ is prime and $k\ge 1$,

$$
\varphi(p^k)=p^k-p^{k-1}=p^k\left(1-\frac1p\right).
$$

Since $\varphi$ is multiplicative, for $n=\prod p_i^{\alpha_i}$:

$$
\varphi(n)=n\prod_{p\mid n}\left(1-\frac{1}{p}\right).
$$

## Important properties

- **Euler’s theorem:** if $\gcd(a,n)=1$ then $a^{\varphi(n)}\equiv 1\pmod n$.
- **Average order:** roughly $\sum_{n\le x}\varphi(n)\sim \frac{3}{\pi^2}x^2$ (analytic methods).
- **Extremes:** $\varphi(n)$ is small when $n$ has many small prime factors.

## Computational notes

Given the prime factorization of $n$, $\varphi(n)$ is cheap to compute via the product formula.
For experiments, you can often compute it for all $n\le N$ efficiently using a sieve-style method.

## Experiments in this repository

- **E101** — Reduced residues (ℤ/qℤ)× as an explicit set; verify size φ(q).
