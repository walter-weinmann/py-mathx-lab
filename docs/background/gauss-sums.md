# Gauss sums refresher

Gauss sums are finite Fourier transforms of Dirichlet characters. In Phase 2 they serve two purposes:

1. **A correctness/structure check for characters:** for primitive characters, the Gauss sum magnitude obeys a clean law.
2. **A bridge to analytic number theory:** Gauss sums appear in functional equations for Dirichlet $L$-functions and in explicit evaluations of some special values.

This page gives the definitions and the specific facts that the experiments use, with enough context to interpret the plots.

## Additive characters and the Fourier viewpoint

Fix a modulus $q\ge 1$. The basic additive character modulo $q$ is
$$
e_q(n) := \exp\!\left(\frac{2\pi i n}{q}\right).
$$
It is periodic mod $q$ and satisfies $e_q(m+n)=e_q(m)e_q(n)$. You can view $e_q(an)$ as a Fourier mode on the finite group $\mathbb{Z}/q\mathbb{Z}$.

A Dirichlet character $\chi$ modulo $q$ is (after restricting to units) a *multiplicative* character on $(\mathbb{Z}/q\mathbb{Z})^\times$.
Gauss sums mix the multiplicative character $\chi$ with the additive phase $e_q(\cdot)$, i.e. they are “multiplicative objects seen through additive Fourier glasses”.

## Core definitions

Let $\chi$ be a Dirichlet character modulo $q$. The (basic) **Gauss sum** is
$$
\tau(\chi) := \sum_{a=0}^{q-1} \chi(a)\, e_q(a).
$$

A more general “twisted” Gauss sum is
$$
\tau(\chi, b) := \sum_{a=0}^{q-1} \chi(a)\, e_q(ba)\qquad (b\in\mathbb{Z}).
$$

### Immediate properties

- If $b\equiv 0\pmod q$, then $\tau(\chi,b)=\sum_a\chi(a)$.
- If $\gcd(b,q)=1$, then a change of variables implies the relation
  $$
  \tau(\chi,b) = \overline{\chi}(b)\,\tau(\chi).
  $$

This identity is the main reason experiments can focus on $\tau(\chi)$ without losing information: all invertible twists are just rotations/scalings by a root of unity.

## The magnitude law $|\tau(\chi)|=\sqrt{q}$ for primitive characters

The central numerical pattern is:

> If $\chi$ is **primitive** modulo $q$, then $|\tau(\chi)| = \sqrt{q}$.

A good way to remember *why* this is plausible is to compute the squared magnitude and watch orthogonality collapse the double sum. Start with
$$
|\tau(\chi)|^2 = \tau(\chi)\,\overline{\tau(\chi)}
= \sum_{a=0}^{q-1}\sum_{b=0}^{q-1} \chi(a)\overline{\chi}(b)\, e_q(a-b).
$$

For primitive characters, the sum reorganizes into complete additive character sums with perfect cancellation, giving exactly $q$.
For **imprimitive** characters (induced from a smaller conductor), the same cancellation can fail; magnitudes may be smaller (and in some cases can vanish). This is why Phase 2 experiments should either restrict to primitive characters for “$\sqrt{q}$ laws” or explicitly label imprimitive cases.

## Quadratic Gauss sums (cleanest special case)

For an odd prime $p$ and the quadratic character (Legendre symbol) $\chi(n)=\left(\frac{n}{p}\right)$, the Gauss sum has a famous closed form:
$$
\tau(\chi) = \varepsilon_p\,\sqrt{p},\qquad
\varepsilon_p =
\begin{cases}
1, & p\equiv 1\pmod 4,\\
i, & p\equiv 3\pmod 4.
\end{cases}
$$

So not only is the magnitude $\sqrt{p}$, but the argument depends on $p\bmod 4$.
This is a strong “sanity target” for Phase 2: if your implementation of $\chi$ is correct and you use a consistent residue convention, the plotted points should land on the expected circle with the expected symmetry.

## Why Gauss sums matter for Dirichlet $L$-functions (high level)

For a primitive character $\chi$, the completed $L$-function satisfies a functional equation of the form
$$
\Lambda(s,\chi) = W(\chi)\,\Lambda(1-s,\overline{\chi}),
$$
where the **root number** $W(\chi)$ has absolute value $1$ and is built from $\tau(\chi)$ (up to normalization by $\sqrt{q}$ and a parity factor).

You do not need the full functional equation machinery for Phase 2 plots, but it explains why Gauss sums appear naturally whenever you connect characters, $L$-functions, and oscillations in arithmetic progression counts.

## Practical numerical notes for experiments

- **Residue conventions:** be consistent about whether you sum $a=0,\dots,q-1$ or $a=1,\dots,q$; both are valid but should not be mixed.
- **Non-units:** if you extend $\chi$ by $0$ on $\gcd(a,q)>1$, those terms contribute $0$, but you must ensure your implementation really does this.
- **Floating-point cancellation:** Gauss sums are dominated by cancellation. Use complex128 and avoid rounding before taking magnitudes.

## References

See {doc}`../references`.

{cite:p}`berndtevanswilliams1998gaussjacobisums,davenport2000multiplicativenumbertheory,iwanieckowalski2004analyticnumbertheory`

## Experiments in this repository

- **E067** — Gauss sums: magnitude vs. $\sqrt{q}$ (Phase 2 core).
- **E109** — Gauss sums $\tau(\chi)$: magnitude law and geometry for characters modulo $q$.
