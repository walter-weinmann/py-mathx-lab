# Fermat numbers

Fermat numbers are the integers

\[
F_n = 2^{2^n} + 1 \quad (n \ge 0).
\]

They grow extremely quickly and are central to a classic “counterexample” story:
Fermat conjectured that all $F_n$ are prime, but $F_5$ is composite (Euler). {cite:p}`KrizekLucaSomer2013LecturesOnFermatNumbers,WikipediaContributors2025FermatNumber`

## Key facts

* **Coprime property:** $\gcd(F_m, F_n)=1$ for $m \ne n$. In fact, $F_0F_1\cdots F_{n-1} = F_n - 2$. {cite:p}`KrizekLucaSomer2013LecturesOnFermatNumbers`
* **Fermat primes:** If $F_n$ is prime, it is called a Fermat prime (known: $n=0..4$). {cite:p}`OEISFoundationInc2025A000215FermatNumbers`
* **Pépin test (primality):** For $n\ge 1$, $F_n$ is prime iff $3^{(F_n-1)/2} \equiv -1 \pmod{F_n}$. {cite:p}`KrizekLucaSomer2013LecturesOnFermatNumbers`

## What to experiment with

* **Factor hunting:** Search for small prime factors of $F_n$ (using modular arithmetic and wheel/primorial filters).
* **Pépin vs. trial division:** Compare performance and failure modes as $n$ increases.
* **Structure of known factors:** Many known prime factors have the form $k\cdot 2^{n+2} + 1$; explore how often such candidates appear.
* **Euclid-style numbers:** Explore $E_n = 1 + \prod_{i=0}^{n} p_i$ and compare “Euclid primes” vs. Fermat primes (they behave very differently).

## References

See {cite:t}`KrizekLucaSomer2013LecturesOnFermatNumbers,OEISFoundationInc2025A000215FermatNumbers,WikipediaContributors2025FermatNumber`.
