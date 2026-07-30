# BAR-052: balanced overlap primes have large half-orders

Status: `PROVED`

## Definitions

For input length \(m\ge9\), put
\[
\ell_m=\left\lceil\sqrt{2^{m-1}}\right\rceil
\]
and let \(\delta_m\) be the least odd integer \(d\ge3\) such that
\(33^d>\ell_m\). Define
\(\kappa_m=\lceil\log_2(\delta_m+1)\rceil\).
These are public, exact integer thresholds.

## Theorem

If a balanced prime \(p>7\) divides
\(R_q=3^{2^q-1}+32^{2^q-1}\), and BAR-051 writes
\(\operatorname{ord}_p(3/32)=2d_p\) with \(d_p\) odd, then
\[
p<33^{d_p},\quad p\equiv1\pmod{2d_p},\quad
d_p\ge\delta_m,\quad q\ge\kappa_m.
\]
In particular,
\[
d_p>\frac{m-1}{2\log_2 33},
\qquad q\ge\log_2m-O(1).
\]

## Proof

BAR-051 gives \(z_p^{d_p}=-1\) for
\(z_p=3\cdot32^{-1}\pmod p\), hence
\(p\mid3^{d_p}+32^{d_p}\). The case \(d_p=1\) would force
\(p\mid35\), impossible for \(p>7\), so \(d_p\ge3\). The binomial theorem
gives \(3^{d_p}+32^{d_p}<33^{d_p}\), proving the strict size bound.
Lagrange's theorem gives \(2d_p\mid p-1\), proving the residue condition.

Since \(p\ge\ell_m\), the definition of \(\delta_m\) yields
\(d_p\ge\delta_m\). Also \(d_p\mid2^q-1\), so
\(q\ge\lceil\log_2(d_p+1)\rceil\ge\kappa_m\).
Finally \(p\ge2^{(m-1)/2}\) and \(p<33^{d_p}\) give the displayed linear
bound; taking another logarithm gives the first-gap bound.

## Method barrier

The size condition alone removes only \(q<\kappa_m=O(\log m)\). It does not
exclude \(D=\lfloor m/2\rfloor\): for \(m\ge9\),
\(\delta_m\le m+1\le2^D-1\), so a size-admissible interval remains.
This compatibility statement is not an existence theorem for a divisor of
\(R_D\). Residue-class counting is left to M60.

## Adversarial checks

- The excluded \(d=1\) case is discharged explicitly.
- The implementation uses strict integer inequalities, not floating point.
- The residue condition is necessary, not sufficient.
- Compatibility at \(q=D\) is not claimed to produce a prime.
