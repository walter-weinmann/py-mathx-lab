# Riemann zeta function ζ(s)

The **Riemann zeta function** ζ(s) is the Dirichlet series
\[
\zeta(s)=\sum_{n\ge 1} \frac{1}{n^s},
\]
which converges for \(\Re(s)>1\) and extends (by analytic continuation) to a meromorphic function on \(\mathbb{C}\) with a single simple pole at \(s=1\).

## Key ideas

- **Euler product (primes):** for \(\Re(s)>1\),
  \[
  \zeta(s)=\prod_{p\ \text{prime}}\frac{1}{1-p^{-s}},
  \]
  linking ζ(s) directly to prime distribution.
- **Functional equation:** ζ(s) satisfies a symmetry relating \(s\) and \(1-s\), which is central for studying zeros.
- **Zeros:** ζ(s) has *trivial zeros* at negative even integers and *nontrivial zeros* in the critical strip \(0<\Re(s)<1\), conjecturally all on the critical line \(\Re(s)=\tfrac12\) (Riemann Hypothesis).

## Why it matters in this project

Many “analytic prime number theory” numerics (prime counting approximations, explicit formulas, prime races, etc.) are most naturally expressed in terms of ζ(s), its logarithmic derivative, and its zeros.

## References

- cite:p:`titchmarsh1986zeta`
- cite:p:`edwards1974zeta`
- cite:p:`ivic1985zeta`
- cite:p:`WikipediaContributors2025RiemannZetaFunction`
