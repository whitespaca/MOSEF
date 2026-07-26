# EXP-0008 - M9 exponent-encoding divisor-budget search

## Registration

- Research question: does the exact bit-length divisor budget in DEF-009
  dominate \(\tau(d)\), does divisor enumeration recover exactly every odd
  prime hit by \(p-1\mid d\) or \(p+1\mid d\), and do the single- and
  multi-exponent hit bounds in BAR-004 survive bounded falsification?
- Core implementation commit:
  `1416d70a6bc39a4c7491e9ec86e4e67f96293962`.
- Host and toolchains: `research/toolchains/windows-amd64-20260725.json`.
- Seed: none; the registered search is deterministic and exhaustive within
  each stated loop.
- Bounds: every positive exponent \(1\le d<2^{18}\); direct comparison of the
  divisor-generated oracle with both divisibility predicates for every
  \(1\le d\le4096\) and every odd prime \(3\le p\le4093\); and every subset
  of size at most three drawn from the maximum-divisor-count representative
  at each bit length \(1,\ldots,18\).
- Pruning: integer factorization uses a deterministic smallest-prime-factor
  sieve. Divisor families are generated from the complete factorization.
  Record-family tests omit permutations and duplicates but enumerate every
  retained subset. No exponent or direct prime in the registered rectangles
  is sampled.
- Stopping rule: complete the finite loops above or stop immediately at the
  first divisor-enumeration, budget, hit-bound, oracle, or REF-005
  counterexample.
- Command:

```powershell
python scripts/run_m9_divisor_budget_search.py --bit-length-max 18 --direct-exponent-max 4096 --prime-max 4093
```

## Result

- Status: `PASS`.
- Exact divisor-enumeration and bit-length-budget checks: 262,143 each.
- Single-exponent hit-bound checks: 262,143.
- Direct hit-oracle comparisons: 2,306,048 across 563 odd primes.
- Record-family hit-bound checks: 987.
- Largest single-exponent global hit set: 114 odd primes, for
  \(d=166{,}320\).
- At bit length 18, the largest observed divisor count was 168, first attained
  by \(d=221{,}760\); the exact one-length budget was 16,681,088.
- The smallest exponent strictly above both \(p+1\) and \(q+1\) that leaves a
  distinct odd-prime pair entirely unhit was
  \((d,p,q,N)=(7,3,5,15)\), confirming REF-005's minimal bounded
  counterexample.
- Canonical summary SHA-256:
  `b8357f9436ef4d31d072f62dab4f3c8dedad41d6f1787803bf5df2f485ca53ed`.

Selected divisor counts, signatures, pair predicates, and hit counts were
independently evaluated by Python, Rust, and C#:

```powershell
python scripts/check_m9_divisor_budget_differential.py
```

This passed 46 cross-language comparisons.

## Interpretation and limitations

The search attempts to falsify the exact finite combinatorial steps used by
BAR-004; the proof, not bounded enumeration, supplies universal and
asymptotic validity. The observed maximum divisor and hit counts are finite
range records, not asymptotic estimates and not evidence that the upper
budget is tight.

The experiment tests explicit integers and explicit exponent families. It
does not model a compressed circuit or batch representation for exponentially
many implicit exponents, does not recognize the promise from \(N\), does not
transfer the finite prime rectangle to a natural semiprime distribution, and
does not give a general classical factoring algorithm or lower bound.
