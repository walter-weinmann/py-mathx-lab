# Gram points and zero counting

A **Gram point** is (informally) a value \(t\) where the Riemann--Siegel theta function \(\theta(t)\) hits an integer multiple of \(\pi\). These points are useful landmarks when visualizing \(Z(t)\) and tracking sign changes.

The **Riemann--von Mangoldt formula** gives the asymptotic count of nontrivial zeros up to height \(T\):
$$
N(T)=\frac{T}{2\pi}\log\!\left(\frac{T}{2\pi}\right)-\frac{T}{2\pi}+O(\log T)\quad (T\to\infty),
$$
with refinements that include the argument of ζ on the critical line.

## Key ideas

- **Bookkeeping:** zero counting provides a “sanity check” for numerical root-finding: we can compare a computed zero list against \(N(T)\).
- **Gram blocks / Gram's law:** empirical rules about how zeros sit between consecutive Gram points (useful, but not always true).
- **Practical numerics:** many experiments become clearer when plotted against \(\theta(t)\) or indexed by Gram points.

## Experiments in this repository

- **E116** — Observed zero counts (via sign changes) vs Riemann–von Mangoldt estimate.

## References

See {doc}`../references`.

{cite:p}`titchmarsh1986,odlyzko1992zeta10to20thzero,WikipediaContributors2025RiemannVonMangoldtFormula,WikipediaContributors2025ZFunction`
