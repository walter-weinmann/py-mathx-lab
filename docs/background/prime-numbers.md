# Prime numbers refresher

This page is a *beginner-friendly* refresher for experiments about **prime numbers**.
It is intentionally broad: it covers the prime-related ideas most commonly explored
with computation (distribution, sieves, primality testing, gaps, and prime patterns).

## Core definitions

### Primes and composites

A positive integer $p \ge 2$ is **prime** if its only positive divisors are $1$ and $p$.
If $n \ge 2$ is not prime, it is **composite**.

Equivalently,

$$
p \text{ is prime } \iff \forall\, a,b \in \mathbb{N}: \; p = ab \Rightarrow (a=1 \text{ or } b=1).
$$

### Greatest common divisor and coprimality

The **greatest common divisor** of integers $a,b$, written $\gcd(a,b)$, is the largest positive integer dividing both.
We say $a$ and $b$ are **coprime** if $\gcd(a,b)=1$.

Coprimality appears constantly in modular arithmetic and in many prime-related proofs.

### Congruences (modular arithmetic)

For integers $a,b$ and $m\ge 2$,

$$
a \equiv b \pmod m
$$

means $m$ divides $a-b$.
Many prime experiments (residue classes, sieves, primality tests) are naturally expressed modulo $m$.

### Prime factorization (the “atomic” viewpoint)

The **Fundamental Theorem of Arithmetic** says every integer $n\ge 2$ factors uniquely (up to ordering) as

$$
n = \prod_{i=1}^k p_i^{\alpha_i},
$$

where the $p_i$ are distinct primes and the $\alpha_i$ are positive integers.
This makes primes the “building blocks” of the integers. {cite:p}`hardywright2008introtheorynumbers`

## Key quantitative language

### Infinitely many primes

Euclid’s classic argument shows there are infinitely many primes.
This matters experimentally because it justifies questions like “how often do primes occur as numbers grow?” {cite:p}`hardywright2008introtheorynumbers`

### The prime counting function and the Prime Number Theorem

Let $\pi(x)$ be the number of primes $\le x$.
The **Prime Number Theorem** (PNT) states

$$
\pi(x) \sim \frac{x}{\log x}\quad (x\to\infty).
$$

Informally: primes thin out, and the “typical” gap size near $x$ is about $\log x$. {cite:p}`apostol1976introanalyticnumbertheory`

For experiments, two very common comparisons are:

- $\pi(x)$ vs. $x/\log x$,
- $\pi(x)$ vs. $\mathrm{Li}(x)$ (the logarithmic integral), which is often a better approximation in practice. {cite:p}`apostol1976introanalyticnumbertheory,rosserschoenfeld1962approximateformulasprimefunctions`

### Explicit bounds (useful sanity checks)

Many sources provide explicit inequalities for $\pi(x)$, the $n$th prime $p_n$, and related functions.
These bounds are useful to validate computations and pick experiment ranges safely. {cite:p}`rosserschoenfeld1962approximateformulasprimefunctions,dusart2018explicitestimatesfunctionsprimes,axler2019newestimatesnthprime`

## Computational building blocks

### Generating primes: sieves

If you need *all* primes up to a bound $N$, a sieve is usually best.

**Sieve of Eratosthenes (idea).**
Start with a boolean array “possibly prime,” then repeatedly cross out multiples of each found prime.
Time is roughly $O(N\log\log N)$, memory is $O(N)$ booleans.

**Segmented sieve.**
For large $N$, store only a window $[L,R]$ at a time; this keeps memory bounded while preserving speed.
Segmented sieves are often the right choice once $N$ grows beyond typical RAM-friendly sizes. {cite:p}`crandallpomerance2005primenumberscomputationalperspective`

### Testing primality (single numbers)

If you need to test primality of individual (possibly large) integers, common strategies are:

- **Trial division** up to $\sqrt{n}$ (great for small $n$, too slow for large),
- **Probabilistic tests** such as **Miller–Rabin**, fast and extremely reliable with good parameters, {cite:p}`rabin1980probabilisticalgorithmprimality`
- **Deterministic polynomial-time** primality testing (AKS), important theoretically but rarely used for practical large-number work. {cite:p}`agrawalkayalsaxena2004primesisinp`

In an experiment repo, it is common to use Miller–Rabin for speed and then either:
(1) accept “probable prime” status (with a stated error bound),
or (2) confirm with stronger checks for the sizes you care about. {cite:p}`crandallpomerance2005primenumberscomputationalperspective`

### Factorization (often the bottleneck)

Many arithmetic functions become easy once a number is factored, but factoring large integers is hard.
Even “toy” factorization methods (e.g., Pollard’s rho) make excellent experiments because performance varies wildly with input structure. {cite:p}`crandallpomerance2005primenumberscomputationalperspective`

## Prime gaps and prime patterns

### Prime gaps

Let $p_n$ be the $n$th prime.
The **prime gap** sequence is

$$
g_n = p_{n+1}-p_n.
$$

Heuristically, “typical” gaps near $p$ are size $\log p$, but gaps vary a lot.
Two natural experimental viewpoints are:

- **local statistics**: histogram of $g_n$ in a range,
- **record gaps**: the largest gap seen up to $x$ (maximal gaps / first occurrences). {cite:p}`cramer1936orderofmagnitudedifferenceconsecutiveprimes,nicely1999newmaximalprimegaps,Caldwell2000PrimeGapsPrimePages`

A common normalization is $g_n/\log p_n$, which helps compare different scales.

### Twin, cousin, and sexy primes (prime pairs)

A **prime pair** is a pair of primes $(p,p+d)$ with fixed even difference $d$:

- **twin primes**: $d=2$,
- **cousin primes**: $d=4$,
- **sexy primes**: $d=6$.

These are all instances of “prime constellations.”

### Prime $k$-tuples (constellations)

A **prime $k$-tuple** is a set of offsets $\{h_1,\dots,h_k\}$ such that $p+h_i$ are simultaneously prime.
Hardy–Littlewood heuristics predict asymptotic counts for many such patterns (including twins). {cite:p}`hardylittlewood1923partitionumerorumIII`

Modern sieve breakthroughs show **bounded prime gaps** exist (there are infinitely many $g_n$ below some constant),
but we still do not know whether the twin prime conjecture is true. {cite:p}`zhang2014boundedgapsbetweenprimes,maynard2015smallgapsbetweenprimes,polymath2014boundedgapsbetweenprimes`

## Primes in structure (residue classes and progressions)

### Residue classes

Primes (except 2) are odd, so they lie in residue classes modulo 2.
More generally, you can study how primes distribute among residue classes modulo $q$.
Experiments here include “prime races” and small biases in counts.

### Arithmetic progressions of primes

A classical result (Dirichlet’s theorem) says that if $\gcd(a,q)=1$, then the arithmetic progression

$$
a,\; a+q,\; a+2q,\dots
$$

contains infinitely many primes.
A landmark modern result (Green–Tao) shows primes contain arbitrarily long arithmetic progressions. {cite:p}`greentao2008primesarithmeticprogressions`

For experiments, you can stay at an elementary level (searching for 3-term or 4-term prime APs in ranges)
while still getting meaningful patterns.

## Other prime families you may include (optional)

These are often nice “side quests” that still fit under “Prime Numbers”:

- **Sophie Germain primes**: $p$ prime and $2p+1$ prime,
- **safe primes**: $q$ prime with $(q-1)/2$ prime,
- **Mersenne primes**: $2^p-1$ prime (you already have a dedicated page), {cite:p}`WikipediaContributors2025MersennePrime`
- **palindromic / repunit primes**: “pattern-based” primes useful for search experiments.

## What experiments typically visualize

Typical “prime numbers lab” plots and tables include:

- **Prime density:** $\pi(x)$ vs. $x/\log x$, and error curves $\pi(x)-x/\log x$. {cite:p}`apostol1976introanalyticnumbertheory`
- **Bounds and approximations:** compare $\pi(x)$ with explicit inequalities (sanity checks). {cite:p}`rosserschoenfeld1962approximateformulasprimefunctions,dusart2018explicitestimatesfunctionsprimes`
- **Sieve scaling:** runtime/memory vs. $N$ for classic vs. segmented sieves. {cite:p}`crandallpomerance2005primenumberscomputationalperspective`
- **Gaps:** histograms of $g_n$, normalized gaps $g_n/\log p$, record gaps vs. $\log^2 x$. {cite:p}`cramer1936orderofmagnitudedifferenceconsecutiveprimes,nicely1999newmaximalprimegaps`
- **Prime pairs:** counts of twin/cousin/sexy primes in $[1,x]$, compared to Hardy–Littlewood style heuristics. {cite:p}`hardylittlewood1923partitionumerorumIII`
- **Bounded gaps story:** “what bound was known when?” (Zhang → Maynard → Polymath) plus empirical gap data. {cite:p}`zhang2014boundedgapsbetweenprimes,maynard2015smallgapsbetweenprimes,polymath2014boundedgapsbetweenprimes`
- **Primality tests:** speed vs. integer size (bits), and false-positive rates for weak tests vs. Miller–Rabin. {cite:p}`rabin1980probabilisticalgorithmprimality,agrawalkayalsaxena2004primesisinp`
- **Progressions:** frequency of 3-term prime APs in ranges; maximal AP length in a window. {cite:p}`greentao2008primesarithmeticprogressions`

For “ground truth” sequences and curated lists, OEIS and PrimePages are practical reference points. {cite:p}`OEIS2025A001223PrimeGaps,OEIS2025A001097TwinPrimes,Caldwell2000PrimeGapsPrimePages`

## Practical numerical caveats

- **Pick the right primitive:** if you need *many* primes up to $N$, use a sieve; if you need primality of a few large numbers, use primality testing.
- **Memory matters for sieves:** a naive boolean list of length $N$ can be huge; segmented sieves avoid this.
- **State what “prime” means in code:** if you use Miller–Rabin, your results are “probable primes” unless you add a deterministic guarantee for your size range. {cite:p}`rabin1980probabilisticalgorithmprimality`
- **Avoid floating-point traps:** use natural logs, guard against $\log(0)$, and remember that $\log x$ changes slowly.
- **Be precise with pair-counting:** decide whether you count pairs by their smaller prime $p$ (common), and avoid double-counting.
- **Separate discovery from verification:** for pattern-hunting (e.g., long APs), do fast screening first, then verify candidates carefully.

## References

See {doc}`../references`.

{cite:p}`hardywright2008introtheorynumbers,apostol1976introanalyticnumbertheory,crandallpomerance2005primenumberscomputationalperspective,rosserschoenfeld1962approximateformulasprimefunctions,dusart2018explicitestimatesfunctionsprimes,hardylittlewood1923partitionumerorumIII,cramer1936orderofmagnitudedifferenceconsecutiveprimes,zhang2014boundedgapsbetweenprimes,maynard2015smallgapsbetweenprimes,polymath2014boundedgapsbetweenprimes,greentao2008primesarithmeticprogressions,rabin1980probabilisticalgorithmprimality,agrawalkayalsaxena2004primesisinp`
