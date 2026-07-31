# M85 - Independent semantic validation of the M41 certificate

## Status and scope

This milestone supplies an independently designed, standard-library-only
semantic checker for the frozen M41 certificate at input length \(m=29\).
It strengthens the executable evidence for `THM-014`, `BAR-035`, and
`EMP-040`; it does not change their status or scope.

The checker validates one registered row, not every M31--M46 row. It does not
prove injectivity for \(m>29\), recognize the balanced-factor promise,
minimize over other selector families, establish an asymptotic cap rate, or
solve general classical polynomial-time factoring.

## Why M41 is the selected row

The final M46 row was considered first. Its construction certificate contains
3,298 coordinates on 3,299 primes, requiring roughly 10.88 million
coordinate/prime evaluations before predecessor and mutation checks. M41
retains the same relevant trust obligations with a smaller audit surface:

- a complete reconstructed population of 685 primes;
- 1,528 registered certificate coordinates;
- 234,270 unordered population pairs;
- a unique predecessor collision \(\{18979,21031\}\);
- a unique newly admitted repair coordinate at cap 103; and
- the nonmonotone finite threshold
  \(L_{29}^{\star}=103<L_{28}^{\star}=104\).

The construction certificate therefore needs about 1.05 million
coordinate/prime evaluations while still exercising population completeness,
descriptor grammar, quotient semantics, injectivity, raw predecessor
collision, and incremental repair.

## Clean-room boundary

The executable
`scripts/check_m85_m41_semantic_certificate.py` imports only:

- `hashlib` and `json`;
- `math`, `pathlib`, `typing`; and
- `__future__`.

It does not import:

- `python/mosef_reference`;
- the M41 audit or schema generator;
- any M31--M46 differential checker; or
- a repository serialization helper.

The 548-line source is below the 1,000-line acceptance limit. An AST test
enforces the import boundary and rejects relative imports.

## Independent reconstruction

### Population

The checker derives the exact integer interval

\[
 \left\lceil\sqrt{2^{28}}\right\rceil
 \le p\le
 \left\lfloor\sqrt{2^{29}-1}\right\rfloor
\]

and runs a standard sieve through the upper endpoint. Filtering the sieve
reconstructs

\[
 \mathcal P_{29}
 =\{p\text{ prime}:2^{28}\le p^2<2^{29}\}
\]

as the same ordered list of 685 primes registered in the artifact.

### Descriptor grammar

For each cap \(L\), the checker independently enumerates
\((i,A,B,g)\) with \(2\le A,B,g\le L\), \(A\ne B\), and

\[
\begin{aligned}
 i=4 &: A\equiv B\equiv3\pmod4,\\
 i=6 &: A\equiv5\pmod6,\quad B\equiv3\pmod6.
\end{aligned}
\]

It reconstructs 89,789 descriptors at cap 102, 95,778 at cap 103,
99,424 at cap 105, and 109,782 at cap 108.

### Primitive residues

Let

\[
 S_k(x)=1+x+\cdots+x^{k-1}.
\]

The checker evaluates this polynomial by the field identity

\[
 S_k(x)=
 \begin{cases}
 k,&x=1,\\
 (x^k-1)(x-1)^{-1},&x\ne1,
 \end{cases}
\]

not by the repository's binary geometric-sum routine. Its derivative is

\[
 S_k'(x)=
 \begin{cases}
 k(k-1)/2,&x=1,\\
 \bigl(kx^{k-1}(x-1)-(x^k-1)\bigr)(x-1)^{-2},&x\ne1.
 \end{cases}
\]

For a descriptor, put

\[
 F(x)=aS_A(x)+S_B(x^A),\qquad
 a=\begin{cases}1&i=4,\\2&i=6.\end{cases}
\]

The removed cyclotomic is
\(\Phi_4(x)=x^2+1\) or
\(\Phi_6(x)=x^2-x+1\), and \(F=\Phi_iC\).
When \(\Phi_i(g)\ne0\pmod p\), the checker computes

\[
 C(g)=F(g)\Phi_i(g)^{-1}\pmod p.
\]

At a cyclotomic root it avoids invalid division. Differentiating the exact
polynomial identity gives

\[
 C(g)=F'(g)\Phi_i'(g)^{-1}\pmod p.
\]

All M41 population primes exceed 16,000 while \(g\le103\), so the positive
integer values \(\Phi_4(g)\) and \(\Phi_6(g)\) are strictly below \(p\).
Consequently the registered M41 certificate uses only the unit-division
branch; its cofactor bits do not depend on the derivative branch. The latter
is retained to make the standalone formula total at simple cyclotomic roots
and is tested separately on the valid small descriptor
\((\Phi_4,A,B,g,p)=(\Phi_4,3,7,2,5)\), where it agrees with the exact integer
quotient. No registered root-case evidence is claimed.

The cyclotomic/cofactor resultant is reconstructed from the exact linear
remainder. For order four the remainder coefficients are

\[
 u=\frac{A(B+2)+1}{4},\qquad
 v=\frac{A(B-2)+1}{4},\qquad R_4=u^2+v^2.
\]

For order six they are

\[
 u=-\frac{2(A(B-2)+1)}3,\qquad
 v=\frac{A(B+4)+4}3,\qquad R_6=u^2+uv+v^2.
\]

Together with the base, two stages, two public bounds, and direct
cyclotomic, these formulas reconstruct all eight primitive support bits.

## Certificate implication

The first 1,527 registered sources are validated as legal cap-102
coordinates. Recomputed packed signatures on those coordinates have exactly
one duplicate bucket:

\[
 \{18979,21031\}.
\]

This sublist shows that the full cap-102 selector has at most this one
collision. The checker also evaluates all eight primitive exits of all
89,789 cap-102 descriptors on the two tracked primes and finds identical
masks descriptor by descriptor. Hence the full selector has at least that
collision, so it has exactly that one collision.

The last registered coordinate is

```text
phi4:87:95:103:cofactor
```

and independently evaluates to \((0,1)\) on the tracked pair. Appending it
makes the recomputed 1,528-coordinate signatures injective on all 685 primes,
which checks all 234,270 unordered pairs at once. The checker additionally
enumerates all 5,989 descriptors first admitted at cap 103 and all 47,912
new primitive coordinates. The displayed coordinate is the unique one that
separates the predecessor pair. Zero new coordinates cannot repair an
existing collision, while this one coordinate does; the incremental minimum
is therefore one.

Raw selector inclusion transfers cap-103 injectivity to the registered caps
105 and 108. Descriptor and raw-coordinate counts at all four caps are
reconstructed. The cap-103 normalization counts are checked for an exact
partition of the raw coordinates, but the checker does not rerun the
generator's full normalization search: the independently evaluated
separating subcertificate is already sufficient for injectivity.

## Integrity is secondary, not trusted as semantics

The checker recomputes the legacy embedded summary SHA-256 after removing
`summary_sha256` and the four primitive vectors. The vectors were appended
after the original M41 summary hash was calculated and are therefore outside
that legacy hash projection. Each vector is instead recomputed semantically.

Mutation tests alter the population, a descriptor, a primitive mask, and a
packed signature. The first three mutations recompute the legacy hash before
validation, so their rejection demonstrates that hash agreement alone is
insufficient.

## Result

The frozen artifact passes the independent semantic checker:

```text
M85 independent M41 semantic checker: PASS
(685 primes, 1528 certificate coordinates, 234270 pairs,
89789 predecessor descriptors, 47912 new raw coordinates)
```

Eight targeted tests pass, including the import/size boundary, four semantic
mutation classes, and the separate exact-quotient root case. This is a
reproducible computer-assisted finite
validation, not external peer review or a formal proof assistant result.
