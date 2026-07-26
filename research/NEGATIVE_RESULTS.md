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

## NR-003 - Divisor coverage does not imply order separation

- Date: 2026-07-26
- Affected claim: `REF-002`, status `REFUTED`.
- Exact hypothesis: if every \(1\le r\le n\) divides at least one member of a
  positive difference family \(\Delta^+(S,T)\), then every profile containing
  two distinct orders in \([n]\) is separated by a member of that family.
- Proof of failure: for \(n=2\), set \(S=\{3\}\), \(T=\{1\}\), and
  \(\Delta^+(S,T)=\{2\}\). Orders 1 and 2 both have the same nonempty
  signature \(\{2\}\), so the profile \((1,2)\) has only a simultaneous hit.
- Actual multiplicative-order witness:
  \(\operatorname{ord}_2(5)=1\), \(\operatorname{ord}_3(5)=2\), but
  \(\gcd(5^2-1,6)=6\). The smallest odd witness is
  \((N,g,d)=(15,4,2)\).
- Deterministic search:
  `python scripts/run_m4_difference_cover_search.py --order-bound 8
  --candidate-max 12 --modulus-max 200 --construction-bound 200` checked
  4,095 candidate families and 114,660 pair profiles with no seed. Among 576
  covers, 240 had noninjective signatures. Summary hash:
  `4c046ae8694070b59f5e328f94038fe32cb84b5ab716bb86a62e79636077e55f`.
- Surviving repair: require injectivity of \(r\mapsto\Sigma_\Delta(r)\) on the
  target order range. The explicit interval difference family satisfies this
  stronger condition but uses \(\Theta(n)\) candidate pairs and is not a
  polynomial-bit-complexity construction when \(n\) is exponentially large.
- Source boundary: this negative result does not refute the conditional
  Umans--Wang algorithms, which factor actual prefactored integers and resolve
  collisions without multiplicative-order separation.

## NR-004 - Conjugate Lucas parameters do not create an independent channel

- Date: 2026-07-26
- Affected claim: `REF-003`, status `REFUTED`.
- Exact hypothesis: pairing a unit \(a\) with
  \(P=a+a^{-1}\pmod N\) makes the Lucas GCD
  \(\gcd(V_d(P,1)-2,N)\) an independent separator that can repair a failure of
  \(\gcd(a^d-1,N)\).
- Proof of failure:
  \[
  V_d(a+a^{-1},1)-2=a^{-d}(a^d-1)^2.
  \]
  The residues have identical prime support. For square-free \(N\), their raw
  GCDs are equal. If the exponent family also contains \(2\), any proper
  discriminant GCD follows from the multiplicative exponent-2 candidate, so
  the combined family has exactly the multiplicative success domain.
- Strict degradation witness:
  \((N,a,P,d)=(25,2,15,4)\) gives discriminant GCD \(1\),
  multiplicative GCD \(5\), and Lucas GCD \(25\).
- Deterministic search:
  `python scripts/run_m5_multigroup_search.py --modulus-max 700 --base-max 32
  --parameter-max 32 --exponent-max 12` checked 9,773 families and 117,276
  exact identities with no seed. It found zero derived-Lucas-only family
  successes. Summary hash:
  `98f2be052a315231292c73319fa98066cf4d8fc4cd66740f207b2d99c7f616f5`.
- Surviving boundary: arbitrary Lucas parameters are not covered. The bounded
  witness \((N,a,P,d)=(15,2,9,3)\) has multiplicative GCD \(1\), discriminant
  GCD \(1\), and Lucas GCD \(5\). This is an exact complement example, not an
  independence probability or a universal guarantee.
- Source boundary: Williams's \(p+1\) method requires the nonsplit
  Legendre-symbol branch. The conjugate discriminant is a square and forces
  the split branch; Williams does not claim independence for this pairing.
