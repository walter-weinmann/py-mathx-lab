# Heegner numbers

## Overview

The **Heegner numbers** are the nine positive integers

$$
d \in \{1,2,3,7,11,19,43,67,163\}
$$

for which the imaginary quadratic field $K=\mathbb{Q}(\sqrt{-d})$ has **class number**
$h_K = 1$. Equivalently, the ring of integers $\mathcal{O}_K$ is a **unique factorization domain** (UFD).
{cite:p}`WikipediaContributors2025HeegnerNumber,Weisstein2025HeegnerNumberMathWorld`

This “exactly nine” phenomenon is one of the landmark classification results in classical algebraic number theory
and is tightly connected to:
- the arithmetic of **binary quadratic forms** (Gauss),
- **complex multiplication** of elliptic curves and **singular moduli** (Heegner–Stark),
- and the famous “almost integer” $e^{\pi\sqrt{163}}$.

{cite:p}`Cox2013PrimesOfTheFormX2PlusNY2`

---

## 1. Imaginary quadratic fields and discriminants

Let $d>0$ be squarefree and set $K=\mathbb{Q}(\sqrt{-d})$.

### 1.1 The ring of integers $\mathcal{O}_K$

A frequent pitfall is assuming $\mathcal{O}_K=\mathbb{Z}[\sqrt{-d}]$ always holds.
In fact:

- If $d\equiv 1,2 \pmod 4$, then
  $$
  \mathcal{O}_K=\mathbb{Z}[\sqrt{-d}],
  \qquad
  \Delta_K=-4d.
  $$
- If $d\equiv 3 \pmod 4$, then
  $$
  \mathcal{O}_K=\mathbb{Z}\!\left[\frac{1+\sqrt{-d}}{2}\right],
  \qquad
  \Delta_K=-d.
  $$

Here $\Delta_K$ is the (fundamental) **field discriminant**.
{cite:p}`Cox2013PrimesOfTheFormX2PlusNY2`

### 1.2 Heegner discriminants

Because the theory is often indexed by discriminant rather than by $d$, it is useful to record:

$$
\Delta \in \{-4,-8,-3,-7,-11,-19,-43,-67,-163\}
$$

These are exactly the **negative fundamental discriminants** with class number $1$.
{cite:p}`Cox2013PrimesOfTheFormX2PlusNY2`

---

## 2. Class number and unique factorization

### 2.1 From element factorization to ideal factorization

The ring $\mathcal{O}_K$ is a **Dedekind domain**. This implies:

- Every nonzero ideal factors uniquely into prime ideals.
- But elements in $\mathcal{O}_K$ may fail to factor uniquely into irreducibles.

The mechanism measuring “how far” we are from principal ideals is the **ideal class group**:

$$
\mathrm{Cl}(\mathcal{O}_K)
=
\frac{\{\text{nonzero fractional ideals of }\mathcal{O}_K\}}
{\{\text{principal fractional ideals}\}}.
$$

Its cardinality is the **class number**:

$$
h_K := \#\mathrm{Cl}(\mathcal{O}_K).
$$

{cite:p}`Cox2013PrimesOfTheFormX2PlusNY2`

### 2.2 Why $h_K=1$ is the same as “UFD” here

For rings of integers in number fields (Dedekind domains), we have the chain of equivalences:

$$
h_K=1
\iff
\text{every ideal is principal (PID)}
\iff
\mathcal{O}_K \text{ is a UFD}.
$$

So Heegner numbers classify precisely the imaginary quadratic integer rings with unique factorization.
{cite:p}`Cox2013PrimesOfTheFormX2PlusNY2`

### 2.3 A concrete failure of unique factorization

In $\mathbb{Z}[\sqrt{-5}]$ (which corresponds to $d=5$, **not** a Heegner number), we have:

$$
6 = 2\cdot 3 = (1+\sqrt{-5})(1-\sqrt{-5}),
$$

and these are genuinely distinct factorizations (up to units), so UFD fails; indeed $h_{\mathbb{Q}(\sqrt{-5})}>1$.
{cite:p}`Cox2013PrimesOfTheFormX2PlusNY2`

---

## 3. Gauss’ binary quadratic forms viewpoint

Binary quadratic forms provide a very concrete model for class groups.

A primitive positive definite binary quadratic form is

$$
Q(x,y)=ax^2+bxy+cy^2,
\qquad a,b,c\in\mathbb{Z},
$$

with negative discriminant

$$
\Delta=b^2-4ac<0.
$$

Two forms are equivalent if related by an $\mathrm{SL}_2(\mathbb{Z})$ change of variables.
Gauss’ composition defines a finite abelian group on equivalence classes, and that group matches the ideal class group
(for the order of discriminant $\Delta$; in particular for fundamental $\Delta$ it matches $\mathrm{Cl}(\mathcal{O}_K)$).
{cite:p}`Cox2013PrimesOfTheFormX2PlusNY2`

### 3.1 Reduced forms and the class number

A positive definite form $(a,b,c)$ is **reduced** if:

$$
|b|\le a\le c,
$$

and if $|b|=a$ or $a=c$, then additionally $b\ge 0$.

A key fact: the number of reduced forms of discriminant $\Delta$ equals the class number $h(\Delta)$.
So $h(\Delta)=1$ means: **there is exactly one reduced form** for that discriminant.
{cite:p}`Cox2013PrimesOfTheFormX2PlusNY2`

### 3.2 The unique reduced forms for the Heegner discriminants

For each Heegner discriminant, the single reduced form can be written explicitly:

- $\Delta=-4$: $x^2+y^2$
- $\Delta=-8$: $x^2+2y^2$
- $\Delta=-3$: $x^2+xy+y^2$
- $\Delta=-7$: $x^2+xy+2y^2$
- $\Delta=-11$: $x^2+xy+3y^2$
- $\Delta=-19$: $x^2+xy+5y^2$
- $\Delta=-43$: $x^2+xy+11y^2$
- $\Delta=-67$: $x^2+xy+17y^2$
- $\Delta=-163$: $x^2+xy+41y^2$

You can verify, for example, that $x^2+xy+41y^2$ has discriminant $1-4\cdot 1\cdot 41=-163$.
This “single reduced form” phenomenon is another face of class number one.
{cite:p}`Cox2013PrimesOfTheFormX2PlusNY2`

---

## 4. The class-number-one theorem (why exactly nine?)

The theorem states that there are **exactly nine** imaginary quadratic fields of class number one.
Historically:

- **Heegner (1952)** proved the result using modular functions and the emerging ideas of **complex multiplication**.
  {cite:p}`Heegner1952DiophantischeAnalysisUndModulfunktionen`
- A gap in the original proof was later clarified and the argument completed/strengthened in later work (notably by **Stark**),
  leading to the modern accepted classification.
  {cite:p}`Stark1967CompleteDeterminationClassNumberOne,Stark1969GapInTheoremOfHeegner`
- The broader Diophantine toolkit around these questions is closely linked to effective bounds from
  linear forms in logarithms (Baker’s theory).
  {cite:p}`Baker1966LinearFormsInLogarithmsI`

A widely used modern reference that connects the class group, quadratic forms, and complex multiplication in one narrative is Cox.
{cite:p}`Cox2013PrimesOfTheFormX2PlusNY2`

---

## 5. Why Heegner numbers create “almost integers”

The most famous numerical surprise is:

$$
e^{\pi\sqrt{163}} \approx 262537412640768743.999999999999\ldots
$$

This is not an accident; it comes from **complex multiplication** and the $q$-expansion of the modular $j$-invariant.

### 5.1 The $j$-invariant and its $q$-series

Let $j(\tau)$ be the modular $j$-invariant. It has a Fourier expansion in

$$
q = e^{2\pi i\tau}
$$

of the form

$$
j(\tau) = q^{-1} + 744 + 196884\,q + \cdots,
$$

with integer coefficients.
{cite:p}`DiamondShurman2005FirstCourseModularForms`

When $\tau$ is an **imaginary quadratic** point in the upper half-plane (a CM point), $j(\tau)$ is an **algebraic integer**.
More precisely, $j(\tau)$ generates the **Hilbert class field** of $K=\mathbb{Q}(\tau)$.
When $h_K=1$, the Hilbert class field is just $K$ itself, and the special values become exceptionally explicit.
{cite:p}`Cox2013PrimesOfTheFormX2PlusNY2`

### 5.2 Why $d=163$ is the showpiece

Take

$$
\tau=\frac{1+\sqrt{-163}}{2}.
$$

Then $\mathrm{Im}(\tau)=\frac{\sqrt{163}}{2}$, so

$$
|q| = e^{-2\pi\,\mathrm{Im}(\tau)} = e^{-\pi\sqrt{163}},
$$

which is astronomically small. Also $\mathrm{Re}(\tau)=\tfrac12$, so $q$ is *negative real* to extremely high precision:

$$
q = e^{2\pi i(\frac12+i\frac{\sqrt{163}}{2})}
  = e^{\pi i}\,e^{-\pi\sqrt{163}}
  = -e^{-\pi\sqrt{163}}.
$$

Therefore $q^{-1}\approx -e^{\pi\sqrt{163}}$ and the expansion implies

$$
j(\tau) = q^{-1} + 744 + O(q)
$$

is extremely close to $q^{-1}+744$.

For this specific CM point, complex multiplication yields the celebrated exact value

$$
j\!\left(\frac{1+\sqrt{-163}}{2}\right)=-640320^3.
$$

Substituting $q^{-1}\approx -e^{\pi\sqrt{163}}$ gives

$$
e^{\pi\sqrt{163}} \approx 640320^3 + 744,
$$

and the error is on the order of $e^{-\pi\sqrt{163}}$, explaining why the approximation is absurdly accurate.
{cite:p}`Cox2013PrimesOfTheFormX2PlusNY2,Weisstein2025HeegnerNumberMathWorld,WikipediaContributors2025HeegnerNumber`

---

## 6. Analytic class number formula (bridge to $L$-functions)

A second “high-level” way to see class numbers is the Dirichlet class number formula.
For a negative fundamental discriminant $\Delta<0$:

$$
h(\Delta)=\frac{w\,\sqrt{|\Delta|}}{2\pi}\,L(1,\chi_\Delta).
$$

Here:
- $w$ is the number of roots of unity in $\mathcal{O}_K$; for imaginary quadratic fields,
  $w=2$ except for $\Delta=-4$ (Gaussian integers, $w=4$) and $\Delta=-3$ (Eisenstein integers, $w=6$).
- $\chi_\Delta(n)=\left(\frac{\Delta}{n}\right)$ is the Kronecker symbol (a quadratic Dirichlet character),
- and
  $$
  L(1,\chi_\Delta)=\sum_{n=1}^{\infty}\frac{\chi_\Delta(n)}{n}.
  $$

This formula is the doorway from “class number” into Dirichlet characters and $L$-functions, and it is a natural starting point
for computational experiments around prime races / residue classes later.
{cite:p}`Cox2013PrimesOfTheFormX2PlusNY2`

---

## 7. Computation-friendly viewpoints (good experiment hooks)

### 7.1 Counting reduced forms (elementary and visual)

For a negative fundamental discriminant $\Delta$, enumerate all integer triples $(a,b,c)$ with:

$$
b^2 - 4ac = \Delta,\quad a>0,\quad |b|\le a\le c,
$$

apply the reduced-form tie-break rules, and count reduced forms. That count is $h(\Delta)$.

For the Heegner discriminants, you will find exactly one reduced class.

### 7.2 “Almost integers” via truncated $q$-series

Choose $d\in\{19,43,67,163\}$ and set $\tau=(1+\sqrt{-d})/2$.
Compute $q=e^{2\pi i\tau}$ numerically and compare:

$$
q^{-1} + 744
\quad \text{vs.} \quad
j(\tau)
$$

approximating $j(\tau)$ by truncating its $q$-expansion. The gap shrinks dramatically as $d$ increases, with $d=163$ the most striking.

---

## 8. Common confusion: Heegner numbers vs Heegner points

- **Heegner numbers**: the nine $d$ for which $\mathbb{Q}(\sqrt{-d})$ has class number $1$.
- **Heegner points**: CM points on modular curves / elliptic curves used in deep results about ranks of elliptic curves
  (e.g. Gross–Zagier and Kolyvagin).

They share the same complex multiplication background, but they are different objects.

---

## References

- {cite:t}`Heegner1952DiophantischeAnalysisUndModulfunktionen`
- {cite:t}`Stark1967CompleteDeterminationClassNumberOne`
- {cite:t}`Stark1969GapInTheoremOfHeegner`
- {cite:t}`Baker1966LinearFormsInLogarithmsI`
- {cite:t}`Cox2013PrimesOfTheFormX2PlusNY2`
- {cite:t}`DiamondShurman2005FirstCourseModularForms`
- {cite:t}`Weisstein2025HeegnerNumberMathWorld`
- {cite:t}`WikipediaContributors2025HeegnerNumber`
