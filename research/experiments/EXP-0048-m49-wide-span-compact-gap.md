# EXP-0048: M49 wide-span compact-gap audit

## Status

`EMPIRICAL` for the bounded signature profiles and independent
implementation checks. The linear-span obstruction is the proof of
`BAR-043`, not an extrapolation from these records.

## Deterministic commands

```powershell
python scripts/run_m49_wide_span_compact_gap_audit.py
python scripts/generate_m49_wide_span_compact_gap_schema.py
python scripts/check_m49_wide_span_compact_gap_differential.py
```

No random seed is used.

## Registered selectors

For each \(m\in\{20,24,28,32,36,40\}\), the audit evaluates
\[
\{m,\ldots,2m\}
\quad\text{with threshold }4
\]
and
\[
\{2m,\ldots,4m\}
\quad\text{with threshold }6.
\]
The spans are respectively \(m\) and \(2m\), beyond the range of
`BAR-042`. Both retain polynomial descriptor, compact modular-evaluation,
and GCD cost.

Across 12 profiles, the audit records:

- 62,128 balanced-prime signatures;
- 3,645,232 compact signature coordinates;
- zero observed primes at or above the registered high-weight thresholds;
- zero injective profiles;
- zero profiles where the conservative finite inequality in `BAR-043`
  alone forces a collision;
- maximum observed signature weight one.

The last two facts are intentionally reported together. The finite
signatures are highly colliding, but the theorem's high-weight union bound
is too conservative at these lengths. Observed sparsity is not substituted
for the asymptotic proof.

Three explicit common-support witnesses validate the GCD-gap reduction:

- \(p=11\) at levels \((4,8,12,16)\), with common gap \(4\);
- \(p=179\) at levels \((6,17,28)\), with common gap \(11\);
- \(p=409\) at levels \((9,17,25)\), with common gap \(8\).

Canonical summary SHA-256:

```text
958223f09db3abd12b46fcda81cc22a553158c1cc92ef4918ad8f2bc9a3202a9
```

Registered schema SHA-256:

```text
970fb769aa2d307ff691ad19ee1226bae89ad860363fb726348b8d80144239ad
```

## Independent implementation

The independent verifier reconstructs every signature coordinate directly
from
\[
2^{3\cdot2^t+5}\equiv-3\pmod p.
\]
It recomputes all 12 profile summaries, checks the three common-support
witnesses and their reduced overlap integers, and independently verifies
the pair formula on each profile. It confirms 3,645,232 coordinates, 12
pair formulas, 12 profile records, and all registered population counts.

## Interpretation

The finite profiles validate the wide-window implementation, Hamming-weight
accounting, and higher-overlap GCD reduction. They do not prove the
asymptotic result. `BAR-043` separately proves that every fixed linear span
\(\Delta_m\le Cm\) fails for this exact public compact-gap family by choosing
a fixed overlap order \(h>2C\). Superlinear spans, other compact families,
adaptive schedules, and general factoring remain outside the result.
