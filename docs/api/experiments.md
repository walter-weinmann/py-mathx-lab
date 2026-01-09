# Experiment registry and suites (`mathxlab.experiments`)

This page documents the *reusable* entry points under `mathxlab.experiments`.

Excluded on purpose:

- Private helper modules: `_*.py`
- Runnable experiment scripts: `e001*.py` … `e999*.py`

Included:

- The experiment registry (`mathxlab.experiments`)
- Suite-style runners (non-`e###` modules)

```{autosummary}
:toctree: generated/experiments

mathxlab.experiments
mathxlab.experiments.number_theory_suite
mathxlab.experiments.prime_suite
mathxlab.experiments.spiral_suite
```
