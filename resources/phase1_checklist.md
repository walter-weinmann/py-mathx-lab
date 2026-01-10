# Phase 1 Checklist — Infrastructure & “Pure Output” Sanity

This checklist is the **Definition of Done** for Phase 1 experiments.

**Scope (Phase 1 experiments):**
- E024 — Ulam spiral
- E124 — Klauber triangle
- E125 — Sacks spiral
- E126 — Hexagonal number spiral
- E019 — Prime density (PNT-style visualization; Phase-1 sanity level)

**Goal:** Ensure each experiment reliably produces correct artifacts, readable figures, and a short but complete report — **before** deep math work.

---

## How to use

- Create a copy of this checklist per experiment (or keep one checklist and tick items per experiment).
- Work in this order: **A → B → C → D → E → F**.
- If something fails, fix earlier sections first (A/B) before polishing (C/D/E).

---

## A) Run & artifacts (output contract)

- [ ] A1. Experiment runs end-to-end without manual intervention.
- [ ] A2. Output directory is **only** `out/e###/` (no stray files elsewhere).
- [ ] A3. `out/e###/params.json` is written.
- [ ] A4. `out/e###/report.md` is written.
- [ ] A5. `out/e###/figures/` exists.
- [ ] A6. At least **one** figure PNG is saved into `out/e###/figures/`.
- [ ] A7. Figure filenames are stable and meaningful (no random hashes).
- [ ] A8. If writing fails (figure/report), the run **fails loudly** (non-zero exit / exception).
- [ ] A9. (If used by your pipeline) `out/e###/manifest.json` is written/updated.

**Done for A:** After one run, `out/e###/` is complete and consistent.

---

## B) Parameters & reproducibility

- [ ] B1. `params.json` contains **all** parameters that affect output or runtime
      (e.g., `n_max`, `x_max`, `grid_type`, `layers`, `size`, `step`, `sample_size`).
- [ ] B2. If randomness exists, `seed` is a parameter and is saved to `params.json`.
- [ ] B3. Defaults are CI-safe (runtime stable; no accidental “huge run”).
- [ ] B4. Optional but recommended: two presets exist
      - `preset="ci"` (small/fast)
      - `preset="local"` (bigger/more detailed)
- [ ] B5. Re-running with the same params produces the same artifact structure
      (and for deterministic plots, the same images).

**Done for B:** Runs are comparable and reproducible; CI stays stable.

---

## C) Figure quality (readability)

- [ ] C1. Each figure has a clear title (include key parameters like `n_max`, `x_max`, `size`, `layers`).
- [ ] C2. Axes are labeled **or** intentionally omitted and explained in the report (common for spirals).
- [ ] C3. Scale is explicit (linear/log clearly indicated).
- [ ] C4. Legends are present only if they add information (otherwise remove).
- [ ] C5. Overplotting is controlled (marker size/alpha/downsampling so patterns remain visible).
- [ ] C6. Export resolution is sufficient for both thumbnail and full-size viewing.
- [ ] C7. No clipped labels/titles (tight layout / bbox handling).

**Done for C:** A reader can understand what the plot is showing without extra explanation.

---

## D) report.md minimum standard (Phase 1 level)

- [ ] D1. **Summary** (3–6 sentences): what is computed and what is shown.
- [ ] D2. **Parameters** section: bullet list of the main parameters and values.
- [ ] D3. **Key observation**: 2–5 concrete bullets that a reader can verify from the figures.
- [ ] D4. **Interpretation**: 1 short paragraph with cautious interpretation (no overclaim).
- [ ] D5. **Caveats**: at least 4 bullets, e.g.
      - finite N / finite range
      - sampling bias (linear vs log grids)
      - visualization artifacts / perception bias
      - runtime depends on implementation details
- [ ] D6. Use “observed up to …” instead of “always/proves …” unless it’s truly proved.
- [ ] D7. If multiple figures exist: one-line guide (“Fig 1 shows… Fig 2 shows…”).

**Done for D:** The report is short, complete, and safe in its claims.

---

## E) Docs page & consistency

- [ ] E1. Experiment docs follow the same structure as your chosen reference page (e.g., e024):
      Goal → Method → Results → Interpretation → Caveats → References → Related experiments.
- [ ] E2. Tags are valid (restricted to `docs/tags.md`).
- [ ] E3. **Related experiments** lists 2–6 relevant experiment IDs/links.
- [ ] E4. References are minimal and useful (1–3 strong sources are enough).
- [ ] E5. No broken internal links (figures/reports/references).

**Done for E:** Docs build cleanly and pages look uniform.

---

## F) Phase 1 batch sanity (project-level)

- [ ] F1. All Phase 1 experiments run back-to-back locally (E024, E124, E125, E126, E019).
- [ ] F2. Tests + lint/format + typing targets pass after the changes.
- [ ] F3. Docs build passes (no new warnings/errors introduced).
- [ ] F4. Gallery thumbnails look reasonable (at least one “hero” figure per experiment is readable).
- [ ] F5. No experiment writes outside its own `out/e###/` directory.

**Done for F:** Phase 1 is closed: reproducible, CI-safe, output-clean.

---

## Notes (optional)

- Phase 1 is intentionally “low math knowledge”. Prefer clarity, reproducibility, and disciplined reporting.
- Deeper theory upgrades happen in Phase 2 (probabilistic guarantees, bounds, residue classes, etc.).
