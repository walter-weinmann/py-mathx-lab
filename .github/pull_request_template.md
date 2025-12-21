## Summary

Describe the purpose of this PR in 1–5 sentences.

## Type of change

- [ ] Bug fix
- [ ] Documentation
- [ ] New experiment
- [ ] Refactor / maintenance
- [ ] CI / tooling

## Details

Explain what changed and why. Include links to issues/discussions if relevant.

## Reproducibility / verification

Commands you ran:

- [ ] `make final`
- [ ] `make docs` (if only docs changed)
- [ ] `make run EXP=... ARGS="..."` (if experiment changed/added)

Notes / outputs:
- …

## Experiment checklist (only if applicable)

- [ ] Experiment module follows naming scheme `experiments/e###_<name>.py`
- [ ] Experiment is runnable as a module (`python -m experiments.e###_<name> ...`)
- [ ] Outputs go only to `--out` directory
- [ ] Deterministic behavior (seeded) if randomness is used
- [ ] Docs updated (`docs/experiments.md`, optional detail page under `docs/experiments/`)

## Documentation checklist (only if applicable)

- [ ] Pages build locally (`make docs`)
- [ ] Links work (no broken internal refs)
- [ ] New pages are discoverable (toctree or hub links)

## Additional context

Anything else the maintainer should know (tradeoffs, follow-ups, scope limits).
