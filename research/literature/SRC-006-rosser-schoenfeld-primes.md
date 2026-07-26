# SRC-006 - Rosser--Schoenfeld bounds for the \(n\)-th prime

## Bibliographic record

J. Barkley Rosser and Lowell Schoenfeld, "Approximate Formulas for Some
Functions of Prime Numbers," *Illinois Journal of Mathematics* 6(1), 1962,
64--94. DOI: `10.1215/ijm/1255631807`.
Authoritative artifact:
`https://projecteuclid.org/journalArticle/Download?urlid=10.1215/ijm/1255631807`.

Primary source inspected: the official Project Euclid article scan.

- Retrieval date: 2026-07-26.
- Result classification: primary-source audit of an imported explicit bound;
  no novelty claim.
- Inspected range: complete 31-page article scan, with the imported statement
  on printed page 69 (PDF page 6), Theorem 3 and its corollary.

## Imported statement

Let \(p_n\) be the \(n\)-th prime. Equation (3.13), the corollary to
Theorem 3 on printed page 69, states

\[
p_n<n(\log n+\log\log n)\qquad(6\le n),
\]

where the article uses natural logarithms.

M11 uses only the consequence \(p_n=O(n\log n)\). For the first-primes
primorial

\[
P_r=\prod_{j=1}^{r}p_j,
\]

the inspected inequality gives

\[
\log_2 P_r
\le r\log_2 p_r
=O(r\log r).
\]

The matching elementary lower bound does not come from the paper:
\(p_j\ge j+1\), so the final \(\lceil r/2\rceil\) factors alone give
\(\log_2P_r=\Omega(r\log r)\).

## Exact limitations

- The imported result supplies an upper bound for the size and construction
  range of \(P_r\); it says nothing about primes of the form \(d\pm1\) for
  divisors \(d\mid P_r\).
- It supplies no lower bound on the combined \(p-1/p+1\) hit count of a
  primorial exponent.
- It supplies no promise recognizer, input-density theorem, factoring
  algorithm, or lower bound.
- M11's optimized divisor estimate and channel-disjointness statement are
  self-contained project derivations, not attributed to Rosser--Schoenfeld.
