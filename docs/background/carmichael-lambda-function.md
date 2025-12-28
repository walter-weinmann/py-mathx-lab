# Carmichael’s $\lambda(n)$ function refresher

Carmichael’s function $\lambda(n)$ is the exponent of the multiplicative group modulo $n$.
It refines Euler’s theorem by giving the *smallest* universal exponent.
See {cite:p}`erdospomeranceschmutz1991carmichaelslambdafunction` and {cite:p}`nivenzuckermanmontgomery1991introductiontheorynumbers`.

## Definition

Let $(\mathbb{Z}/n\mathbb{Z})^\times$ be the multiplicative group of units modulo $n$.
The **exponent** of a finite group $G$ is $\mathrm{lcm}$ of the orders of all elements.
Carmichael’s function $\lambda(n)$ is the exponent of $(\mathbb{Z}/n\mathbb{Z})^\times$.

Equivalently, $\lambda(n)$ is the smallest positive integer such that for all integers $a$ with $\gcd(a,n)=1$:

$$
a^{\lambda(n)}\equiv 1 \pmod n.
$$

Always $\lambda(n)\mid \varphi(n)$.

## Prime power formula (useful in code)

For odd primes $p$ and $k\ge 1$:

$$
\lambda(p^k)=\varphi(p^k)=p^{k-1}(p-1).
$$

For $2^k$:

$$
\lambda(2)=1,\quad \lambda(4)=2,\quad \lambda(2^k)=2^{k-2}\;\text{ for }k\ge 3.
$$

For general $n=\prod p_i^{\alpha_i}$:

$$
\lambda(n)=\mathrm{lcm}\big(\lambda(p_i^{\alpha_i})\big).
$$

## Why it is interesting experimentally

- highlights differences between “group size” ($\varphi$) and “group exponent” ($\lambda$)
- connects to orders modulo $n$ and to cryptographic-style modular arithmetic
- has rich average-order results and rare extreme behavior (see {cite:p}`erdospomeranceschmutz1991carmichaelslambdafunction`)

## Experiment ideas

- compare $\lambda(n)$ vs. $\varphi(n)$ on ranges
- visualize distribution of $\varphi(n)/\lambda(n)$
- record-breakers for large $\varphi(n)/\lambda(n)$
