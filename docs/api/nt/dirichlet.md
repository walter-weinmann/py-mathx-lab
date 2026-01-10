# `mathxlab.nt.dirichlet`

Dirichlet characters and small numerical helpers.

:::{admonition} Stability
:class: note

Status: **Experimental**.

This project treats the documented names as the *public surface*, but details may still evolve.
If you need strict API guarantees, add `__all__ = [...]` to each module and version releases accordingly.
:::

## Design notes
- Functions are designed for experiment-scale inputs (not cryptographic workloads).
- Prefer explicit parameters (e.g., `n_max`) for reproducibility.

## Examples

### Evaluate a Dirichlet character

```python
from mathxlab.nt.dirichlet import all_characters
chi = all_characters(5)[1]
print(chi(2))
```

## Public API

:::{list-table}
:header-rows: 1
:widths: 22 10 68

* - Name
  - Kind
  - Summary
* - `euler_phi`
  - function
  - Compute Euler's totient φ(n) by prime factorization.
* - `reduced_residues`
  - function
  - Return the reduced residue system modulo ``q`` (sorted).
* - `DirichletCharacter`
  - class
  - Dirichlet character modulo q.
* - `all_characters`
  - function
  - Enumerate all Dirichlet characters modulo q.
* - `character_table`
  - function
  - Return the full character table as a matrix.
* - `conductor`
  - function
  - Compute the conductor of a character by brute-force divisor checks.
* - `orthogonality_matrix`
  - function
  - Compute the character orthogonality matrix for modulus q.
:::
## Reference

### Classes

:::{autoclass} mathxlab.nt.dirichlet.DirichletCharacter
:members:
:member-order: bysource
:show-inheritance:
:::

### Functions

:::{autofunction} mathxlab.nt.dirichlet.euler_phi
:::

:::{autofunction} mathxlab.nt.dirichlet.reduced_residues
:::

:::{autofunction} mathxlab.nt.dirichlet.all_characters
:::

:::{autofunction} mathxlab.nt.dirichlet.character_table
:::

:::{autofunction} mathxlab.nt.dirichlet.conductor
:::

:::{autofunction} mathxlab.nt.dirichlet.orthogonality_matrix
:::

