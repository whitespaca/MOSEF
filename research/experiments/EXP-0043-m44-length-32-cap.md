# EXP-0043: M44 length-32 cap audit

## Status

`EMPIRICAL` for the registered exact partition-refinement and certificate
computations. The complete collision and construction certificates promoted
to BAR-038 and THM-017 are finite proof objects.

## Deterministic commands

```powershell
python scripts/run_m44_length_32_cap_audit.py
python scripts/generate_m44_length_32_cap_schema.py
python scripts/check_m44_length_32_cap_differential.py
```

No random seed is used.

## Registered result

At \(m=32\), \(m+113\) gives cap 145 and
\(\lceil60m/13\rceil\) gives cap 148. Cap 145 leaves one 14-prime bucket
and 91 failed pairs; cap 148 leaves one six-prime bucket and 15 failed
pairs. Exact transition profiles through cap 167 give collision-pair counts
\[
15,10,10,10,10,6,6,6,3,3,3,1,1,1,1,1,1,1,1,0.
\]
The cap-166 predecessor is \(\{59699,63463\}\). The only new nonconstant
primitive pattern is \((1,0)\), supplied by
`phi4:167:119:93:cofactor`. It appends to 1,748 predecessor coordinates to
give a 1,749-coordinate injective certificate. Thus
\(L_{32}^{\star}=167\), the minimum incremental repair size is one, and
the repaired finite envelopes are \(m+135\) and \(c>83/16\), with
\(\lceil26m/5\rceil\) as one fixed multiplicative witness.

The registered audit checked:

- two complete exact partition profiles at caps 145 and 148;
- 1,750 balanced primes and 1,530,375 unordered pairs;
- 284,004 public-maximum descriptors and 82,130,579 optimized public
  local-exit evaluations;
- twenty transition profiles at caps 148 through 167;
- 131,992 new transition descriptors, 388,074 optimized tracked local
  exits, and 791,952 full independent tracked local exits;
- 415,996 cap-167 descriptors and 3,327,968 raw coordinates;
- 82,518,653 optimized local-exit evaluations through cap 167;
- 20,656 new cap-167 descriptors and 165,248 primitive-coordinate checks;
- one distinct repair pattern, one minimum repair coordinate, 1,749
  construction coordinates, and 1,530,375 certificate pairs;
- 3,060,750 construction-coordinate local-exit evaluations;
- 16 selected Rust/C# command comparisons and four dense vector checks;
- 548,388 independent public-cap descriptor checks;
- 791,952 independent transition local-exit checks;
- 165,248 independent repair-coordinate checks; and
- 1,530,375 independent construction-certificate pair checks.

Canonical summary SHA-256:

```text
6d09e1831de30009de0e770dea2d17271e8e00ccff0c09ecd11aba42fdc55b13
```

Registered schema SHA-256:

```text
a05de0bf7941d2c44bf0d5d79488f90f467c33cb5a8ec986ca5de0aa5f39aa21
```

## Interpretation

The result refutes both M43 schedules on one new complete population and
fixes the exact lower threshold at cap 167. The common finite additive and
multiplicative envelopes are repaired by the new length-32 row. It
establishes no asymptotic rate, behavior at \(m>32\), promise recognizer,
density, or general factoring algorithm or lower bound.
