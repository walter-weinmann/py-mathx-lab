# Wiki publishing (repo-managed)

This repository treats `wiki/` as the **source of truth** for GitHub Wiki pages.

Workflow
- Edit Markdown files in `wiki/` in normal PRs.
- CI checks links inside `wiki/`.
- On merge to `main`, CI publishes `wiki/` to the GitHub Wiki repo: `<owner>/<repo>.wiki.git`.

Setup required
- Create a fine-grained PAT with access to this repo (Contents: read/write).
- Add it as a repo secret named `WIKI_TOKEN`.

Notes
- Keep math-heavy pages with MyST/Sphinx roles in `docs/`, not in the GitHub Wiki.
