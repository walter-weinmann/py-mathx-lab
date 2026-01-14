# Execution plan (waves)

A “wave” is a batch of experiments finalized together using the same strict pipeline.

## Why waves

- Keeps naming conventions and plots consistent across a cluster.
- Ensures shared utilities are validated once per wave, not repeatedly.
- Produces visible progress in the gallery.

## Typical wave content

- 6–20 experiments in a coherent topic cluster
- at least one background article update (if definitions are reused often)
- perf tests for shared functions (when runtime-sensitive)
