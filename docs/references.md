# References

This page lists the bibliography used across the documentation and experiment write-ups.

## How to cite

Use `[]` with a BibTeX key.

Example:

- “We follow standard numerical analysis references [knuth1997].”

If you want a dedicated reference list on an experiment page, add at the end of that page:

```md
## References

```{bibliography}
:filter: docname in docnames
````

````

This will include only the entries that are actually cited on that page.

## Full bibliography

```{bibliography}
:all:
````
