# EXXX: <Experiment title>

**Status:** `stable`  <!-- stable | draft | wip -->

**Deterministic:** `yes`  <!-- yes | no | partial -->


```{figure} ../_static/experiments/exxx_hero.png
:width: 80%
:alt: Preview figure for EXXX
```

**Tags:** `number-theory`, `quantitative-exploration`, `visualization`  <!-- add more -->
See: {doc}`../tags`. Do not introduce new tags without adding them to `docs/tags.md`.

## Highlights

* 2–4 bullets: what is visually interesting or surprising?
* Prefer concrete outcomes (plots, thresholds, record values, counterexamples).
* Keep it short: the gallery uses this section as “why click?”

## Background

Link to lightweight background pages for the key math concept(s):

* {doc}`../background/<topic>`

## Research question

State the **single** main question your experiment tries to answer (2–5 sentences).

* Object/model:
* What varies (parameters):
* What is observed/measured:
* What would count as an interesting outcome:

## Method

**Inputs**

* Key parameters and ranges:
* Sampling / truncation choices:

**Procedure**

* Bullet list the computational steps:
* Complexity notes if relevant:

**Metrics / observables**

* What exactly is plotted / measured / compared:

## How to run

* Recommended: `make run EXP=exxx`
* Direct: `uv run --extra dev python -m mathxlab.experiments.exxx`

Optional arguments:

* `make run EXP=exxx ARGS="--seed 123 --n 200000"`

## Outputs

This experiment follows the standard output contract:

* `out/exxx/figures/` — generated figures (PNG)
* `out/exxx/report.md` — short narrative report
* `out/exxx/params.json` — run parameters (stable JSON)
* `out/exxx/logs/` — run logs (created by the runner/Makefile)

:open:
If this experiment is included in the docs gallery, sync artifacts into `docs/`:

* run the experiment, producing `out/exxx/…`
* sync snapshots: `make snapshots IDS="exxx"`
* confirm the hero image exists at: `docs/_static/experiments/exxx_hero.png`

If useful, include the implementation for quick review:

```{literalinclude} ../../mathxlab/experiments/exxx.py
:language: python
:linenos:
```

## Interpretation (optional)

- 3–6 sentences: what do the results mean, and what is the key takeaway?

## Caveats (optional)

- Finite N / truncation bias:
- Numeric stability / precision:
- Performance limits:

## References

Use Sphinx bibtex citations.

- Primary: {cite:t}`someKey`, {cite:t}`anotherKey`
- Background: {cite:t}`backgroundKey`

## Related experiments

List a few experiments that are closely connected (ideally 3–6).
Keep reasons short (3–6 words).

- {doc}`e0xx` — definition / baseline
- {doc}`e0yy` — same metric, different regime
- {doc}`e0zz` — visualization variant
```
