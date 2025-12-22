# Experiments

This page is the public “gallery” of experiments.

If you are new to the idea of *mathematical experimentation*, start with {doc}`../mathematical-experimentation`.


**Conventions**
- Experiments are identified by stable IDs: **E001, E002, …**
- Each experiment should document:
  - **Goal**
  - **How to run**
  - **Parameters**
  - **Results**
  - **Notes / pitfalls**
  - **References**

## Gallery images

For a more attractive gallery, each experiment may optionally provide a small **hero image**
stored in the docs tree under:

- `docs/_static/experiments/<experiment_id>_hero.png`

This keeps documentation builds stable (no dependency on generated `out/` artifacts) while still allowing
experiments to produce rich figures during execution.


## Index

(e001-taylor-error-landscapes-gallery)=
### E001: Taylor Error Landscapes

```{figure} ../_static/experiments/e001_hero.png
:width: 65%
:alt: Preview figure for E001
```


**Tags:** analysis, numerics, visualization

**Goal**  
Build intuition for Taylor series truncation error by visualizing error magnitude as a function of:
- polynomial order
- evaluation point
- function choice (e.g. `exp`, `sin`, `log(1+x)`)

**How to run**
```bash
make run EXP=e001_taylor_error_landscapes ARGS="--out out/e001 --seed 1"
```

**Notes**

* Keep domains sane (`log(1+x)` needs `x > -1`).
* Compare absolute vs. relative error depending on the function.
* Document which norm/metric you plot for the “landscape”.

---

## Recommended tags (use consistent spelling)

* analysis
* number-theory
* probability
* geometry
* numerics
* optimization
* visualization

---

```{toctree}
:hidden:
:maxdepth: 1

e001
```
