# BAR-064: Standard bit length and exact migration boundary

Status: `PROVED`

## Definitions

For every positive integer \(N\), the standard binary input length is

\[
n(N)=\operatorname{bitlength}(N)
=\lfloor\log_2N\rfloor+1
=\lceil\log_2(N+1)\rceil .
\]

For the sole purpose of auditing the former repository wording, write

\[
\ell_0(N)=\lceil\log_2N\rceil .
\]

All algorithmic complexity and all length-indexed public constructors now use
\(n(N)\). The symbol \(\ell_0\) is not an alternative complexity convention.

## Exact discrepancy theorem

For every \(N\ge1\),

\[
n(N)-\ell_0(N)=
\begin{cases}
1,&N\text{ is a power of two},\\
0,&N\text{ is not a power of two}.
\end{cases}
\]

### Proof

There is a unique integer \(e\ge0\) with
\(2^e\le N<2^{e+1}\). Therefore \(n(N)=e+1\). If \(N=2^e\), then
\(\ell_0(N)=e\). If \(2^e<N<2^{e+1}\), then
\(\ell_0(N)=e+1\). These are the only cases. \(\square\)

Thus the former statement that \(\lceil\log_2N\rceil\) is the binary bit
length is refuted by every \(N=2^e\), including \(N=1\). The two quantities
differ by at most one, so replacing the former parameter does not change a
polynomial-versus-superpolynomial asymptotic classification. It does change
exact length indices and rejection-sampling endpoints, and therefore cannot
be left as an informal convention.

## Effect on exact project results

### Balanced odd-semiprime certificates

The finite selector population is

\[
\mathcal P_n=\{p\text{ prime}:2^{n-1}\le p^2<2^n\}.
\]

For every \(p,q\in\mathcal P_n\),
\[
2^{n-1}\le pq<2^n.
\]
Every such product is odd and greater than one, hence is not a power of two.
The discrepancy theorem gives
\[
\operatorname{bitlength}(pq)=\ell_0(pq)=n.
\]
Consequently the frozen M31--M46 selector certificates and the 26-row M50
summary for \(9\le n\le34\) retain exactly the same populations, signatures,
thresholds, predecessor collisions, and hashes. This preservation is a
property of the odd balanced domain, not permission to retain the former
definition elsewhere.

### Prime powers and recursive algorithms

Odd prime powers are not powers of two and keep their former exact index.
Inputs \(2^e\) move from legacy index \(e\) to standard bit length \(e+1\).
The existing complete-factorization wrappers already apply exact
perfect-power preprocessing before a promise splitter, so the mathematical
success proofs on residual non-perfect-powers are unchanged. Their local and
global complexity parameters, random-bit samplers, and public schedules must
nevertheless be stated using the standard bit length.

### Implementation audit

The Python population path checks integer products with `int.bit_length()`;
the Rust verifier uses the word width minus `leading_zeros`; and the C#
verifier uses `BigInteger.GetBitLength()`. These are standard bit-length
operations. EXP-0059 independently reconstructs their finite boundary,
recounts every M50 population, and verifies that no frozen selector artifact
changes.

## Scope

BAR-064 repairs an exact definition and proves the migration boundary. It
does not construct a new separator, recognize either hereditary promise,
extend a finite selector certificate, prove UCSS, or solve general classical
polynomial-time factoring.
