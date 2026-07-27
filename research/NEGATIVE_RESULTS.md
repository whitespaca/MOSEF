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

## NR-008 - Boundary node count alone does not guarantee prime separation

- Date: 2026-07-26.
- Affected claim: `REF-007`, status `REFUTED`.
- Exact hypothesis: every common factor-oblivious DEF-010 schedule with
  \(\Theta(k\log k)\) charged multiplication nodes has a nonvanishing
  combined \(p-1/p+1\) promise fraction on each stipulated exponentially
  large common-input-length prime population.
- Proof of failure: use repeated squaring for
  \(t(k)=\lfloor k\log_2k\rfloor\) nodes and expose every exponent
  \(1,2,4,\ldots,2^{t(k)}\). Their divisor union contains only
  \(t(k)+1\) powers of two. At most \(2(t(k)+1)\) odd primes can be one more
  or one less than those divisors, so the global hit set is polynomial.
  BAR-003 makes the promised-pair fraction vanish on every stipulated
  \(2^{\Omega(k)}\)-size population.
- Surviving boundary: some \(\Theta(k\log k)\)-node schedules, including the
  first-primes primorial family in BAR-006, have exponentially many divisors.
  The counterexample refutes sufficiency of node count alone; it does not
  rule out a construction with a proved prime-yield guarantee.
## NR-009 - Total primorial divisor capacity does not survive factor-scale restriction

- Date: 2026-07-27.
- Status: `REFUTED` claim `REF-008`.
- Hypothesis tested: the \(2^{r}\) total divisors of the first-primes
  primorial \(P_r\), with \(r=\Theta(k)\), should produce enough \(d\pm1\)
  primes to maintain a nonvanishing combined-promise fraction on an
  exponentially large population of \(O(k)\)-bit factors.
- Counterargument: a relevant divisor has \(d=q\pm1\le2^{\beta k}+1\).
  If it uses \(t\) of the primorial's distinct prime factors, then
  \((t+1)!\le d\), so \(t=O(k/\log k)\). Among \(r=O(k)\) available primes
  there are only
  \(2^{O(k\log\log k/\log k)}=2^{o(k)}\) such divisors, regardless of whether
  their \(d\pm1\) neighbors are prime.
- Evidence: BAR-007 and deterministic EXP-0011; independent adversarial
  review.
- Scope: first-primes primorials and nested subfamilies. This does not refute
  every exact-boundary exponent family or prove a general factoring lower
  bound.

## NR-010 - Squareful and noninitial supports do not escape factor-scale scarcity

- Date: 2026-07-27.
- Status: `REFUTED` claim `REF-009`.
- Hypothesis tested: at the exact \(O(k\log k)\) exponent-length boundary,
  repeated prime powers or a support that skips the smallest primes can create
  exponentially many \(O(k)\)-bit divisors and restore a nonvanishing
  combined-promise fraction.
- Counterargument: split prime powers at
  \(Y_k=k/(\log k)^2\). Small-prime exponent choices contribute only
  \(2^{O(k/\log k)}\). The exponent contains only \(O(k)\) large-prime
  occurrences, while an \(O(k)\)-bit divisor can select only
  \(O(k/\log k)\) of them. The resulting labeled-occurrence binomial count is
  \(2^{O(k\log\log k/\log k)}=2^{o(k)}\), independently of squarefreeness or
  whether the support is initial.
- Evidence: BAR-008 and deterministic EXP-0012; independent adversarial
  review.
- Scope: common polynomial-size explicit schedules with \(O(k\log k)\)-bit
  exponents, plus the stated DEF-010 transfer. Longer exponents,
  exponentially many exponents, adaptive factor dependence, richer
  representations, other channels, and general factoring remain outside the
  result.

## NR-011 - Charged same-base inversion does not enlarge the exponent hit family

- Date: 2026-07-27.
- Status: `REFUTED` claim `REF-010`.
- Hypothesis tested: permitting modular ratios in a factor-oblivious
  same-base straight-line program might use cancellation and negative
  exponents to evade the factor-scale scarcity of BAR-008 at
  \(O(k\log k)\) charged-node cost.
- Counterargument: signed formal exponents still satisfy
  \(|z_i|\le2^i\). For a unit base,
  \(g^{-d}-1=-g^{-d}(g^d-1)\), so negative and positive exponents have
  exactly the same GCD with \(N\), while exponent zero yields only the full
  collision. Removing signs, zeros, and duplicates leaves a polynomial
  explicit list with \(O(k\log k)\)-bit exponents, to which BAR-008 applies.
- Evidence: BAR-009 and deterministic EXP-0013; independent adversarial
  review, including a separate full-syntax enumeration with self-ratios.
- Scope: the charged, factor-oblivious, same-base DEF-014 unit branch.
  Proper factors discovered by the initial base GCD are separate exits.
  Implicit batches, modulus-specific shortcuts, adaptive factor-dependent
  choices, special endomorphisms, unrelated multi-base expressions, other
  groups, and general factoring remain open.

## NR-012 - A compact selector does not compress materialized batch leaves

- Date: 2026-07-27.
- Status: `REFUTED` claim `REF-011`.
- Hypothesis tested: a compact selector plus one aggregate root GCD might test
  exponentially many same-base exponent candidates at polynomial charged cost
  even when evaluated by a standard product tree.
- Counterargument: DEF-015 enumerates, evaluates, stores, and charges every
  selected leaf. An \(n\)-leaf binary tree has exactly \(n-1\) internal
  multiplications, so polynomial total charged work forces polynomial \(n\).
  The aggregate also does not add proper successes: a proper root GCD implies
  a proper leaf GCD. It can lose them; \(N=21,g=2,\Delta=\{2,3\}\) has leaf
  GCDs \(3,7\) but root GCD \(21\).
- Evidence: BAR-010 and deterministic EXP-0014; independent adversarial and
  source-scope review.
- Scope: the selector-described standard tree with mandatory leaf
  materialization. Specialized circuits that compute the formal or residue
  product without materializing every leaf, adaptive factor-dependent
  selectors, other channels, and general factoring remain open.

## NR-013 - Product-DAG sharing repeats atoms but does not synthesize distinct tests

- Date: 2026-07-27.
- Status: `REFUTED` claim `REF-012`.
- Hypothesis tested: reusing subproducts in a polynomial-size same-base
  product DAG provides an exponentially indexed family of distinct exponent
  tests or a new proper-factor success absent from its explicit atoms.
- Counterargument: the \(s\)-th gate can represent \(2^s\) unfolded
  occurrences by repeated self-product, but every occurrence is one of the
  explicitly emitted atoms and every node has a nonnegative formal
  multiplicity vector over that finite table. A proper node GCD therefore
  implies a proper used atom GCD.
- Repetition can instead destroy a prime-power separator:
  \(N=9,g=4,d=1\) has atom GCD \(3\), while its square has full GCD \(9\).
  Complementary atoms at \(N=21,g=2,\Delta=(2,3)\) likewise aggregate to the
  full collision.
- Evidence: BAR-011 and deterministic EXP-0015; 611,572 syntax checks,
  517,020 residue circuits, 3,581,928 valuation components, and 10 selected
  cross-language comparisons.
- Scope: no statement about addition, subtraction, division, composition,
  closed-form atom synthesis, modulus-specific identities, adaptive
  factor-dependent computation, other groups, or general arithmetic
  circuits.
- Revisit only with a precise richer circuit whose uniform constructor,
  formal outputs, residue evaluation, and factor extraction are all charged.

## NR-014 - Dyadic geometric compression is one quotient, not an exponential test family

- Date: 2026-07-27.
- Status: `REFUTED` claim `REF-013`.
- Hypothesis tested: the \(2^t\) monomials in
  \((g^{2^t}-1)/(g-1)=\sum_{i<2^t}g^i\), or exact modular division by
  \(g-1\), provide \(2^t\) separately extractable same-base exponent tests
  at \(O(t)\) charged cost or a proper-factor success when every explicit
  dyadic-component GCD is trivial or full.
- Counterargument: the quotient has the factorized form
  \(\prod_{j<t}(g^{2^j}+1)\). A proper quotient GCD implies a proper GCD for
  one of those \(t\) factors; a proper numerator GCD implies a proper GCD for
  the denominator or a dyadic factor. A proper nonunit denominator is itself
  an extracted factor, and a full denominator leaves the division-free
  product defined. The expanded \(2^t\)-coefficient output is exponential if
  requested.
- Small boundaries: \(N=15,g=4,t=1\) has complementary denominator/factor
  GCDs \(3,5\) but full numerator GCD \(15\). At \(N=6,g=1,t=3\), division
  has a full denominator collision while the explicit quotient path has GCD
  \(2\). At \(N=45,g=8,t=5\), factor GCDs \(9,5\) aggregate to full quotient
  and numerator collisions. At \(N=8,g=1,t=2\), component GCDs \(2,2\)
  aggregate to the different proper quotient GCD \(4\), so the theorem
  preserves success existence rather than exact factor value.
- Evidence: BAR-012 and deterministic EXP-0016; 55,154 circuits, 275,770
  recurrence checks, 2,047 coefficient checks, and 12 selected
  cross-language comparisons.
- Scope: the exact DEF-017 dyadic telescope only. No claim is made for
  arbitrary rational straight-line programs, arbitrary polynomial
  composition, adaptive factor-dependent computation, other groups, or
  general arithmetic circuits.
- Revisit with a different uniform circuit identity whose extraction output
  cannot be reduced to a polynomial-size explicit component list.

## NR-015 - An arbitrary geometric sum is one compact value, not a new extraction path

- Date: 2026-07-27.
- Status: `REFUTED` claim `REF-014`.
- Hypothesis tested: replacing the dyadic exponent by an arbitrary public
  \(M\) might let the \(O(\log M)\)-size binary circuit for
  \(S_M(g)=\sum_{i<M}g^i\) produce a proper factor not already accounted for
  by its endpoint, denominator, or public exponent.
- Counterargument: the exact identity
  \((g-1)S_M(g)=g^M-1\) gives an exhaustive denominator trichotomy. If
  \(g-1\) is a unit, quotient and endpoint GCDs are identical. If it has a
  proper GCD, that denominator already factors \(N\). If it has full GCD,
  \(g\equiv1\pmod N\), so \(S_M(g)\equiv M\pmod N\) and the quotient GCD is
  exactly \(\gcd(M,N)\).
- Different factor values remain possible in the proper branch:
  \(N=15,g=4,M=2\) gives denominator GCD \(3\), quotient GCD \(5\), and full
  endpoint collision. For \(N=8,g=1,M=4\), quotient and public exponent GCDs
  both equal \(4\), including the repeated prime power.
- Evidence: BAR-013 and deterministic EXP-0017; 64 symbolic identities,
  320,896 modular circuits, zero unexplained reductions, and 12 selected
  cross-language comparisons.
- Scope: the exact DEF-018 single geometric-sum circuit only. Arbitrary
  rational programs, cancellation-obscured multi-denominator identities,
  adaptive factor-dependent computation, other groups, and general factoring
  remain open.
- Revisit with a precise richer identity whose total intermediate-division
  semantics and extraction outputs do not reduce to these three GCD paths.

## NR-016 - A two-stage geometric cancellation does not hide a new quotient path

- Date: 2026-07-27.
- Status: `REFUTED` claim `REF-015`.
- Hypothesis tested: cancellation in
  \(S_{AB}(g)/S_A(g)=S_B(g^A)\) can create a proper quotient success not
  accounted for by the rational numerator, a proper intermediate
  denominator, or the public multiplier GCD.
- Counterargument: the exact certificate
  \(S_{AB}(X)=S_A(X)S_B(X^A)\) gives \(U=LQ\). If \(L\) is a unit, numerator
  and quotient GCDs are identical. If \(L\) has a proper GCD, it already
  factors \(N\). If \(L\) is full, then
  \((g-1)L=g^A-1\equiv0\pmod N\), so \(g^A\equiv1\pmod N\),
  \(Q\equiv B\pmod N\), and the quotient GCD is the public \(\gcd(B,N)\).
  Independently, the composed denominator \(g^A-1\) follows BAR-013.
- Different factor values remain possible in the proper branch:
  \(N=15,g=2,A=B=2\) gives intermediate and quotient GCDs \(3\) and \(5\),
  while the rational numerator GCD is full.
- Evidence: BAR-014 and deterministic EXP-0018; 144 symbolic identities,
  177,264 modular circuits, 354,528 residue identities, zero unexplained
  reductions, and 12 selected Python/Rust/C# comparisons.
- Scope: the exact DEF-019 two-stage geometric identity only. Iterated
  quotient chains, arbitrary rational programs, unrelated denominators,
  adaptive factor-dependent computation, other groups, and general factoring
  remain open.
- Revisit with an explicitly charged iterated identity whose intermediate
  denominator exits and compact versus expanded outputs are fully specified.

## NR-017 - Iterated public quotient products do not hide a new stage

- Date: 2026-07-27.
- Status: `REFUTED` claim `REF-016`.
- Hypothesis tested: a public chain
  \(M_i=\prod_{j\le i}A_j\) might make an iterated geometric quotient or its
  aggregate product expose a proper factor outside the charged prefix
  numerators, intermediate denominators, composed denominators, public
  multipliers, and explicit stage quotient GCDs.
- Counterargument: each exact certificate
  \(S_{M_i}(X)=S_{M_{i-1}}(X)S_{A_i}(X^{M_{i-1}})\) is one BAR-014 instance.
  Thus a unit prefix preserves the quotient/numerator GCD, a proper prefix is
  already a factor exit, and a full prefix makes the quotient congruent to
  the public \(A_i\). Each composed denominator separately follows BAR-013.
  If the final product has a proper GCD, no stage quotient can be zero modulo
  \(N\), while all stage quotients cannot be units; hence some explicit stage
  quotient has a proper GCD.
- Masking remains possible and is retained rather than hidden:
  \(N=15,g=2,(A_1,A_2,A_3)=(2,2,3)\) has a proper stage quotient GCD before
  the final product becomes a full collision. Proper prefix and quotient
  divisor values may also differ.
- Evidence: BAR-015 and deterministic EXP-0019; 155 symbolic chains,
  190,805 modular chains, 529,330 stages, zero unexplained cases, and 12
  selected cross-language comparisons. Independent review additionally
  checked 58,680 small chains and a 256-bit prefix.
- Scope: the exact DEF-020 product-only public factor chain. Cross-stage
  addition/subtraction, arbitrary subset extraction, unrelated denominators,
  adaptive factor-dependent computation, other groups, and general
  arithmetic circuits remain open.
- Revisit with an explicitly charged factorization-independent
  linear-combination grammar over certified stage values.

## NR-018 - Product-only component implications fail under signed addition

- Date: 2026-07-27.
- Status: `REFUTED` claim `REF-017`.
- Hypothesis tested: a proper GCD of a signed combination of explicit
  quotient stages must already occur in a charged stage, prefix, denominator,
  multiplier, coefficient, or weighted-stage GCD.
- Counterexample: at \(N=9\), \(g=2\), factors \((5,5)\), and coefficients
  \((-1,1)\), the stage quotients are \(4,7\), the weighted residues are
  \(5,7\), and every retained component has GCD one with \(9\). Their
  aggregate is \(3\), whose GCD is the proper factor \(3\).
- Exact formal output:
  \[
  S_5(X^5)-S_5(X)
  =-X-X^2-X^3-X^4+X^5+X^{10}+X^{15}+X^{20}.
  \]
  All eight nonzero monomials and coefficients are explicitly charged.
- Evidence: BAR-016, its adversarial audit, and deterministic EXP-0020;
  1,301,300 combinations included 13,800 new proper aggregates and 6,262
  strict all-unit successes, with zero semantic failures and 12 selected
  Python/Rust/C# agreements.
- Scope: the exact DEF-021 single signed aggregate. This does not provide a
  universal schedule, a success-rate or density theorem, a promise recognizer,
  or a lower bound for adaptive or general arithmetic circuits.
- Revisit by characterizing the prime-power congruence and valuation
  conditions that make a public signed quotient combination succeed.

## NR-019 - The symmetric M21 mechanism is not algebraically unclassified

- Date: 2026-07-27.
- Status: `REFUTED` claim `REF-018`.
- Hypothesis tested: the repeated-factor signed difference
  \(S_A(g^A)-S_A(g)\) creates a proper GCD with no compact endpoint/cofactor
  decomposition.
- Counterargument:
  \[
  S_A(X^A)-S_A(X)
  =X(X^{A-1}-1)
   \sum_{j=1}^{A-1}X^{j-1}S_j(X^{A-1}).
  \]
  At every prime power dividing \(N\), the difference valuation is the
  capped sum of the endpoint and cofactor valuations. A unit endpoint
  preserves the cofactor GCD, a proper endpoint already factors \(N\), and a
  full endpoint forces a full difference.
- The M21 witness is an endpoint case because
  \(\gcd(2^4-1,9)=3\). The cofactor branch remains real:
  \(N=55,g=2,A=3\) has unit stage quotients and endpoint, but
  \(H_3(2)=11\).
- Evidence: BAR-017 and deterministic EXP-0021; 27,209 compact/expanded
  evaluations, 43,148 prime-power valuation checks, zero unexplained cases,
  and 12 Python/Rust/C# agreements.
- Scope: the exact repeated-factor, coefficients \((-1,1)\) family. Unequal
  factors, arbitrary coefficients, longer chains, adaptive choices, other
  groups, and general arithmetic circuits remain open.
- Revisit with the unequal depth-two signed difference before considering
  longer schedules.

## NR-020 - The natural unequal common factor is not a complete explanation

- Date: 2026-07-27.
- Status: `REFUTED` claim `REF-019`.
- Hypothesis tested: every proper GCD of
  \(D_{A,B}(g)=S_B(g^A)-S_A(g)\) is already a proper GCD of
  \(gS_{\gcd(A-1,B-1)}(g)\).
- Counterexample: at \((N,g,A,B)=(25,3,3,2)\), the stage residues are
  \(13,3\), the difference is \(15\), and its GCD is \(5\). The common step
  is one, so the natural common factor is the unit \(3\). Unit division gives
  residual cofactor \(5\bmod25\), and the independent rational-prefix
  reduction gives the same residue.
- Positive boundary: BAR-018 proves
  \(D_{A,B}=XS_hC_{A,B}\), exact endpoint polynomial GCDs \(S_h\), and a
  total common-factor trichotomy. The refutation concerns only completeness
  of the natural factor, not that factorization.
- Evidence: deterministic EXP-0022 found 7,848 proper unit-common-factor
  cofactor cases and 3,408 proper common-factor cases, with zero unexplained
  failures and 12 Python/Rust/C# agreements.
- Scope: one unequal depth-two normalized difference. No success-rate,
  recognition, universal schedule, density, general factoring, or
  general-circuit claim follows.
- Revisit by classifying the surviving unit-prefix rational residue.

## NR-021 - Boundary and common-step factors do not classify primitive cyclotomic factors

- Date: 2026-07-27.
- Status: `REFUTED` claim `REF-020`.
- Hypothesis tested: every cyclotomic factor of a primitive numerator
  \(c_1S_A(X)+c_2S_B(X^A)\) is forced either by its value at \(X=1\), or,
  when \(c_1=-c_2\), by the M23 common-step difference factor.
- Counterexample: for \((A,B,c_1,c_2)=(3,7,1,1)\), evaluation at \(i\)
  gives \(S_3(i)=i\) and \(S_7(i^3)=-i\). Therefore
  \(\Phi_4=X^2+1\) divides the primitive numerator. Neither coefficients
  sum to zero nor does \(3+7=0\).
- Strict modular witness: at \((N,g)=(55,2)\), the two stages are 7 and 8,
  both units, the content and both public resultant bounds are units, but
  the aggregate is 15 and has GCD 5. The unit-prefix rational residue is 10
  and has the same GCD.
- Positive boundary: BAR-019 gives both exact stage resultants, public
  overlap bounds, total content and prefix semantics, and the exact
  root-of-unity equation. It does not claim that exceptional orders have no
  further arithmetic structure.
- Evidence: EXP-0023 performed 150,528 exact cyclotomic divisions on 1,176
  primitive coefficient pairs and found six exceptional factors in the
  registered box, with zero failed identities and 12 cross-language
  disagreements.
- Scope: one unequal depth-two signed numerator. No completeness beyond the
  finite order bound, density, recognizer, universal schedule, general
  factoring result, or general circuit lower bound follows.
- Revisit by classifying when the root-of-unity ratio
  \(-Q_2(\zeta)/Q_1(\zeta)\) is rational for primitive coefficient pairs.
