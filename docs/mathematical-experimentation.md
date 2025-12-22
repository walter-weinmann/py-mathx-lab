# Mathematical experimentation

Mathematical experimentation is the practice of **using examples, computation, and visualization to discover structure**:
to generate conjectures, find counterexamples, estimate quantities, and build intuition that later supports (or refutes)
formal arguments.

It is *not* “proof by computer output”. Instead, experiments are a disciplined way to ask better questions and to
stress-test ideas—especially now that modern computers make it easy to explore large search spaces, high precision
numerics, and rich visualizations.

This repository, **py-mathx-lab**, is a small “lab notebook” of such experiments: compact, reproducible, and readable.

## What counts as an “experiment” in mathematics?

An experiment is a finite procedure that produces evidence about a mathematical claim or object. Typical outcomes:

- **Conjecture generation**: patterns suggest statements that might be true (or false).
- **Counterexample search**: systematic exploration tries to break a hypothesis early.
- **Quantitative exploration**: estimate constants, rates, limits, or distributions.
- **Model checking**: validate (or invalidate) approximations and heuristics.
- **Visualization**: reveal structure that is hard to see symbolically.

The modern viewpoint—where computation is a genuine part of mathematical discovery—is widely discussed under the name
*experimental mathematics* ({cite:p}`BaileyBorweinCrandall2004TenProblems,BaileyBorwein2005ExperimentalMathematics,Borwein2005ExperimentalMathematician`).
Some authors emphasize “plausible reasoning” supported by computation, paired with careful verification and eventual proof
({cite:p}`BorweinBailey2008MathematicsByExperiment,Borwein2009Crucible`).
Other texts take a more problem-driven, exploratory style aimed at students and engineers ({cite:p}`li2003mathematicsexperiments`),
or present computation as a tool to formulate concrete research problems ({cite:p}`arnold2015experimentalmath`).

## Why computers change the game

Computers do not replace mathematical thinking—but they expand what is feasible to *inspect*:

- **Scale**: enumerate millions of cases (to find the first failure, or build confidence).
- **Precision**: compute with high-precision floats or exact rationals/integers to avoid roundoff illusions.
- **Multiple lenses**: combine numerics, exact arithmetic, symbolic manipulation, and plotting.
- **Search**: automate discovery (parameter sweeps, optimization, random sampling, heuristics).
- **Reproducibility**: re-run the same pipeline with fixed seeds and pinned dependencies.

Used well, computation turns “I wonder if…” into “here is evidence, here are edge cases, and here is what we should prove next”.

## Experiments vs. proofs

A proof is the end of the story; an experiment is often the beginning.

Experiments are excellent for:

- **disproving** statements (one counterexample ends it),
- identifying **what is actually true** (after a naive conjecture fails),
- suggesting **lemmas** and **invariants** that make a proof possible.

But experiments can also mislead. Common failure modes:

- floating point error and catastrophic cancellation,
- plotting artifacts,
- “pattern matching” based on too few samples,
- unintentional selection bias (“I tried the cases that worked”).

The goal is to use experiments to *reduce uncertainty*, not to hide it.

## Targets for py-mathx-lab

py-mathx-lab aims to be a practical, long-lived collection of experiments with shared conventions:

1. **Reproducible runs**  
   Each experiment is runnable as a module, writes results to a single output directory, and (when relevant) uses a fixed seed.

2. **Readable code**  
   The code should be short, well-typed, and structured so readers can modify it.

3. **Useful artifacts**  
   Each experiment should generate at least one of:
   - a figure
   - a table / summary statistics
   - a counterexample / witness object
   - a short narrative explaining what was learned

4. **Clear boundaries**  
   An experiment write-up should state:
   - what is being tested,
   - what counts as “success” or “failure”,
   - what might invalidate the result (precision limits, domain constraints, runtime limits).

5. **Traceability**  
   Each page includes references to books/papers that motivated the work or explain the background.

## Repository conventions for experiments

An experiment page should usually include:

- **Goal** (one paragraph)
- **How to run** (a command that works from the repo root)
- **Parameters** (including defaults and ranges, if swept)
- **Results** (figures/tables and a short interpretation)
- **Notes / pitfalls** (numerical caveats, surprising behavior)
- **References** (bibliography keys)

In code, prefer:

- deterministic outputs (fixed seeds, stable sorting),
- explicit configuration objects / CLI arguments,
- sanity checks (dimension checks, bounds checks, invariants),
- cross-checks (e.g., float vs. exact, two independent formulas).

## Examples of good “experiment themes”

The experiment format supports many domains, for example:

- **Numerical analysis**: error landscapes, stability regions, conditioning, Monte Carlo integration.
- **Number theory**: continued fractions and convergents, integer sequences, modular patterns, primality heuristics.
- **Geometry/topology**: random point clouds, curvature approximations, combinatorial invariants.
- **Optimization/probability**: stochastic search behavior, concentration phenomena, empirical distributions.

A concrete example of a rich, experiment-friendly topic is continued fractions, where it is natural to compute and plot
convergents, partial quotient statistics, and periodicity phenomena ({cite:p}`borwein2014neverendingfractions`).

---

**Next steps:** start with {doc}`getting-started`, then browse the {doc}`experiments` gallery and use the tags to find topics.
