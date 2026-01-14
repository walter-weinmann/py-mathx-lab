# Getting started

This page is a short operational checklist for working with the repo.

## One-time setup

- Ensure your Python environment can run the project (the repo uses `uv` for dependency sync).
- Install system tools required by the docs build (LaTeX only if you build PDFs).

## Daily workflow (typical)

1. Sync dependencies (dev extras):
   - `uv sync --extra dev`
2. Run a specific experiment (example):
   - `make run EXP=e070`
3. Build docs (to check MyST + citations + links):
   - `make docs`
4. Run the test suite:
   - `make pytest`
5. If you changed performance-sensitive code:
   - `make pytest-perf` (or your perf targets)

Related:
- [The “Check & Refine” workflow](The-Check-&-Refine-workflow.md)
- [Development conventions](Development-conventions.md)
