# Experiments

This page is the public “gallery” of experiments.

**Conventions**
- Experiments are identified by stable IDs: **E001, E002, …**
- Each experiment should document:
  - **Goal**
  - **How to run**
  - **Parameters**
  - **Results**
  - **Notes / pitfalls**
  - **References**

## Index

### E001: Taylor Error Landscapes
<a id="e001-taylor-error-landscapes"></a>

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
* Compare absolute vs relative error depending on the function.
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

experiments/e001
````
