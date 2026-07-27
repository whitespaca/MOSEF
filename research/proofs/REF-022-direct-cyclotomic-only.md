# REF-022 - Direct exceptional cyclotomic GCDs are not exhaustive

## Status

`REFUTED`.

## Candidate statement

For the fixed \(\Phi_4\) and \(\Phi_6\) exceptional families of THM-003,
every proper aggregate GCD that survives the two stage GCDs and M24 public
overlap bounds is already produced by the direct fixed-cyclotomic GCD.

## Minimized obstructions

Within the deterministic EXP-0025 ordering, the first square-free
\(\Phi_4\) obstruction is

\[
(N,g,A,B)=(15,11,3,7).
\]

Here both stage GCDs, both public-bound GCDs, and
\(\gcd(\Phi_4(11),15)\) equal one, while
\(\gcd(C_4(11),15)=\gcd(F_4(11),15)=5\).

The corresponding square-free \(\Phi_6\) obstruction is

\[
(N,g,A,B)=(35,8,5,3),
\]

where the same five preliminary GCDs are units and the cofactor GCD is
five. Repeated-prime obstructions are \((9,4,11,7)\) for \(\Phi_4\),
with cofactor GCD three, and \((25,3,5,3)\) for \(\Phi_6\), with
cofactor GCD five.

## Surviving repair

BAR-020 replaces the false interpretation with an exact two-factor
extraction grammar. The fixed cyclotomic factor is only one branch; its
cofactor has an independent compact evaluator and can strictly add
extraction power. This repair still proves no successful public schedule,
density, or universal factorization result.
