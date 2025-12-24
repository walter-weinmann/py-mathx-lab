# EXXX: <Experiment title>

```{figure} ../_static/experiments/exxx_hero.png
:width: 80%
:alt: Preview figure for EXXX
```

**Tags:** <tag1>, <tag2>, <tag3>

## Goal

State in 2–4 sentences what the experiment tries to learn or test.

Include (when relevant) the mathematical object(s) and the observable(s) you will measure/visualize.
Prefer concrete wording like “estimate”, “search”, “compare”, “visualize”, “stress-test”.

## Background (quick refresher)

Link to a lightweight background page for the key math concept(s):

- {doc}`../background/<topic>`

Keep background pages short and practical: one definition/theorem, one key formula, and typical pitfalls.

## Research question

State the **single** main question your experiment tries to answer.

- What object or model do you study?
- What is varied (parameters)?
- What is observed/measured?
- What would count as an interesting outcome (pattern, conjecture, counterexample)?

### Examples

Write 1–3 questions that can be answered by running code and inspecting output.

Examples:

- How does \(X\) change as parameter \(\alpha\) varies?
- Does property \(P\) appear to hold for all \(n \le N\)? Where does it fail?
- What is the empirical distribution of \(Y\) and how does it compare to a theoretical prediction?

## Why this qualifies as a mathematical experiment

Briefly justify why this page is an *experiment* (not just an exposition or a proof sketch).

Use 4–7 bullets. Touch at least three of:

- **Finite procedure:** what computation / enumeration / visualization is run?
- **Observable(s):** what quantity is measured, estimated, compared, or plotted?
- **Parameter space:** what is varied (and over what ranges)?
- **Outcome:** what kind of evidence is produced (patterns, conjectures, counterexamples, estimates)?
- **Reproducibility:** where are parameters/seeds recorded and which artifacts are written?
- **Failure modes:** what could mislead (precision, bias, insufficient bounds)?

Keep it concrete and specific to this experiment.

## Experiment design

- Data / sampling:
  - describe the domain, range, grid, random sampling, enumeration bounds
- Parameters:
  - list parameters and their default values
- Outputs:
  - name the artifacts you expect to create (figures, tables, witness objects)
- Reproducibility:
  - state which seed is used and how it is passed

## How to run

Repository convention:

```bash
make run EXP=exxx_<module_name> ARGS="--out out/exxx --seed 1"
```

The experiment should write into `out/exxx/`:

- `params.json` (the parameters of the run)
- `report.md` (short narrative summary)
- `figures/*.png` (and optionally `data/*.csv`)

## Results

Insert or summarize the key figures/tables and what they show.

**Minimal requirement:** at least one figure or table with a short interpretation (3–8 sentences).

## Notes / pitfalls

Call out what can invalidate the results:

- precision limits, floating-point issues, cancellation, overflows
- selection bias / insufficient search bounds
- algorithmic complexity / timeouts
- “looks true” for small \(n\) but false later

Be explicit about what is evidence vs. what would require a proof.

## Gallery images (recommended)

To keep the gallery attractive **and** keep docs builds stable (no dependency on generated `out/` artifacts):

1. run the experiment locally,
2. pick one representative output figure,
3. copy it into the docs tree under:

   `docs/_static/experiments/exxx_hero.png`

Then reference it at the top of this page via the `{figure}` directive (see above).

## Extensions

List 2–6 ways to extend the experiment:

- broaden the parameter sweep
- search for counterexamples under tighter constraints
- compare with an alternative method/approximation
- use higher precision arithmetic or exact arithmetic
- validate against known theorems / benchmarks

## References

See {doc}`../references`.

Add 1–4 specific bibliography keys that motivated the experiment or give background:

{cite:p}`<Key1>,<Key2>`
