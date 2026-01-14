# Prime number races refresher

A **prime number race** compares prime counts in different residue classes, e.g.
$$
\pi(x;4,3)\ \text{vs.}\ \pi(x;4,1).
$$

Although $\pi(x;q,a)\sim \mathrm{Li}(x)/\varphi(q)$ suggests “no winner,” finite ranges often show persistent preferences (biases).

**How this repository measures a race (Phase 2 convention).** For each reduced residue class $a$ (with $\gcd(a,q)=1$) we compare
$\pi(x;q,a)$ to the baseline $\mathrm{li}(x)/\varphi(q)$ and define the error term
$$
E(x;q,a) := \pi(x;q,a) - \frac{\mathrm{li}(x)}{\varphi(q)}.
$$
Race curves are typically differences such as $\Delta(x)=\pi(x;q,a)-\pi(x;q,b)$; the baseline cancels, so $\Delta(x)=E(x;q,a)-E(x;q,b)$.
For the exact definitions and the baseline/error plots used throughout Phase 2, see {doc}`primes-in-arithmetic-progressions`.

## The classic example: Chebyshev’s bias mod 4

Empirically, for many ranges of $x$ one observes
$$
\pi(x;4,3) > \pi(x;4,1),
$$
even though both are asymptotically equal.

Rubinstein–Sarnak analyze this phenomenon through the lens of $L$-function zeros and propose models for the distribution of race leaders.

## Practical notes for experiments

- Bias claims depend on *how you sample* $x$ (linear vs log-grid); be explicit.
- With small cutoffs (say $x\le 10^7$), you’ll see “apparent stability” that may later flip; that’s expected.
- Counting primes is the bottleneck; keep an eye on runtime and memory, and record parameters in your manifest.

## References

See {doc}`../references`.

{cite:p}`rubinsteinsarnak1994chebyshevsbias,granvillemartin2006primenumberraces`

## Experiments in this repository

- **E112** — Prime race curves $\pi(x;q,a) - \pi(x;q,b)$: sign changes and time-in-lead.
