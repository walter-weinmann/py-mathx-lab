# Valid Tags

This page defines the allowed tags for experiments in **py-mathx-lab**. Tags are used in the {doc}`experiments/experiments_gallery` and individual experiment pages to categorize content.

## Primary Tags (Domains)

These represent the broad mathematical area of the experiment.

| Tag                        | Description                                                 |
|:---------------------------|:------------------------------------------------------------|
| `analysis`                 | Calculus, real/complex analysis, limits, and approximation. |
| `conjecture-generation`    | Patterns suggest statements that might be true (or false).  |
| `counterexample-search`    | Systematic exploration tries to break a hypothesis early.   |
| `model-checking`           | Validate (or invalidate) approximations and heuristics.     |
| `number-theory`            | Properties of integers, divisibility, and prime numbers.    |
| `quantitative-exploration` | Estimate constants, rates, limits, or distributions.        |
| `visualization`            | Reveal structure that is hard to see symbolically.          |

## Secondary Tags

- `carmichael` — Carmichael numbers (absolute Fermat pseudoprimes).
- `factorization` — Integer factorization methods and hardness.
- `fermat` — Fermat numbers and Fermat primes.
- `primorial` — Primorials, Euclid numbers, primorial primes.
- `pseudoprime` — Pseudoprimes, primality-test failures.
- `semiprime` — Semiprimes, RSA-type composites.
- `wieferich` — Wieferich primes and related congruences.

These provide more specific detail about the techniques or sub-topics involved.

| Tag              | Description                                                      |
|:-----------------|:-----------------------------------------------------------------|
| `classification` | Grouping objects into classes based on shared properties.        |
| `exploration`    | Open-ended search for patterns or properties.                    |
| `numerics`       | Heavy use of floating-point or high-precision computation.       |
| `open-problems`  | Related to famous unproven conjectures.                          |
| `optimization`   | Finding maxima, minima, or best-fit parameters.                  |
| `perfect`        | Related specifically to perfect, abundant, or deficient numbers. |
| `search`         | Systematic search through a large state space.                   |
| `sigma`          | Related to the sum-of-divisors function $\sigma(n)$.             |
| `taylor`         | Related to Taylor series and their approximations.               |

## Usage

When adding a new experiment:
1. Choose at least one **Primary Tag** (Domain or Type).
2. Choose one or more **Secondary Tags** (Topics & Methods).
3. Add them to the `**Tags:**` line in your `.md` file.
4. Update the {doc}`experiments/experiments_gallery` using the corresponding CSS classes (`tag-primary` for primary tags, `tag-secondary` for secondary tags).
