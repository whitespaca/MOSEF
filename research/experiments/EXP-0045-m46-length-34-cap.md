# EXP-0045: M46 length-34 cap audit

## Status

`EMPIRICAL` for the registered exact partition-refinement and certificate
computations. The complete collision and construction certificates promoted
to BAR-040 and THM-019 are finite proof objects.

## Deterministic commands

```powershell
python scripts/run_m46_length_34_cap_audit.py
python scripts/generate_m46_length_34_cap_schema.py
python scripts/check_m46_length_34_cap_differential.py
```

No random seed is used.

## Registered result

At \(m=34\), \(m+162\) gives cap 196 and
\(\lceil147m/25\rceil\) gives cap 200. Cap 196 leaves the three-prime
bucket \(\{97927,99527,127877\}\) and three failed pairs; cap 200 leaves
the pair \(\{97927,99527\}\). Cap 201 is injective. The only new
nonconstant primitive pattern is \((1,0)\), supplied by
`phi6:149:201:45:cofactor`. It appends to 3,297 predecessor coordinates to
give a 3,298-coordinate injective certificate. Thus
\(L_{34}^{\star}=201\), the minimum incremental repair size is one, and
the repaired finite envelopes are \(m+167\) and \(c>100/17\), with
\(\lceil53m/9\rceil\) as a fixed multiplicative witness.

The registered audit checks:

- two complete exact partition profiles at caps 196 and 200;
- 3,299 balanced primes and 5,440,051 unordered pairs;
- 704,261 public-maximum descriptors and 306,350,153 optimized public
  local-exit evaluations;
- two transition profiles at caps 200 and 201;
- 10,139 new transition descriptors, 16,238 optimized tracked local exits,
  and 20,278 full independent tracked local exits;
- 714,400 cap-201 descriptors and 5,715,200 raw coordinates;
- 306,366,391 optimized local-exit evaluations through cap 201;
- 10,139 new cap-201 descriptors and 81,112 primitive-coordinate checks;
- one distinct repair pattern, one minimum repair coordinate, 3,298
  construction coordinates, and 5,440,051 certificate pairs;
- 10,880,102 construction-coordinate local-exit evaluations;
- 16 selected Rust/C# command comparisons and four dense vector checks;
- 1,368,821 independent public-cap descriptor checks;
- 20,278 independent transition local-exit checks;
- 81,112 independent repair-coordinate checks; and
- 5,440,051 independent construction-certificate pair checks.

Canonical summary SHA-256:

```text
52c7899c6d93a747b52fa531e4261ba842acbceb06ae28f420005f8606c85a11
```

Registered schema SHA-256:

```text
34942d674d0451b219bde70fc65909ef3baa6516b08d61df36bf6ea91e8cde61
```

## Interpretation

The result refutes both M45 schedules on one new complete population and
fixes the exact lower threshold at cap 201. The common finite additive and
multiplicative envelopes are repaired by the new length-34 row. It
establishes no asymptotic rate, behavior at \(m>34\), promise recognizer,
density, or general factoring algorithm or lower bound.
