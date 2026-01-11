# Primality testing: guarantees, error bounds, and what to report

This page explains how we talk about primality tests in **py-mathx-lab**:
what is guaranteed, what is probabilistic, and what must be recorded in experiment reports.

Core references:
{cite:p}`crandallpomerance2005primenumberscomputationalperspective,rabin1980probabilisticalgorithmprimality`.

## Deterministic vs probabilistic (project language)

A primality test can have different guarantees:

- **Deterministic**: returns the correct answer for every input in its stated domain.
- **Probabilistic (one-sided error)**:  
  - If it returns **composite**, that is *always correct*.  
  - If it returns **probably prime**, that can be wrong with some probability.

**Project reporting rule:** every experiment that uses a probabilistic test must state:

- “probabilistic vs deterministic” (and the domain if deterministic),
- bases / rounds used,
- a conservative error probability statement (when available),
- and known counterexamples / failure modes when applicable.

(Practically: put this into `out/e###/report.md` as a short, explicit section.)

## Fermat probable prime test (FPP)

For odd $n>2$ and a base $a$ with $\gcd(a,n)=1$, Fermat’s congruence says:
$$
a^{n-1}\equiv 1\pmod n
\quad\text{for prime } n.
$$

If the congruence fails, $n$ is composite (a **witness** was found).  
If it passes, $n$ is a **Fermat probable prime** to base $a$.

### Why Fermat alone is not reliable

There exist composite numbers that pass Fermat’s test for many bases.
In particular, **Carmichael numbers** pass the test for *all* bases coprime to $n$.
So Fermat is best treated as a **cheap pre-filter**, not a strong claim of primality.

See {doc}`carmichael-numbers`.

### Known counterexamples (Fermat)

- $341 = 11\cdot 31$ is a classic base-2 pseudoprime.
- $561 = 3\cdot 11\cdot 17$ is the smallest Carmichael number.

## Miller–Rabin (strong probable prime test)

Write
$$
n-1=d\,2^s\quad (d\text{ odd}).
$$
For a chosen base $a$, Miller–Rabin tests a short chain of squarings modulo $n$ and returns:

- **composite** (a witness was found), or
- **strong probable prime** to base $a$.

### Standard error bound (what you may claim)

For any odd composite $n$, at most one quarter of bases $a\in\{2,\dots,n-2\}$ can make $n$
look prime to the Miller–Rabin test. Therefore, if you test $k$ **independent random bases**,
$$
\Pr(\text{composite passes all }k\text{ rounds})\le 4^{-k}.
$$
This is the classical Rabin bound. {cite:p}`rabin1980probabilisticalgorithmprimality`

### Practical “deterministic” statements

Sometimes you will see statements like “Miller–Rabin is deterministic for 64-bit integers using
a fixed base set.” Such claims depend on **external results** that specify an input range and
a particular base set.

In this project:

- If you use **random bases**, treat MR as probabilistic and report $4^{-k}$.
- If you use a **fixed base list**, report it as an engineering choice, and only call it
  deterministic if your documentation *also* cites a theorem covering your input range.

## Pipeline viewpoint (how tests combine)

In experiments, primality tests often appear as components in a larger pipeline:

1. Handle trivial cases: $n<2$, even numbers, perfect squares.
2. Trial division up to a small bound (fast removal of tiny factors).
3. Miller–Rabin as a strong “probable prime” filter (with stated guarantee).
4. If composite but no factor found: a factor-finding step (e.g. Pollard–$\rho$) and recursion.

See {doc}`semiprimes` and {doc}`prime-numbers` for context.

## Report checklist (copy/paste into `report.md`)

Use a short section in `out/e###/report.md` that states:

- **Status**: deterministic vs probabilistic
- **Method**: Fermat / MR / combination
- **Bases / rounds**:
  - fixed list (write the list), or
  - random rounds $k$ (state how bases are sampled)
- **Error statement**:
  - MR random rounds: $P(\text{false prime})\le 4^{-k}$
  - Fermat: no uniform bound; mention Carmichael numbers
- **Correctness cross-check**:
  - compare decisions to a trusted reference on a CI-safe range
- **Known counterexamples / failure modes**:
  - include at least one concrete counterexample when relevant (e.g. 341, 561)

## References

- {cite:p}`crandallpomerance2005primenumberscomputationalperspective`
- {cite:p}`rabin1980probabilisticalgorithmprimality`
