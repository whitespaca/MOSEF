# SRC-008 - Pollard's factorization and primality-testing paper

## Bibliographic record

John M. Pollard, "Theorems on Factorization and Primality Testing,"
*Mathematical Proceedings of the Cambridge Philosophical Society* 76(3),
1974, 521--528. DOI: `10.1017/S0305004100049252`.

- Official metadata and abstract record:
  <https://doi.org/10.1017/S0305004100049252>
- Complete primary-article page images inspected through Daniel J.
  Bernstein's bibliographic mirror:
  <https://cr.yp.to/bib/1974/pollard.html>
- Retrieval and inspection date: 2026-07-31.
- Inspection level: `FULL_ARTICLE`.
- Inspected range: pages 521--528.
- Concatenated SHA-256 of the eight inspected page images, in page order:
  `1305c66f35223daa75bc53852d0352cd2dc70682f931cb8a62cb57820b6d1e8d`.

The official Cambridge record supplied the venue, volume, issue, pages, year,
and DOI. The complete content audit used page images of the published
primary article because the official full text was not openly retrievable.

## Inspected mechanism

Pages 521--526 prove a separate \(N^{1/4+\delta}\)-scale theoretical
factorization result in the paper's radix/Turing-style cost model. That
result is not a polynomial-time theorem in the binary input length.

Pages 526--528 then describe the practical smooth-\(p-1\) method. For a
candidate factor \(q\), the intended favorable form is \(q-1=A\) or \(Ap\),
where \(A\) is supported on primes at most a bound \(L\) and the remaining
prime \(p\), when present, lies between \(L\) and \(M\). The stage-one
procedure chooses one small \(a>1\), raises it by a product of prime powers
bounded by \(L\), and computes a GCD with \(n\). A unit GCD continues to the
second stage. A full collision leads to a smaller bound or backtracking.
The second stage batches a product and, when that product gives a full GCD,
returns to individual terms.

## M83 comparison boundary

Pollard supplies the classical local smooth-\(p-1\) mechanism and explicit
miss/full-collision handling. The inspected paper does **not** state:

- a hereditary promise at every residual factorization node;
- a fresh exact uniform base for every schedule trial;
- the project's \(5/12\) complete-cycle success lower bound;
- almost-sure complete recursive factorization on that promise; or
- expected bit complexity polynomial in the original binary input length.

THM-001 is therefore positioned as a scoped project synthesis around an
established mechanism. The exact theorem formulation was not located in this
source, but that negative observation is not evidence of novelty or priority.

## Repository use and limitations

- Claim family: `THM-001`.
- Paper locations: the related-work sections of
  `paper/focused/promise-factorization-en.tex`,
  `paper/focused/promise-factorization-ko.tex`, `paper/main.tex`, and
  `paper/main-ko.tex`.
- Result classification: established algorithmic background plus a
  scope-difference audit; no imported claim status and no novelty claim.
- This source gives no membership recognizer or density theorem for the
  repository's hereditary promise.
- The theoretical result on pages 521--526 must not be conflated with the
  practical \(p-1\) method on pages 526--528.
