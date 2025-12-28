# Carmichael numbers

A Carmichael number is a composite $n$ such that

\[
a^{n-1} \equiv 1 \pmod{n}
\]

for every integer $a$ coprime to $n$. They are **absolute Fermat pseudoprimes**, so they defeat the naive Fermat primality test. {cite:p}`WikipediaContributors2025CarmichaelNumber,PrimePagesGlossary2025CarmichaelNumber`

## Key facts

* **Korselt’s criterion (1899):** $n$ is Carmichael iff (i) $n$ is squarefree and (ii) for every prime $p\mid n$, we have $(p-1)\mid (n-1)$. {cite:p}`Conrad2004KorseltsCriterionForCarmichaelNumbers,WikipediaContributors2025CarmichaelNumber`
* **At least 3 prime factors:** No Carmichael number is the product of only two primes. {cite:p}`WikipediaContributors2025CarmichaelNumber`
* **Infinitely many:** Alford–Granville–Pomerance proved there are infinitely many Carmichael numbers. {cite:p}`AlfordGranvillePomerance1994InfinitelyManyCarmichaelNumbers`
* **Historical origin:** Carmichael studied these numbers in the early 20th century. {cite:p}`Carmichael1912CompositeNumbersSatisfyingFermatTheorem`

## What to experiment with

* **Counterexample search:** Find Carmichael numbers by generating squarefree products and testing Korselt’s criterion.
* **“Fermat test is not enough”:** Show that all bases $a$ with $\gcd(a,n)=1$ pass Fermat for a Carmichael $n$, while a Miller–Rabin test quickly finds witnesses.
* **Distribution experiments:** Count Carmichael numbers up to $X$ and compare growth to simple heuristics.
* **Construction families:** Implement Chernick-style constructions and see when factors are prime.

## References

See {cite:t}`AlfordGranvillePomerance1994InfinitelyManyCarmichaelNumbers,Conrad2004KorseltsCriterionForCarmichaelNumbers,OEISFoundationInc2025A002997CarmichaelNumbers,WikipediaContributors2025CarmichaelNumber`.
