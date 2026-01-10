# `mathxlab.exp.logging`

Reusable helpers for the `mathxlab` project.

:::{admonition} Stability
:class: note

Status: **Experimental**.

This project treats the documented names as the *public surface*, but details may still evolve.
If you need strict API guarantees, add `__all__ = [...]` to each module and version releases accordingly.
:::

## Design notes
- Keep experiment scripts small: delegate I/O, seeding, and logging here.
- Aim for reproducible outputs (fixed seeds, stable file names).

## Examples

### Enable verbose logging for mathxlab code

```python
from mathxlab.exp.logging import LoggingConfig, setup_logging
setup_logging(config=LoggingConfig(verbose=True))
```

## Public API

:::{list-table}
:header-rows: 1
:widths: 22 10 68

* - Name
  - Kind
  - Summary
* - `LoggingConfig`
  - class
  - Configuration for experiment logging.
* - `setup_logging`
  - function
  - Set up logging for experiment runs.
* - `get_logger`
  - function
  - Get a logger for a specific module.
:::
## Reference

### Classes

:::{autoclass} mathxlab.exp.logging.LoggingConfig
:members:
:member-order: bysource
:show-inheritance:
:::

### Functions

:::{autofunction} mathxlab.exp.logging.setup_logging
:::

:::{autofunction} mathxlab.exp.logging.get_logger
:::

