# Divisibility and modular arithmetic (Phase 2 core)

This page is the *toolbox layer* for elementary number theory experiments:
**divisibility**, **gcd**, **congruences**, **residue classes**, and **modular inverses** appear
in primality testing, factorization, and prime-distribution checks.

References for standard results:
{cite:p}`apostol1976introanalyticnumbertheory,nivenzuckermanmontgomery1991introductiontheorynumbers`.

## Divisibility

For integers $a$ and $b$ with $b \ne 0$, we say **$b$ divides $a$** (written $b \mid a$) if
there exists an integer $k$ such that $a=bk$.

Basic closure rules used constantly:

- If $b\mid a$ and $b\mid c$, then $b\mid (a\pm c)$.
- If $b\mid a$, then $b\mid ac$ for any integer $c$.
- If $b\mid a$ and $a\mid b$, then $|a|=|b|$.

## Greatest common divisor (gcd)

The **greatest common divisor** of $a$ and $b$, written $\gcd(a,b)$, is the largest positive
integer $d$ such that $d\mid a$ and $d\mid b$.

We call $a$ and $b$ **coprime** if $\gcd(a,b)=1$.

### Bézout identity (extended gcd)

There exist integers $x,y$ such that
\[
\gcd(a,b)=ax+by.
\]

This identity is what enables **modular inverses** and appears directly in many algorithms
(e.g. computing inverses for modular division).

### Euclidean algorithm

If $a=bq+r$ with $0\le r<|b|$, then
\[
\gcd(a,b)=\gcd(b,r).
\]
Repeatedly applying this step gives the Euclidean algorithm, which runs in time
polynomial in the number of digits of the input.

## Congruences and residue classes

For integers $a,b$ and modulus $m\ge 1$,
\[
a\equiv b\pmod m
\quad\Longleftrightarrow\quad
m\mid (a-b).
\]

This is an equivalence relation; its equivalence classes are called the
**residue classes modulo $m$**.

In computations, we usually represent residues by integers in $\{0,1,\dots,m-1\}$.
That is a *representation choice*; the underlying object is the residue class.

### Arithmetic modulo $m$

If $a\equiv a'\pmod m$ and $b\equiv b'\pmod m$, then:

- $a+b\equiv a'+b'\pmod m$
- $ab\equiv a'b'\pmod m$

So addition and multiplication “mod $m$” are well-defined.

## Units and modular inverses

An integer $a$ has a multiplicative inverse modulo $m$ if and only if
\[
\gcd(a,m)=1.
\]
In that case, there exists $a^{-1}$ such that
\[
aa^{-1}\equiv 1\pmod m.
\]

In code, compute $a^{-1}$ via the extended Euclidean algorithm
(Bézout coefficients).

**Important practical note:** if $\gcd(a,m)\ne 1$, then “division by $a$ modulo $m$”
is not defined.

## Euler’s totient function and Euler’s theorem

Let $\varphi(m)$ be the number of integers in $\{1,\dots,m\}$ that are coprime to $m$.
Then **Euler’s theorem** states:
\[
\gcd(a,m)=1 \;\Rightarrow\; a^{\varphi(m)}\equiv 1\pmod m.
\]
This generalizes Fermat’s little theorem (below) and is a conceptual bridge between
congruences and multiplicative structure.

## Fermat’s little theorem (FLT)

If $p$ is prime and $p\nmid a$, then
\[
a^{p-1}\equiv 1\pmod p.
\]

FLT motivates Fermat-style primality tests, but there are composite numbers that can still
pass such tests (pseudoprimes, especially Carmichael numbers). See {doc}`carmichael-numbers`.

## Modular exponentiation (what you implement)

Nearly every algorithm in this phase needs fast computation of $a^e\bmod m$.

Use **binary exponentiation** (“square-and-multiply”), which evaluates $a^e$ in
$O(\log e)$ modular multiplications.

Practical checklist for implementations:

- Reduce $a$ modulo $m$ once at the start.
- Use repeated squaring; never compute $a^e$ as a huge integer first.
- Use constant-time or side-channel-resistant variants only if you have a security goal
  (this project typically does not).

## Chinese remainder theorem (CRT)

If $m$ and $n$ are coprime, then for any residues $a\pmod m$ and $b\pmod n$,
there exists a unique residue $x\pmod{mn}$ such that
\[
x\equiv a\pmod m,\qquad x\equiv b\pmod n.
\]
Equivalently, the ring $\mathbb{Z}/(mn)\mathbb{Z}$ “splits” into
$\mathbb{Z}/m\mathbb{Z}\times \mathbb{Z}/n\mathbb{Z}$ when $\gcd(m,n)=1$.

CRT is the conceptual reason that many modular phenomena can be studied prime-power by prime-power.
It is also a common proof tool for counterexamples and constructions.

## How this connects to Phase 2 experiments

- **Primality tests**: Fermat and Miller–Rabin use modular exponentiation and gcd checks.
- **Factorization**: Pollard–$\rho$ uses repeated modular iteration and gcd($|x-y|,n$).
- **Residue classes**: counting primes in residue classes is literally “arithmetic modulo $m$”.

Suggested related pages:

- {doc}`prime-numbers`
- {doc}`primality-testing`
- {doc}`semiprimes`
- {doc}`carmichael-numbers`
- {doc}`prime-counting-approximations`
