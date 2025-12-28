# Partition function $p(n)$ refresher

The partition function $p(n)$ counts the number of ways to write $n$ as a sum of positive integers,
ignoring order (e.g. $4=4=3+1=2+2=2+1+1=1+1+1+1$ gives $p(4)=5$).
See {cite:p}`andrews1984theoryofpartitions`.

## Definition

A **partition** of $n$ is a multiset of positive integers with sum $n$.
The partition function $p(n)$ is the number of such partitions.

Conventions:
- $p(0)=1$ (empty partition)
- $p(n)=0$ for $n<0$

## Generating function

The ordinary generating function is

$$
\sum_{n\ge 0} p(n) q^n = \prod_{m\ge 1}\frac{1}{1-q^m}.
$$

This identity is the starting point for many algorithms and proofs.

## Growth

$p(n)$ grows very rapidly (roughly like $\exp(C\sqrt{n})$), so experiments often use log-scales
or focus on modular patterns.

## Experiment ideas

- compute $p(n)$ for $n\le N$ via dynamic programming and plot $\log p(n)$
- explore congruences (e.g. Ramanujan-type congruences)
- compare exact values to asymptotic approximations (later experiment)
