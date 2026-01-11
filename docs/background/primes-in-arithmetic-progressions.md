# Primes in arithmetic progressions refresher

For integers $q\ge 1$ and $a$, define
$$
\pi(x;q,a) := \#\{p \le x : p \text{ prime and } p \equiv a \pmod q\}.
$$

## Core statements

### Dirichlet’s theorem (existence)

If $\gcd(a,q)=1$, then there are infinitely many primes $p \equiv a \pmod q$.

### Prime number theorem in arithmetic progressions (equidistribution)

For fixed $q$ and $\gcd(a,q)=1$,
$$
\pi(x;q,a) \sim \frac{\mathrm{Li}(x)}{\varphi(q)} \quad (x\to\infty).
$$

So, asymptotically, primes split evenly among the reduced residue classes.

## What experiments usually visualize or measure

- Raw counts $\pi(x;q,a)$ for small moduli $q$ (2,3,4,5,8,10,12,…).
- Differences (races): $\pi(x;q,a)-\pi(x;q,b)$.
- “Leader changes”: values of $x$ where the sign of the difference flips.

## Practical numerical caveats

- Use a segmented sieve for $\pi(x;q,a)$ if $x$ gets large.
- For small $x$, visual phenomena are dominated by finite-size effects; that’s fine, but label plots honestly (e.g., “up to $10^7$”).
- If you use $\mathrm{Li}(x)$ for normalization, document the approximation you use.

## References

See {doc}`../references`.

{cite:p}`dirichlet1837primesinprogressions,davenport2000multiplicativenumbertheory`

## Experiments in this repository

- **E113** — First prime in each residue class (smallest p ≡ a mod q for all a∈(ℤ/qℤ)×).
