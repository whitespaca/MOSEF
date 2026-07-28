# THM-004 and BAR-025: diversified exceptional-selector certificates

## Status

`THM-004` and `BAR-025` are `PROVED` in the exact finite promise model below.
The normalization lemma holds for every input length \(m\ge9\). The positive
construction is restricted to \(9\le m\le15\), and the obstruction is an
explicit collision for the same selector at \(m=16\). Neither statement is an
asymptotic theorem about all polynomial selectors.

## Public selector and quantifier order

For an input length \(m\ge9\), before the particular input \(N\) is received,
construct the lexicographically ordered descriptor set
\[
\mathcal T_m=\{(i,A,B,g):2\le A,B,g\le m,\ A\ne B\},
\]
subject to one of the public exceptional-family conditions
\[
\begin{aligned}
i=4 &: A\equiv B\equiv3\pmod4,\\
i=6 &: A\equiv5\pmod6,\quad B\equiv3\pmod6.
\end{aligned}
\]
The constructor receives \(m\), not \(N\), its factors, a support oracle, or
any local root data. It emits at most \(2(m-1)^3\) descriptors.

For one descriptor retain the following primitive charged GCD exits, in this
order:

1. the base \(g\);
2. \(Q_1(g)=S_A(g)\);
3. \(Q_2(g)=S_B(g^A)\);
4. the first public overlap bound \(B\);
5. the second public overlap bound \(B\) for \(\Phi_4\), or \(2B\) for
   \(\Phi_6\);
6. the direct \(\Phi_i(g)\);
7. the public cyclotomic/cofactor resultant \(R_i\) from BAR-021;
8. the independently evaluated compact cofactor \(C_i(g)\).

The aggregate \(F_i(g)=\Phi_i(g)C_i(g)\) is still evaluated by the public
algorithm. Its prime-support bit is the Boolean OR of the direct and cofactor
bits. Likewise every retained stage/aggregate overlap bit is an AND of
already retained primitive bits. These derived coordinates therefore cannot
separate two primes whose primitive signatures are equal.

## Balanced population and total semantics

Let
\[
\mathcal P_m=\{p\text{ prime}:2^{m-1}\le p^2<2^m\}.
\]
Every distinct \(p,q\in\mathcal P_m\) gives an \(m\)-bit square-free
semiprime \(pq\). For \(m\ge9\), an elementary induction gives
\[
2^{(m-1)/2}>m,
\]
so every \(p\in\mathcal P_m\) exceeds \(m\). Thus every scheduled base is a
unit modulo every population prime, and neither \(B\) nor \(2B\) contributes
a nonconstant population coordinate. Outside this promise, the ordinary base
GCD is total: a proper value is a factor, while a full base collision skips
that descriptor's unit-only continuation.

For a primitive public integer \(z\), define its analytical support column
\[
h_z(p)=\mathbf1_{p\mid z}\qquad(p\in\mathcal P_m).
\]
This column is a proof object. The public algorithm computes residues and
GCDs modulo \(N\); it does not enumerate \(\mathcal P_m\) or factor \(z\).

## Exact normalization lemma

Delete every all-zero or all-one support column and identify every pair of
equal remaining columns. Record one bit for each distinct nonconstant
column. Call the resulting map \(\nu_m\).

For any population primes \(p,q\), the complete charged selector separates
\(pq\) if and only if
\[
\nu_m(p)\ne\nu_m(q).
\]
Indeed, a constant column never distinguishes a pair, and replacing equal
columns by one copy preserves every equality comparison. Conversely, every
retained normalized bit is one original charged primitive exit. The omitted
aggregate and overlap coordinates are Boolean functions of retained
primitive coordinates and cannot distinguish equal primitive signatures.
BAR-024 then converts signature inequality exactly into a proper GCD.

This normalization also prevents double counting. Cofactor novelty is the
drop in collision pairs after all noncofactor primitive columns have first
formed their partition and the genuinely new cofactor columns are then
added. A cofactor hit already duplicated by a direct or resultant column
contributes zero marginal pairs.

## THM-004: finite restricted construction

For every \(m\in\{9,10,\ldots,15\}\), the full public selector
\(\mathcal T_m\) has an injective normalized signature on
\(\mathcal P_m\). Hence it exposes a proper factor of every
\[
N=pq,\qquad p\ne q,\quad p,q\in\mathcal P_m.
\]
The following complete certificates list the population size, descriptor
count, number of normalized columns, and the size of a checked separating
sublist.

| \(m\) | \(|\mathcal P_m|\) | \(|\mathcal T_m|\) | normalized | certificate |
|---:|---:|---:|---:|---:|
| 9 | 2 | 32 | 2 | 1 |
| 10 | 3 | 36 | 3 | 2 |
| 11 | 3 | 100 | 4 | 2 |
| 12 | 4 | 110 | 4 | 3 |
| 13 | 6 | 120 | 9 | 4 |
| 14 | 7 | 130 | 7 | 6 |
| 15 | 11 | 252 | 12 | 10 |

The exact primes, public column sources, and distinct packed signatures are
stored in
`schemas/m31-diversified-compact-signature-vectors-v1.json`, SHA-256
`f27e1681525d9c71f488c07457ed998cd43a8ea85ccac5b6e8e1b1e7227e93d0`.
The independent dense verifier expands each selected cofactor polynomial,
evaluates every certificate coordinate modulo every listed prime, and checks
all 104 prime pairs. This is a complete finite certificate, not sampling.

## BAR-025: exact selector collision

At \(m=16\),
\[
\mathcal P_{16}=
\{191,193,197,199,211,223,227,229,233,239,241,251\}.
\]
The selector contains 270 descriptors and 2,160 raw primitive coordinates.
After removing 2,054 constant coordinates and merging 96 duplicates, ten
normalized columns remain. The three primes
\[
191,\qquad227,\qquad233
\]
have the same normalized signature. Therefore the three semiprimes
\[
191\cdot227,\qquad191\cdot233,\qquad227\cdot233
\]
receive only unit or full-collision GCDs from every charged exit.

The dense verifier independently evaluates all eight primitive exit types for
all 270 descriptors on all three primes and checks equality descriptor by
descriptor. This single exact counterexample refutes the claim that this
specific selector is injective for every \(m\ge9\).

## Complexity and recognition

Each descriptor contains \(O(\log m)\) public bits. BAR-020 evaluates the
compact cofactor using \(O(\log A+\log B)=O(\log m)\) modular composition
steps, and BAR-021 computes \(R_i\) with \(O(\log m)\)-bit public arithmetic.
The complete schedule therefore uses \(O(m^3\log m)\) compact modular steps
up to the fixed per-step arithmetic cost, \(O(m^3)\) GCDs and retained
outputs, and polynomial bit complexity in the \(m\)-bit modulus.

The condition \(p,q\in\mathcal P_m\) is a factor-dependent promise. The
algorithm does not recognize that promise before factoring. For the finite
lengths in THM-004, the public selector is nevertheless factorization
independent and its successful GCD is directly verifiable.

## Adversarial review

- **Hidden factor access:** rejected. Only \(m\) determines the descriptor
  ranges. Population primes occur only in the proof and certificate verifier.
- **Aggregate double counting:** rejected. Aggregate support is
  cyclotomic OR cofactor support and is excluded from the normalized basis.
- **Stage and direct overlap:** rejected. Both public bounds and \(R_i\) are
  primitive coordinates before duplicates are removed.
- **Full collisions:** retained. Equal one-bits fail just as equal zero-bits
  do; BAR-024 is applied to complete binary signatures.
- **Dense-output leakage:** rejected. Dense expansion is used only by the
  independent finite certificate verifier. The public algorithm uses the
  compact BAR-020 evaluator and charges any requested dense output.
- **Complexity:** descriptor count, encodings, modular work, GCDs, outputs,
  and extraction are all polynomially charged.
- **Recognition:** the balanced promise is not claimed recognizable without
  factoring.
- **Finite-to-asymptotic leakage:** rejected. THM-004 stops at \(m=15\);
  BAR-025 refutes one selector at \(m=16\) and says nothing about a different
  polynomial selector.
- **General factoring:** neither result proves or disproves a classical
  polynomial-time algorithm for arbitrary integers.
