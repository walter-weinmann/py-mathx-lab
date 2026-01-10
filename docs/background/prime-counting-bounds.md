# Prime counting: explicit bounds (not just asymptotics)

Prime counting experiments often start from approximations (PNT-style) such as $x/\log x$.
For Phase 2, we also want **explicit inequalities**: formulas that are proven to hold for all $x$ in a stated range.

This page focuses on how to use explicit bounds correctly in experiments:

- put the bound formula in the report,
- name the theorem/source,
- verify it numerically on the plotted range,
- and avoid overselling asymptotic statements at small $x$.

## The prime counting function

Let

$$\pi(x) = \#\{p \le x : p \text{ prime}\}.$$

For approximations, see {doc}`prime-counting-approximations`.

## Example: Dusart-style explicit bounds

A convenient family of explicit bounds uses expansions in $1/\log x$.
For example, Dusart gives (among many results) inequalities of the form:

$$\pi(x) \ge \frac{x}{\log x}\left(1 + \frac{1}{\log x}\right) \quad \text{for } x > 599,$$

and

$$\pi(x) \le \frac{x}{\log x}\left(1 + \frac{1.2762}{\log x}\right) \quad \text{for } x > 1.$$

(See Theorem 6.9 in {cite}`dusart2010estimatesfunctionsoverprimes`.)

These bounds are not the tightest known, but they are easy to implement and they demonstrate the discipline: **formula + validity range**.

## Stronger bounds exist

Classical work such as Rosser--Schoenfeld provides explicit inequalities for $\pi(x)$ and related functions. See {cite}`rosserschoenfeld1962approximateformulasprimefunctions`.
More recent refinements and alternative explicit estimates are discussed in {cite}`dusart2018explicitestimatesfunctionsprimes`.

## How to use a bound in an experiment

### 1) Put the theorem statement in the report

In `out/e###/report.md`, include:

- the exact inequality you implemented,
- the stated validity range,
- and the precise meaning of symbols (e.g. natural log).

### 2) Verify numerically on your plotted range

If you plot $\pi(x)$ and a bound $B(x)$ on $x \in [A,B]$, then verify the inequality on that same grid:

- check `pi(x) <= B(x)` (or the other direction) at each grid point,
- report the first violation (if any) as a witness.

This does **not** prove the theorem, but it catches implementation mistakes.

### 3) State the range where the bound becomes meaningful

A bound can be true but useless for small $x$.
To report "where it becomes meaningful", pick an operational criterion.
For example:

- relative gap `|B(x) - pi(x)| / pi(x) <= 0.05`, or
- relative gap compared to $x/\log x$, or
- a fixed vertical error tolerance.

Then report the smallest $x$ in your sampled range where the criterion holds.
Label this as **finite-range behavior**.

### 4) Avoid asymptotic overclaims

Statements like "$\pi(x) \sim x/\log x$" are asymptotic.
They describe what happens as $x \to \infty$.
In reports and captions:

- keep the phrase "asymptotic" for the theory statement,
- and use "finite-range behavior" for what your plot shows.

## How this connects to experiments

- Approximations and PNT-style plots: {doc}`prime-counting-approximations`
- Arithmetic progressions and prime races: {doc}`primes-in-arithmetic-progressions`, {doc}`prime-number-races`

## References

See {doc}`../references`.
