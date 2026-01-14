# Strict pipeline per wave

Use this pipeline when finalizing a wave of experiments.

1. Run all experiments in the wave with stable defaults.
2. Confirm figures and hero outputs exist and are readable.
3. Build docs: `make docs` (fix warnings, broken links, citations).
4. Run tests: `make pytest`.
5. Run perf tests when core utilities changed: `make pytest-perf`.
6. Sync gallery assets and rebuild docs.
7. Promote experiments to validated.

See also:
- [The “Check & Refine” workflow](The-Check-&-Refine-workflow.md)
- [Promote experiments to “validated”](Promote-experiments-to-validated.md)
