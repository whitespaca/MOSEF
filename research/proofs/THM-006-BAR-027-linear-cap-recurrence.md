# THM-006 and BAR-027: first linear-cap recurrence

## Claim status and scope

- `DEF-033`: `DEFINITION`.
- `THM-006`: `PROVED` on the complete finite balanced-semiprime promise
  \(9\le m\le21\).
- `BAR-027`: `PROVED` for the exact DEF-032 selector at \(m=21\).
- `REF-029`: `REFUTED`.

No claim below concerns \(m>21\), promise recognition, or general classical
polynomial-time factoring.

## DEF-033: finite cap envelopes

When it exists, define the first injective cap
\[
L_m^\star=\min\{L\ge m:\mathcal T_{m,L}
\text{ is injective on }\mathcal P_m\}.
\]
For a finite range \(9\le m\le M\), define
\[
t_M^\star=\max_{9\le m\le M}(L_m^\star-m),\qquad
c_M^\star=\max_{9\le m\le M}\frac{L_m^\star-1}{m}.
\]
Then \(m+t\) covers the registered thresholds exactly when integer
\(t\ge t_M^\star\), while \(\lceil cm\rceil\) covers them exactly when
\(c>c_M^\star\). These are finite certificate envelopes, not asymptotic
growth rates.

## BAR-027: recurrence at the next length

At \(m=21\), both M32 schedules give
\[
m+11=\left\lceil\frac{151m}{100}\right\rceil=32.
\]
The complete balanced population has 57 primes. The cap-32 selector has
2,511 descriptors, 20,088 raw primitive coordinates, and 69 normalized
nonconstant coordinates, but
\[
1031,\quad1231,\quad1319,\quad1433
\]
share one signature. Thus all six pair products fail every charged exit.

The independent dense verifier evaluates every one of the 2,511 descriptors
on all four primes and confirms equal branch-total masks. This proves an
exact recurrence collision, not a sampled failure, and refutes REF-029:
\(m+11\) does not remain injective through \(m=21\). The
\(\lceil151m/100\rceil\) schedule fails on the same exact selector.

At cap 33, 2,752 descriptors yield 74 normalized coordinates and 57 distinct
signatures. A deterministic 53-coordinate sublist has pairwise distinct
packed signatures; the dense verifier checks all 1,596 population pairs.
Because cap 32 collides and every smaller selector is its subset, cap 33 is
the exact first injective cap \(L_{21}^\star\).

## THM-006: repaired finite construction

The M32 thresholds give \(t_{20}^\star=11\). Since
\(L_{21}^\star-21=12\), DEF-033 gives
\[
t_{21}^\star=12.
\]
Therefore the public factorization-independent selector with
\[
L(m)=m+12
\]
is injective on every complete balanced population for \(9\le m\le21\) and
exposes a proper factor of every distinct-prime balanced semiprime in this
finite range. Offset 12 is minimal because offset 11 is exactly the failed
cap-32 selector at \(m=21\).

For multiplicative caps, M32 gives \(c_{20}^\star=3/2\), while the new row
gives
\[
\frac{L_{21}^\star-1}{21}=\frac{32}{21}>\frac32.
\]
Hence the exact coefficients covering the complete range through 21 are
\(c>32/21\). The old witness \(151/100\) fails; \(153/100\) is one fixed
public succeeding witness.

## Cost and recognition

Both repaired schedules remain linear, so DEF-032 gives
\(O(m^3\log m)\) compact modular work, \(O(m^3)\) GCDs and outputs, and
polynomial total bit complexity. Population enumeration, normalization, and
dense expansion are certificate operations only. The balanced promise
remains factor dependent and is not claimed recognizable before factoring.

## Adversarial review

- Both failed M32 formulas are evaluated exactly at the same public cap 32.
- The four-prime bucket preserves all six full/unit collision pairs.
- Cap-33 injectivity is a complete 57-prime certificate, not sampling.
- Exact threshold minimality follows from the cap-32 collision and raw
  selector inclusion.
- The 53-coordinate greedy certificate is not claimed minimum.
- \(c=32/21\) is excluded because the ceiling condition is strict.
- No finite envelope is described as an asymptotic rate.
- General factoring and promise recognition remain open.
