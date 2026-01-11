# Dirichlet $L$-functions refresher

Dirichlet characters package congruence information; Dirichlet $L$-functions turn that into analytic objects whose zeros control prime distribution in residue classes.

## Core definitions

Let $\chi$ be a Dirichlet character modulo $q$. The **Dirichlet $L$-function** is
$$
L(s,\chi) = \sum_{n=1}^\infty \frac{\chi(n)}{n^s},
\qquad \Re(s) > 1.
$$

For $\Re(s)>1$, it has an **Euler product**:
$$
L(s,\chi) = \prod_{p \nmid q}\left(1-\frac{\chi(p)}{p^s}\right)^{-1}.
$$

For the principal character:
$$
L(s,\chi_0) = \zeta(s)\prod_{p\mid q}\left(1-p^{-s}\right).
$$

The decisive analytic fact (used in Dirichlet’s theorem) is:
$$
L(1,\chi) \ne 0 \quad \text{for every nonprincipal character } \chi.
$$

## What experiments usually visualize or measure

- Convergence of partial sums $\sum_{n\le N}\chi(n)n^{-s}$ for various $s$.
- Convergence of partial Euler products over primes.
- Sensitivity near $s=1$ (slow convergence) and how to stabilize it.

## Practical numerical caveats

- Near $s=1$, both series and Euler products converge painfully slowly.
- For Euler products, compute via logs:
  $$
  \log L(s,\chi) \approx -\sum_{p\le P}\log\left(1-\chi(p)p^{-s}\right)
  $$
  to reduce catastrophic multiplication error.
- If you compare characters, always keep the same prime cutoff $P$ to make plots comparable.

## References

See {doc}`../references`.

{cite:p}`dirichlet1837primesinprogressions,davenport2000multiplicativenumbertheory,serre1973coursearithmetic,washington1997introductioncyclotomicfields`

## Experiments in this repository

- **E110** — Dirichlet L-series partial sums at s=1 and s=1/2 (principal vs nonprincipal).
- **E111** — Euler product vs Dirichlet series truncations for L(s,χ): error vs cutoff.
