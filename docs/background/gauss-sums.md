# Gauss sums and the discrete Fourier viewpoint

Gauss sums are “finite Fourier transforms” of Dirichlet characters.
They are a compact way to see how characters interact with additive phases, and they
show up naturally in functional equations and explicit evaluations of certain $L$-values.

## Core definitions

Let $\chi$ be a Dirichlet character modulo $q$ and write
\[
e_q(a)=\exp\!\left(\frac{2\pi i a}{q}\right).
\]
The (normalized) **Gauss sum** is
\[
\tau(\chi)=\sum_{a=1}^{q} \chi(a)\,e_q(a).
\]

For a **primitive** character $\chi$ modulo $q$, one has the fundamental magnitude law
\[
|\tau(\chi)|=\sqrt{q}.
\]
(For imprimitive characters, the behavior is more subtle and often smaller.)

A key identity connecting Gauss sums to character orthogonality is:
\[
\sum_{a \bmod q} \chi(a)\,e_q(an)=\overline{\chi}(n)\,\tau(\chi)
\quad (\gcd(n,q)=1),
\]
and it vanishes when $\gcd(n,q)>1$.

## What experiments usually visualize or measure

- The cloud of complex values $\tau(\chi)$ for all characters modulo a fixed $q$.
- The “circle of radius $\sqrt{q}$” phenomenon for primitive characters.
- Quadratic characters as a special case (values close to $\pm\sqrt{q}$ or $\pm i\sqrt{q}$ depending on $q$).

## Practical numerical caveats

- Always be explicit about the representative set for residues (e.g. $a=1,\dots,q$).
- For imprimitive characters, confirm whether the implementation returns the induced
  character or the primitive lift; this changes $\tau(\chi)$ drastically.
- Use complex128 (or higher) if you push $q$ large; cancellation is extreme in
  the raw sum definition.

## References

See {doc}`../references`.

{cite:p}`berndtevanswilliams1998gaussjacobisums,davenport2000multiplicativenumbertheory`

## Experiments in this repository

- **E109** — Gauss sums $\tau(\chi)$: magnitude law and geometry for characters modulo $q$.
