# `mathxlab.nt.convolution`

Dirichlet convolution helpers.

:::{contents} On this page
:local:
:depth: 2
:::

## Quickstart

```python
from mathxlab.nt.convolution import dirichlet_convolution, epsilon, ConvolutionResult
```

:::{list-table} Public API
:header-rows: 1
:widths: 20 10 70

* - Name
  - Kind
  - Summary
* - `ConvolutionResult`
  - class
  - Result of a Dirichlet convolution computed on a prefix.
* - `dirichlet_convolution`
  - function
  - Compute the Dirichlet convolution (f*g)(n) for n <= n_max.
* - `epsilon`
  - function
  - Return the identity element ε for Dirichlet convolution on [0..n_max].
* - `ones`
  - function
  - Return the constant-one function 1(n)=1 for n>=1.
* - `identity`
  - function
  - Return the identity arithmetic function id(n)=n.
:::

## Reference
### Classes
::{autoclass} mathxlab.nt.convolution.ConvolutionResult:members::member-order: bysource:show-inheritance::::

### Functions
::{autofunction} mathxlab.nt.convolution.dirichlet_convolution:::
::{autofunction} mathxlab.nt.convolution.epsilon:::
::{autofunction} mathxlab.nt.convolution.ones:::
::{autofunction} mathxlab.nt.convolution.identity:::
