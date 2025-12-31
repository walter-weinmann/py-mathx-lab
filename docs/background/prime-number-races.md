# Prime number races refresher

A **prime number race** compares prime counts in different residue classes, e.g.
\[
\pi(x;4,3)\ \text{vs.}\ \pi(x;4,1).
\]

Although $\pi(x;q,a)\sim \mathrm{Li}(x)/\varphi(q)$ suggests “no long-term winner,” finite ranges often show persistent preferences (biases).

## The classic example: Chebyshev’s bias mod 4

Empirically, for many ranges of $x$ one observes
\[
\pi(x;4,3) > \pi(x;4,1),
\]
even though both are asymptotically equal.

Rubinstein–Sarnak analyze this phenomenon via the distribution of zeros of relevant $L$-functions (under standard hypotheses).

## What experiments usually visualize or measure

- The difference curve $D(x)=\pi(x;q,a)-\pi(x;q,b)$ and its sign changes.
- The “race leaderboard” among several classes (e.g., mod 8 or mod 12).
- Histogram / empirical distribution of a normalized statistic sampled on a log-grid of $x$ (choose a normalization and stick to it).

## Practical numerical caveats

- Bias claims depend on *how you sample* $x$ (linear vs log-grid); be explicit.
- With small cutoffs (say $x\le 10^7$), you’ll see “apparent stability” that may later flip; that’s expected.
- Counting primes is the bottleneck; keep an eye on runtime and memory, and record parameters in your manifest.

## References

See {doc}`../references`.

{cite:p}`rubinsteinsarnak1994chebyshevsbias,granvillemartin2006primenumberraces`

## Experiments in this repository

- **E112** — Prime race curves π(x;q,a) − π(x;q,b): sign changes and time-in-lead.
