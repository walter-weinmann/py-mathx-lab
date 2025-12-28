# Primorials

The primorial of a prime $p_k$ is

\[
p_k\# = \prod_{i=1}^{k} p_i
\]

(the product of the first $k$ primes). Primorials are a natural “smoothing knob” in experimental number theory: they amplify small prime structure and appear in constructions like Euclid numbers $p_k\# \pm 1$. {cite:p}`PrimePagesGlossary2025Primorial,OEISFoundationInc2025A002110Primorial`

## Key facts

* **Growth:** $\log(p_k\#) = \sum_{i\le k} \log p_i$; by the prime number theorem this is asymptotic to $p_k$ (in a coarse sense). {cite:p}`HardyWright2008AnIntroductionToTheTheoryOfNumbers`
* **Euclid numbers:** $p_k\# + 1$ is coprime to all primes $\le p_k$, but is usually composite (so: “Euclid’s proof does *not* generate primes”). {cite:p}`PrimePagesGlossary2025Primorial`

## What to experiment with

* **Euclid-number factorization:** For $E_k = p_k\# \pm 1$, try to find small factors and compare +1 vs. -1.
* **Primorial wheels:** Use primorials to build “wheel sieves” and benchmark against a simple sieve.
* **Primorial primes / plus/minus primes:** Scan for primes of the form $p_k\# \pm 1$ and visualize rarity.

## References

See {cite:t}`OEISFoundationInc2025A002110Primorial,PrimePagesGlossary2025Primorial,WikipediaContributors2025Primorial`.
