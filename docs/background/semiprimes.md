# Semiprimes

A semiprime is an integer that is the product of two primes (not necessarily distinct), i.e.

$$
n = pq \quad (p, q \text{ prime}).
$$

Semiprimes sit at the center of practical factorization hardness and are the basic objects behind RSA-style moduli. {cite:p}`RivestShamirAdleman1978RSA,OEISFoundationInc2025A001358Semiprimes`

## Key facts

* **Sequence:** The semiprimes form OEIS sequence A001358. {cite:p}`OEISFoundationInc2025A001358Semiprimes`
* **RSA context:** RSA uses $N=pq$ and the difficulty of factoring $N$ (when $p,q$ are large and random-looking). {cite:p}`RivestShamirAdleman1978RSA`
* **Special cases:** $p=q$ yields squares of primes; $p\ne q$ yields “RSA-like” semiprimes.

## What to experiment with

* **Distribution:** Count semiprimes up to $X$ and compare empirical growth with simple heuristic approximations.
* **Factorization methods:** Benchmark trial division, Pollard’s rho, and (for larger sizes) ECM bindings if you later allow optional deps.
* **RSA-style generation:** Generate balanced semiprimes ($p,q$ same bitlength) and compare factorization difficulty vs unbalanced ones.
* **Smoothness:** Explore how often $p-1$ or $q-1$ is smooth (motivates $p-1$ factoring methods).

## References

See {cite:t}`RivestShamirAdleman1978RSA,OEISFoundationInc2025A001358Semiprimes`.
