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

## NR-005 - Small-magnitude combined schedules miss balanced semiprimes

- Date: 2026-07-26
- Affected claim: `REF-004`, status `REFUTED`.
- Exact hypothesis: a common finite \(p-1/p+1\) exponent schedule can cover
  every balanced semiprime through a divisibility asymmetry while its largest
  exponent remains below each prime factor minus one.
- Proof of failure: if \(D=\max\Delta\) and \(p>D+1\), neither \(p-1\) nor
  \(p+1\) divides any \(d\in\Delta\), so the combined signature of \(p\) is
  zero. Two such primes have equal signatures and no \(p-1\) or \(p+1\)
  asymmetry in either orientation.
- Smallest unrestricted witness: \(\Delta=\{1\}\) and
  \(N=15=3\cdot5\). This witness is not asserted to lie in the balanced
  interval used by BAR-003.
- Balanced consequence: for
  \(S_n=\{p:2^n<p<2^{n+1/2}\}\), all pair products have bit length
  \(2n+1\). If \(\max\Delta(2n+1)+1<2^n\), the exact promised-pair density on
  this explicitly defined finite distribution is zero.
- Deterministic search:
  `python scripts/run_m8_promise_density_search.py --prime-max 101
  --candidate-max 18 --family-size-max 3 --balanced-n-max 6` checked 987
  exponent families, 296,100 prime pairs, and 184,994 magnitude-zero pair
  cases with no seed. Summary hash:
  `fb2f861f1670c3e4f68a0e8b461f430e7e10eeb966d9f5bec48886c810dd6cd3`.
- Surviving boundary: the argument does not exclude an exponent with
  \(\Theta(k)\) bits whose value exceeds the balanced factors, nor does it
  prove a recognition or general factoring lower bound.

## NR-006 - Large exponent value does not replace divisor structure

- Date: 2026-07-26
- Affected claim: `REF-005`, status `REFUTED`.
- Exact hypothesis: once a common exponent \(d\) strictly exceeds both
  \(p+1\) and \(q+1\), its numerical magnitude guarantees a local
  \(p-1\) or \(p+1\) divisibility asymmetry for the semiprime \(pq\).
- Proof of failure: take \(d=7\), \(p=3\), and \(q=5\). Although
  \(7>p+1=4\) and \(7>q+1=6\), none of \(p-1=2\), \(p+1=4\),
  \(q-1=4\), or \(q+1=6\) divides 7. Both combined signatures are zero, so
  \(N=15\) is outside both local promises.
- Minimality in the registered box: exhaustive increasing search through
  \(d\le4096\) and odd primes through 4093 found
  \((d,p,q,N)=(7,3,5,15)\) first under the strict
  \(d>\max(p+1,q+1)\) condition.
- Deterministic search:
  `python scripts/run_m9_divisor_budget_search.py --bit-length-max 18
  --direct-exponent-max 4096 --prime-max 4093` checked 262,143 exact divisor
  budgets, 2,306,048 direct hit-oracle cases, and 987 record families with no
  seed. Summary hash:
  `b8357f9436ef4d31d072f62dab4f3c8dedad41d6f1787803bf5df2f485ca53ed`.
- Surviving boundary: BAR-004 counts explicit exponent divisors and supplies
  a stipulated-population upper bound. It does not rule out
  \(L(k)\not=o(k\log k)\), exponentially many explicit exponents, compressed
  implicit evaluation, adaptive factor-dependent schedules, other algebraic
  channels, or a general classical factoring algorithm.

## NR-007 - Compact tower syntax does not give compact multiplication-only evaluation

- Date: 2026-07-26
- Affected claim: `REF-006`, status `REFUTED`.
- Exact hypothesis: inside DEF-010, the descriptor
  \(\operatorname{tower}(s)=2^{2^s}\) makes exact formal evaluation of
  \(g^{\operatorname{tower}(s)}\bmod N\) possible with a number of charged
  multiplication nodes polynomial in \(s\).
- Proof of failure: after \(t\) earlier-parent multiplication nodes, BAR-005
  gives maximum formal exponent \(2^t\). Reaching \(2^{2^s}\) therefore needs
  \(t\ge2^s\). Repeated squaring attains equality, so this is the exact cost
  inside the model.
- Deterministic search:
  `python scripts/run_m10_compressed_exponent_search.py --step-max 7
  --descriptor-level-max 16` checked 17 tower levels, including the
  65,537-bit level-16 exponent and its 65,536 squarings. Summary hash:
  `67508cf957fa356350a707a58f1079aebcea4f02481ff826cd5ed09727d210fa`.
- Surviving boundary: this is not a lower bound for computing an equal residue
  for a fixed modulus and base, for addition-subtraction chains, inversions,
  special endomorphisms, adaptive factor branches, or another explicitly
  costed algebraic representation. It does not address whether
  \(\Theta(k\log k)\)-step schedules have useful divisor structure.
