# EXP-0010 - M11 boundary divisor and primorial schedule search

## Registration

- Research question: does the exact DEF-011 divisor budget fail on a bounded
  exhaustive box, and what divisor capacity, multiplication cost, actual
  \(q\pm1\) prime yield, and channel balance occur for the first-primes
  primorial family at the \(\Theta(r\log r)\) boundary?
- Core implementation commit:
  `cd391e5cf64207ea7dc2f6e4dd55cf469af45424`.
- Host and toolchains: `research/toolchains/windows-amd64-20260725.json`.
- Seed: none; every registered loop is deterministic.
- Bounds: every positive exponent \(d<2^{18}\); diagnostic bit lengths
  \(16,32,\ldots,4096\); and primorials \(P_r\) for \(1\le r\le12\).
- Pruning: the smallest-prime-factor table covers every registered exponent.
  Primorial divisors are generated from every subset of the first \(r\)
  primes. Candidate primality results are cached by value, but no distinct
  candidate is omitted. A complete sieve through
  \(\lfloor\sqrt{P_{12}+1}\rfloor\) supplies every possible trial divisor.
- Stopping rule: complete the finite loops above or stop immediately at the
  first divisor-budget, divisor-enumeration, node-accounting, direct-signature,
  channel-disjointness, or inspected Rosser--Schoenfeld-bound disagreement.
- Command:

```powershell
python scripts/run_m11_boundary_schedule_search.py `
  --exponent-max 262144 --primorial-count-max 12
```

## Result

- Status: `PASS`.
- Exact DEF-011 divisor-budget checks: 262,143.
- Primorial schedules: 12, containing \(2^r\) exactly enumerated divisors at
  each \(1\le r\le12\).
- Distinct primality candidates checked: 8,157, using 1,777,936 exact trial
  divisions after caching.
- Rosser--Schoenfeld equation (3.13) checks: seven, for \(6\le r\le12\).
- At \(r=12\),
  \(P_{12}=7{,}420{,}738{,}134{,}810\) has 43 bits, 4,096 divisors, and an
  exact binary straight-line cost of 67 multiplication nodes. It produced 897
  odd-prime hits: 449 in the \(q-1\) channel and 448 in the \(q+1\) channel.
  No prime occurred in both channels. Within this finite hit set, 201,152 of
  401,856 unordered pairs had different one-exponent signatures, a fraction
  \(449/897\).
- Canonical summary SHA-256:
  `22699f23a1421805cb472ddca1723e8d580d601cd25ca72b8b2cd134743e4f83`.

Selected primorial divisor counts, combined signatures, asymmetries, and hit
counts were independently evaluated by Python, Rust, and C#:

```powershell
python scripts/check_m11_boundary_schedule_differential.py
```

This passed 32 cross-language comparisons.

## Interpretation and limitations

The exhaustive divisor-budget checks try to falsify the exact integer
inequality; universal validity and the leading asymptotic coefficient come
from BAR-006's proof, not from the finite box. The primorial records show that
exponential divisor capacity and both disjoint channels occur at small
boundary instances. The near-balance at \(r=12\) is only a finite observation.

The experiment does not prove any asymptotic lower bound on primes of the form
\(d\pm1\) for \(d\mid P_r\), any nonvanishing fraction on an external
common-input-length prime population, any natural-density theorem, any
recognizer, or any general factoring result. The displayed within-hit fraction
conditions on the experiment's own hit set and is not the population model in
BAR-006.
