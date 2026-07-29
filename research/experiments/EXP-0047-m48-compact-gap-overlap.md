# EXP-0047: M48 compact-gap overlap audit

## Status

`EMPIRICAL` for the bounded signature profiles and independent
implementation checks. The asymptotic short-span obstruction is the proof
of `BAR-042`, not a regression from these records.

## Deterministic commands

```powershell
python scripts/run_m48_compact_gap_overlap_audit.py
python scripts/generate_m48_compact_gap_overlap_schema.py
python scripts/check_m48_compact_gap_overlap_differential.py
```

No random seed is used.

## Registered selectors

For every \(20\le m\le40\), the audit evaluates both public level windows
\[
\{m,\ldots,m+\lfloor m/4\rfloor\}
\quad\text{and}\quad
\{2m,\ldots,2m+\lfloor m/4\rfloor\}.
\]
Both have polynomial descriptor, compact modular-evaluation, and GCD cost.
The second window checks that the overlap bound is invariant under a common
level shift.

Across 42 profiles, the audit records:

- 163,794 balanced-prime signatures;
- 1,636,992 compact signature coordinates;
- 11 exact overlap integers for level gaps 1 through 11;
- three explicit common-support witnesses:
  \((p,t,u)=(11,4,8),(179,6,17),(409,9,17)\);
- 40 profiles where the exact finite inequality in `BAR-042` alone forces a
  collision;
- zero injective profiles and zero multi-hit balanced primes in the
  registered windows.

The two length-20 profiles fall outside the conservative finite inequality
but are directly noninjective. At length 40, each 11-candidate window has
22,394 balanced primes, one observed all-zero signature class, zero
multi-hit primes, and all 250,734,421 pairs collide. Its pair-specific
multi-hit population upper bound is 1,034.

Canonical summary SHA-256:

```text
48b95a0e1acb799fce06e2aa25492eebc432daef6c6e8c14abd962ef0c7170d2
```

Registered schema SHA-256:

```text
c1a659a6081df2b46f492379b97c9b624f0041772068d19e89337550c19eaa8e
```

## Independent implementation

The independent verifier reconstructs every support coordinate directly
from
\[
2^{3\cdot2^t+5}\equiv-3\pmod p,
\]
recomputes the 11 overlap integers, checks the three nontrivial overlap
witnesses, and independently derives every signature bucket and pair count.
It confirms 1,636,992 coordinates, 42 pair formulas, and all registered
population summaries.

## Interpretation

The finite profiles validate the shifted-window implementation and the
conservative overlap ledger. They do not prove that arbitrary wide-span
encoded level lists fail. `BAR-042` proves only that polynomial candidate
count plus span at most \((1/2-\varepsilon)m\) is insufficient. M49 must
test level gaps at or beyond the unresolved half-length boundary without
turning finite sparsity into an asymptotic theorem.
