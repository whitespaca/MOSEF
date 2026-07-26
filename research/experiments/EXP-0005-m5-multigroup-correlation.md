# EXP-0005 - M5 conjugate-channel correlation search

## Registration

- Research question: can the conjugately paired Lucas channel
  \(P=a+a^{-1}\) expose a factor when the retained multiplicative family
  cannot, do the exact algebraic identities or square-free GCD equality fail,
  and do independently selected Lucas parameters behave differently?
- Core implementation commit:
  `7ca79de49c404b10c1b1b355ff10b8a8d7d59635`.
- Host and toolchains: `research/toolchains/windows-amd64-20260725.json`.
- Seed: none; the registered search is deterministic and exhaustive within
  each stated loop.
- Bounds: composite \(4\le N\le700\), unit bases
  \(1\le a\le\min(32,N-1)\), exponents \(1\le d\le12\), and arbitrary
  independently tested Lucas parameters \(0\le P\le\min(32,N-1)\).
- The conjugate family uses every exponent in \([12]\), so it contains the
  exponent \(2\) required by BAR-002's discriminant implication.
- Pruning: prime moduli and nonunit bases are excluded from the conjugate
  family by definition. The independent-parameter complement search is
  restricted to odd composite moduli and nontrivial unit bases \(a\ge2\);
  it counts only nondegenerate sequence factors after a multiplicative miss
  or simultaneous collision at the same exponent.
- Command:

```powershell
python scripts/run_m5_multigroup_search.py --modulus-max 700 `
  --base-max 32 --parameter-max 32 --exponent-max 12
```

## Result

- Status: `PASS`.
- Conjugate families: 9,773.
- Exact identity checks: 117,276.
- Pointwise sequence-success implications: 36,048.
- Discriminant-to-exponent-2 implications: 9,773.
- Square-free raw-GCD equality checks: 69,192.
- Multiplicative success families: 9,037.
- Derived Lucas success families: 8,774.
- Combined success families: 9,037, exactly equal to the multiplicative
  success domain.
- Derived-Lucas-only family successes: 0.
- Both channels failed in 736 conjugate families.
- The bound contains 19 Carmichael-number/base families; both channels failed
  in one of them.
- First nondegenerate prime-power degradation:
  \((N,a,P,d)=(25,2,15,4)\), where the multiplicative GCD is \(5\) and the
  derived Lucas GCD is \(25\).
- First discriminant-degenerate sequence factor in the registered ordering:
  \((N,a,P,d)=(6,5,4,1)\), where the sequence GCD is \(2\). This confirms that
  a full discriminant GCD must not be conflated with the later sequence GCD.
- The first independently parameterized odd complement is
  \((N,a,P,d)=(15,2,9,3)\): multiplication misses, the discriminant GCD is
  \(1\), and the Lucas sequence GCD is \(5\).
- There were 58,661 independently parameterized same-exponent complement
  tuples in the registered finite box.
- Canonical summary SHA-256:
  `98f2be052a315231292c73319fa98066cf4d8fc4cd66740f207b2d99c7f616f5`.

Selected outcomes, including all discriminant-degenerate sequence branches,
were independently evaluated by Python, Rust, and C#:

```powershell
python scripts/check_m5_multigroup_differential.py
```

This passed 18 cross-language comparisons.

## Interpretation and limitations

The search attempts to falsify BAR-002 and audits the three implementations;
the algebraic proof, not finite enumeration, supplies universal validity.
The zero derived-Lucas-only count applies only to the conjugate map and an
exponent family containing \(2\). The independent-parameter counts are
unweighted tuple counts in a bounded box, not probabilities, density
estimates, asymptotic evidence, or proof of independent failures. Nothing in
this experiment gives a general factoring algorithm or lower bound.
