# M85 adversarial semantic-checker review

## Review boundary

This internal review treats the checker as a potentially faulty proof
program. It compares the executable only with the public definitions in
`THM-004`, `THM-005`, and `THM-014`, plus the frozen M41 JSON artifact.
It is not external peer review and not a proof-assistant verification.

## Threats checked

### 1. Generator reuse disguised as independence

The checker imports only Python standard-library modules. An AST regression
test rejects project imports and relative imports. It does not call the M41
audit, generator, differential checker, or `python/mosef_reference`.

Result: PASS.

### 2. Trusting the registered prime list

The checker derives the exact square interval from \(m=29\), runs its own
sieve, and requires exact ordered equality with all 685 registered primes.
A rehashed mutation of the last prime is rejected.

Result: PASS.

### 3. Trusting serialized descriptor strings

Every source is parsed canonically and checked against the order-four or
order-six congruence grammar, unequal-factor rule, and public cap. The first
1,527 sources must lie at cap 102 and the last must be the declared cap-103
repair. A rehashed cap-104 mutation is rejected before signature use.

Result: PASS.

### 4. Circular cofactor evaluation

The checker does not port the compact cofactor implementation. Away from a
cyclotomic root it divides the exact exceptional numerator by the
cyclotomic value in the finite field. At a root it uses the differentiated
identity \(F'=\Phi'C+\Phi C'\). On the actual M41 population,
\(p>16{,}000\), \(g\le103\), and both positive cyclotomic values are below
\(p\), so no registered descriptor reaches the root branch. The certificate
therefore relies only on independently reconstructed unit division. A
separate valid small descriptor \((\Phi_4,A,B,g,p)=(\Phi_4,3,7,2,5)\)
exercises the simple-root derivative formula and agrees with the exact
integer quotient.

Result: PASS with the registered-versus-synthetic boundary explicit.

### 5. Hash-only acceptance

Population, descriptor, and primitive-vector mutations are rehashed before
validation and still fail semantic checks. Packed signatures are compared
with freshly recomputed values.

Result: PASS.

### 6. Showing only that a sublist collides

The 1,527-coordinate predecessor sublist proves there is at most one
collision bucket. The checker separately evaluates every cap-102 descriptor
on the tracked pair and proves that this pair collides across the complete
raw selector. These two directions establish the exact sole collision.

Result: PASS.

### 7. Showing repair without injectivity

All 1,528 certificate coordinates are evaluated on every reconstructed
prime. The resulting 685 signatures are distinct and agree exactly with the
registered packed values, so all 234,270 pairs are separated.

Result: PASS.

### 8. Unsupported uniqueness or minimality

The checker evaluates all 5,989 descriptors first admitted at cap 103 and
all eight exits, finding exactly one coordinate that separates the tracked
pair. The incremental minimum is one because zero coordinates preserve the
collision. No minimum is claimed for the full 1,528-coordinate certificate.

Result: PASS.

### 9. Overstating normalization coverage

The checker verifies that the registered constant, duplicate, and normalized
counts partition the raw cap-103 coordinate count. It does not independently
reconstruct all 1,555 normalized masks. This does not weaken the injectivity
conclusion because a semantically verified separating sublist suffices.

Result: PASS with this limitation recorded.

### 10. Extending one row to the whole table

M85 validates M41 only. M46 was rejected as the first minimal target after a
cost audit found roughly 10.88 million construction evaluations. The M50
integrity checker and per-row legacy semantic paths remain necessary for
other rows.

Result: PASS with no table-wide independence claim.

### 11. Finite-to-asymptotic or general-factoring leakage

The proof, experiment, trust model, and bilingual manuscripts retain the
\(m=29\), exact-selector, factor-dependent-promise scope. General classical
polynomial-time factoring remains open.

Result: PASS.

## Verdict

PASS for the bounded M85 deliverable. The checker independently reconstructs
the M41 semantic kernel within its stated trust boundary. The result
strengthens reproducibility but does not promote a mathematical claim or
constitute external review.
