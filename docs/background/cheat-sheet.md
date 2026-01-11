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


## Extended Euclidean algorithm (egcd)

The **extended Euclidean algorithm** computes integers $(g, x, y)$ such that

$$g = \gcd(a,b) \quad\text{and}\quad ax + by = g.$$

Key use:

- If $\gcd(a,m)=1$, then $ax + my = 1$, so $ax \equiv 1 \pmod m$ and **$x$ is the modular inverse of $a$ mod $m$**.

Practical notes:

- The coefficient $x$ is not unique, but $x \bmod m$ is the unique inverse in $\{0,\dots,m-1\}$.
- Always reduce: `inv = x % m`.

See also: {doc}`primality-testing`, {doc}`factorization-pipelines` (many algorithms rely on gcd/egcd steps).


## Failure cases (common pitfalls)

Typical situations where modular routines or number-theory experiments fail or produce misleading results.

**Inverse does not exist:**

- $a^{-1} \pmod m$ exists **iff** $\gcd(a,m)=1$.
- If $\gcd(a,m)\ne 1$, there is **no** multiplicative inverse.
- In Python, `pow(a, -1, m)` raises `ValueError` when the inverse does not exist.

**Bad modulus:**

- Most modular arithmetic assumes $m\ge 2$.
- In Python, `pow(a, e, m)` requires `m != 0` and (in practice) `m > 0`; otherwise you get an exception.

**Exponent sign mistakes:**

- Modular exponentiation uses $e\ge 0$.
- `pow(a, e, m)` with a **negative** `e` is not allowed, except for the special case `pow(a, -1, m)` (inverse).

**Residue class counting pitfalls:**

- Always fix your representative set (usually $0,1,\dots,m-1$).
- When counting primes mod $q$, decide whether you count:
  - all residues (including $0$), or
  - only the **reduced residue system** (residues $a$ with $\gcd(a,q)=1$).
- Remember: primes dividing $q$ land in residue $0 \pmod q$ (and can distort “prime race” plots if not handled explicitly).

**Silent “visual” failures:**

- Many claims “look true” at small $N$ but change at larger $N$.
- Always record finite cutoffs and use caution language (“finite-range behavior”).

See also: {doc}`exploratory-visualizations`.


## Greatest common divisor (gcd)

The **greatest common divisor** $\gcd(a,b)$ is the largest positive integer dividing both $a$ and $b$.

Core facts:

- $\gcd(a,b)=\gcd(b, a\bmod b)$ (Euclid’s algorithm).
- $\gcd(a,0)=|a|$.
- $\gcd(a,m)=1$ is exactly the condition “$a$ is invertible modulo $m$”.

Why it matters in this lab:

- Modular inverses, CRT steps, and many “failure modes” are just $\gcd\ne 1$.
- Factorization pipelines often discover non-trivial factors via gcd computations.

Practical tip:

- Compute gcd early and explicitly when you rely on inverses or division mod $m$.

See also: {doc}`factorization-pipelines`.


## Modular exponentiation (pow, square-and-multiply)

Goal: compute

$$a^e \bmod m$$

efficiently, without ever forming the huge integer $a^e$.

**Best practice in Python:**

- Use the built-in: `pow(a, e, m)`
- Complexity is $O(\log e)$ modular multiplications (fast exponentiation under the hood).

**Square-and-multiply idea (binary exponentiation):**

Write $e$ in binary. Repeatedly square, and multiply in when the current bit is 1.

Sketch:

- Initialize `result = 1`, `base = a % m`, `exp = e`
- While `exp > 0`:
  - If `exp` is odd: `result = (result * base) % m`
  - `base = (base * base) % m`
  - `exp //= 2`

Why it matters in this lab:

- Primality tests (e.g. Fermat/Miller–Rabin) are dominated by modular exponentiation.
- Efficient modular exponentiation makes “large N” experiments feasible.

See also: {doc}`primality-testing`.


## Modular inverse (gcd/egcd → inverse)

The **modular inverse** of $a$ modulo $m$ is an integer $a^{-1}$ such that

$$a\cdot a^{-1} \equiv 1 \pmod m.$$

Existence and uniqueness:

- An inverse exists **iff** $\gcd(a,m)=1$.
- If it exists, it is unique modulo $m$.

How to compute:

1) **Extended Euclid (theory-first):**  
   If egcd gives $ax + my = 1$, then $x \bmod m$ is the inverse.

2) **Python shortcut (recommended):**  
   `pow(a, -1, m)` returns the inverse if it exists (and raises `ValueError` otherwise).

Sanity check:

- After computing `inv`, verify `(a * inv) % m == 1`.

Common mistakes:

- Forgetting to reduce the result to a standard representative: use `inv % m`.
- Attempting inversion when $\gcd(a,m)\ne 1$ (no inverse).

See also: {doc}`prime-numbers` (units mod $m$), {doc}`factorization-pipelines`.


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


## Prime counting approximations (x/log(x), li(x))

A common first approximation to $\pi(x)$ is
$$\frac{x}{\log(x)}$$
(where $\log$ is the **natural logarithm**).

A more accurate classic approximation is the **logarithmic integral** $\operatorname{li}(x)$.

Plot/report checklist:

- Say explicitly what you plot: $\pi(x)$ vs $x/\log(x)$ (or vs $\operatorname{li}(x)$).
- Clarify whether the “error” is **absolute** ($\pi(x)-x/\log(x)$) or **relative**.
- For finite ranges, label statements as “finite-range behavior”.

See also: {doc}`prime-counting-approximations`.


## Prime counting function π(x)

The **prime counting function** $\pi(x)$ counts how many primes are $\le x$.

- If $x$ is an integer: $\pi(x)=\#\{p\ \text{prime} : p\le x\}$.
- In experiments with an upper bound $\text{n}_{\max}$, the endpoint value is $\pi(\text{n}_{\max})$.

Why it matters in this lab:

- Many plots compare $\pi(x)$ to analytic approximations.
- Always state the finite range (e.g. $2\le x\le \text{n}_{\max}$) to avoid “asymptotic overclaiming”.

See also: {doc}`prime-counting-approximations`, {doc}`prime-counting-bounds`.


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
