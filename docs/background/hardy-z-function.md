# Hardy's Z-function and the critical line

For real \(t\), the **Hardy Z-function** is defined (up to standard conventions) by
$$
Z(t)=e^{i\theta(t)}\,\zeta\!\left(\tfrac12+it\right),
$$
where \(\theta(t)\) is the Riemann--Siegel theta function. The key feature is that **Z(t) is real-valued for real t**, so zeros of \(Z(t)\) correspond to zeros of ζ(s) on the critical line.

## Key ideas

- **Real signal:** studying sign changes of \(Z(t)\) is a practical way to bracket zeros on \(\Re(s)=\tfrac12\).
- **Theta function:** \(\theta(t)\) captures the “oscillatory phase” of ζ on the critical line and is closely tied to Gram points.
- **Numerical workflows:** many computational approaches to zeta zeros are formulated in terms of \(Z(t)\), \(\theta(t)\), and their approximations.

## Why it matters in this project

It gives a clean, visualization-friendly path from “complex ζ-values” to “real curves” whose roots can be bracketed and counted.

## Experiments in this repository

- **E115** — Hardy Z sign-change scan and zero bracketing (bisection refinement).

## References

See {doc}`../references`.

{cite:p}`titchmarsh1986,odlyzko1992zeta10to20thzero,WikipediaContributors2025ZFunction,WikipediaContributors2025RiemannVonMangoldtFormula`
