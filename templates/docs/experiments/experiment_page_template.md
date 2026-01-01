# EXXX: <Experiment title>

```{figure} ../_static/experiments/exxx_hero.png
:width: 80%
:alt: Preview figure for EXXX
```

**Tags:** `number-theory`, `quantitative-exploration`, `visualization`  <!-- add more -->
See: {doc}`../tags`. Do not introduce new tags without adding them to `docs/tags.md`.

## Highlights

- 2–4 bullets: what is visually interesting or surprising?
- Prefer concrete outcomes (plots, thresholds, record values, counterexamples).
- Keep it short: the gallery uses this section as “why click?”

## Goal

State in 2–4 sentences what the experiment tries to learn or test.

Prefer verbs like **estimate**, **search**, **compare**, **visualize**, **stress-test**.

## Background (quick refresher)

Link to lightweight background pages for the key math concept(s):

- {doc}`../background/<topic>`

## Research question

State the **single** main question your experiment tries to answer.

- What object or model do you study?
- What is varied (parameters)?
- What is observed/measured?
- What would count as an interesting outcome?

## Method

- Bullet list the computational steps.
- Note the parameter ranges and sampling choices.
- Mention complexity notes if relevant.

## How to run

- `make run EXP=exxx`
- `uv run python -m mathxlab.experiments.exxx`

## Outputs

This experiment follows the standard output contract:

- `out/exxx/figures/` — generated figures (PNG)
- `out/exxx/report.md` — short narrative report
- `out/exxx/params.json` — run parameters (stable JSON)
- `out/exxx/logs/` — run logs (created by the runner/Makefile)

## Figure LaTeX tips

Most figures are generated with Matplotlib **mathtext**, not full LaTeX.
Keep expressions simple and mathtext-compatible:

- Prefer `$arphi(n)/n$`, `$\mu(n)$`, `$\Omega(n)$`, `$\sum_{k\le x}$`.
- Avoid unsupported commands (e.g. `\pmod`, `\operatorname{...}`).
- Use raw strings in Python: `title = r"$\varphi(n)/n$"`.

If you need full LaTeX rendering, consider enabling `text.usetex=True`
in the experiment code (but that adds external dependencies).

## References

Use Sphinx bibtex citations:

- See {cite:t}`someKey`, {cite:t}`anotherKey`.

## Related experiments

List a few experiments that are closely connected (ideally 3–6):

- {doc}`e0xx` (<short reason>)
- {doc}`e0yy` (<short reason>)
- {doc}`e0zz` (<short reason>)

