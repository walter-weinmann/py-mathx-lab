<!-- TEMPLATE:BEGIN -->

## Algorithmic guarantees

- **Method:** (name the algorithm)
- **Status:** `DETERMINISTIC` | `PROBABILISTIC`

### If probabilistic

- **Randomness / bases:** (list bases used or how randomness was sampled)
- **Conservative error statement:**
  - For **Miller-Rabin**, a common bound is: `P(false prime) <= 4^{-k}` after `k` independent random bases.
  - If you use a **fixed base set** (engineering choice), state the intended input range.

## Correctness cross-check

State how you validated correctness for a CI-safe range.

- **Reference:** (e.g., sieve ground truth, deterministic trial division)
- **Checked range:** (e.g., `n <= 1_000_000`)
- **Result:** mismatches = `0` (or list the smallest mismatch as a witness)

## Known counterexamples / failure modes (when applicable)

Use this section when the method is known to fail on structured inputs.

- **Fermat test:** Carmichael numbers pass for all coprime bases (smallest: `561`).
- **Fermat base-2 pseudoprime:** `341 = 11 * 31` passes `2^(n-1) mod n = 1` but is composite.
- **Miller-Rabin:** specific bases can be fooled by strong pseudoprimes (state the bases used).
- **Pollard rho:** may stall for unlucky seeds; retries and parameter changes are expected.

## Runtime knobs (CI-safe)

List the knobs that keep runtime bounded in CI.

- `n_max`: (upper bound)
- `sample_size`: (how many candidates were tested)
- `max_rounds` / `max_retries`: (for randomized algorithms)
- `seed`: (if randomness is involved)

## Finite-range behavior (for asymptotics / explicit bounds)

When referencing an asymptotic statement (e.g., PNT), explicitly separate:

- **Theory statement:** what is true as `x -> infinity`.
- **Finite range used here:** `x in [A, B]`.
- **Where it becomes meaningful:** state a measurable criterion (e.g., relative error < 5%) and the smallest `x` where that holds.

<!-- TEMPLATE:END -->
