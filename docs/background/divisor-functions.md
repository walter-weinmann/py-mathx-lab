# Divisor functions $d(n)$ and $\sigma_k(n)$ refresher

Divisor functions measure how many divisors a number has, and how large they are.
They are classical examples of multiplicative functions. See {cite:p}`apostol1976introanalyticnumbertheory`.

## Counting divisors: $d(n)$

Let $d(n)$ (also written $\tau(n)$) be the number of positive divisors of $n$.

If $n=\prod p_i^{\alpha_i}$, then

$$
d(n)=\prod (\alpha_i+1).
$$

## Sum of divisors: $\sigma_k(n)$

For $k\ge 0$,

$$
\sigma_k(n)=\sum_{d\mid n} d^k.
$$

The case $k=1$ is the usual sum-of-divisors function $\sigma(n)$.

For a prime power,

$$
\sigma_k(p^\alpha)=1+p^k+p^{2k}+\cdots+p^{\alpha k}
=\frac{p^{(\alpha+1)k}-1}{p^k-1}.
$$

Again, multiplicativity gives $\sigma_k(n)$ from prime powers.

## Highly composite numbers (extremal behavior)

Numbers that maximize $d(n)$ up to a range are called **highly composite numbers**.
Ramanujan’s classic paper studies their structure. {cite:p}`ramanujan1915highlycompositenumbers`

## Experiment ideas

- visualize $d(n)$ up to $N$ and highlight record-breakers
- compare $\sigma(n)$ to $n$ (abundant / perfect / deficient classification)
- log-scale plots of $d(n)$ to make extremes visible

## Experiments in this repository

- **E096** — Record-holders for τ(n) up to N (highly composite flavor).
- **E097** — σ(n)/n landscape: deficient / perfect / abundant classification.
- **E098** — Extremals of σ(n)/n^α across α (phase changes / superabundant intuition).

## References

See {doc}`../references`.

{cite:p}`apostol1976introanalyticnumbertheory,ramanujan1915highlycompositenumbers,alaogluerdos1944highlycompositeandsimilarnumbers,robin1984grandesvaleurssommediviseurs,lagarias2002elementaryproblemequivalentrh`
