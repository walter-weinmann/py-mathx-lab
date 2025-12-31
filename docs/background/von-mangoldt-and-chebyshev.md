# von Mangoldt $\Lambda(n)$ and Chebyshev functions refresher

The von Mangoldt function concentrates on prime powers and is central in analytic number theory.
Chebyshev functions summarize prime distributions and are used in proofs of the Prime Number Theorem.
See {cite:p}`montgomeryvaughan2006multiplicativenumbertheoryi` and {cite:p}`tenenbaum2015introanalyticprobabilisticnumbertheory`.

## von Mangoldt function

Define

$$
\Lambda(n) =
\begin{cases}
\log p, & \text{if } n=p^k \text{ for a prime }p\text{ and }k\ge 1,\\
0, & \text{otherwise.}
\end{cases}
$$

So $\Lambda(n)$ “picks out” primes and prime powers.

## Chebyshev functions

Two common Chebyshev functions:

- $\theta(x)=\sum_{p\le x}\log p$
- $\psi(x)=\sum_{n\le x}\Lambda(n)$

Since $\psi$ sums $\log p$ over prime powers, it is smoother and often easier in analysis.

## Why these matter

- $\psi(x)\sim x$ is essentially equivalent to the Prime Number Theorem.
- $\Lambda$ is tied to the logarithmic derivative of $\zeta(s)$ (via Dirichlet series).

## Experiment ideas

- plot $\psi(x)$ and compare to $x$
- plot $\theta(x)$ and compare to $x$
- compare contributions from primes vs. higher prime powers in $\psi(x)$

## Experiments in this repository

- **E103** — Chebyshev ψ(x) jumps at prime powers (Λ support).
- **E104** — Von Mangoldt Λ statistics (support, value distribution, summatory behavior).
- **E119** — ψ(x) − x oscillations (prime-weighted deviation view).
