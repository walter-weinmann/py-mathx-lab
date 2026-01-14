# Output quality rubric

An experiment is “good enough” to be considered validated when it meets the criteria below.

## Reproducibility

- Stable defaults: running the experiment without special flags produces meaningful output.
- Outputs are deterministic (or the seed is fixed and saved).
- `params.json` (or your equivalent snapshot) is complete and matches the documented run.

## Plot quality

- Clear question → clear plot: one plot answers one question.
- Axes labels, units, legend labels, and a sensible scale are present.
- The chosen grid (linear vs log) is documented when it affects interpretation.

## Runtime discipline

- Default run is “CI-friendly”.
- Larger “exploration” runs are possible via parameters.

## Documentation quality

- Short highlights + explanation + caveats.
- Cross-links to background pages for definitions.
- Citations for nontrivial claims.

## Validation

- `make docs` passes.
- `make pytest` passes.
- If you touched core utilities used by many experiments, perf tests stay within bounds.

See also:
- [The “Check & Refine” workflow](The-Check-&-Refine-workflow)
