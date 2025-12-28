# Möbius function $\mu(n)$ and Mertens function $M(x)$ refresher

The Möbius function $\mu(n)$ is the main tool for inversion over divisors.
The Mertens function $M(x)=\sum_{n\le x}\mu(n)$ is a classic “oscillatory” summatory function.
See {cite:p}`apostol1976introanalyticnumbertheory`, {cite:p}`tenenbaum2015introanalyticprobabilisticnumbertheory`.

## Möbius function

Define $\mu(1)=1$. For $n>1$:

- $\mu(n)=0$ if $n$ is divisible by the square of a prime (not squarefree)
- otherwise $\mu(n)=(-1)^k$ where $k$ is the number of distinct prime factors of $n$

So for squarefree $n=p_1p_2\cdots p_k$,

$$
\mu(n)=(-1)^k.
$$

## Möbius inversion (most important identity)

If

$$
F(n)=\sum_{d\mid n} f(d),
$$

then

$$
f(n)=\sum_{d\mid n}\mu(d)\,F\!\left(\frac{n}{d}\right).
$$

## Mertens function and a famous counterexample

The **Mertens function** is

$$
M(x)=\sum_{n\le x}\mu(n).
$$

A historic conjecture was $|M(x)|<\sqrt{x}$ for all $x\ge 1$ (the **Mertens conjecture**).
It was disproved by Odlyzko and te Riele. {cite:p}`odlyzkoteriele1985disproofmertensconjecture`

## Why $M(x)$ is experiment-friendly

- $M(x)$ exhibits sign changes and irregular growth (“random walk-like” behavior).
- It is deeply connected to the Riemann zeta function and the Riemann hypothesis.

Typical experiment: plot $M(x)$ for growing $x$ and compare to envelopes like $\pm \sqrt{x}$ or $\pm x^{1/2}\log x$.
