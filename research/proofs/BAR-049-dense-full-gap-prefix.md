# BAR-049: a dense interval realizes the complete GCD-gap prefix

## Claim status and scope

- `DEF-042`: `DEFINITION`.
- `BAR-049`: `PROVED`.
- `REF-051`: `REFUTED`.

This result concerns the exact public level geometry used in BAR-046. It
shows that realizability pruning removes no gap at all for the
maximum-density interval. It does not assert that every overlap integer has
a balanced prime divisor.

## DEF-042

For \(s\ge2\), span \(\Delta\ge1\), and
\(1\le h\le\Delta\), let
\[
I_{s,\Delta}=\{s,s+1,\ldots,s+\Delta\}
\]
and use the realizable-gap set \(\mathcal G_h\) from DEF-040.

## BAR-049

The exact identity is
\[
\mathcal G_h(I_{s,\Delta})
=
\left\{1,2,\ldots,
\left\lfloor\frac{\Delta}{h}\right\rfloor
\right\}.
\tag{1}
\]

The upper inclusion is BAR-047. For the reverse inclusion, fix
\[
1\le q\le\left\lfloor\frac{\Delta}{h}\right\rfloor.
\]
Then
\[
\{s,s+q,\ldots,s+hq\}\subseteq I_{s,\Delta}
\]
is an \((h+1)\)-subset and its offset GCD is exactly \(q\). Thus every
integer in the prefix occurs, proving (1).

At maximum level packing \(r=\Delta+1\), the all-gap union
\(R_1,\ldots,R_{\lfloor\Delta/h\rfloor}\) used by BAR-046 is therefore an
exact realizability ledger rather than a superset. This proves BAR-049 and
refutes REF-051.

## Limitations

- Exact realizability of \(q\) only means that an \((h+1)\)-subset has that
  offset GCD. It does not produce a prime that hits those levels.
- The result does not show injectivity or noninjectivity at \(c=1/2\).
- Sparse public lists can realize a strict subset of the prefix.
- Other compact families and general classical factoring remain open.
