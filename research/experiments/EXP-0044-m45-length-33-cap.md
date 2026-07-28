# EXP-0044: M45 length-33 cap audit

## Status

`EMPIRICAL` for the registered exact partition-refinement and certificate
computations. The complete collision and construction certificates promoted
to BAR-039 and THM-018 are finite proof objects.

## Deterministic commands

```powershell
python scripts/run_m45_length_33_cap_audit.py
python scripts/generate_m45_length_33_cap_schema.py
python scripts/check_m45_length_33_cap_differential.py
```

No random seed is used.

## Registered result

At \(m=33\), \(m+135\) gives cap 168 and
\(\lceil26m/5\rceil\) gives cap 172. Cap 168 leaves one 12-prime bucket
and 66 failed pairs; cap 172 leaves one eight-prime bucket and 28 failed
pairs. Exact profiles at caps 172 through 195 give collision counts
\[
28,28,28,15,15,10,10,6,6,6,6,6,3,3,3,3,1,1,1,1,1,1,1,0.
\]
The cap-194 predecessor is \(\{80309,92671\}\). The only new nonconstant
primitive pattern is \((1,0)\), supplied by
`phi4:195:91:20:cofactor`. It appends to 2,409 predecessor coordinates to
give a 2,410-coordinate injective certificate. Thus
\(L_{33}^{\star}=195\), the minimum incremental repair size is one, and
the repaired finite envelopes are \(m+162\) and \(c>194/33\), with
\(\lceil147m/25\rceil\) as a fixed multiplicative witness.

The registered audit checks:

- two complete exact partition profiles at caps 168 and 172;
- 2,410 balanced primes and 2,902,845 unordered pairs;
- 447,678 public-maximum descriptors and 158,193,605 optimized public
  local-exit evaluations;
- 24 transition profiles at caps 172 through 195;
- 213,474 new transition descriptors, 751,601 optimized tracked local
  exits, and 1,707,792 full independent tracked local exits;
- 661,152 cap-195 descriptors and 5,289,216 raw coordinates;
- 158,945,206 optimized local-exit evaluations through cap 195;
- 28,112 new cap-195 descriptors and 224,896 primitive-coordinate checks;
- one distinct repair pattern, one minimum repair coordinate, 2,410
  construction coordinates, and 2,902,845 certificate pairs;
- 5,808,100 construction-coordinate local-exit evaluations;
- 16 selected Rust/C# command comparisons and four dense vector checks;
- 866,180 independent public-cap descriptor checks;
- 1,707,792 independent transition local-exit checks;
- 224,896 independent repair-coordinate checks; and
- 2,902,845 independent construction-certificate pair checks.

Canonical summary SHA-256:

```text
2a3d7c347eeea57c36fd3a585744a30818a5ff0543840607f91514e1786feb23
```

Registered schema SHA-256:

```text
a9ba5df141ecefdf9c7a946bd5bf7f17dd44c5748b843385f6e1f0165e311cd2
```

## Interpretation

The result refutes both M44 schedules on one new complete population and
fixes the exact lower threshold at cap 195. The common finite additive and
multiplicative envelopes are repaired by the new length-33 row. It
establishes no asymptotic rate, behavior at \(m>33\), promise recognizer,
density, or general factoring algorithm or lower bound.
