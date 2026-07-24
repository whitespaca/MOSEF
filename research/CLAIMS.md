# Claims Ledger

Statuses are exactly: `DEFINITION`, `PROVED`, `CONDITIONAL`, `CONJECTURE`,
`HEURISTIC`, `EMPIRICAL`, `OPEN`, and `REFUTED`.

| ID | Status | Exact statement | Hypotheses | Evidence | Sources | Code / experiment | Adversarial review | Last verified |
|---|---|---|---|---|---|---|---|---|
| DEF-001 | DEFINITION | For a positive integer input \(N\), the project measures input length as \(m=\lceil\log_2 N\rceil\). | \(N\ge 1\). | `CODEX.md` section 4 | None | None | Definition checked against constitution | 2026-07-25 |
| DEF-002 | DEFINITION | For \(g\) coprime to \(N\) and \(d>0\), \(D_N(g,d)=\{p\mid N:\operatorname{ord}_p(g)\mid d\}\); \((g,d)\) is an order separator exactly when this set is nonempty and is not the set of all distinct prime divisors of \(N\). | \(N\ge2\), \(\gcd(g,N)=1\), \(d\in\mathbb Z_{>0}\). | `CODEX.md` section 4 | None | None | Definition checked against constitution | 2026-07-25 |
| EXT-001 | PROVED | Primality decision has an unconditional deterministic algorithm whose running time is polynomial in the binary input length. | Standard deterministic Turing-machine model used by the cited paper. | `research/literature/BASELINE.md` SRC-001 | SRC-001 | None | Imported theorem; official journal PDF inspected, including complexity discussion | 2026-07-25 |
| EXT-002 | PROVED | There is a probabilistic algorithm that completely factors every positive integer \(n\) in expected time \(L_n[1/2,1+o(1)]\). | Probabilistic algorithm and expected-time model defined in the cited paper; asymptotic as \(n\to\infty\). | `research/literature/BASELINE.md` SRC-002 | SRC-002 | None | Imported theorem; official journal record and paper theorem inspected | 2026-07-25 |
| OPEN-001 | OPEN | It is unknown within this project whether, for every composite \(N\), a POSF satisfying all size, exponent-bit-length, construction, separation, and evaluation requirements in `CODEX.md` can be constructed in time polynomial in \(m\). | Classical computation; worst-case inputs; no access to the unknown factorization. | `CODEX.md` sections 4-6; no proof exists in this repository | None | None | Threat-model review pending M2; must not be promoted from empirical evidence | 2026-07-25 |
