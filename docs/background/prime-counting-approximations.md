# Prime counting approximations: π(x), Li(x), and R(x)

The prime-counting function \(\pi(x)\) counts primes up to \(x\). Two standard smooth approximations are:

- the **logarithmic integral** \(\mathrm{Li}(x)\), and
- **Riemann's R function** \(R(x)\) (a Möbius-weighted combination of \(\mathrm{Li}(x^{1/n})\)).

These approximations are central for numerical experiments around the Prime Number Theorem, error terms, and the visual “shape” of prime races.

## Key ideas

- **PNT baseline:** \(\pi(x)\sim \frac{x}{\log x}\), and \(\mathrm{Li}(x)\) is often an excellent smooth baseline.
- **R(x) as a refinement:** R(x) folds in prime-power information and is closely connected to explicit-formula viewpoints.
- **Error terms:** plotting \(\pi(x)-\mathrm{Li}(x)\) or \(\psi(x)-x\) reveals oscillations and sign changes.

## References

See {doc}`../references`.

{cite:p}`titchmarsh1986,WikipediaContributors2025PrimeCountingFunction`
