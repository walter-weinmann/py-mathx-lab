# Quadratic polynomials (algebraic) refresher

A **quadratic polynomial** over a field $F$ is a degree-2 polynomial

$$
f(x)=ax^2+bx+c,\qquad a\ne 0,\quad a,b,c\in F.
$$

Over $F=\mathbb{R}$ or $\mathbb{C}$ this is the familiar object from school algebra, but many experiments treat $f$ over other fields (like $\mathbb{Q}$ or finite fields $\mathbb{F}_p$). {cite:p}`DummitFoote2004AbstractAlgebra,WikipediaContributors2026QuadraticEquation`

## Completing the square

A standard normal form is obtained by completing the square:

$$
ax^2+bx+c
= a\left(x+\frac{b}{2a}\right)^2 - \frac{b^2-4ac}{4a}.
$$

This shows that (over a field of characteristic $\ne 2$) every quadratic is a shifted/scaled square plus a constant term.

## Discriminant and factorization

The **discriminant** is

$$
\Delta=b^2-4ac.
$$

Over a field where square roots make sense, the roots are

$$
x = \frac{-b \pm \sqrt{\Delta}}{2a}.
$$

Algebraically, this means:

- $f$ **factors** over $F$ iff $\Delta$ is a square in $F$ (when $\mathrm{char}(F)\ne 2$).
- If $\Delta$ is not a square, the polynomial is **irreducible** over $F$.

### Finite field case ($\mathbb{F}_p$, odd prime $p$)

Over $\mathbb{F}_p$, “$\Delta$ is a square” means $\Delta$ is a quadratic residue mod $p$.
This is the bridge between algebra and number theory: quadratic residues, Legendre symbols, and Gauss sums.

## Why quadratics show up in prime experiments

Quadratics are the simplest non-linear polynomials, so they are a natural testbed for “prime values of polynomials”:

- Example: $n^2+1$ (Landau’s 4th problem).
- Example: $n^2+n+41$ (Euler’s famous prime-producing streak).

Even when a polynomial produces many primes early on, modular obstructions (e.g., always divisible by some prime for some residue class) inevitably appear.

## Practical numerical caveats

- **Stable quadratic formula:** over floating point numbers, use a stable variant when $b^2\gg 4ac$ to avoid catastrophic cancellation.
- **Exact arithmetic:** for modular experiments, keep everything as integers mod $p$; don’t mix floats.
- **Normalization:** many plots look cleaner after shifting/scaling to the monic form $x^2+Bx+C$ (when working over a field with $a^{-1}$).

## References

See {doc}`../references`.

{cite:p}`DummitFoote2004AbstractAlgebra,WikipediaContributors2026QuadraticEquation`
