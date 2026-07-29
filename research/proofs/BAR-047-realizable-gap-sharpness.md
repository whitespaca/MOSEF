# BAR-047: the realizable-GCD-gap envelope is universally sharp

## Claim status and scope

- `DEF-040`: `DEFINITION`.
- `BAR-047`: `PROVED`.
- `REF-049`: `REFUTED`.

This is a method barrier for the exact DEF-035 level geometry. It does not
prove that a balanced prime divides the extremal overlap integer, that the
associated signatures are injective, or that the \(c=1/2\) endpoint is open
in every possible refinement.

## DEF-040: realizable gaps

For a finite set \(T=\{t_0<\cdots<t_{r-1}\}\) and \(1\le h<r\), define
\[
\mathcal G_h(T)=
\left\{
\gcd(u_1-u_0,\ldots,u_h-u_0):
\{u_0<\cdots<u_h\}\subseteq T
\right\}.
\]
If \(\Delta=t_{r-1}-t_0\), every \(q\in\mathcal G_h(T)\) satisfies
\[
q\le\left\lfloor\frac{\Delta}{h}\right\rfloor.
\tag{1}
\]

## Proof of the upper bound

For a witnessing subset \(u_0<\cdots<u_h\), write
\(u_i-u_0=qv_i\). The positive integers \(v_1<\cdots<v_h\) are distinct,
so \(v_h\ge h\). Therefore
\[
hq\le qv_h=u_h-u_0\le\Delta,
\]
which proves (1).

## BAR-047: exact attainability

For every positive pair \(h,q\) and every initial level \(s\ge2\), take
\[
T_{h,q,s}=\{s,s+q,\ldots,s+hq\}.
\tag{2}
\]
This set has span \(\Delta=hq\), and its only \((h+1)\)-subset is the whole
set. The offset GCD is exactly \(q\). Hence
\[
\max\mathcal G_h(T_{h,q,s})
=q
=\left\lfloor\frac{\Delta}{h}\right\rfloor.
\tag{3}
\]
The universal envelope used by BAR-046 is therefore sharp, even on a
factor-independent public list with \(h+1\) distinct levels.

The same equality survives maximum-density packing. The full interval
\[
I_{h,q,s}=\{s,s+1,\ldots,s+hq\}
\tag{4}
\]
has \(r=\Delta+1\) and contains \(T_{h,q,s}\) as an \((h+1)\)-subset, so
\(q\in\mathcal G_h(I_{h,q,s})\). Combined with (1), its maximum realizable
gap is again exactly \(q=\Delta/h\).

In particular, no universal constant \(\varepsilon>0\) can replace (1) by
\[
\max\mathcal G_h(T)\le
(1-\varepsilon)\frac{\Delta}{h},
\]
and no universal \(o(\Delta/h)\) bound is possible. This proves BAR-047 and
refutes REF-049.

## Consequences and limitations

- Removing unrealizable smaller gaps may reduce a particular finite prefix,
  but one realizable extremal \(q\) already has overlap-integer bit length
  \(\Theta(2^q)\). Thus realizability alone cannot improve the leading
  worst-case exponent in BAR-046.
- The witnesses (2) and (4) say nothing about whether \(R_q\) has a balanced prime
  divisor in the relevant population. It is a sharpness result for the
  geometry-to-overlap ledger, not an adversarial semiprime construction.
- Shared prime divisors among the \(R_q\)'s and primitive-part accounting are
  not used. They are the next falsification target.
- General classical factoring remains open.
