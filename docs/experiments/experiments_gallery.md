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
make run EXP=e001_taylor_error_landscapes ARGS="--out out/e001 --seed 1"
```

**Open**
- Read the full experiment page: {doc}`e001`
- References used across experiments: {doc}`../references`

---

```{admonition} More experiments are coming
:class: note

As new experiments (E002, E003, …) are added, they will appear here automatically.
Each one will include a hero image, a runnable command, and a link to its full write‑up.
```

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
