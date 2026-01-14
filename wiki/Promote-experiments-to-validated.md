# Promote experiments to “validated”

Use this checklist when an experiment is ready to move from “draft” to “validated”.

## Promotion checklist

1. Docs page is complete:
   - Highlights, interpretation, and caveats are present.
   - References are present and build cleanly.

2. Outputs are stable:
   - Hero figure exists (if the experiment is part of the gallery).
   - Figure filenames follow the repo convention.
   - Params snapshot corresponds to the documented run.

3. CI signals are clean:
   - `make docs` passes.
   - `make pytest` passes.
   - `make pytest-perf` (when relevant) passes.

4. Gallery sync:
   - Copy/sync the hero figure + report snapshot + manifest snapshot into `docs/` (if your pipeline uses this).
   - Rebuild docs and verify the gallery entry renders correctly.

See also:
- [Output quality rubric](Output-quality-rubric.md)
- [Promote experiments to "validated"](Promote-experiments-to-validated.md)
