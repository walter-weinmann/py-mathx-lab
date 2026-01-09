# Euler’s prime-generating polynomial refresher

One of the most famous “too good to be true” examples in experimental number theory is Euler’s quadratic

$$
f(n)=n^2+n+41.
$$

For integers $n=0,1,\dots,39$ it produces **prime numbers**. This is an unusually long initial run for such
a simple polynomial, and it remains a classic motivation for computational “prime-value” experiments.
{cite:p}`WikipediaContributors2025LuckyNumbersOfEuler,Weisstein2025EulerPrimeMathWorld`

## The basic facts

- For $0\le n\le 39$, $f(n)$ is prime.
- At $n=40$,
  $$
  f(40)=40^2+40+41=1681=41^2,
  $$
  so the prime streak stops immediately afterward. {cite:p}`Weisstein2025EulerPrimeMathWorld`

(You will also see the equivalent form $n^2-n+41$ in the literature; it is just a shift:
$n^2-n+41 = f(n-1)$.)

## What “prime-producing polynomial” can mean

The phrase *prime-producing* is used in three different (and easily confused) ways:

1. **Prime for every integer input.**  
   Apart from constant polynomials (e.g. $f(n)=2$), this is impossible for integer polynomials.
   {cite:p}`HardyWright2008AnIntroductionToTheTheoryOfNumbers`

2. **Prime for a long initial run.**  
   This is what Euler’s polynomial does: it produces primes for many *consecutive* values, but not forever.
   {cite:p}`WikipediaContributors2025LuckyNumbersOfEuler`

3. **Prime infinitely often.**  
   Here the goal is not “always prime”, but “infinitely many $n$ with $f(n)$ prime”. For degree $1$,
   Dirichlet’s theorem proves this (arithmetic progressions). For degree $\ge 2$ it is open in general,
   and conjectures (Bunyakovsky, Bateman–Horn) give a framework and quantitative predictions.
   {cite:p}`dirichlet1837primesinprogressions,WikipediaContributors2025BunyakovskyConjecture,BatemanHorn1962HeuristicAsymptoticFormula`

In experimental projects it helps to state explicitly which of the three you mean, because they lead to
very different “success criteria” and plots.

## Why a nonconstant integer polynomial cannot be prime for all integers

Let $f\in\mathbb{Z}[x]$ be nonconstant. Pick any integer $m$ with $|f(m)|>1$ (such an $m$ exists because
a nonconstant polynomial is unbounded). Consider the values

$$
f\bigl(m + k\,f(m)\bigr), \qquad k=1,2,3,\dots
$$

Because $m+kf(m)\equiv m\pmod{f(m)}$ and $f$ has integer coefficients, we get the congruence

$$
f\bigl(m + k\,f(m)\bigr) \equiv f(m) \pmod{f(m)}.
$$

So $f(m)$ divides $f(m+kf(m))$. For all sufficiently large $k$ the absolute value
$\bigl|f(m+kf(m))\bigr|$ is strictly larger than $|f(m)|$, hence $f(m+kf(m))$ has a nontrivial divisor
and is composite. This shows:

> No nonconstant polynomial with integer coefficients can take prime values for all integers.

This simple divisibility trick is one of the reasons why Euler’s streak is remarkable but still
compatible with the “no prime for all inputs” principle. {cite:p}`HardyWright2008AnIntroductionToTheTheoryOfNumbers`

## Why Euler’s quadratic has such a long streak

Two complementary explanations are useful:

### 1) A built-in factor at $n=40$

The identity
$$
f(n) \equiv 0 \pmod{41} \quad\text{when } n\equiv 40 \pmod{41}
$$
is not an accident: the first failure happens exactly at $n=40$ where $f(40)=41^2$.

More generally, for any prime $q$, the set of residues $n\bmod q$ for which $f(n)\equiv 0\pmod q$ forms
a “local obstruction”: every such residue forces a composite value (unless the value equals $q$ itself).
Counting and visualizing these local obstructions is often the fastest way to understand why some
polynomials are “better” prime generators than others.

### 2) An algebraic number theory viewpoint (Heegner number 163)

Euler’s polynomial is naturally a **norm form** in the quadratic field $\mathbb{Q}(\sqrt{-163})$.
Let
$$
\omega = \frac{1+\sqrt{-163}}{2}.
$$
Then the (field) norm satisfies
$$
N(n+\omega) = (n+\omega)(n+\overline{\omega}) = n^2+n+41 = f(n).
$$

The discriminant here is $-163$, and $163$ is a **Heegner number**: the ring of integers of
$\mathbb{Q}(\sqrt{-163})$ has class number $1$, i.e. it enjoys unique factorization.
This special property is one reason the prime streak for $41$ is unusually long compared to “random”
quadratics. {cite:p}`WikipediaContributors2025HeegnerNumber,Weisstein2025HeegnerNumberMathWorld,Cox2013PrimesOfTheFormX2PlusNY2`

A classical theorem of Rabinowitsch makes the link precise: for a prime $p$, the polynomial
$n^2+n+p$ produces primes for $n=0,\dots,p-2$ **if and only if** the discriminant $1-4p$ is the negative
of a Heegner number. In particular, $p=41$ corresponds to $1-4p=-163$. {cite:p}`WikipediaContributors2025HeegnerNumber`

This is also why the so-called *lucky numbers of Euler* are exactly
$2,3,5,11,17,41$. {cite:p}`WikipediaContributors2025LuckyNumbersOfEuler,Weisstein2025LuckyNumberOfEulerMathWorld`

## Prime values infinitely often: what we believe (and what is known)

Euler’s polynomial fails to be prime eventually, but it is widely believed to take **prime values
infinitely often**. Proving this is currently out of reach for essentially any polynomial of degree
$\ge 2$.

A standard “minimal sanity check” for a polynomial $f\in\mathbb{Z}[x]$ to have infinitely many prime
values is:

- **(irreducible)** $f$ should be irreducible over $\mathbb{Q}$,
- **(no fixed prime divisor)** the gcd of the integer values $f(0),f(1),f(2),\dots$ should be $1$.

Bunyakovsky’s conjecture asserts that these necessary conditions are also sufficient.
{cite:p}`WikipediaContributors2025BunyakovskyConjecture`

Bateman–Horn goes further and predicts an asymptotic density: roughly,
the count of primes among $f(1),\dots,f(N)$ should be

$$
\sim C(f)\,\int_2^N \frac{dt}{\log f(t)},
$$

where $C(f)$ is an explicit constant built from local obstruction data modulo each prime.
{cite:p}`BatemanHorn1962HeuristicAsymptoticFormula`

For experiments, this is extremely useful: it gives you a quantitative “expected curve” to plot against
your observed prime counts.

## What to experiment with

A few experiment ideas that scale from quick checks to deeper projects:

- **Streak length across Euler’s form:** for primes $p$, measure the length of the initial prime run of
  $n^2+n+p$ and compare $p\in\{2,3,5,11,17,41\}$ to nearby primes.
  {cite:p}`WikipediaContributors2025LuckyNumbersOfEuler,WikipediaContributors2025HeegnerNumber`

- **Local obstruction profile:** for each small prime $q$, count the number of solutions to
  $f(n)\equiv 0\pmod q$ and visualize the “obstruction density” across $q$.

- **Bateman–Horn calibration:** empirically estimate $C(f)$ from a truncated Euler product over small
  primes and compare Bateman–Horn’s predicted prime count against the observed count.

- **Baselines:** compare Euler’s polynomial against random quadratics $n^2+an+b$ with the same size
  of coefficients, filtered by “no fixed prime divisor”, so you can see what is truly special and what
  is selection bias.

## Practical numerical caveats

- **Big integers:** $f(n)$ grows like $n^2$; primality testing dominates runtime quickly.
- **Avoid accidental float conversion:** keep $n$ and $f(n)$ as Python integers throughout.
- **Sampling bias:** focusing only on “nice-looking” polynomials can be misleading; compare against
  random baselines rather than only showcasing “winners”.

## References

See {doc}`../references`.

{cite:p}`WikipediaContributors2025LuckyNumbersOfEuler,Weisstein2025EulerPrimeMathWorld,HardyWright2008AnIntroductionToTheTheoryOfNumbers,WikipediaContributors2025BunyakovskyConjecture,BatemanHorn1962HeuristicAsymptoticFormula,WikipediaContributors2025HeegnerNumber,Weisstein2025HeegnerNumberMathWorld,Cox2013PrimesOfTheFormX2PlusNY2,Weisstein2025LuckyNumberOfEulerMathWorld,dirichlet1837primesinprogressions`
