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

## How to use this wiki

Use the **navigation on the right** (Sidebar) to find:
- setup + conventions
- workflows and rubrics
- execution plans (waves)
- phase roadmap pages

If you’re new here, start with **Getting started** in the Sidebar.

---

## What lives where

**Wiki**
- operational runbooks, workflows, checklists
- phase plan and execution “operating system”

**Docs (`docs/`)**
- math exposition, longer narratives, citations and Sphinx/MyST structure

**Experiments**
- runnable modules producing outputs under `out/e###/`
- aim: reproducible figures + params snapshots (+ optional report snapshot)

---

## Editing & maintenance (repo-managed wiki)

This repo treats `wiki/` as the **source of truth** for the GitHub Wiki.

- Edit pages under `wiki/` via PRs
- CI checks links under `wiki/`
- On merge to `main`, CI publishes `wiki/` to the GitHub Wiki repository

See: `wiki/README.md` (in the repo) for the publishing mechanism.
