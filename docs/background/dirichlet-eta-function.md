# Dirichlet eta function η(s)

The **Dirichlet eta function** is the alternating Dirichlet series
$$
\eta(s)=\sum_{n\ge 1} \frac{(-1)^{n-1}}{n^s},
$$
which converges for \(\Re(s)>0\) (by alternating-series arguments). It is related to the Riemann zeta function by
$$
\eta(s) = \left(1-2^{1-s}\right)\zeta(s).
$$

## Key ideas

- **Faster convergence:** for real \(s>1\), the alternating series often converges more rapidly than the plain ζ-series.
- **Analytic continuation:** the identity above provides an analytic continuation of ζ(s) away from the factor \(1-2^{1-s}\).
- **Numerical gateway:** η(s) is a convenient “entry point” for simple ζ(s) numerics without complex contour methods.

## Why it matters in this project

When we want quick, small-scale experiments (e.g. comparing partial sums, smoothing, or convergence acceleration), η(s) provides stable numerics with minimal infrastructure.

## Experiments in this repository

- **E114** — ζ(1/2+it) via η(s): truncation/precision stability map.

## References

See {doc}`../references`.

{cite:p}`edwards1974,titchmarsh1986,WikipediaContributors2025RiemannZetaFunction`
