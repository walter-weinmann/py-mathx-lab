# Cheat sheet

Quick, experiment-oriented reminders of core concepts and common pitfalls.
Entries are kept **alphabetical by topic title** so this page stays easy to scan.
Each topic is intentionally short and points to the relevant background pages and references.

## Chebyshev functions $\theta(x)$ and $\psi(x)$

- $\theta(x)=\sum_{p\le x}\log p$ (primes only).
- $\psi(x)=\sum_{n\le x}\Lambda(n)=\sum_{p^k\le x}\log p$ (includes prime powers).
- Weighted counts are often smoother than $\pi(x)$ and connect more directly to analytic theory.

See also: {doc}`von-mangoldt-and-chebyshev`. Refs: {cite:p}`apostol1976introanalyticnumbertheory,montgomeryvaughan2006multiplicativenumbertheoryi`.

## Congruent integers

- $a\equiv b\pmod m$ means $m\mid(a-b)$.
- Congruences are statements about residue classes, not about a unique representative.

See also: {doc}`divisibility-and-modular-arithmetic`. Refs: {cite:p}`hardywright2008introtheorynumbers`.

## Dirichlet character $\chi\bmod q$

- A Dirichlet character $\chi$ modulo $q$ is periodic mod $q$, completely multiplicative, and
  $\chi(n)=0$ when $\gcd(n,q)>1$.
- The **principal character** $\chi_0$ satisfies $\chi_0(n)=1$ for $\gcd(n,q)=1$ and $0$ otherwise.
- Values lie on the unit circle (for units) and encode multiplicative structure of residues mod $q$.

See also: {doc}`dirichlet-characters`. Refs: {cite:p}`davenport2000multiplicativenumbertheory,nivenzuckermanmontgomery1991introductiontheorynumbers`.

## Dirichlet $L$-function $L(s,\chi)$

- For $\Re(s)>1$: $L(s,\chi)=\sum_{n\ge1}\chi(n)n^{-s}=\prod_{p\nmid q}(1-\chi(p)p^{-s})^{-1}$.
- The Euler product highlights the prime connection; the series is often easier numerically.
- Near $s=1$, naive truncation can converge slowly; smoothing/damping is common in experiments.

See also: {doc}`dirichlet-l-functions`. Refs: {cite:p}`davenport2000multiplicativenumbertheory,montgomeryvaughan2006multiplicativenumbertheoryi`.

## Dirichlet’s theorem and PNT(AP) (experiment baseline form)

- If $\gcd(a,q)=1$, then there are infinitely many primes $p\equiv a\pmod q$ (Dirichlet).
- For fixed $q$ and $\gcd(a,q)=1$: $\pi(x;q,a)\sim \mathrm{li}(x)/\varphi(q)$ (PNT in AP).
- Error term used in Phase 2 plots: $E(x;q,a)=\pi(x;q,a)-\mathrm{li}(x)/\varphi(q)$.

See also: {doc}`primes-in-arithmetic-progressions`. Refs: {cite:p}`dirichlet1837primesinprogressions,iwanieckowalski2004analyticnumbertheory`.

## Euler’s totient $\varphi(q)$

- $\varphi(q)$ counts invertible residue classes: $\varphi(q)=\#(\mathbb{Z}/q\mathbb{Z})^\times$.
- If $q=\prod p_i^{k_i}$ then $\varphi(q)=q\prod_i(1-1/p_i)$.
- In Phase 2, $1/\varphi(q)$ is the “fair share” factor for residues in PNT(AP) baselines.

See also: {doc}`euler-totient-function`, {doc}`divisibility-and-modular-arithmetic`. Refs: {cite:p}`hardywright2008introtheorynumbers`.

## Extended Euclidean algorithm (egcd)

- Computes integers $(x,y)$ with $ax+by=\gcd(a,b)$.
- Key for modular inverses: if $\gcd(a,m)=1$ then $ax\equiv1\pmod m$.

See also: {doc}`divisibility-and-modular-arithmetic`. Refs: {cite:p}`nivenzuckermanmontgomery1991introductiontheorynumbers`.

## Failure cases (common pitfalls)

- Forgetting to restrict to $\gcd(a,q)=1$ when discussing PNT(AP) or prime races.
- Mixing sampling grids (linear vs log) across related race experiments.
- Comparing truncated Euler products with different prime cutoffs (not comparable).
- Treating “bias” on a finite range as a theorem; it is an observed phenomenon at that scale.

See also: {doc}`prime-number-races`, {doc}`primes-in-arithmetic-progressions`.

## Gauss sum $\tau(\chi)$

- Basic Gauss sum: $\tau(\chi)=\sum_{a=0}^{q-1}\chi(a)\exp(2\pi i a/q)$.
- For primitive $\chi$, the magnitude satisfies $|\tau(\chi)|=\sqrt{q}$ (key Phase 2 pattern).
- Often interpreted as a finite Fourier transform of the character.

See also: {doc}`gauss-sums`. Refs: {cite:p}`berndtevanswilliams1998gaussjacobisums,davenport2000multiplicativenumbertheory`.

## Greatest common divisor (gcd)

- $\gcd(a,b)$ is the largest integer dividing both.
- $\gcd(a,q)=1$ is the “invertible mod $q$” condition used throughout Phase 2.

See also: {doc}`divisibility-and-modular-arithmetic`. Refs: {cite:p}`hardywright2008introtheorynumbers`.

## Modular exponentiation (`pow`, square-and-multiply)

- Compute $a^e\bmod m$ efficiently in $O(\log e)$ multiplications.
- In Python: `pow(a, e, m)` (requires $e\ge0$, and $m>0$ in practice).

See also: {doc}`primality-testing`.

## Modular inverse

- The inverse of $a\bmod m$ exists iff $\gcd(a,m)=1$.
- In Python 3.8+: `pow(a, -1, m)` returns the inverse (raises if none exists).

See also: {doc}`divisibility-and-modular-arithmetic`.

## Modulo

- “$n\bmod m$” is a representative of the residue class of $n$ modulo $m$.
- Be consistent about representatives (usually $0,1,\dots,m-1$) when indexing arrays/plots.

See also: {doc}`divisibility-and-modular-arithmetic`.

## Orthogonality (Dirichlet characters)

- Over the reduced residues, characters satisfy discrete orthogonality relations.
- Practical interpretation: averaging over characters can isolate a specific residue-class signal.
- Used as a correctness check (character tables and indicator reconstructions).

See also: {doc}`dirichlet-characters`. Refs: {cite:p}`davenport2000multiplicativenumbertheory,montgomeryvaughan2006multiplicativenumbertheoryi`.

## Prime counting approximations ($x/\log x$, $\mathrm{li}(x)$)

- $x/\log x$ is a rough first-order approximation to $\pi(x)$.
- $\mathrm{li}(x)$ is the standard smooth baseline used in the experiments (and in PNT(AP) baselines).

See also: {doc}`prime-counting-approximations`. Refs: {cite:p}`apostol1976introanalyticnumbertheory`.

## Prime counting function $\pi(x)$

- $\pi(x)=\#\{p\le x: p\ \text{prime}\}$.
- For progressions: $\pi(x;q,a)$ counts primes $\le x$ with $p\equiv a\pmod q$.

See also: {doc}`prime-numbers`, {doc}`primes-in-arithmetic-progressions`.

## Prime counting in residue classes $\pi(x;q,a)$

- Definition: $\pi(x;q,a)=\#\{p\le x: p\equiv a\pmod q\}$.
- Only reduced residues ($\gcd(a,q)=1$) participate in equidistribution statements.
- Error term used in plots: $E(x;q,a)=\pi(x;q,a)-\mathrm{li}(x)/\varphi(q)$.

See also: {doc}`primes-in-arithmetic-progressions`.

## Prime definition

- A prime is an integer $p\ge2$ with exactly two positive divisors: $1$ and $p$.
- In experiments, always specify whether you include $p=2$ separately when using odd-only sieves/tests.

See also: {doc}`prime-numbers`.

## Prime mask / sieve idea

- A sieve produces a boolean mask `is_prime[n]` for $0\le n\le N$.
- Masks support fast bulk computations: prime lists, residue-class counts, race differences.

See also: {doc}`primality-testing`, {doc}`prime-numbers`.

## Prime race difference $\Delta(x;q,a,b)$

- Define $\Delta(x;q,a,b)=\pi(x;q,a)-\pi(x;q,b)$.
- Because baselines cancel, races compare error terms implicitly: $\Delta=E(x;q,a)-E(x;q,b)$.
- “Leader fraction” depends on sampling: a log grid weights decades more evenly than a linear grid.

See also: {doc}`prime-number-races`, {doc}`primes-in-arithmetic-progressions`. Refs: {cite:p}`granvillemartin2006primenumberraces,rubinsteinsarnak1994chebyshevsbias`.

## Reduced residue system (units mod $q$)

- $(\mathbb{Z}/q\mathbb{Z})^\times$ is the set of residues $a\bmod q$ with $\gcd(a,q)=1$.
- It has size $\varphi(q)$ and is the domain on which characters behave multiplicatively.

See also: {doc}`divisibility-and-modular-arithmetic`, {doc}`dirichlet-characters`.

## Residue class

- A residue class modulo $m$ is the set $\{n: n\equiv a\pmod m\}$ for some $a$.
- In code, we store a representative (often $a\in\{0,\dots,m-1\}$) but the math object is the class.

See also: {doc}`divisibility-and-modular-arithmetic`.

## Sampling choices (linear vs log)

- Linear-in-$x$ sampling overweights large $x$ values in “time-in-lead” style statistics.
- Log-in-$x$ sampling gives each decade similar weight and is usually more stable for race distributions.

See also: {doc}`prime-number-races`, {doc}`exploratory-visualizations`.

## von Mangoldt function $\Lambda(n)$

- $\Lambda(n)=\log p$ if $n=p^k$ for some prime $p$ and $k\ge1$, else $0$.
- Summing $\Lambda(n)$ up to $x$ yields $\psi(x)$ (Chebyshev’s second function).

See also: {doc}`von-mangoldt-and-chebyshev`. Refs: {cite:p}`apostol1976introanalyticnumbertheory`.
