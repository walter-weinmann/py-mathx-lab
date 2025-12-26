# Experiments

This page is the public gallery of *mathematical experiments* in this repository.

If you are new to the idea of experimental mathematics, start here: {doc}`../mathematical-experimentation`.

## Gallery

::::{grid} 1 2 3 3
:gutter: 2
:class-container: sd-pb-2

:::{grid-item-card} **E001** — Taylor Error Landscapes
:img-top: ../_static/experiments/e001_hero.png
:link: e001
:link-type: doc
:class-card: sd-shadow-sm

{bdg-primary}`analysis` {bdg-secondary}`numerics` {bdg-info}`visualization`

Visualize where Taylor polynomials approximate $\sin(x)$ well (and where they don’t) by plotting error landscapes over $(n, x_0, x)$.

+++
**Run:** `make run EXP=e001 ARGS="--seed 1"`
:::

:::{grid-item-card} **E002** — Even Perfect Numbers
:img-top: ../_static/experiments/e002_hero.png
:link: e002
:link-type: doc
:class-card: sd-shadow-sm

{bdg-primary}`number-theory` {bdg-info}`visualization` {bdg-secondary}`numerics`

Generate even perfect numbers from Mersenne exponents and visualize how digit count and bit length explode with $p$.

+++
**Run:** `make run EXP=e002 ARGS="--seed 1"`
:::

:::{grid-item-card} **E003** — Abundancy Landscape
:img-top: ../_static/experiments/e003_hero.png
:link: e003
:link-type: doc
:class-card: sd-shadow-sm

{bdg-primary}`number-theory` {bdg-secondary}`numerics` {bdg-info}`visualization`

Compute $\sigma(1..N)$ with a divisor-sum sieve and map the landscape of $I(n)=\sigma(n)/n$, highlighting $I(n)=2$.

+++
**Run:** `make run EXP=e003 ARGS="--seed 1"`
:::

:::{grid-item-card} **E004** — σ(n) Benchmark
:img-top: ../_static/experiments/e004_hero.png
:link: e004
:link-type: doc
:class-card: sd-shadow-sm

{bdg-primary}`number-theory` {bdg-secondary}`optimization` {bdg-info}`numerics`

Benchmark two mathematically equivalent ways to compute $\sigma(n)$ and measure the crossover where each wins.

+++
**Run:** `make run EXP=e004 ARGS="--seed 1"`
:::

:::{grid-item-card} **E005** — Odd Perfect Number Filters
:img-top: ../_static/experiments/e005_hero.png
:link: e005
:link-type: doc
:class-card: sd-shadow-sm

{bdg-primary}`number-theory` {bdg-secondary}`search` {bdg-info}`visualization`

Apply necessary constraints for odd perfect numbers as staged filters and plot how fast the candidate pool collapses.

+++
**Run:** `make run EXP=e005 ARGS="--seed 1"`
:::

:::{grid-item-card} **E006** — Near-Miss σ(n)≈2n
:img-top: ../_static/experiments/e006_hero.png
:link: e006
:link-type: doc
:class-card: sd-shadow-sm

{bdg-primary}`number-theory` {bdg-secondary}`numerics` {bdg-info}`visualization`

Search for integers whose $\sigma(n)$ is unusually close to $2n$ and visualize the best “near misses”.

+++
**Run:** `make run EXP=e006 ARGS="--seed 1"`
:::

::::

```{toctree}
:hidden:
:maxdepth: 1

e001
e002
e003
e004
e005
e006
