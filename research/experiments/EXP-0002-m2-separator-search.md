# EXP-0002 - M2 bounded separator falsification search

## Registration

- Research question: do the support sufficiency, square-free equivalence, and
  valuation equivalence statements fail on a bounded exact search?
- Core implementation commit:
  `7691b61dfef292d0da8af5eb022d62cc52383634`.
- Host and toolchains: `research/toolchains/windows-amd64-20260725.json`.
- Seed: none; enumeration is deterministic.
- Bounds: composite \(4\le N\le500\), integer \(2\le g\le20\), and
  \(1\le d\le20\).
- Pruning: skip prime \(N\) and bases with \(\gcd(g,N)\ne1\). No other cases
  are pruned.
- Command:

```powershell
python scripts/run_m2_separator_search.py --n-max 500 --base-max 20 --exponent-max 20
```

## Result

- Status: `PASS`.
- Candidate evaluations: 78,860.
- Square-free candidate evaluations: 46,140.
- Direct outcomes: 55,496 nontrivial factors, 18,661 misses, and 4,703
  simultaneous collisions.
- No counterexample was found to support-separator sufficiency, square-free
  support equivalence, or the exact valuation criterion in the registered box.
- The support-only equivalence on all composite inputs was refuted 5,672 times.
  The smallest witness is \((N,g,d)=(4,3,1)\), with valuation profile
  \(((2,2,1))\) and GCD \(2\). The smallest odd witness is \((9,2,2)\).
- Canonical summary SHA-256:
  `89bda0d3ea8054542151fda07d00c1e2711536b7339952618aea692c1d74cc59`.

Selected outcome vectors were independently evaluated by Python, Rust, and C#:

```powershell
python scripts/check_m2_separator_differential.py
```

This passed 24 cross-language comparisons, including direct-factor,
invalid-base, miss, nontrivial-factor, simultaneous-collision, prime-power,
mixed repeated-prime, order-one, equal-order, and Carmichael cases.

## Interpretation and limitations

The prime-power obstruction is proved definitionally in
`research/proofs/M2-formal-specification.md`; the finite search only finds its
smallest witnesses and audits the executable semantics. Passing the search
does not prove the lemmas, asymptotic complexity, a universal constructor, or
the existence of either repaired family in `OPEN-002` and `OPEN-003`.
