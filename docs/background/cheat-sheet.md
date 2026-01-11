# Cheat sheet

Quick, experiment-oriented reminders of core concepts and common pitfalls.
Entries are kept **alphabetical by title** so this page stays easy to scan.

## Congruent integers

Two integers $a$ and $b$ are **congruent modulo** $m$ (with $m\ge 2$) if they leave the **same remainder**
when divided by $m$.

Equivalent definition:

- $a \equiv b \pmod m$  **iff**  $m$ divides $a-b$ (written $m\mid(a-b)$).

Examples:

- $17 \equiv 2 \pmod 5$ because $17-2=15$ is divisible by $5$.
- $12 \equiv 17 \pmod 5$ because $12-17=-5$ is divisible by $5$ (so they are in the same residue class mod $5$).
- $29 \equiv 1 \pmod 7$ because $29-1=28$ is divisible by $7$.
- Negative numbers work the same: $-3 \equiv 4 \pmod 7$ because $-3-4=-7$ is divisible by $7$.

Why it matters in this lab:

- “Prime races” / residue class counts use statements like $p \equiv a \pmod q$.
- Many “obstructions” are modular: e.g. $n^2+1 \not\equiv 0 \pmod 4$ for any integer $n$.
- Always record the modulus and the representative set you use (e.g. residues $0,1,\dots,q-1$).

See also: {doc}`prime-numbers`.


## Modulo

Working **modulo** $m$ means we consider integers only up to their remainder upon division by $m$ (with $m\ge 2$).

Two closely related notations:

- **Remainder value:** $a \bmod m$ is the remainder when dividing $a$ by $m$ (often taken in $\{0,1,\dots,m-1\}$).
- **Congruence relation:** $a \equiv b \pmod m$ means $a$ and $b$ have the same remainder mod $m$, equivalently $m\mid(a-b)$.

Examples:

- $17 \bmod 5 = 2$
- $12 \equiv 17 \pmod 5$

Why it matters in this lab:

- Most “residue class” plots and counts are statements about values modulo $m$.
- Always record the modulus $m$ and the chosen representative set (e.g. residues $0,1,\dots,m-1$).

See also: {doc}`prime-numbers`.

## Plot caveats (finite N)

Most plots in this lab visualize **finite** data (a finite cut-off $N$) even when the underlying theory is asymptotic.

Common pitfalls:

- **Finite-range artifacts:** patterns can appear “structured” at small/moderate $N$ and fade (or change) at larger $N$.
- **Boundary effects:** plots on a window (e.g. a spiral of size `size`) can exaggerate edge structure.
- **Binning and smoothing:** histogram bin width, kernel smoothing, and interpolation can create or hide apparent trends.
- **Marker and rasterization choices:** marker size, transparency, and image resolution can bias what is visually salient.
- **Axis scaling:** linear vs log scaling changes what “looks flat” or “looks curved”.

What to report (minimum):

- the effective cut-off $N$ (or $\text{size}^2$ when the window size determines $N$),
- any binning/smoothing parameters,
- axis scales (linear/log),
- a one-paragraph caveat: “finite-range behavior; do not overinterpret as asymptotic truth”.

See also: {doc}`prime-counting-approximations`, {doc}`prime-counting-bounds`, {doc}`exploratory-visualizations`.

## Prime definition

A **prime number** is an integer $p>1$ whose only positive divisors are $1$ and $p$.

Key reminders:

- $1$ is **not** prime.
- Every integer $n>1$ has a unique factorization into primes (up to ordering): the **Fundamental Theorem of Arithmetic**.
- In computational experiments, “prime” typically means “prime in $\mathbb{Z}$”.

See also: {doc}`prime-numbers`.

## Prime mask / sieve idea

A **prime mask** is a boolean array `is_prime[0..N]` where `is_prime[n]` indicates whether $n$ is prime.

The standard construction is the **Sieve of Eratosthenes**:

1. Start with `is_prime[n]=True` for $n=2,\dots,N$.
2. For each prime $p\le \sqrt{N}$, mark multiples $2p,3p,\dots$ as composite.

Why it matters:

- **Deterministic** for all $n\le N$.
- Time complexity is about $O(N\log\log N)$ with $O(N)$ memory.
- Enables fast “prime/non-prime” overlays in plots (spirals, heatmaps, density curves).

Common refinements (when $N$ grows):

- **Odd-only sieve:** store only odd indices to halve memory.
- **Segmented sieve:** sieve in blocks when $N$ is too large to hold a full mask in memory.

See also: {doc}`primality-testing`, {doc}`factorization-pipelines`, {doc}`prime-numbers`.

## Residue class

A **residue class** (also called a **congruence class**) modulo $m$ is the set of all integers that are congruent to a given integer $a$.

Definition:

- $$[a]_m = \{\,a + km \mid k\in\mathbb{Z}\,\}.$$

Key facts:

- There are exactly $m$ residue classes modulo $m$: $[0]_m,[1]_m,\dots,[m-1]_m$.
- $$a \equiv b \pmod m \iff a\in[b]_m \iff b\in[a]_m.$$

Example (mod $5$):

- $$[2]_5 = \{\dots,-8,-3,2,7,12,17,22,\dots\}$$
- So $2$, $12$, and $17$ are all in the same residue class modulo $5$.

Why it matters in this lab:

- Counting primes in arithmetic progressions is counting primes in residue classes, e.g. $p \equiv a \pmod q$.
- “Modular obstructions” are statements that a polynomial cannot hit certain residue classes.

See also: {doc}`prime-numbers`.

## Sampling choices (linear vs log)

When you sweep a parameter (e.g. $x$ in $\pi(x)$, or a grid over $(a,b)$), the **sampling strategy** affects what you see.

**Linear sampling** (equal steps):

- best for “local structure” (short-range variation),
- simple to interpret,
- can waste points at large scales if you need many orders of magnitude.

**Log sampling** (points spaced geometrically):

- best for “scale behavior” across orders of magnitude,
- often reveals stabilization toward asymptotic trends,
- can hide local oscillations because spacing grows with $x$.

What to record in `params.json` / `report.md`:

- range (min/max),
- number of sample points,
- spacing rule (linear/log),
- any randomness / seeding used for subsampling.

See also: {doc}`exploratory-visualizations`.
