# EXP-0025 - M26 exceptional cyclotomic quotient audit

## Status

`EMPIRICAL`, deterministic and reproducible.

## Question and null outcome

Do the compact formulas for \(C_4\) and \(C_6\) ever disagree with exact
dense division, product reconstruction, or capped prime-power valuations in
the registered box? Does every apparent residual success disappear into a
stage GCD, M24 public overlap bound, or the direct fixed-cyclotomic GCD?
Any disagreement is a failure and is not discarded.

## Registered commands

```text
python scripts/run_m26_exceptional_cyclotomic_audit.py \
  --factor-max 19 --modulus-max 160 --base-max 40
python scripts/check_m26_exceptional_cyclotomic_differential.py
```

There is no random seed. The audit enumerates every recognized exceptional
ordered pair through 19, every composite modulus through 160, and every unit
base from 2 through the smaller of 40 and \(N-1\).

## Checks

- Exact monic division reconstructs every exceptional numerator.
- Compact quotient evaluation agrees with dense Horner evaluation.
- \(\Phi_i(g)C_i(g)\equiv F_i(g)\pmod N\).
- For every prime power dividing every enumerated modulus, the capped
  valuation of the product is the capped sum of factor valuations.
- Direct, residual, and full-collision branches follow BAR-020.
- Residual witnesses are minimized lexicographically by modulus, formal
  numerator degree, \(A\), \(B\), and base within the registered box.
- Ten canonical vectors agree in Python, Rust, and C#.

## Result

The audit covered 29 exceptional pairs: 20 \(\Phi_4\) and 9 \(\Phi_6\).
It completed:

- 29 exact symbolic divisions;
- 61,277 modular evaluations;
- 61,277 compact-versus-dense cofactor checks;
- 61,277 product reconstructions;
- 122,583 capped prime-power valuation checks;
- 30,417 unit, 30,323 proper-factor, and 537 full-collision direct
  cyclotomic branches;
- 3,987 residual proper factors on the unit-cyclotomic branch;
- 1,873 residual proper factors after both stages and both M24 public
  overlap bounds were also units;
- zero failures;
- 20 selected Python/Rust/C# comparisons.

The minimized clean residual witnesses are:

- \(\Phi_4\), repeated prime:
  \((N,g,A,B)=(9,4,11,7)\), cofactor GCD \(3\);
- \(\Phi_4\), square-free:
  \((15,11,3,7)\), cofactor GCD \(5\);
- \(\Phi_6\), repeated prime:
  \((25,3,5,3)\), cofactor GCD \(5\);
- \(\Phi_6\), square-free:
  \((35,8,5,3)\), cofactor GCD \(5\).

In all four, the direct cyclotomic GCD, both stage GCDs, and both public
overlap-bound GCDs are one.

Canonical summary SHA-256:

```text
aa160aff769f98463268f641365c3a7ac498f2c5dc4e70a018f86a4d116bdbbb
```

## Interpretation boundary

The finite audit does not prove BAR-020, a success density, or schedule
coverage. It refutes the direct-cyclotomic-only interpretation inside the
box and supplies exact regression witnesses. It makes no general classical
polynomial-time factoring claim.
