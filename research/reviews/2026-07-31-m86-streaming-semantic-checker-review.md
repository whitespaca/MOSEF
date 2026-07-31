# M86 adversarial streaming-checker review

## Review boundary

This internal review treats the M86 executable as a potentially faulty proof
program. It compares the code with the public definitions used by
`THM-004`, `THM-005`, and `THM-019`, plus the frozen M46 artifact. It is not
external peer review or proof-assistant verification.

## Threats checked

### 1. Hidden reuse of the implementation under test

The checker imports only Python standard-library modules. It does not import
the M46 generator, M46 differential checker, M85 checker, or project
number-theory implementation. An AST test rejects project and relative
imports.

Result: PASS.

### 2. Trusting the serialized prime population

The checker derives the exact standard-bit-length square interval, runs a
fresh sieve, and requires ordered equality with all 3,299 registered primes.
A rehashed population mutation is rejected.

Result: PASS.

### 3. Reproducing descriptor counts with the wrong grammar

The iterator is derived directly from the two congruence classes and the
unequal-factor rule. It independently obtains 704,261 descriptors at cap 200
and 714,400 at cap 201. A separate test enumerates both counts.

Result: PASS.

### 4. Misidentifying the cap-201 increment

The public cap grammar is nested. Therefore a cap-201 descriptor is new
exactly when one of \(A,B,g\) equals 201. The checker filters by the equivalent
condition \(\max\{A,B,g\}=201\) and obtains exactly 10,139 descriptors.

Result: PASS.

### 5. Invalid quotient division at a cyclotomic root

The smallest reconstructed population prime is 92,683, while
\(\Phi_4(g)\le201^2+1=40,402\) and
\(\Phi_6(g)<40,402\). Hence no registered denominator vanishes. The checker
asserts this range separation before evaluating the certificate and has no
unneeded root branch.

Result: PASS.

### 6. Hiding a materialized certificate matrix

The source loop owns a list with one integer per prime. Each coordinate is
evaluated across the population and immediately packed into those integers.
No per-coordinate vector or prime-by-coordinate table is retained. A small
oracle test checks the streaming assembly invariant. The recorded mutable
certificate state is 3,299 signature slots.

Result: PASS.

### 7. Trusting packed signatures as semantics

All 10,880,102 coordinate/prime bits are recomputed before exact comparison
with the packed artifact values. A packed-signature mutation is rejected.

Result: PASS.

### 8. Proving only a subcertificate collision

The first 3,297 sources leave at most the one tracked duplicate bucket. The
checker also evaluates every cap-200 descriptor on both tracked primes and
finds identical eight-bit masks. Thus the full selector has both at most and
at least that collision.

Result: PASS.

### 9. Unsupported repair uniqueness or minimum

Every one of the 81,112 primitive sources associated with the 10,139 new
descriptors is compared on the tracked pair. Exactly
`phi6:149:201:45:cofactor` differs. Zero new coordinates cannot remove the
cap-200 collision, and this one does. The review found no claim that the full
3,298-coordinate certificate is minimum.

Result: PASS.

### 10. Inferring cap-201 injectivity from the repair pair alone

The checker independently recomputes all 3,298 certificate coordinates on
all 3,299 primes and requires 3,299 distinct packed signatures. The repair
scan is used for uniqueness and incremental minimum, not as a substitute for
the population-wide injectivity check.

Result: PASS.

### 11. Overstating the clean-room coverage

M86 validates M46 only. Together M85 and M86 provide clean-room paths for
two of the 26 M50 rows. Legacy semantic paths and M50 integrity checks remain
necessary for the other 24 rows.

Result: PASS with the two-row scope explicit.

### 12. Finite-to-asymptotic or general-factoring leakage

The checker, proof, experiment, and bilingual manuscript wording keep
the \(m=34\), exact-selector, factor-dependent-promise scope. General
classical polynomial-time factoring remains open.

Result: PASS.

## Verdict

PASS for the bounded M86 deliverable. The checker independently reconstructs
the M46 semantic kernel with coordinate-streaming memory. It strengthens
finite reproducibility but does not promote a claim, constitute external
review, or resolve the original general factoring problem.
