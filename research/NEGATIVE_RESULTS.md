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

## NR-002 - Divisibility asymmetry does not make a fixed base separate

- Date: 2026-07-26
- Affected claim: `REF-001`, status `REFUTED`.
- Exact hypothesis: if distinct primes \(p,q\mid N\) satisfy
  \(p-1\mid d\) and \(q-1\nmid d\), then a fixed unit base \(a\) necessarily
  yields a nontrivial \(\gcd(a^d-1,N)\).
- Proof of failure: with \(N=51\), \(p=3\), \(q=17\), \(a=2\), and
  \(d=\operatorname{lcm}(1,\ldots,8)=840\), the divisibility conditions hold,
  but \(\operatorname{ord}_{17}(2)=8\mid840\). Thus both primes divide
  \(2^{840}-1\), and the GCD is all of \(N\).
- Minimality in the registered box: deterministic enumeration found this as
  the smallest collision for fixed base \(2\), \(N\le500\), and
  \(1\le B\le20\). Independent adversarial review confirmed the enumeration.
- Canonical search summary:
  `0a1d2ca2fef29126b60f3a9377454200e33fce20c0b49c081ea527622f8c536d`.
- Surviving repair: THM-001 samples a fresh uniform residue. At least half of
  the units avoid the proper root subgroup modulo \(q\), while nonzero
  nonunits expose a direct factor, giving success probability at least
  \(5/12\) per witness trial.
