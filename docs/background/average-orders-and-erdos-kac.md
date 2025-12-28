# Average orders and the Erdős–Kac viewpoint

Many arithmetic functions are “wild” pointwise but have predictable average behavior.
This page gives a short refresher on *average order*, *normal order*, and the Erdős–Kac phenomenon.
See {cite:p}`tenenbaum2015introanalyticprobabilisticnumbertheory` and {cite:p}`erdoskac1940gaussianlawerrorsadditivefunctions`.

## Average order vs. normal order

- **Average order:** a function $A(x)$ such that
  $$
  \sum_{n\le x} f(n) \approx \sum_{n\le x} A(n)
  $$
  or $f$ has mean value described by $A$.

- **Normal order:** a function $N(n)$ such that “most” integers satisfy
  $$
  f(n) \approx N(n).
  $$

A classic example: for most $n$, $\omega(n)$ is close to $\log\log n$.

## Erdős–Kac theorem (informal statement)

Let $\omega(n)$ be the number of distinct prime factors.
Erdős and Kac proved that the normalized variable

$$
\frac{\omega(n)-\log\log n}{\sqrt{\log\log n}}
$$

has an approximately standard normal distribution over $n\le x$ as $x\to\infty$.
{cite:p}`erdoskac1940gaussianlawerrorsadditivefunctions`

## Experiment ideas

- for a chosen $N$, compute $\omega(n)$ for $n\le N$ and histogram the normalized values
- compare the empirical mean/variance with $\log\log N$
- explore how the fit improves as $N$ grows
