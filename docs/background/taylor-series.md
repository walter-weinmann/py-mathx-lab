# Taylor series refresher

This page is a *beginner-friendly* refresher for experiments that use Taylor polynomials.
You only need basic calculus (derivatives) to follow it.

## Taylor polynomial

Assume $f$ has enough derivatives near $x_0$ (this is true for $\sin(x)$, $\cos(x)$, polynomials, exponentials, etc.). The Taylor polynomial of degree $n$ around $x_0$ is
$$
T_n(x; x_0) = \sum_{k=0}^{n} \frac{f^{(k)}(x_0)}{k!}\,(x-x_0)^k .
$$

**Intuition:** $T_n(x;x_0)$ is the polynomial that matches $f(x_0)$ and the first $n$ derivatives at $x_0$.
It is usually accurate when $x$ is close to $x_0$.

For $f(x)=\sin(x)$, the derivatives cycle, and around $x_0=0$ this becomes
$$
\sin(x) \approx x - \frac{x^3}{3!} + \frac{x^5}{5!} - \cdots .
$$
## Truncation error and the remainder

The approximation error is the remainder
$$
R_n(x; x_0) = f(x) - T_n(x; x_0).
$$
Under standard conditions, Taylor’s theorem gives a remainder representation. One common form is the
(Lagrange) remainder:
$$
R_n(x; x_0) = \frac{f^{(n+1)}(\xi)}{(n+1)!}\,(x-x_0)^{n+1}
\quad \text{for some } \xi \text{ between } x \text{ and } x_0 .
$$
This is the key qualitative message for experiments like E001:

- the factor $(x-x_0)^{n+1}$ makes the method **local** (good near $x_0$, potentially bad far away),
- increasing $n$ helps most where $|x-x_0|$ is small.

## What experiments typically visualize

In a numerical experiment, you often look at

- absolute error: $|R_n(x; x_0)|$
- relative error: $|R_n(x; x_0)| / |f(x)|$ (careful near zeros of $f$)

and plot them across a domain to see where the approximation is reliable.

## Practical numerical caveats

Even when the mathematics are correct, computation can mislead:

- large $|x-x_0|$ and high $n$ can produce huge intermediate terms,
- subtractive cancellation can reduce accuracy,
- floating-point rounding can dominate before the theoretical truncation error does.

A common “extension” experiment is to repeat the same plots using higher precision arithmetic to separate
*truncation error* from *rounding error*.

## Introductory reading

If you want a longer, *beginner-friendly* treatment (beyond this refresher), these are good starting points:

- A rigorous calculus textbook with a clean presentation of Taylor’s theorem and remainders: {cite:p}`Apostol1991CalculusVolume1`.
- A proof-oriented classic (slower, deeper): {cite:p}`Spivak2008Calculus`.
- For the numerical viewpoint (truncation vs. rounding error): {cite:p}`BurdenFaires2015NumericalAnalysis`.

## References

See {doc}`../references`.

{cite:p}`Apostol1991CalculusVolume1,Spivak2008Calculus,BurdenFaires2015NumericalAnalysis`
