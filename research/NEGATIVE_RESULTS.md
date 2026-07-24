# Negative Results

## NR-001 - Universal support-POSF coverage includes an impossible prime-power case

- Date: 2026-07-25
- Affected claim: `OPEN-001`, transitioned from `OPEN` to `REFUTED`.
- Exact hypothesis: a family whose success condition is a nonempty proper set
  \(D_N(g,d)\subset P(N)\) can guarantee an order separator for every composite
  \(N\).
- Motivation: this was the original all-composite POSF target in the project
  constitution.
- Proof of failure: for \(N=p^e\), \(e\ge2\), the set \(P(N)=\{p\}\) is a
  singleton. Every order support is therefore either empty or all of \(P(N)\);
  it can never be nonempty and proper.
- Smallest valuation-only witness: \((N,g,d)=(4,3,1)\) has
  \(D_4(3,1)=P(4)\), but \(\gcd(3-1,4)=2\). The smallest odd witness is
  \((9,2,2)\), which returns \(3\).
- Deterministic search: `python scripts/run_m2_separator_search.py --n-max 500
  --base-max 20 --exponent-max 20` checked 78,860 unit-base candidates with no
  seed and found 5,672 nonsquarefree support-only false negatives. Summary hash:
  `89bda0d3ea8054542151fda07d00c1e2711536b7339952618aea692c1d74cc59`.
- Surviving repairs: `OPEN-002` preprocesses perfect powers before applying a
  support-POSF to residual composites; `OPEN-003` asks for a valuation-separating
  family on all composites. Neither repair is proved constructible.
