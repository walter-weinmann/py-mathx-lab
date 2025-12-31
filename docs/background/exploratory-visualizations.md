# Exploratory visualizations for arithmetic functions

Several experiments in this project are intentionally “EDA-like”: they produce
**heatmaps**, **atlases**, and **correlation matrices** for many functions at once.
This page collects best practices so those figures remain interpretable and comparable.

## Core definitions

Given a function table $F(n)$ for $n=1,\dots,N$ and a list of arithmetic functions
$f_1,\dots,f_m$, two common derived views are:

- **Heatmap atlas:** visualize values $f_j(n)$ as an image (rows = functions, columns = $n$
  or blocks of $n$).
- **Correlation matrix:** compute an empirical correlation between columns $f_i(n)$ and
  $f_j(n)$ (Pearson or rank-based).

## What experiments usually visualize or measure

- “Texture”: squarefree bands, prime powers, smooth numbers, record-holders, etc.
- Clustering: which functions behave similarly on $1..N$ (after normalization).
- Stability: how patterns change when $N$ grows or when you sample on a log grid.

## Practical numerical caveats

- **Normalize first.** Raw scales differ wildly (e.g. $\sigma(n)$ vs $\mu(n)$).
  Typical choices: z-score, log1p, or scaling by $n^\alpha$.
- **Beware heavy tails.** Extremal values can dominate Pearson correlation; consider
  Spearman correlation or winsorization for robustness.
- **Sampling matters.** Linear $n$ emphasizes small structure; log-spaced $n$ emphasizes
  asymptotic behavior. Record the sampling rule in the figure caption.

## References

See {doc}`../references`.

{cite:p}`BorweinBailey2008MathematicsByExperiment,arnold2015experimentalmath`

## Experiments in this repository

- **E122** — Heatmap atlas of μ, ω, Ω and related “squarefree texture” features.
- **E123** — Correlation matrix of arithmetic functions (with normalization variants).
