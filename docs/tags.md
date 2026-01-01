# Valid Tags

This page defines the allowed tags for experiments in **py-mathx-lab**. Tags are used in the
{doc}`experiments/experiments_gallery` and individual experiment pages to categorize content.

## Primary Tags (Domains)

These represent the broad mathematical area of the experiment.

| Tag                        | Description                                                                          |
|:---------------------------|:-------------------------------------------------------------------------------------|
| `analysis`                 | Calculus, real/complex analysis, limits, and approximation.                          |
| `aps`                      | Arithmetic Progressions and related theorems.                                        |
| `conjecture-generation`    | Patterns suggest statements that might be true (or false).                           |
| `counterexample-search`    | Systematic exploration tries to break a hypothesis early.                            |
| `dirichlet-characters`     | Dirichlet characters modulo $q$, orthogonality, and primitive characters.            |
| `l-functions`              | Dirichlet $L$-functions and related analytic objects controlling prime distribution. |
| `model-checking`           | Validate (or invalidate) approximations and heuristics.                              |
| `number-theory`            | Properties of integers, divisibility, and prime numbers.                             |
| `prime-races`              | Prime number races (e.g., Chebyshev bias) comparing counts in residue classes.       |
| `quantitative-exploration` | Estimate constants, rates, limits, or distributions.                                 |
| `visualization`            | Reveal structure that is hard to see symbolically.                                   |

## Secondary Tags (Topics & Methods)

These provide more specific detail about the techniques or subtopics involved.

| Tag                     | Description                                                                                  |
|:------------------------|:---------------------------------------------------------------------------------------------|
| `arithmetic-functions`  | Classical functions on integers (e.g., $\phi$, $\mu$, $\sigma$, $\tau$) and their relations. |
| `bounds`                | Explicit mathematical bounds (e.g., on prime-counting functions).                            |
| `carmichael-lambda`     | Carmichael’s lambda function λ(n), the exponent of (Z/nZ)*.                                  |
| `carmichael`            | Carmichael numbers (absolute Fermat pseudoprimes).                                           |
| `classification`        | Grouping objects into classes based on shared properties.                                    |
| `critical-line`         | Zeta/L-function values on Re(s)=1/2 and related numerics.                                    |
| `dirichlet-convolution` | Dirichlet convolution of arithmetic functions and identity checks.                           |
| `dirichlet-series`      | Dirichlet generating functions and related analytic tools.                                   |
| `divisor-function`      | Divisor functions such as τ(n)=d(n) and σ(n), including record behavior.                     |
| `explicit-formula`      | Explicit formulas connecting primes and zeros (ψ(x), π(x), etc.).                            |
| `exploration`           | Open-ended search for patterns or properties.                                                |
| `factorization`         | Integer factorization methods and hardness.                                                  |
| `fermat`                | Fermat numbers and Fermat primes.                                                            |
| `gaps`                  | Studies of the distribution of gaps between primes.                                          |
| `generating-functions`  | Ordinary/exponential generating functions (esp. partitions).                                 |
| `gram-points`           | Gram points and Gram's law heuristics for zeta zeros.                                        |
| `hardy-z`               | Hardy's Z-function and Riemann–Siegel theta function.                                        |
| `heuristics`            | Probabilistic or empirical models (e.g., Cramér’s model for primes).                         |
| `li-x`                  | Logarithmic integral $\operatorname{li}(x)$ and its relation to $\pi(x)$.                    |
| `liouville`             | Liouville function λ(n) and related parity questions for Ω(n).                               |
| `lucas-lehmer`          | Lucas–Lehmer primality test for Mersenne numbers.                                            |
| `mangoldt`              | von Mangoldt function Λ(n) and related Chebyshev functions θ(x), ψ(x).                       |
| `mersenne`              | Mersenne numbers $M_p = 2^p - 1$ and Mersenne primes.                                        |
| `miller-rabin`          | Miller–Rabin primality test and its counterexamples.                                         |
| `mobius`                | Möbius function $\mu(n)$, Möbius inversion, squarefree indicators.                           |
| `multiplicative`        | Multiplicative arithmetic functions; Dirichlet convolution viewpoints.                       |
| `numerics`              | Heavy use of floating-point or high-precision computation.                                   |
| `omega`                 | Prime-factor counting functions ω(n) and Ω(n) (distinct vs with multiplicity).               |
| `open-problems`         | Related to famous unproven conjectures.                                                      |
| `optimization`          | Finding maxima, minima, or best-fit parameters.                                              |
| `partition`             | Partition function p(n), identities, and asymptotics.                                        |
| `perfect`               | Related specifically to perfect, abundant, or deficient numbers.                             |
| `pnt`                   | Prime Number Theorem and related asymptotics.                                                |
| `primes`                | Prime number distribution, density, and related theorems.                                    |
| `primorial`             | Primorials, Euclid numbers, primorial primes.                                                |
| `pseudoprime`           | Pseudoprimes, primality-test failures.                                                       |
| `pseudoprimes`          | Collective study of various types of pseudoprimes.                                           |
| `riemann-zeta`          | Riemann zeta function ζ(s): series, Euler product, analytic continuation, zeros.             |
| `search`                | Systematic search through a large state space.                                               |
| `semiprime`             | Semiprimes, RSA-type composites.                                                             |
| `sieving`               | Sieve methods (Eratosthenes, Sundaram, Atkin, etc.).                                         |
| `sigma`                 | Related to the sum-of-divisors function $\sigma(n)$.                                         |
| `summatory`             | Summatory functions (e.g., Mertens $M(x)$, summatory totient $\Phi(x)$).                     |
| `taylor`                | Related to Taylor series and their approximations.                                           |
| `totient`               | Euler’s totient function $\phi(n)$, totient equations, summatory behavior.                   |
| `twin`                  | Twin primes and the twin prime conjecture.                                                   |
| `klauber`               | Klauber triangle and prime patterns between consecutive squares.                             |
| `sacks`                 | Sacks spiral ($r=\sqrt{n},\ \theta=2\pi\sqrt{n}$) and related prime patterns.           |
| `hex-spiral`            | Integer spirals on a hexagonal lattice (hex-grid prime maps).                                |
| `ulam`                  | Ulam spiral and related prime patterns in 2D.                                                |
| `wieferich`             | Wieferich primes and related congruences.                                                    |
| `wilson`                | Wilson’s theorem and Wilson primes.                                                          |
| `zeta-zeros`            | Nontrivial zeros, zero-counting $N(T)$, root bracketing.                                     |

## Usage

When adding a new experiment:
1. Choose at least one **Primary Tag** (Domain or Type).
2. Choose one or more **Secondary Tags** (Topics & Methods).
3. Add them to the `**Tags:**` line in your `.md` file.
4. Update the {doc}`experiments/experiments_gallery` using the corresponding CSS classes
   (`tag-primary` for primary tags, `tag-secondary` for secondary tags).
