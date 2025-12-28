# Wieferich primes

A Wieferich prime (base 2) is a prime $p$ such that

\[
2^{p-1} \equiv 1 \pmod{p^2}.
\]

Only two are currently known: $1093$ and $3511$. {cite:p}`OEISFoundationInc2025A001220WieferichPrimes,WikipediaContributors2025WieferichPrime`

## Key facts

* **Origin (Fermat’s Last Theorem, first case):** Wieferich proved in 1909 that if the first case of FLT fails for an odd prime exponent $p$, then $p$ must be a Wieferich prime (base 2). {cite:p}`Wieferich1909ZumLetztenFermatschenTheorem`
* **Rarity:** Heuristics suggest Wieferich primes are very sparse; whether infinitely many exist is open. {cite:p}`WikipediaContributors2025WieferichPrime`
* **Generalization:** One can define Wieferich primes for any base $a$ via $a^{p-1} \equiv 1 \pmod{p^2}$. {cite:p}`PrimePagesGlossary2025WieferichPrime`

## What to experiment with

* **Fast search:** Implement modular exponentiation (pow with mod) to test primes up to a bound and recover $1093,3511$.
* **Near-Wieferich primes:** Measure the $p$-adic valuation $v_p(2^{p-1}-1)$ and look for unusually large values.
* **Connections:** Explore overlaps with other “rare prime” phenomena (e.g., Wall–Sun–Sun, Wilson) as *tags* rather than hard coupling.

## References

See {cite:t}`Wieferich1909ZumLetztenFermatschenTheorem,OEISFoundationInc2025A001220WieferichPrimes,WikipediaContributors2025WieferichPrime`.
