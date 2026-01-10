# EXXX: Title in plain English

```{figure} ../_static/experiments/exxx_hero.png
:width: 80%
:alt: Preview figure for EXXX
```

**Tags:** `number-theory`, `...`  
See: {doc}`../tags`.

## Highlights

- One sentence: what you computed.
- One sentence: what you checked.
- One sentence: which artifacts were written (`params.json`, `report.md`, figures).

## Goal

State the goal as an observable claim.

## Background (quick refresher)

- {doc}`../background/prime-numbers`
- {doc}`../background/...`

## Research question

Write the question so it has a measurable outcome.

## Why this qualifies as a mathematical experiment

- **Finite procedure:** ...
- **Observable(s):** ...
- **Parameter space:** ...
- **Outcome:** ...
- **Reproducibility:** ...

## Experiment design

- **Inputs:** ...
- **Method:** ...
- **Checks:** ...
- **Artifacts written:** ...

## How to run

```bash
make run EXP=exxx
```

Direct invocation:

```bash
uv run --extra dev python -m mathxlab.experiments.exxx --out out/exxx
```

## Notes / pitfalls

- ...

## Extensions

- ...

## Published run snapshot

```{include} ../reports/exxx.md
:start-after: "<!-- REPORT:BEGIN -->"
:end-before: "<!-- REPORT:END -->"
```

::: {dropdown} params.json (snapshot)
:open:

```{literalinclude} ../params/exxx.json
:language: json
```

:::

## References

See {doc}`../references`.

## Related experiments

- {doc}`e###` (...)
