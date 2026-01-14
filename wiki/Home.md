# py-mathx-lab Wiki — Home

Welcome to the **py-mathx-lab** project wiki.

This wiki is the **control room** for keeping the repository consistent:
- experiments (E###) and their “output contract”
- docs + gallery hygiene
- validation workflow (“Check & Refine”)
- the learning path (easy → hard) that matches math prerequisites

> Rule of thumb: **operational** content lives here (workflows, runbooks, checklists).
> **Math exposition** lives in `docs/` (Sphinx/MyST, citations, longer background articles).

---

## Quick links

**Read-first (results)**
- Experiments gallery (read-first): https://github.com/walter-weinmann/py-mathx-lab/tree/main/docs/experiments
- Docs root: https://github.com/walter-weinmann/py-mathx-lab/tree/main/docs
- Experiments source modules: https://github.com/walter-weinmann/py-mathx-lab/tree/main/mathxlab/experiments

**Workflow**
- [The “Check & Refine” workflow](The-Check-&-Refine-workflow.md)
- [Output quality rubric](Output-quality-rubric.md)
- [Promote experiments to “validated”](Promote-experiments-to-validated.md)
- [How to work with GitHub issues](How-to-work-with-GitHub-issues.md)

**Setup**
- [Global setup (do once)](Global-setup-do-once.md)
- [Development conventions](Development-conventions.md)
- [Tags / References (docs hygiene)](Tags-and-References-docs-hygiene.md)

---

## How this repo is organized

**Experiments (E###)**
- Each experiment is a runnable module that produces outputs under `out/e###/`.
- The goal is reproducible outputs: figures + params snapshots + (optional) report snapshot.

**Docs**
- `docs/` is the public documentation surface (MyST/Sphinx).
- The gallery is the curated entry point for readers.

**Wiki**
- The wiki is where we keep the “operating system” of the repo: rules, validation pipeline, phase plan, and checklists.

---

## The “Check & Refine” loop (what we do repeatedly)

A typical iteration for an experiment:

1. **Run** the experiment with a stable default parameter set.
2. **Inspect outputs**: hero image + key figures + params snapshot.
3. **Fix**:
   - mathematical clarity (definitions, notation, correct claims)
   - visualization comparability (axes, sampling grids, normalization)
   - performance regressions (if relevant)
4. **Update docs**:
   - experiment page narrative
   - references (add/clean citations)
   - gallery entry (thumbnail + highlights)
5. **Validate** via Make targets / CI.
6. **Promote** experiment to “validated” when it meets the rubric.

Details: [The “Check & Refine” workflow](The-Check-&-Refine-workflow.md)

---

## Phase roadmap (easy → hard)

Phases are ordered by prerequisite knowledge and by code dependencies.

- [Phase 2 — Elementary number theory: divisibility, primes, modular arithmetic](Phase-2---Elementary-number-theory.md)
- [Phase 3 — Multiplicative functions & convolution identities](Phase-3---Multiplicative-functions-and-convolution-identities.md)
- [Phase 4 — Primes in patterns and progressions](Phase-4---Primes-in-patterns-and-progressions.md)
- [Phase 5 — Dirichlet characters & Gauss sums](Phase-5---Dirichlet-characters-and-Gauss-sums.md)
- [Phase 6 — L-functions, zeta, zeros, functional equation](Phase-6---L-functions-zeta-zeros.md)

If you are working “wave-based” (batching experiments into a consistent pipeline), start here:
- [Execution plan (waves)](Execution-plan-waves.md)
- [Strict pipeline per wave](Strict-pipeline-per-wave.md)

---

## Page types (conventions)

To keep the wiki consistent, pages should be one of:

- **Workflow / Runbook** (step-by-step, copy/paste friendly)
- **Policy / Rubric** (what “good” means; acceptance gates)
- **Plan / Roadmap** (what we do next, ordered)
- **Templates** (issue templates, checklists)

Try to keep pages:
- operational (do this, then that)
- short (link out instead of duplicating long docs)
- stable (avoid time-sensitive notes unless clearly marked)

---

## Editing & maintenance (repo-managed wiki)

This repo treats `wiki/` as the **source of truth** for the GitHub Wiki.

- Edit pages under `wiki/` via PRs
- CI checks links under `wiki/`
- On merge to `main`, CI publishes `wiki/` to the GitHub Wiki repository

See: `wiki/README.md` (in the repo) for the publishing mechanism.

---

## Where to put what (fast decision)

Put it in the **Wiki** if:
- it’s operational (how-to, runbook, checklist)
- it changes frequently
- it helps you maintain consistency across experiments

Put it in **docs/** if:
- it’s math exposition
- it needs citations (`{cite:p}`), MyST cross-links (`{doc}`), or Sphinx build validation
- it’s meant for readers of the documentation site
