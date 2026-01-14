# Dirichlet’s theorem and PNT(AP) in the form used by the experiments

This page is the Phase 2 background for experiments about primes in residue classes and prime races.
It states Dirichlet’s theorem and the prime number theorem in arithmetic progressions (PNT(AP))
*exactly in the normalization used by the experiments*:

- baseline: $\mathrm{li}(x)/\varphi(q)$,
- error plots: $\pi(x;q,a)-\mathrm{li}(x)/\varphi(q)$ (and derived race differences).

## The counting function $\pi(x;q,a)$

Fix integers $q\ge 1$ and $a$. Define
$$
\pi(x;q,a) := \#\{p\le x : p\ \text{prime and}\ p\equiv a\pmod q\}.
$$

Only **reduced residue classes** participate in the classical equidistribution theorems:

- If $\gcd(a,q)=1$, then the congruence class $a\bmod q$ contains infinitely many primes.
- If $\gcd(a,q)>1$, then the class contains at most one prime (the common divisor itself), so it is not part of the PNT(AP) story.

Let
$$
(\mathbb{Z}/q\mathbb{Z})^\times = \{a\bmod q : \gcd(a,q)=1\}
$$
denote the reduced residue system, and let $\varphi(q)=\#(\mathbb{Z}/q\mathbb{Z})^\times$ be Euler’s totient.

## The baseline $\mathrm{li}(x)/\varphi(q)$

The logarithmic integral is
$$
\mathrm{li}(x) := \operatorname{PV}\int_0^x \frac{dt}{\log t}.
$$

In numerical work one often uses the “offset” version
$$
\mathrm{Li}(x) := \int_2^x \frac{dt}{\log t},
$$
and treats the two as essentially the same baseline for large $x$ (they differ by a constant).
Phase 2 uses the baseline in the form
$$
\text{baseline}(x;q) := \frac{\mathrm{li}(x)}{\varphi(q)}.
$$

**Interpretation:** if primes are “evenly spread” across the $\varphi(q)$ reduced residue classes, then each class should get about a $1/\varphi(q)$ share of the total prime mass predicted by $\mathrm{li}(x)$.

## Dirichlet’s theorem (existence of primes in each reduced residue class)

**Theorem (Dirichlet, 1837).** If $\gcd(a,q)=1$, then there are infinitely many primes $p$ such that
$p\equiv a\pmod q$.

This is the minimal statement the experiments rely on: every reduced residue class shows up forever,
so “race leaders” can change infinitely often in principle.

### Why characters and $L$-functions enter (one paragraph)

The proof introduces Dirichlet characters $\chi\bmod q$ and their $L$-functions
$$
L(s,\chi) = \sum_{n\ge 1}\frac{\chi(n)}{n^s}\qquad (\Re(s)>1),
$$
and shows that for **nonprincipal** characters $\chi$, the value $L(1,\chi)$ is nonzero.
Using character orthogonality, one can express the indicator of a residue class $a\bmod q$ as an average over characters,
which lets one “filter primes by congruence class” and prove that every reduced class contains infinitely many primes.

## Prime number theorem in arithmetic progressions (equidistribution)

Dirichlet’s theorem says primes exist in each reduced class; PNT(AP) says they are *asymptotically equidistributed*.

**Theorem (PNT(AP), fixed modulus form).** Fix $q\ge 1$ and let $\gcd(a,q)=1$. Then, as $x\to\infty$,
$$
\pi(x;q,a) \sim \frac{\mathrm{li}(x)}{\varphi(q)}.
$$

Equivalently, the difference
$$
E(x;q,a) := \pi(x;q,a) - \frac{\mathrm{li}(x)}{\varphi(q)}
$$
is “small compared to” $\mathrm{li}(x)/\varphi(q)$ in the limit $x\to\infty$.

## The experiment’s error-term plots

Most Phase 2 plots are based on $E(x;q,a)$. Typical visualizations include:

- **Raw error:** plot $E(x;q,a)$ vs $x$.
- **Multiple residues:** plot $E(x;q,a)$ for several $a\in(\mathbb{Z}/q\mathbb{Z})^\times$ on the same axes.
- **Race differences (baseline cancels):** for two residues $a,b$ define
  $$
  \Delta(x;q,a,b) := \pi(x;q,a)-\pi(x;q,b) = E(x;q,a)-E(x;q,b).
  $$

So, race experiments are directly about comparing error terms across residues.

### What size should $E(x;q,a)$ have? (qualitative)

For the ranges used in computational experiments, it is normal that $E(x;q,a)$ oscillates and does not look “small” pointwise.
The key phenomenon is not monotone convergence but **oscillation around the baseline**.

A useful benchmark statement (not required for running the experiments, but helpful for interpretation) is:
under GRH one expects roughly
$$
E(x;q,a) = O\!\left(\sqrt{x}\,\log x\right)
$$
for fixed $q$ (and more refined uniform statements are known with restrictions on $q$).
This heuristic explains why, even when $\pi(x;q,a)$ is close to the baseline in relative terms, the raw difference can still have visible swings.

## How $L$-function zeros explain oscillations (high level)

A guiding principle is: **zeros of Dirichlet $L$-functions drive oscillations in residue-class prime counts**.
Very roughly, character orthogonality lets you write “error terms in a class” as sums over contributions from nonprincipal characters,
and analytic number theory relates those contributions to the zeros of $L(s,\chi)$.
You do not need to compute zeros for Phase 2, but this explains why race plots can show long-lasting biases and sign changes.

## Practical numerical notes for experiments

- Always restrict to $a$ with $\gcd(a,q)=1$ when discussing equidistribution or races.
- Sampling matters: using a linear grid in $x$ vs a log grid in $x$ weights different ranges differently and can change “leader fractions”.
- If you approximate $\mathrm{li}(x)$ numerically, document the method and keep it consistent across experiments (baseline consistency matters more than ultimate accuracy for qualitative plots).

## References

See {doc}`../references`.

{cite:p}`dirichlet1837primesinprogressions,davenport2000multiplicativenumbertheory,montgomeryvaughan2006multiplicativenumbertheoryi,iwanieckowalski2004analyticnumbertheory`

## Experiments in this repository

- **E070** — $\pi(x;q,a)$ for several reduced residue classes (baseline comparison).
- **E071** — $E(x;q,a)=\pi(x;q,a)-\mathrm{li}(x)/\varphi(q)$ error-term plots.
- **E072–E075** — Prime races and race distributions (differences of $\pi(x;q,a)$).
- **E081** — Effect of modulus on PNT(AP) error behavior (comparative error plots).
