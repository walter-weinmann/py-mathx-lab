# `mathxlab.nt.dirichlet`

Dirichlet characters and small numerical helpers.

:::{contents} On this page
:local:
:depth: 2
:::

## Quickstart

```python
from mathxlab.nt.dirichlet import euler_phi, reduced_residues, DirichletCharacter
```

:::{list-table} Public API
:header-rows: 1
:widths: 20 10 70

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
::{autoclass} mathxlab.nt.dirichlet.DirichletCharacter:members::member-order: bysource:show-inheritance::::

### Functions
::{autofunction} mathxlab.nt.dirichlet.euler_phi:::
::{autofunction} mathxlab.nt.dirichlet.reduced_residues:::
::{autofunction} mathxlab.nt.dirichlet.all_characters:::
::{autofunction} mathxlab.nt.dirichlet.character_table:::
::{autofunction} mathxlab.nt.dirichlet.conductor:::
::{autofunction} mathxlab.nt.dirichlet.orthogonality_matrix:::
