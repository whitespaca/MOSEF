# EXP-0042: M43 length-31 cap audit

## Status

`EMPIRICAL` for the registered raw-prefix, transition, and full normalized
computations. The complete collision and construction certificates promoted
to BAR-037 and THM-016 are finite proof objects.

## Deterministic commands

```powershell
python scripts/run_m43_length_31_cap_audit.py
python scripts/generate_m43_length_31_cap_schema.py
python scripts/check_m43_length_31_cap_differential.py
```

No random seed is used.

## Registered result

At \(m=31\), \(m+93\) gives cap 124 and
\(\lceil49m/12\rceil\) gives cap 127. Cap 124 leaves one 18-prime bucket
and 153 failed pairs; cap 127 leaves one 12-prime bucket and 66 failed
pairs. Exact transition profiles through cap 144 give collision-pair counts
\[
66,66,66,66,21,21,21,21,10,10,6,6,1,1,1,1,1,0.
\]
The cap-143 predecessor is \(\{37483,44963\}\). The only new nonconstant
primitive pattern is \((1,0)\), supplied by
`phi6:11:105:144:cofactor`. It appends to 3,361 old representative columns
to give a 3,362-coordinate injective certificate. Thus
\(L_{31}^{\star}=144\), the minimum incremental repair size is one, and
the repaired finite envelopes are \(m+113\) and \(c>143/31\), with
\(\lceil60m/13\rceil\) as one fixed multiplicative witness.

The registered audit checked:

- two complete lossless raw-prefix profiles at caps 124 and 127;
- 1,280 balanced primes and 818,560 unordered pairs;
- 180,558 public-maximum descriptors and 231,114,240 raw-prefix local exits;
- eighteen transition profiles at caps 127 through 144;
- 81,990 transition descriptors, 983,880 tracked local exits, and 1,188
  tracked pair checks;
- one cap-144 normalized profile with 262,548 descriptors and 336,061,440
  local exits;
- 2,100,384 raw and 3,474 normalized cap-144 coordinates;
- 818,560 raw-versus-normalized pair equivalences;
- 1,836 new cap-144 descriptors and 14,688 primitive-coordinate checks;
- one distinct repair pattern, one minimum repair coordinate, 3,362
  construction coordinates, and 818,560 certificate pairs;
- 16 selected Rust/C# command comparisons and four dense vector checks;
- 346,608 independent public-cap descriptor checks;
- 983,880 independent transition local-exit checks;
- 14,688 independent repair-coordinate checks; and
- 818,560 independent construction-certificate pair checks.

Canonical summary SHA-256:

```text
c15234f614eb9602b6b704700a9660c4a0d486d7e2f965e59af2967eb2cf6888
```

Registered schema SHA-256:

```text
d333d0cebe6c79e2c7a02629be8c3c6a2ea84cb651e184a4cd3a08d1bef969db
```

## Interpretation

The result refutes both M42 schedules on one new complete population and
fixes the exact lower threshold at cap 144. The common finite additive and
multiplicative envelopes are repaired by the new length-31 row. It
establishes no asymptotic rate, behavior at \(m>31\), promise recognizer,
density, or general factoring algorithm or lower bound.
