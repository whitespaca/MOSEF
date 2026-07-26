# SRC-004 - Umans and Wang divisor conjecture

- Retrieval date: 2026-07-26.
- Citation: Chris Umans and Siki Wang, "A number-theoretic conjecture implying
  faster algorithms for polynomial factorization and integer factorization,"
  arXiv:2511.10851v1, 13 November 2025.
- Authoritative record: `https://arxiv.org/abs/2511.10851v1`.
- Inspected artifact: official arXiv v1 HTML, including Sections 3, 5, and 6.
- Classification: conjectural structured divisor-cover constructions with
  conditional polynomial- and integer-factorization consequences.

## Exact imported content

Definition 3.1 calls a set \(A\) an \(n\)-divisor set when every
\(i\in\{1,\ldots,n\}\) divides at least one \(a\in A\). Conjectures 3.2 and
3.3 ask for such an \(A\) represented as the pairwise difference set
\(S-T\), with simultaneous cardinality, magnitude, and generalized-arithmetic-
progression structure bounds. These are conjectures, not available
constructions.

Proposition 3.4 shows how an arithmetic-progression divisor set with at most
\(n^{2\beta}\) elements can be represented through two sets of about
\(n^\beta\) elements. The trivial interval divisor set therefore recovers the
baby-step/giant-step boundary \(\beta=1/2\); it does not establish the
conjectured improved parameters.

For integer factorization, Conjecture 5.1 adds a prefactoring requirement:
the prime factorization of each difference \(s-t\) must be output within the
stated time. Theorem 5.2 then assumes:

1. every integer at most \(\lfloor\sqrt N\rfloor\) divides the product of the
   registered integers \(A_i\);
2. interval products of the \(A_i\) can be evaluated efficiently modulo a
   divisor;
3. each \(A_i\) can be factored efficiently.

Its recursive GCD procedure isolates the small prime factors of \(N\) among
the \(A_i\). Theorem 5.5 is conditional on the Strong Prefactored Divisor
Conjecture and gives a deterministic
\(\widetilde O(N^{\max(\alpha,\beta)/2+o(1)})\) algorithm. This is exponential
in the binary input length and is not a polynomial-time MOSEF result.

Section 6 explicitly treats even the arithmetic-progression version as open
and identifies primes and balanced two-factor composites as difficult
coverage cases.

## Source-text audit

The following are limitations or textual mismatches in the inspected v1, not
claims that its conjectures are false:

1. Conjectures 3.2, 3.3, and 5.1 assert existence for infinitely many \(n\)
   and do not supply a uniform constructor for \(S,T\). The factorization
   theorems are phrased for arbitrary input sizes. Applying the existential
   statements as uniform algorithms therefore needs an additional
   quantifier/construction argument that is not explicit in the inspected
   text.
2. Lemmas 5.3 and 5.4 state their interval-product routines for \(d\le n\),
   while Theorem 5.2 requests the same capability for \(d\le N\), and its
   recursion can begin with a modulus larger than \(n=\lfloor\sqrt N\rfloor\).
   The elementary product algorithms may extend, but the written hypotheses
   do not match verbatim.
3. The conjectures describe \(S,T\) as positive-integer sets, yet a directed
   difference \(S-T\) can contain zero or negative values; Proposition 3.4
   also uses a set containing zero. Conjecture 5.1 asks for the prime
   factorization of every difference. A sign/zero convention is therefore
   required before the prefactoring condition is literally well-defined.
4. The sentence immediately preceding Theorem 5.5 calls the resulting
   algorithm unconditional, while the theorem itself explicitly assumes the
   Strong Prefactored Divisor Conjecture. This note follows the theorem
   statement and classifies the bound as conditional.

These discrepancies prevent this repository from treating the paper as a
discharged unconditional factoring theorem. They do not affect the internal
BAR-001 counterexample, which uses only the source's divisor-property
definition.

## Scope boundary for M4

The paper's divisor property guarantees that each target integer divides some
difference. Its polynomial-factor application removes all irreducible factors
whose degrees divide that difference. Its integer-factor application instead
uses divisibility of actual prime factors into a product of prefactored
differences.

Neither application states that a difference divisible by one multiplicative
order must fail to be divisible by another. Therefore the source supports the
M4 divisor-cover definition and its construction costs, but it does not
support an inference from divisor coverage to MOSEF order separation. That
extra implication must be proved separately or refuted.

## Imported use

- `EXT-003`: exact source statement and conditional scope.
- `BAR-001`: motivates the divisor-cover premise whose separation gap is
  analyzed internally.
- Manuscript section on divisor coverage versus order separation.
