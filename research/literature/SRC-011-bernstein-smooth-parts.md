# SRC-011 - Bernstein's batch smooth-part algorithm

## Bibliographic record

Daniel J. Bernstein, "How to Find Smooth Parts of Integers," author draft,
10 May 2004. Permanent document ID:
`201a045d5bb24f43f0bd0d97fcf5355a`.

- Author-hosted primary manuscript:
  <https://cr.yp.to/factorization/smoothparts-20040510.pdf>
- Retrieval and inspection date: 2026-07-31.
- Inspection level: `FULL_ARTICLE`.
- Inspected range: complete seven-page draft, especially Algorithm 2.1 and
  Theorems 2.2--2.3 on pages 3--4.
- Retrieved PDF SHA-256:
  `2ef7aa60f8133ec1125bac4a39498285b626c0f553571fb00385822377facda7`.

## Inspected result

Given a finite set \(P\) of primes and a finite sequence \(S\) of positive
integers, Algorithm 2.1:

1. forms the product of the primes using a product tree;
2. reduces that product modulo all inputs using a remainder tree;
3. raises each remainder by repeated squaring to a sufficient power; and
4. takes one GCD per input.

Theorem 2.2 proves that each output is the largest \(P\)-smooth divisor of
the corresponding input. Theorem 2.3 gives time
\(O(b(\log b)^2\log\log b)\), where \(b\) is the total input bit count. The
abstract states the softer \(b(\log b)^{2+o(1)}\) bound. Page 4 also places
product/remainder-tree batch factorization in an earlier algorithmic
history.

## M83 comparison boundary

This source establishes product trees, remainder trees, repeated powering,
and per-item GCD as charged batch-evaluation mechanisms. It assumes a given
prime set and input sequence. It does not:

- construct a universal factor-independent separating selector;
- show that a product of signed candidate lifts preserves individual GCD
  semantics;
- prove injectivity on any balanced-prime population; or
- supply the selector-specific support/span barriers BAR-041--BAR-046.

The repository therefore treats batch trees as known evaluation machinery,
not as evidence for separator coverage or aggregation soundness.

## Repository use and limitations

- Claim families: contextual use for `BAR-024`, `THM-004`, `THM-005`,
  `THM-014`, `THM-019`, and `BAR-041`--`BAR-046`.
- Paper locations: the related-work sections of the finite focused paper
  pair and both archival manuscripts.
- Result classification: established evaluation background; no imported
  selector theorem and no novelty claim.
- The inspected item is explicitly a draft. Its permanent ID, date, and
  author-hosted checksum are recorded rather than representing it as a final
  journal publication.
