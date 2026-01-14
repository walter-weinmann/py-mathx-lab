# Phase 2 — Elementary number theory

Phase 2 introduces the foundations required for later analytic work:

- divisibility and congruences
- primes and sieve-based computation
- modular arithmetic and residue classes
- early “output sanity” experiments for number-theoretic functions

This phase should also lock down conventions for sampling grids and plot normalization.

## 1) Phase 2 background knowledge: what to learn, in which order

### A. Phase-2 core prerequisites (minimal but essential)

1. **Modular arithmetic fundamentals**

   * Congruences, reduced residue system, units ((\mathbb{Z}/q\mathbb{Z})^*)
   * Euler’s totient (\varphi(q)), Chinese Remainder Theorem idea
   * Why “non-units” matter (characters are (0) on non-units in your experiments). 
     *Use:* this is the backbone for *all* character tables and residue-class prime counts.

2. **Multiplicative functions + Dirichlet convolution**

   * Multiplicative vs completely multiplicative functions
   * Dirichlet convolution, identity (\varepsilon), Möbius inversion
   * Why convolution shows up when comparing Dirichlet series and Euler products (your documentation cross-links (L)-functions to convolution background). 

3. **Basic complex numbers for “phase view”**

   * Roots of unity, argument/phase, complex conjugation
   * Simple numeric stability expectations for plotting phases

*(These are already explicitly treated as Phase-2 “core” in the background chapter.)* 

---

### B. Dirichlet characters (build intuition first, then structure)

4. **Definition and construction of Dirichlet characters**

   * Characters as homomorphisms ((\mathbb{Z}/q\mathbb{Z})^* \to \mathbb{C}^*)
   * Extension to (\mathbb{Z}) periodic mod (q), and (0) on non-units
   * Principal character vs non-principal; conductor, primitive vs induced (even if not all are Phase-2, you’ll want consistent terminology)

5. **Character tables and visualization**

   * What a “character table” is and how to interpret it
   * Phase plots: what patterns should look like (symmetries, principal row, missing entries for non-units)
   * This directly supports E064 (phase view) and its “principal character first row / non-units missing” semantics. 

6. **Orthogonality relations**

   * Row/column orthogonality: what it means, what numerical checks should yield
   * How orthogonality reconstructs indicator functions (this is the conceptual bridge to “sanity check” experiments like E077). 

7. **Character sums + cancellation heuristics**

   * Partial sums (S(N)=\sum_{n\le N}\chi(n))
   * Why cancellation is expected for non-principal characters
   * This is explicitly listed as background (“Character sums and cancellation heuristics”). 

---

### C. Gauss sums (needed for the “(\sqrt{q})” magnitude story)

8. **Gauss sums**

   * Definition (\tau(\chi)) and why magnitude (|\tau(\chi)|\approx \sqrt{q}) is a meaningful numerical pattern
   * Prime modulus special case intuition (your E067 notes call this out). 

---

### D. Dirichlet (L)-functions (numerics first, then “why it matters”)

9. **Dirichlet (L(s,\chi)): series and Euler product**

   * Domain where both converge absolutely: (\Re(s)>1)
   * Euler product excluding primes dividing (q) (explicitly noted in your experiment docs). 
   * This is the conceptual foundation for E068 and later for connecting zeros to oscillations in residue-class prime counts.

10. **Special values and slow convergence at (s=1)**

* Why (L(1,\chi)) is delicate numerically (slow convergence)
* Why smoothing helps (this is exactly what E069 is about). 

*(Your doc set already points to background pages for (L)-functions and convolution.)* 

---

### E. Primes in arithmetic progressions and prime races

11. **Dirichlet’s theorem (statement-level) + PNT(AP)**

* Statement: primes equidistribute among reduced residue classes
* First-order prediction used in your plots: (\mathrm{li}(x)/\varphi(q))
* That’s exactly what E070 is comparing against. 

12. **Error terms and “oscillation” viewpoint**

* Interpreting ( \pi(x;q,a) - \mathrm{Li}(x)/\varphi(q))
* Your E071 notes explicitly connect oscillations to zeros of Dirichlet (L)-functions. 

13. **Prime races and Chebyshev bias**

* Race differences like (\pi(x;4,3)-\pi(x;4,1))
* Sensitivity to the (x)-grid choice (linear vs log) — explicitly warned in your experiment pages. 
* Your prime race experiments reference the standard “prime number race” literature (Granville–Martin; Rubinstein–Sarnak). 

---

## 2) Phase 2 experiments: order, and how to revise/finalize them

### Phase 2 experiment set (as listed in the PDF)

Your Phase-2 block is naturally the contiguous run:

* **E064–E071** (characters → (L)-functions → primes in residue classes / PNT(AP)) 
* **E072–E081** (prime races + derived race statistics + orthogonality sanity + modulus effects) 

---

## A. One “finalization checklist” you apply to every Phase-2 experiment

For each experiment (E0xx):

1. **Math/notation pass (consistency)**

   * Use one notation consistently: (\chi), (\varphi(q)), (\pi(x;q,a)), (\mathrm{Li}(x)), (L(s,\chi)), (\tau(\chi))
   * Ensure every displayed formula matches what the code computes (especially where you compute “error proxies” or “derived statistics”).

2. **Reproducibility pass**

   * Deterministic defaults (no hidden randomness; if randomness exists, fixed seed saved to `params.json`)
   * Parameters saved to `params.json` (your docs repeatedly emphasize this pattern). 
   * Ensure output paths are stable: `out/e0xx/figures/...` etc.

3. **Runtime tiering**

   * Define *three parameter tiers* (even if only two are implemented):

     * **CI/preview tier**: conservative cutoffs so builds stay fast (explicitly mentioned in multiple experiment pages). 
     * **Gallery tier**: the published snapshot you want visitors to see
     * **Local exploration tier**: larger cutoffs for “asymptotic regime”

4. **Figure quality pass**

   * Axes labeled, legend meaningful, and plot answers the experiment question at a glance
   * Ensure the “hero”/gallery figure is the most interpretable one (especially for prime races)

5. **Documentation pass**

   * Ensure each page has: *Highlights*, *What this experiment does*, *Outputs*, *How to run*, *Notes*, *Published run snapshot* (your PDF uses exactly that structure). 
   * Make sure the “Notes” section includes interpretive guidance and caveats (e.g., grid sensitivity for races). 

6. **References pass**

   * Every “big claim” has a supporting reference and/or points to your background pages.
   * Your docs already cite a solid core set for this phase: Davenport, Niven et al., Apostol, Montgomery–Vaughan, Granville–Martin, Rubinstein–Sarnak.

7. **Cross-links pass**

   * Ensure `Related experiments` lists are correct and genuinely helpful (your phase is tightly connected: E064↔E065↔E066↔E068↔E070↔E071↔races).

---

## B. Recommended revision order (with rationale)

### Stage 1 — “Characters: definitions → structure → verification”

1. **E064: Dirichlet character tables (phase view)**
   Why first: it’s the most visual “definition builder” and sets conventions (principal row, non-units). 
   Finalization focus:

   * Make the phase plot interpretable for a newcomer (explain principal vs nonprincipal; why gaps appear)
   * Confirm the table ordering is deterministic (so snapshots don’t change)

2. **E065: Orthogonality matrix for Dirichlet characters**
   Why next: it verifies the computed table is *correct* numerically. 
   Finalization focus:

   * Make the orthogonality statement explicit (what inner product, what normalization)
   * Tight numerical tolerances and clear error metric (you already plot an “orthogonality error”). 

3. **E077: Indicator via character orthogonality (sanity check)**
   Why here: it turns orthogonality into a practical reconstruction check; great as a “did we implement characters correctly?” gate before races. 
   Finalization focus:

   * Show the reconstruction error for multiple residues and interpret failures (if any)

---

### Stage 2 — “Character sums and cancellation behavior”

4. **E066: Character partial sums: cancellation profiles**
   Why: builds intuition for cancellation, prepares you for (L)-series behavior and race noise. 
   Finalization focus:

   * Ensure the summary table is stable (ordering, rounding)
   * Explain what “max (|S(N)|)” means and why it matters

5. **E078: Max partial sums across characters**
   Why: extends E066 from “one modulus” to “across characters”. 
   Finalization focus:

   * Make the histogram interpretation clear (what is being histogrammed; what you expect qualitatively)

---

### Stage 3 — “Gauss sums (special but foundational)”

6. **E067: Gauss sums: magnitude vs. (\sqrt{q})**
   Why: it’s a compact “beautiful invariant” experiment and strengthens the characters section. 
   Finalization focus:

   * Add a short explanation of “primitive” and why prime (q) is the clean case (you already hint this in Notes). 

---

### Stage 4 — “Dirichlet (L)-functions: numerics that connect to primes”

7. **E068: Dirichlet (L(s,\chi)): series vs. Euler product**
   Why: this gives the key analytic connection (Euler product ↔ primes). 
   Finalization focus:

   * Very explicit domain conditions ((\Re(s)>1))
   * Explain why primes dividing (q) are excluded from the Euler product (and confirm code matches). 

8. **E069: (L(1,\chi)): slow convergence and smoothing**
   Why: highlights numerical pitfalls and introduces smoothing as a technique. 
   Finalization focus:

   * Document smoothing method clearly (what kernel/window, what the “scales” mean)
   * Provide interpretation: what “converges to (\pi/4)” means in the mod-4 example (your snapshot references this error). 

---

### Stage 5 — “Primes in residue classes and PNT(AP) plots”

9. **E070: Primes in residue classes: (\pi(x;q,a))**
   Why: this is the “entry point” to races; first show the separate curves. 
   Finalization focus:

   * Explain reduced residue classes vs non-reduced
   * Ensure the baseline (\mathrm{li}(x)/\varphi(q)) is computed consistently and documented. 

10. **E071: PNT(AP) numerics: (\pi(x;q,a)-\mathrm{Li}(x)/\varphi(q))**
    Why: it reframes the story as *error terms* and prepares for “who leads”. 
    Finalization focus:

* Make the “zeros of Dirichlet (L)-functions ↔ oscillations” remark precise (statement-level, not overclaimed). 

---

### Stage 6 — “Prime races: mod 4/3/8 + statistics”

11. **E072–E074: the canonical races (mod 4, mod 3, mod 8 leaderboard)**
    These are listed as a set in your doc. 
    Finalization focus for each:

* Standardize race difference definition and normalization across experiments
* Document the grid choice and its consequences (your docs already warn that “who leads” can change when you change sampling). 

12. **E075: Prime race statistic: distribution on a log-grid**
    Why: this starts turning the race plot into comparable summary statistics (important for “final” documentation). 
    Finalization focus:

* Define the statistic precisely and explain what distribution you expect qualitatively

13. **E076: Chebyshev (\psi(x;q,a)): weighted prime counts**
    Why: brings in (\psi) (prime powers weighting) which is closer to explicit-formula territory. 
    Finalization focus:

* Make clear what (\psi) is counting and why it differs from (\pi)

14. **E079–E081: derived race diagnostics and “effect of modulus”**
    Your table of contents lists:

* **E079:** Prime race auto-correlation
* **E080:** Prime race: leading-interval lengths
* **E081:** PNT(AP): effect of modulus on error 
  Finalization focus:
* Ensure these three share a consistent vocabulary and reuse the same baseline definitions from E070–E072
* Make the “effect of modulus” experiment explicitly comparable: fixed (x)-grid policy, fixed visualization style
