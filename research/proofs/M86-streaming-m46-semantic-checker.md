# M86 - Streaming clean-room validation of the M46 certificate

## Status and scope

This milestone supplies a standard-library-only semantic checker for the
frozen M46 certificate at standard input length \(m=34\). It strengthens the
executable evidence for `THM-019`, `BAR-040`, and `EMP-045`; it does not change
their status or scope.

The result concerns the exact DEF-032 selector, the complete registered
balanced population, and caps 200 and 201. It does not prove anything for
\(m>34\), recognize the factor-dependent promise, minimize over other
selector families, establish an asymptotic cap rate, or solve general
classical polynomial-time factoring.

## Clean-room boundary

The 624-line executable
`scripts/check_m86_m46_streaming_certificate.py` imports only:

- `collections.abc`, `hashlib`, `json`, `math`, `pathlib`, `time`, and
  `typing`; and
- `__future__`.

It does not import the M46 audit, schema generator, differential checker,
M85 checker, `python/mosef_reference`, or a repository serialization helper.
An AST regression test enforces this boundary.

## Exact population and descriptor grammar

The checker derives

\[
 \left\lceil\sqrt{2^{33}}\right\rceil
 \le p\le
 \left\lfloor\sqrt{2^{34}-1}\right\rfloor
\]

and sieves the interval independently. It reconstructs the registered ordered
population of 3,299 primes, whose 5,440,051 unordered pairs are exactly

\[
 \binom{3299}{2}.
\]

Descriptors are streamed directly from the congruence grammar

\[
\begin{aligned}
i=4 &: A\equiv B\equiv3\pmod4,\quad A\ne B,\\
i=6 &: A\equiv5\pmod6,\quad B\equiv3\pmod6,
\end{aligned}
\]

with \(2\le A,B,g\le L\). This yields 704,261 descriptors at cap 200
and 714,400 at cap 201. Because the cap grammar is nested, a descriptor is
new at cap 201 exactly when

\[
\max\{A,B,g\}=201.
\]

The checker obtains 10,139 such descriptors without retaining either cap's
descriptor set.

## Primitive semantics

For

\[
S_k(x)=1+x+\cdots+x^{k-1},
\]

the checker uses

\[
S_k(x)=
\begin{cases}
k,&x=1,\\
(x^k-1)(x-1)^{-1},&x\ne1
\end{cases}
\pmod p.
\]

For a descriptor it reconstructs the first and second geometric stages, two
public bounds, the direct cyclotomic value, the cyclotomic/cofactor
resultant, and the cofactor. The cofactor numerator is

\[
F(x)=aS_A(x)+S_B(x^A),\qquad
a=\begin{cases}1&i=4,\\2&i=6,\end{cases}
\]

and \(F=\Phi_iC\). Every M46 population prime satisfies

\[
p\ge92683>201^2+1.
\]

Thus for \(2\le g\le201\), both positive values
\(\Phi_4(g)=g^2+1\) and \(\Phi_6(g)=g^2-g+1\) are strictly below \(p\).
No registered M46 evaluation reaches a cyclotomic root, and the checker may
compute

\[
C(g)=F(g)\Phi_i(g)^{-1}\pmod p
\]

without a derivative branch. This discharged finite bound is checked before
certificate evaluation.

The exact resultants are reconstructed from the linear remainders:

\[
\begin{aligned}
R_4&=u^2+v^2,
&u&=\frac{A(B+2)+1}{4},
&v&=\frac{A(B-2)+1}{4},\\
R_6&=u^2+uv+v^2,
&u&=-\frac{2(A(B-2)+1)}3,
&v&=\frac{A(B+4)+4}3.
\end{aligned}
\]

The four registered primitive vectors are recomputed from these formulas.

## Streaming certificate invariant

Let the legal source list be
\((d_0,k_0),\ldots,(d_{C-1},k_{C-1})\), with \(C=3298\), and let
\(h(d,k,p)\in\{0,1\}\) be the requested primitive exit.
After processing the first \(j\) sources, the checker maintains one integer
per population prime:

\[
\sigma_j(p)=\sum_{\ell=0}^{j-1}h(d_\ell,k_\ell,p)2^\ell.
\]

The invariant holds at \(j=0\) because every signature is zero. At source
\(j\), the checker evaluates that coordinate on every prime and ORs
\(2^j\) precisely into the signatures for which the exit is nonzero. This
gives \(\sigma_{j+1}\), proving the invariant by induction.

Consequently all

\[
3298\cdot3299=10{,}880{,}102
\]

coordinate/prime evaluations are performed without a materialized
10,880,102-cell matrix. The mutable certificate state has exactly 3,299
packed-signature slots. Their raw payload is at most 10,880,102 bits, about
1.30 MiB, plus Python integer and list overhead. The 3,298 parsed sources and
the 1.86 MB frozen JSON artifact are separately bounded inputs.

The final streamed signatures agree exactly with the registered packed
values and are all distinct, so every one of the 5,440,051 unordered pairs
is separated.

## Exact predecessor collision

Masking the final repair bit from the streamed subcertificate leaves exactly
one duplicate bucket,

\[
\{97927,99527\}.
\]

This proves that the full cap-200 selector has at most this collision. The
checker separately streams every one of the 704,261 legal cap-200
descriptors, evaluates all eight primitive exits on both tracked primes, and
finds equal masks descriptor by descriptor. Hence the raw selector has at
least this collision. The two directions prove that it has exactly this one
collision.

## Unique cap-201 repair

For every one of the 10,139 newly admitted descriptors, the checker evaluates
all eight primitive exits on both tracked primes. The only differing source is

```text
phi6:149:201:45:cofactor
```

with pattern \((1,0)\). Appending it to the 3,297-coordinate predecessor
subcertificate yields the already verified injective 3,298-coordinate
certificate. Zero new coordinates preserve the predecessor collision, while
this one coordinate repairs it, so the minimum incremental repair size is
one. No minimum is claimed for the full certificate.

The checker also reconstructs the cap-200/cap-201 descriptor counts, raw
coordinate counts, collision metadata, selected-coordinate counts, relevant
registered operation counts, and the finite repaired schedule labels.

## Result

The frozen artifact passes:

```text
M86 streaming M46 semantic checker: PASS
(3299 primes, 3298 coordinates, 10880102 streamed evaluations,
704261 predecessor descriptors, 81112 new raw coordinates,
3299 peak signature slots)
```

Nine tests cover the frozen result, import and size boundary, streaming
assembly, exact descriptor counts, three rehashed semantic mutations, a
packed-signature mutation, and the unique repair vector. This remains a
reproducible computer-assisted finite validation, not external peer review
or formal proof-assistant verification.
