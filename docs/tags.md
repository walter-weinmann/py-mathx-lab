# Valid Tags

This page defines the allowed tags for experiments in **py-mathx-lab**. Tags are used in the
{doc}`experiments/experiments_gallery` and individual experiment pages to categorize content.

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

## Secondary Tags (Topics & Methods)

These provide more specific detail about the techniques or sub-topics involved.

| Tag                    | Description                                                             |
|:-----------------------|:------------------------------------------------------------------------|
| `arithmetic-functions` | Classical functions on integers (e.g., φ, μ, σ, τ) and their relations. |
| `carmichael`           | Carmichael numbers (absolute Fermat pseudoprimes).                      |
| `classification`       | Grouping objects into classes based on shared properties.               |
| `dirichlet-series`     | Dirichlet generating functions and related analytic tools.              |
| `exploration`          | Open-ended search for patterns or properties.                           |
| `factorization`        | Integer factorization methods and hardness.                             |
| `fermat`               | Fermat numbers and Fermat primes.                                       |
| `generating-functions` | Ordinary/exponential generating functions (esp. partitions).            |
| `mobius`               | Möbius function μ(n), Möbius inversion, squarefree indicators.          |
| `multiplicative`       | Multiplicative arithmetic functions; Dirichlet convolution viewpoints.  |
| `numerics`             | Heavy use of floating-point or high-precision computation.              |
| `open-problems`        | Related to famous unproven conjectures.                                 |
| `optimization`         | Finding maxima, minima, or best-fit parameters.                         |
| `partition`            | Partition function p(n), identities, and asymptotics.                   |
| `perfect`              | Related specifically to perfect, abundant, or deficient numbers.        |
| `primorial`            | Primorials, Euclid numbers, primorial primes.                           |
| `pseudoprime`          | Pseudoprimes, primality-test failures.                                  |
| `search`               | Systematic search through a large state space.                          |
| `semiprime`            | Semiprimes, RSA-type composites.                                        |
| `sigma`                | Related to the sum-of-divisors function $\sigma(n)$.                    |
| `summatory`            | Summatory functions (e.g., Mertens M(x), summatory totient Φ(x)).       |
| `taylor`               | Related to Taylor series and their approximations.                      |
| `totient`              | Euler’s totient function φ(n), totient equations, summatory behavior.   |
| `wieferich`            | Wieferich primes and related congruences.                               |

## Usage

When adding a new experiment:
1. Choose at least one **Primary Tag** (Domain or Type).
2. Choose one or more **Secondary Tags** (Topics & Methods).
3. Add them to the `**Tags:**` line in your `.md` file.
4. Update the {doc}`experiments/experiments_gallery` using the corresponding CSS classes
   (`tag-primary` for primary tags, `tag-secondary` for secondary tags).
