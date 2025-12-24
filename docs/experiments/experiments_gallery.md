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
(link to the page and a copy/paste run command). For details, open the experiment page.

## Hero images

Experiments may optionally provide a small “hero image” stored under:

- `docs/_static/experiments/<experiment_id>_hero.png`

This keeps documentation builds stable (no dependency on generated `out/` artifacts) while still allowing
experiments to generate rich figures during execution.

## Gallery

(e001-taylor-error-landscapes-gallery)=
### E001 - Taylor Error Landscapes

::::{grid} 1 1 2 2
:gutter: 2

:::{grid-item-card} **E001 - Taylor Error Landscapes**
:link: e001
:link-type: doc
:img-top: ../_static/experiments/e001_hero.png

**Tags:** `analysis`, `numerics`, `visualization`

Visualize where Taylor polynomials approximate $\sin(x)$ well (and where they don’t) by plotting error landscapes over $(n, x_0, x)$.

**Run**
```bash
make run EXP=e001 ARGS="--out out/e001 --seed 1"
```

**Open**
- Full experiment page: {doc}`e001`
- Shared references: {doc}`../references`

:::

:::{grid-item-card} **More experiments are coming**
:class-card: sd-text-muted

As new experiments (E002, E003, …) are added, they will appear here automatically.
Each one should include a hero image, a runnable command, and a link to its full write-up.
:::

::::

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
```
