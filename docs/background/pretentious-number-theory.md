# Pretentious number theory refresher

“Pretentious” number theory replaces some zero-driven arguments by measuring how
closely a multiplicative function *pretends* to be a simple model (typically $n^{it}$
or a Dirichlet character). It is especially effective for **comparative** experiments:
*which model explains the data best?*

## Core definitions

Let $f,g$ be multiplicative functions bounded by 1 in magnitude on primes.
The **pretentious distance** up to $x$ is
$$
\mathbb{D}(f,g;x)^2
=\sum_{p\le x}\frac{1-\Re\big(f(p)\overline{g(p)}\big)}{p}.
$$

Interpretation:

- $\mathbb{D}(f,g;x)$ small means $f(p)$ and $g(p)$ “agree” on most primes (in a
  $1/p$-weighted sense).
- $\mathbb{D}(f,g;x)$ large means $f$ cannot be explained well by $g$ on primes.

A common model family is $g(n)=\chi(n)n^{it}$ with a Dirichlet character $\chi$
and real $t$.

## What experiments usually visualize or measure

- Fit $t$ to minimize $\mathbb{D}(f,n^{it};x)$ and plot the best-fit $t(x)$.
- Compare distances $\mathbb{D}(f,\chi;x)$ across characters $\chi$ to see which
  congruence structure matches $f$.
- Use the distance to explain why partial sums of $f(n)$ may be large or small.

## Practical numerical caveats

- Always define the prime cutoff (use the same $x$ for fair comparisons).
- Distance is dominated by small primes; if you want to study “large-prime behavior,”
  consider plotting contributions by prime ranges.
- When fitting $t$, the objective can have shallow minima; report robustness (e.g.,
  multiple initial guesses).

## References

See {doc}`../references`.

{cite:p}`granville2009pretentiousness,granvillesoundararajan2007polyavinogradov`

## Experiments in this repository

- **E120** — Pretentious distance atlas for core multiplicative functions (μ, λ, φ/n, …).
