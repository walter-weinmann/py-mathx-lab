# Jordan totient $J_k(n)$ refresher

Jordan’s totient function generalizes Euler’s totient.
It is multiplicative and appears naturally in group-counting problems.
See {cite:p}`apostol1976introanalyticnumbertheory` and {cite:p}`tenenbaum2015introanalyticprobabilisticnumbertheory`.

## Definition

For a fixed integer $k\ge 1$, the **Jordan totient** function $J_k(n)$ can be defined by

$$
J_k(n)=n^k \prod_{p\mid n}\left(1-\frac{1}{p^k}\right).
$$

For $k=1$, this is Euler’s totient: $J_1(n)=\varphi(n)$.

## Divisor-sum identity

A useful identity is

$$
\sum_{d\mid n} J_k(d)=n^k.
$$

In Dirichlet convolution language:

$$
J_k \ast 1 = \mathrm{id}^k,
$$

hence $J_k = \mu \ast \mathrm{id}^k$.

## Experiment ideas

- compare $J_k(n)$ as $k$ varies
- visualize $J_2(n)$ and $J_3(n)$ over $n\le N$
- compare $J_k(n)/n^k$ as a “prime factor penalty”

## Experiments in this repository

- **E099** — Jordan totients J_k: atlas, identities (J_1=φ), and scaling J_k(n)/n^k.
