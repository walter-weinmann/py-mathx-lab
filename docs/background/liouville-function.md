# Liouville function $\lambda(n)$ refresher

The Liouville function is a simple, oscillatory completely multiplicative function
built from $\Omega(n)$ (the total number of prime factors with multiplicity).
See {cite:p}`tenenbaum2015introanalyticprobabilisticnumbertheory`.

## Definition

Define

$$
\lambda(n)=(-1)^{\Omega(n)}.
$$

So $\lambda(n)=1$ if $n$ has an even total number of prime factors (with multiplicity),
and $\lambda(n)=-1$ otherwise.

Examples:
- $\lambda(1)=1$
- $\lambda(2)=-1$
- $\lambda(4)=\lambda(2^2)=1$
- $\lambda(12)=\lambda(2^2\cdot 3)=-1$

## Key properties

- **Completely multiplicative:** $\lambda(ab)=\lambda(a)\lambda(b)$ for all $a,b$.
- Connected to the Möbius function, but without the “squarefree = 0” behavior.

## Summatory function experiments

A standard experiment is the summatory function

$$
L(x)=\sum_{n\le x}\lambda(n),
$$

which oscillates and has deep connections to primes and zeta-function methods.

## Experiment ideas

- compare $L(x)$ with a random walk
- compare $\lambda(n)$ and $\mu(n)$ on squarefree numbers
- visualize $\lambda(n)$ as a $\pm1$ texture over the integer grid
