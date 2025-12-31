# Dirichlet characters refresher

This page is a *lightweight* background for experiments about primes in residue classes, Dirichlet $L$-functions, and prime races.

## Core definitions

Fix an integer modulus $q \ge 1$. A **Dirichlet character modulo $q$** is a function
$\chi : \mathbb{Z} \to \mathbb{C}$ such that:

1. (Periodicity) $\chi(n+q) = \chi(n)$ for all $n$.
2. (Multiplicativity) $\chi(mn) = \chi(m)\chi(n)$ for all $m,n$.
3. (Support) $\chi(n)=0$ if $\gcd(n,q) > 1$.
4. For $\gcd(n,q)=1$, we have $|\chi(n)|=1$ (so values are roots of unity).

The **principal character** $\chi_0$ modulo $q$ is:
\[
\chi_0(n) =
\begin{cases}
1, & \gcd(n,q)=1,\\
0, & \gcd(n,q)>1.
\end{cases}
\]

A character is **primitive** if it does not “factor through” a smaller modulus (its conductor equals $q$).

### Orthogonality (the workhorse identity)

Let $\chi,\psi$ be Dirichlet characters modulo $q$. Then (over a reduced residue system):
\[
\sum_{\substack{a \bmod q\\ \gcd(a,q)=1}} \chi(a)\overline{\psi(a)} =
\begin{cases}
\varphi(q), & \chi=\psi,\\
0, & \chi\ne \psi.
\end{cases}
\]

A dual identity (summing over characters) is:
\[
\sum_{\chi \bmod q} \chi(a)\overline{\chi(b)} =
\begin{cases}
\varphi(q), & a \equiv b \pmod q,\ \gcd(a,q)=1,\\
0, & \text{otherwise.}
\end{cases}
\]

These are the algebraic “Fourier rules” that make Dirichlet’s argument work.

### Example: modulus $q=4$

There are two characters modulo $4$:

- $\chi_0$ (principal).
- The nontrivial character $\chi_4$:
  \[
  \chi_4(n)=
  \begin{cases}
  0,& 2 \mid n,\\
  1,& n \equiv 1 \pmod 4,\\
  -1,& n \equiv 3 \pmod 4.
  \end{cases}
  \]

This single character already explains the classic race between primes $1 \bmod 4$ and $3 \bmod 4$.

## What experiments usually measure

- How $\sum_{n\le N}\chi(n)$ behaves (cancellation, max partial sums).
- How orthogonality isolates a residue class.
- How many primitive characters exist for a given modulus, and how they “look” as tables.

## Practical numerical caveats

- Always define $\chi(n)=0$ when $\gcd(n,q)>1$ (otherwise identities break).
- Represent $\chi$ as a lookup table on residues $0,\dots,q-1$ and reduce via `n % q`.
- Be careful with complex floats: for most experiments, values are in $\{0,\pm1\}$ or small roots of unity, so you can use exact complex numbers.

## References

See {doc}`../references`.

{cite:p}`dirichlet1837primesinprogressions,irelandrosen1990classicalintromodernnumbertheory,davenport2000multiplicativenumbertheory,serre1973coursearithmetic`

## Experiments in this repository

- **E106** — Character gallery: real vs complex characters; conjugate pairing.
- **E107** — Primitive vs imprimitive via conductor (induced characters).
- **E108** — Orthogonality relations as a heatmap; numeric sanity checks.
