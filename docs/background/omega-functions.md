# Prime-factor counting: $\omega(n)$ and $\Omega(n)$ refresher

Prime-factor counts are central examples of additive arithmetic functions.
They are key in probabilistic number theory and in “typical behavior” experiments.
See {cite:p}`tenenbaum2015introanalyticprobabilisticnumbertheory`.

## Definitions

Let $n=\prod p_i^{\alpha_i}$.

- $\omega(n)$: number of **distinct** prime factors
  $$
  \omega(n)=\#\{p : p\mid n\}.
  $$

- $\Omega(n)$: number of prime factors **with multiplicity**
  $$
  \Omega(n)=\sum_i \alpha_i.
  $$

Examples:
- $12=2^2\cdot 3$ has $\omega(12)=2$ and $\Omega(12)=3$.

## Additivity

If $\gcd(a,b)=1$ then

$$
\omega(ab)=\omega(a)+\omega(b),
$$

and $\Omega$ is even completely additive:

$$
\Omega(ab)=\Omega(a)+\Omega(b)\quad\text{for all }a,b.
$$

## Typical size: Erdős–Kac phenomenon

A famous theorem of Erdős and Kac says (informally) that $\omega(n)$ behaves like a normal random variable
with mean and variance $\log\log n$ after normalization. {cite:p}`erdoskac1940gaussianlawerrorsadditivefunctions`

This is why histograms of $\omega(n)$ over ranges often look Gaussian.

## Experiment ideas

- histogram of $\omega(n)$ for $n\le N$ and compare to a normal curve
- compare $\omega(n)$ vs. $\log\log n$ (“normal order”)
- scatter $\Omega(n)$ vs. $\omega(n)$ to see multiplicities
