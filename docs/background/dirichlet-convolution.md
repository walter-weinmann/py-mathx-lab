# Dirichlet convolution refresher

Dirichlet convolution is a key “algebra” on arithmetic functions and shows up in many proofs and experiments.
See {cite:p}`apostol1976introanalyticnumbertheory` and {cite:p}`tenenbaum2015introanalyticprobabilisticnumbertheory`.

## Definition

For arithmetic functions $f,g:\mathbb{N}\to\mathbb{C}$, their **Dirichlet convolution** is

$$
(f\ast g)(n) = \sum_{d\mid n} f(d)\,g\!\left(\frac{n}{d}\right).
$$

The function $1(n)\equiv 1$ acts like an identity in many formulas, and the **delta function**
$\varepsilon(n)$ (with $\varepsilon(1)=1$ and $\varepsilon(n)=0$ for $n>1$) is the convolution identity:

$$
f\ast \varepsilon = f.
$$

## Möbius inversion

If

$$
F(n)=\sum_{d\mid n} f(d) \quad\Longleftrightarrow\quad F = f \ast 1,
$$

then **Möbius inversion** says

$$
f = F \ast \mu.
$$

This is one of the main reasons $\mu(n)$ appears everywhere.

## Classic identities

- Sum of divisors:
  $$
  \sigma(n) = (1\ast \mathrm{id})(n),
  $$
  where $\mathrm{id}(n)=n$.

- Totient:
  $$
  \varphi = \mu \ast \mathrm{id}.
  $$

- Jordan totient:
  $$
  J_k = \mu \ast \mathrm{id}^k.
  $$

- von Mangoldt:
  $$
  \Lambda = \mu \ast \log,
  $$
  in the sense of Dirichlet series / logarithmic derivatives of $\zeta(s)$.

## Dirichlet series viewpoint (why it’s computationally useful)

If $F(s)=\sum_{n\ge 1} f(n)n^{-s}$ and $G(s)=\sum_{n\ge 1} g(n)n^{-s}$ converge absolutely, then

$$
\sum_{n\ge 1}\frac{(f\ast g)(n)}{n^s}=F(s)\,G(s).
$$

This “turns convolution into multiplication” and underlies many analytic estimates; see
{cite:p}`montgomeryvaughan2006multiplicativenumbertheoryi`.

## Experiments in this repository

- **E102** — Dirichlet convolution identity zoo (μ*1=ε, φ*1=id, 1*1=τ, id*1=σ, …).
- **E121** — Multiplicativity stress tests and convolution sanity checks (random coprime tests).
