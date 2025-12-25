# Experiments

This page is the public gallery of *mathematical experiments* in this repository.

If you are new to the idea of experimental mathematics, start here: {doc}`../mathematical-experimentation`.


## How to read this gallery

Each experiment is identified by a stable ID (**E001**, **E002**, …) and has its own page with:

- **Goal**
- **Research question**
- **Why this qualifies as a mathematical experiment**
- **Experiment design**
- **How to run**
- **Results**
- **Notes / pitfalls**
- **References**

The gallery below is intentionally compact: it shows a preview and the “entry points”
(link to the page and a copy‑paste run command). For details, open the experiment page.


## Hero images

Experiments may optionally provide a small “hero image” stored under:

- `docs/_static/experiments/<experiment_id>_hero.png`

This keeps documentation builds stable (no dependency on generated `out/` artifacts) while still allowing
experiments to generate rich figures during execution.


## Gallery

(e001-taylor-error-landscapes-gallery)=
### {doc}`E001: Taylor Error Landscapes <e001>`

```{figure} ../_static/experiments/e001_hero.png
:width: 70%
:alt: Preview figure for E001
```

**Tags:** analysis, numerics, visualization

**One‑liner**  
Visualize where Taylor polynomials approximate $\sin(x)$ well (and where they don’t) by plotting error landscapes over $(n, x_0, x)$.

**Run**
```bash
make run EXP=e001 ARGS="--seed 1"
```

**Open**
- Read the full experiment page: {doc}`e001`
- References used across experiments: {doc}`../references`

---
---

(e002-even-perfect-numbers-generator-growth-gallery)=
### {doc}`E002: Even Perfect Numbers — Generator and Growth <e002>`

```{figure} ../_static/experiments/e002_hero.png
:width: 70%
:alt: Preview figure for E002
```

**Tags:** number-theory, numerics, visualization

**One‑liner**  
Generate even perfect numbers from Mersenne exponents and visualize how digit count and bit length explode with $p$.

**Run**
```bash
make run EXP=e002 ARGS="--seed 1"
```

**Open**
- Read the full experiment page: {doc}`e002`

---

(e003-abundancy-index-landscape-gallery)=
### {doc}`E003: Abundancy Index Landscape <e003>`

```{figure} ../_static/experiments/e003_hero.png
:width: 70%
:alt: Preview figure for E003
```

**Tags:** number-theory, numerics, visualization

**One‑liner**  
Compute $\sigma(1..N)$ with a divisor-sum sieve and map the landscape of $I(n)=\sigma(n)/n$, highlighting $I(n)=2$.

**Run**
```bash
make run EXP=e003 ARGS="--seed 1"
```

**Open**
- Read the full experiment page: {doc}`e003`

---

(e004-sigma-benchmark-sieve-vs-factorization-gallery)=
### {doc}`E004: Computing σ(n) at Scale — Sieve vs. Factorization <e004>`

```{figure} ../_static/experiments/e004_hero.png
:width: 70%
:alt: Preview figure for E004
```

**Tags:** number-theory, numerics, optimization

**One‑liner**  
Benchmark two mathematically equivalent ways to compute σ(n) and measure the crossover where each wins.

**Run**
```bash
make run EXP=e004 ARGS="--seed 1"
```

**Open**
- Read the full experiment page: {doc}`e004`

---

(e005-odd-perfect-constraints-filter-pipeline-gallery)=
### {doc}`E005: Odd Perfect Numbers — Constraint Filter Pipeline <e005>`

```{figure} ../_static/experiments/e005_hero.png
:width: 70%
:alt: Preview figure for E005
```

**Tags:** number-theory, search, visualization

**One‑liner**  
Apply necessary constraints for odd perfect numbers as staged filters and plot how fast the candidate pool collapses.

**Run**
```bash
make run EXP=e005 ARGS="--seed 1"
```

**Open**
- Read the full experiment page: {doc}`e005`

---

(e006-near-misses-to-perfection-gallery)=
### {doc}`E006: Near Misses to Perfection <e006>`

```{figure} ../_static/experiments/e006_hero.png
:width: 70%
:alt: Preview figure for E006
```

**Tags:** number-theory, numerics, visualization

**One‑liner**  
Search for integers whose σ(n) is unusually close to $2n$ and visualize the best “near misses”.

**Run**
```bash
make run EXP=e006 ARGS="--seed 1"
```

**Open**
- Read the full experiment page: {doc}`e006`

---

## Recommended tags (use consistent spelling)

- analysis
- number-theory
- probability
- geometry
- numerics
- optimization
- visualization


```{toctree}
:hidden:
:maxdepth: 1

e001
e002
e003
e004
e005
e006
```
