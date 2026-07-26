# SRC-005 - Williams's \(p+1\) factoring method

## Bibliographic record

Hugh C. Williams, "A \(p+1\) Method of Factoring," *Mathematics of
Computation* 39(159), July 1982, 225--234.
DOI: `10.1090/S0025-5718-1982-0658227-7`.
Authoritative artifact:
`https://www.ams.org/journals/mcom/1982-39-159/S0025-5718-1982-0658227-7/S0025-5718-1982-0658227-7.pdf`.

Primary source inspected: the official AMS article scan. The scan records
receipt on 1981-03-30 and revision on 1981-09-28.

## Inspected definitions and theorem

Williams defines

\[
U_n(P,Q)=\frac{\alpha^n-\beta^n}{\alpha-\beta},\qquad
V_n(P,Q)=\alpha^n+\beta^n,
\]

where \(\alpha,\beta\) solve \(x^2-Px+Q=0\), with discriminant
\(\Delta=P^2-4Q\). The sequences satisfy

\[
U_{n+1}=PU_n-QU_{n-1},\qquad V_{n+1}=PV_n-QV_{n-1}.
\]

The Lehmer result imported on page 227 assumes an odd prime \(p\),
\(p\nmid Q\), and Legendre symbol \((\Delta/p)=\varepsilon\). For positive
\(m\),

\[
U_{(p-\varepsilon)m}(P,Q)\equiv0\pmod p
\]

and

\[
V_{(p-\varepsilon)m}(P,Q)
\equiv2Q^{m(1-\varepsilon)/2}\pmod p.
\]

The case \(\Delta\equiv0\pmod p\) is outside this statement.

For \(Q=1\), both nondegenerate branches yield a \(V\)-value congruent to
\(2\), but their group orders differ:

- \((\Delta/p)=-1\) is the nonsplit \(p+1\) branch;
- \((\Delta/p)=+1\) is the split \(p-1\) branch.

The first stage assumes \(p+1\mid R\) for a smooth stage-one exponent \(R\)
and the nonsplit discriminant condition. It composes

\[
P_j\equiv V_{r_j}(P_{j-1},1)\pmod N
\]

to obtain \(V_R(P_0,1)\), then computes
\(\gcd(V_R(P_0,1)-2,N)\). Williams requires
\(\gcd(P_0^2-4,N)=1\); a nontrivial proper GCD already factors \(N\), while
a full GCD requires rejecting and reselecting the parameter.

## M5 scope audit

The paper describes the method as analogous to Pollard's \(p-1\) method,
implements both, and reports running \(p-1\) first because it was faster.
Its numerical tables support empirical complementarity only. It makes no
claim that the two methods fail independently. Its explicit independence
assumption concerns repeated choices of \(P_0\) in a heuristic estimate for
obtaining the nonsplit Legendre-symbol branch.

For the M5 conjugate pairing \(P=a+a^{-1}\),

\[
P^2-4=(a-a^{-1})^2.
\]

Thus every nondegenerate odd-prime component is forced into the split branch.
The algebraic correlation result in
`research/proofs/BAR-002-conjugate-channel-correlation.md` is elementary and
is not attributed to Williams.

## Exact limitations

- The imported theorem excludes the zero-discriminant prime component.
- Williams's parameter rejection rule is an algorithmic choice, not proof
  that the later sequence GCD contains no factor. For example,
  \(N=15,P=8,d=1\) has discriminant GCD \(15\) but sequence GCD \(3\).
- The paper does not establish a probability distribution for correlated
  failure between \(p-1\) and \(p+1\).
- No claim here changes the worst-case classical complexity of factoring.
