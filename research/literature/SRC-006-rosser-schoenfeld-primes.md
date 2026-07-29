# SRC-006 - Rosser--Schoenfeld explicit prime-counting bounds

## Bibliographic record

J. Barkley Rosser and Lowell Schoenfeld, "Approximate Formulas for Some
Functions of Prime Numbers," *Illinois Journal of Mathematics* 6(1), 1962,
64--94. DOI: `10.1215/ijm/1255631807`.
Authoritative artifact:
`https://projecteuclid.org/journalArticle/Download?urlid=10.1215/ijm/1255631807`.

Primary source inspected: the official Project Euclid article scan.

- Retrieval dates: 2026-07-26 and 2026-07-29.
- Result classification: primary-source audit of an imported explicit bound;
  no novelty claim.
- Inspected range: complete 31-page article scan, with the imported statement
  on printed page 69 (PDF page 6), Theorems 1--3 and their corollaries. The
  2026-07-29 reinspection used an image of the same printed primary-source
  page because the official Project Euclid download returned an Incapsula
  challenge in the current environment.

## Imported \(n\)-th-prime statement

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

## Imported prime-counting statements for M47

Corollary 1 on printed page 69 states, with natural logarithms,

\[
\frac{x}{\log x}<\pi(x)\qquad(17\le x)
\tag{3.5}
\]

and

\[
\pi(x)<1.25506\frac{x}{\log x}\qquad(1<x).
\tag{3.6}
\]

M47 applies these inequalities only at
\[
x=2^{m/2},\qquad x/\sqrt2=2^{(m-1)/2}.
\]
For \(m\ge10\), both source hypotheses hold. Direct integer arithmetic gives
\[
128\cdot50000^2-81\cdot62753^2
=1{,}026{,}940{,}271>0,
\]
so \(1.25506/\sqrt2<8/9\). Therefore the complete balanced-prime
population satisfies
\[
\begin{aligned}
|\mathcal P_m|
&=\pi(2^{m/2})-\pi(2^{(m-1)/2})\\
&>\frac{2^{m/2}}{\log(2^{m/2})}
 \left(1-\frac{1.25506}{\sqrt2}\frac{m}{m-1}\right)\\
&>\frac{2^{m/2}}{81\log(2^{m/2})}
\qquad(m\ge10).
\end{aligned}
\]
The last step uses \(m/(m-1)\le10/9\). This derivation is a repository
consequence, not a statement quoted from the paper.

## Exact limitations

- The imported result supplies an upper bound for the size and construction
  range of \(P_r\); it says nothing about primes of the form \(d\pm1\) for
  divisors \(d\mid P_r\).
- Equations (3.5) and (3.6) count primes in the balanced interval only after
  the displayed endpoint subtraction; they say nothing about DEF-032
  supports or factoring algorithms by themselves.
- It supplies no lower bound on the combined \(p-1/p+1\) hit count of a
  primorial exponent.
- It supplies no promise recognizer, input-density theorem, factoring
  algorithm, or lower bound.
- M11's optimized divisor estimate and channel-disjointness statement are
  self-contained project derivations, not attributed to Rosser--Schoenfeld.
- M47's exact-output support budget and the comparison with DEF-032 are
  self-contained project derivations. The source supplies only the two
  explicit \(\pi(x)\) inequalities under their stated hypotheses.
