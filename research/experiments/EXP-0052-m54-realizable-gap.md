# EXP-0052: M54 realizable GCD-gap sharpness audit

## Status

`EMPIRICAL` verification of the finite geometry. BAR-047 is proved
symbolically and does not rely on extrapolating these records.

## Commands

```powershell
python scripts/run_m54_realizable_gap_audit.py
python scripts/generate_m54_realizable_gap_schema.py
python scripts/check_m54_realizable_gap_differential.py
```

No random seed is used.

## Registered profiles

The experiment checks all 96 arithmetic-progression witnesses with
\[
1\le h\le6,\qquad 1\le q\le16.
\]
Every witness has \(h+1\) levels, span \(hq\), and maximum realizable gap
equal to \(\lfloor hq/h\rfloor=q\).
Each record also checks the maximum-density interval embedding with
\(r=hq+1=\Delta+1\); the interval contains the registered progression and
therefore realizes the same extremal gap.

It also exhaustively enumerates all \((h+1)\)-subsets of the six-level
progressions
\[
\{2,2+s,\ldots,2+5s\},
\qquad 1\le s\le8,\quad 1\le h\le4.
\]
The 32 ambient profiles cover 544 subsets. The independent checker
reconstructs every GCD and 256 sequence hashes without importing the
reference implementation.

## Results

- 96/96 extremal witnesses attain the universal upper bound;
- 96/96 extremal witnesses embed in a maximum-density interval;
- 32/32 ambient profiles attain their corresponding bound;
- 544 subsets are enumerated exactly;
- 256 level/gap sequence SHA-256 values agree.

Canonical summary SHA-256:

```text
fc09459c7cc6b93a2be7b8255e28fc64f3637e3b9a015ef45757f4b91a7da96c
```

Registered schema file SHA-256:

```text
69c181a7529a6f8a42534146b293add4abe32c3bf845a2da7764d59ad77bcf1c
```

The finite equality checks validate the implementation only. They do not
show that any overlap integer has a balanced prime divisor or that an
endpoint selector is injective.
