# EXP-0018 - M19 nested geometric-quotient audit

## Status

`EMPIRICAL`, deterministic and reproducible. This is an active-milestone
checkpoint rather than a completed publication record.

## Question and null outcome

Can the exact cancellation identity
\[
S_{AB}(X)=S_A(X)S_B(X^A)
\]
fail, can either charged denominator path escape its unit, proper-factor, or
full-collision branch, or can the independent implementations disagree on the
resulting residues and GCDs? Any such case is the null outcome.

## Registered commands

```text
python scripts/run_m19_nested_quotient_search.py \
  --exponent-max 12 --modulus-max 128 --base-max 16
python scripts/check_m19_nested_quotient_differential.py
```

The current deterministic box materializes every ordered pair
\((A,B)\in[1,12]^2\). The modular audit uses every modulus from 4 through 128
and every base from 0 through 16, with the rational denominator
\(L=S_A(g)\) and composed denominator \(C=g^A-1\) classified separately.

## Checks

- Exact coefficient multiplication gives
  \(S_{AB}(X)=S_A(X)S_B(X^A)\).
- The binary geometric-sum evaluators agree with direct modular evaluation
  for \(L\), \(Q=S_B(g^A)\), \(U=S_{AB}(g)\), \(C=g^A-1\), and
  \(E=g^{AB}-1\).
- Every modular circuit satisfies both \(U=LQ\bmod N\) and
  \(E=CQ\bmod N\).
- A unit rational denominator returns \(Q\); a proper rational denominator
  is already a factor exit; and a full rational denominator gives
  \(Q\equiv B\bmod N\).
- The composed denominator independently follows the arbitrary
  geometric-sum unit, proper-factor, and full-collision trichotomy.
- Six selected vectors are checked in Python, Rust, and C#.

## Checkpoint result

The registered audit completed with no counterexample:

- 144 exact symbolic identities and 6,084 coefficient checks;
- 177,264 modular circuits and 354,528 residue identities;
- 120,444 unit, 46,932 proper, and 9,888 full rational-denominator cases;
- 74,028 unit, 66,936 proper, and 36,300 full composed-denominator cases;
- 12,988 proper rational-denominator cases in which the quotient and
  denominator factor values differ;
- zero unexplained reductions;
- 1,231 unit and 894 nonunit base prechecks;
- 12 selected Python/Rust/C# comparisons.

Canonical summary SHA-256:

```text
a6d1bd1344b439901f3d40b9dc226fbcedcaba6886d07363461b0814db6aa2aa
```

## Interpretation boundary

This finite audit does not prove the asymptotic statement or a general
rational-circuit lower bound. The proposed barrier proof remains scoped to
this two-stage geometric identity. The compact pair \((A,B)\) does not make a
dense coefficient vector polynomial in the encoded input length: the quotient
has degree \(A(B-1)\), \(B\) nonzero monomials, and
\(A(B-1)+1\) dense coefficient positions.
