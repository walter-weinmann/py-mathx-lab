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

## Goal

Describe the goal in 2–5 sentences: what this experiment tries to show or measure.

## Why this qualifies as a mathematical experiment

Explain in 3–6 sentences why this work counts as a *mathematical experiment*.

Cover (briefly):

* What is explored empirically (pattern search, conjecture testing, structural exploration)?
* What is the mathematical object under study (sequence, function, set, graph, distribution)?
* What computation adds (scale, exhaustive search, visualization, counterexample hunting)?
* What a “successful outcome” looks like (a conjecture, a refutation, a heuristic, an invariant).

**Tip:** If an older page has headings like “Why this qualifies …”, “Motivation”, or “Why this is interesting”, move the content here.

## Background (quick refresher)

Add 1–3 links to existing background pages in `docs/background/`.
**Important:** never leave placeholder links in the final experiment doc.

Use this exact syntax (replace with real pages that exist in your repo):

```md
- {doc}`../background/<existing_page_slug>`
- {doc}`../background/<existing_page_slug>`
```

If there is no good background page yet, either:

* create one under `docs/background/` first, or
* omit links and instead add 2–4 “quick refresher” bullets (definitions, notation).

## Research question

State the single main question (2–5 sentences):

* Object/model:
* What varies (parameters):
* What is observed/measured:
* What would count as an interesting outcome:

## Experiment design

Describe the design decisions that shape the experiment outcome (keep it concrete and experiment-specific):

* Parameter regime: ranges, grids, sampling strategy
* Controls: fixed constants, baselines, comparison variants
* Randomness: seed usage / determinism and why
* Stopping criteria: max N, time limits, accuracy constraints
* Expected signatures: what patterns would confirm / refute the hypothesis

**Tip:** If older docs use headings like “Experiment design”, “Setup”, “Parameters”, “Plan”, copy/move that content here.

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

## Notes / pitfalls

Capture practical notes that help future readers reproduce and interpret results:

* Performance: runtime, memory hot spots, typical “slow” settings
* Numerical issues: precision, overflow/underflow, instability
* Data issues: discretization artifacts, boundary effects, truncation bias
* Interpretation traps: patterns that look real but are sampling artifacts

**Tip:** Old headings like “Notes”, “Pitfalls”, “Caveats”, “Limitations”, “Gotchas” should move here.

## Published run snapshot

If this experiment is included in the docs gallery, the page should include the
published snapshot (report + params).

Typical includes it (adjust paths only if your repo differs). Copy into the final
experiment page and replace `exxx` with the real experiment id:

```md
```{include} ../reports/exxx.md
:start-after: "<!-- REPORT:BEGIN -->"
:end-before: "<!-- REPORT:END -->"
```

:start-after: "{"
:end-before: "}"

**Important:** do not keep placeholder `exxx` in the final experiment page.

## References

Use only BibTeX keys that exist in `docs/refs.bib`.
**Important:** never leave placeholder keys in the final experiment doc.

Preferred structure (replace with real keys from your `refs.bib`):

```md
- Primary: {cite:t}`<real_key_1>`, {cite:t}`<real_key_2>`
- Background: {cite:t}`<real_key_3>`
```

If you have no citations yet, add at least one “Background” citation or remove
the bullets and keep only a short sentence like “See {doc}`../references`.” until ready.

## Related experiments

List 3–6 closely connected experiments and add a very short reason (3–6 words).
**Important:** never leave placeholder ids in the final experiment doc.

Use this syntax (replace with existing experiment pages):

```md
- {doc}`e0xx` — definition / baseline
- {doc}`e0yy` — same metric, different regime
- {doc}`e0zz` — visualization variant
```
