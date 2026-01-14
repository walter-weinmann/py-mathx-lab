# The “Check & Refine” workflow

This is the repo’s default loop for turning an experiment from “it runs” into “it is stable and publishable”.

## Loop steps

1. **Run**
   - Run the experiment with stable default parameters.
   - Ensure outputs land in `out/e###/` and that the run is deterministic.

2. **Check outputs**
   - Are the figures readable (axes, legends, labels)?
   - Is there a clear “hero” figure if the experiment appears in the gallery?
   - Are params snapshots written and complete?

3. **Refine**
   - Improve plot scales, annotations, and narrative “Highlights”.
   - Reduce runtime for default parameters (CI-friendly tier), while preserving the phenomenon.

4. **Document**
   - Ensure the experiment page explains: what you compute, what to look for, what can mislead you.
   - Add citations and cross-links to background pages where needed.

5. **Validate**
   - Run `make docs` (docs must build cleanly).
   - Run `make pytest` and, when relevant, `make pytest-perf`.

6. **Promote**
   - When the output meets the rubric, mark the experiment as validated and sync gallery assets.

See also:
- [Output quality rubric](Output-quality-rubric)
- [Promote experiments to “validated”](Promote-experiments-to-validated)

See also:
- [The "Check & Refine" workflow](The-Check-&-Refine-workflow.md)
- [Promote experiments to "validated"](Promote-experiments-to-validated.md)
