# EXP-0049: M51 variable-order superlinear-span audit

## Status

`EMPIRICAL` for the bounded signature profiles and independent
implementation checks. The subquadratic-span obstruction is the proof of
`BAR-044`, not an extrapolation from these records.

## Deterministic commands

```powershell
python scripts/run_m51_subquadratic_span_audit.py
python scripts/generate_m51_subquadratic_span_schema.py
python scripts/check_m51_subquadratic_span_differential.py
```

No random seed is used.

## Registered selectors

For each \(m\in\{20,24,28,32,36,40\}\), the audit uses \(r_m=m+1\) public
levels spread monotonically from \(t_0=m\) across each exact span
\[
\Delta_m=\lfloor m^{3/2}\rfloor
\quad\text{and}\quad
\Delta_m=\lfloor m^{7/4}\rfloor.
\]
Both spans are superlinear. The level sums are respectively
\(O(m^{5/2})\) and \(O(m^{11/4})\), so the registered lists retain
polynomial descriptor and compact evaluation cost.

For each list the analytical order is
\[
\ell_m=\lceil\log_2(r_m+1)\rceil,\qquad
h_m=\min\{r_m,\lceil\sqrt{\Delta_m/\ell_m}\rceil\}.
\]
The audit checks the exact integer inequality
\(h_m^2\ell_m\ge\Delta_m\), the high-weight union bound at threshold
\(h_m+1\), the low-weight Hamming capacity, every finite signature, and all
pair counts.

## Registered results

Across 12 profiles, the audit records:

- 62,128 balanced-prime signatures;
- 2,450,864 compact signature coordinates;
- 12 exact variable-order balance checks;
- zero observed primes at or above the registered high-weight thresholds;
- zero injective profiles;
- zero profiles where the conservative finite inequality alone forces a
  collision;
- maximum observed signature weight one.

The \(m^{3/2}\) profiles use \(h_m=5,\ldots,7\), and the \(m^{7/4}\)
profiles use \(h_m=7,\ldots,11\). At the largest registered length \(m=40\),
the two spans are 252 and 636, while the corresponding high-weight-bound bit
lengths are 61 and 88. These finite upper bounds exceed the finite
population scale and therefore do not certify the observed collisions.
Observed weight sparsity is not substituted for the asymptotic proof.

Canonical summary SHA-256:

```text
cf4874600194e17b654bd40e29c33b96babff4860758e79c19f7e76981c63fd2
```

Registered schema SHA-256:

```text
4552818335844443ca9781ab44008a68f18288fdbc557b32c71c4de362cf3003
```

## Independent implementation

The independent verifier reconstructs every signature coordinate directly
from
\[
2^{3\cdot2^t+5}\equiv-3\pmod p.
\]
It separately recomputes the integer square-root order, all 12 profile
summaries, the exact union and Hamming bounds, and every pair formula. It
confirms 2,450,864 coordinates, 12 profile records, 12 pair formulas, and
12 balance inequalities.

## Interpretation

The finite profiles validate that the variable order is computed only from
public list geometry and that the exact `BAR-043` finite bound remains
conservative for a growing order. They do not prove `BAR-044`. The theorem
separately uses
\[
\Delta_m\log_2(r_m+1)=o(m^2)
\]
to make both analytical ledgers \(2^{o(m)}\). The experiment does not cover
the \(\Theta(m^2/\log m)\) boundary, quadratic spans, other compact
families, adaptive schedules, or general factoring.
