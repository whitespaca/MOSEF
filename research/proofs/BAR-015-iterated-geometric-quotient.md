# BAR-015: An iterated geometric-quotient chain reduces stage by stage

## Claim status

- `DEF-020`: `DEFINITION`.
- `BAR-015`: `PROVED`; two independent reviews passed.
- `REF-016`: `REFUTED`.

The proof is elementary and imports no external theorem beyond the already
proved BAR-013 and BAR-014 identities.

## DEF-020: charged public factor chain

Fix \(N\ge2\), an integer base \(g\), a public depth \(r\ge1\), and public
positive integers \(A_1,\ldots,A_r\). After reducing \(g\) and applying the
direct base-GCD precheck, enter the chain only for a unit base. Define
\[
M_0=1,\qquad M_i=\prod_{j=1}^{i}A_j.
\]
At stage \(i\), retain
\[
L_i=S_{M_{i-1}}(g),\qquad h_i=g^{M_{i-1}},\qquad
Q_i=S_{A_i}(h_i),\qquad U_i=S_{M_i}(g),
\]
and
\[
C_i=h_i-1,\qquad E_i=h_i^{A_i}-1=g^{M_i}-1\pmod N.
\]
The exact stage certificate and chain certificate are
\[
S_{M_i}(X)=S_{M_{i-1}}(X)S_{A_i}(X^{M_{i-1}}),       \tag{1}
\]
\[
S_{M_r}(X)=\prod_{i=1}^{r}S_{A_i}(X^{M_{i-1}}).       \tag{2}
\]

Both divisions at every stage have total semantics. The rational path
attempts \(U_i/L_i\); the composed path attempts \(E_i/C_i\). Each
denominator GCD is classified as a unit, proper factor, or full collision,
and \(Q_i\) remains defined in every case. For \(i>1\), the prefix linkage
\[
L_i=U_{i-1}                                                   \tag{3}
\]
is retained explicitly. The final aggregate is
\[
U_r\equiv\prod_{i=1}^{r}Q_i\pmod N.                           \tag{4}
\]

Let \(\alpha_i=\operatorname{bitlength}(A_i)\) and
\(L=\sum_i\alpha_i\). The accounting charges the encoded base, reduction and
precheck, depth and factor list, all prefix products, three DEF-018 binary
evaluators per stage, every retained residue or formal descriptor, both
division attempts per stage, requested GCDs, the final quotient product, and
extraction.

The compact certificate is the public factor list and uses \(O(L)\) bits
apart from self-delimiting list overhead. Stage \(i\)'s quotient has degree
\[
M_{i-1}(A_i-1)=M_i-M_{i-1}
\]
and \(A_i\) nonzero monomials. Its dense coefficient vector has
\(M_i-M_{i-1}+1\) positions; its sparse list has \(A_i\)
coefficient-index pairs, each with an \(O(\operatorname{bitlength}M_i)\)-bit
index. If an expanded prefix polynomial \(S_{M_i}\) is requested, its dense
coefficient list has \(M_i\) entries. Every requested expanded output is
charged by its exact size.

The model exposes the stage quotients, prefix sums, their two total division
paths, and the final product (4). Arbitrary products of subsets, additions
between stages, unrelated denominators, adaptive factor dependence, other
groups, and general rational or arithmetic circuits remain outside.

## BAR-015

Every DEF-020 chain satisfies:

1. the exact identities (1)--(4);
2. at each stage, if \(\gcd(L_i,N)=1\), rational division returns \(Q_i\)
   and \(\gcd(U_i,N)=\gcd(Q_i,N)\);
3. if \(1<\gcd(L_i,N)<N\), the prefix denominator already returns a proper
   factor, although \(Q_i\) may return a different divisor;
4. if \(\gcd(L_i,N)=N\), then \(h_i\equiv1\pmod N\),
   \(Q_i\equiv A_i\pmod N\), and
   \(\gcd(Q_i,N)=\gcd(A_i,N)\);
5. independently, each \(C_i\) has the BAR-013 unit/proper/full
   trichotomy;
6. if \(\gcd(U_r,N)\) is proper, at least one stage quotient \(Q_i\) has a
   proper GCD, and that stage reduces through items 2--5;
7. construction, residue evaluation, and extraction use
   \(O(rL)\) modular operations plus polynomial overhead in the charged
   base and modulus lengths. Since every \(\alpha_i\ge1\), \(r\le L\), so
   this is polynomial in the descriptor length. Expanded outputs are charged
   separately by their stated slot or pair counts.

Thus neither an individual stage quotient nor the retained final quotient
product creates a proper success outside the charged prefix numerator,
prefix denominator, composed denominator, or public multiplier paths.

## Proof

For a fixed stage \(i\), partition the exponents below \(M_i\) uniquely as
\[
t=M_{i-1}q+s,\qquad 0\le q<A_i,\quad 0\le s<M_{i-1}.
\]
Then
\[
\begin{aligned}
S_{M_i}(X)
 &=\sum_{q=0}^{A_i-1}\sum_{s=0}^{M_{i-1}-1}
   X^{M_{i-1}q+s}\\
 &=S_{M_{i-1}}(X)S_{A_i}(X^{M_{i-1}}),
\end{aligned}
\]
proving (1). Multiplying (1) over the linked prefixes and using
\(S_{M_0}=S_1=1\) proves (2). Evaluation proves
\(U_i\equiv L_iQ_i\), (3), and (4). Applying
\((Y-1)S_{A_i}(Y)=Y^{A_i}-1\) at \(Y=h_i\) gives
\(E_i\equiv C_iQ_i\).

If \(L_i\) is a unit, multiplication by \(L_i\) preserves the GCD with
\(N\), so rational division returns \(Q_i\) and
\(\gcd(U_i,N)=\gcd(Q_i,N)\). If \(L_i\) has a proper GCD, that value is
already a factor. Exact divisor equality is not required and can fail at any
stage inherited from the M19 witness.

If \(L_i\equiv0\pmod N\), then
\[
C_i=h_i-1\equiv(g-1)S_{M_{i-1}}(g)\equiv0\pmod N.
\]
Therefore \(h_i\equiv1\pmod N\),
\(Q_i=S_{A_i}(h_i)\equiv A_i\pmod N\), and its GCD is the public
\(\gcd(A_i,N)\). This proves the rational-denominator trichotomy at every
stage. Applying BAR-013 at base \(h_i\) proves the independent composed
trichotomy for \(C_i\).

For the final product, use integer lifts
\(\widetilde Q_i=S_{A_i}(g^{M_{i-1}})\). Identity (2) gives
\[
\widetilde U_r=\prod_i\widetilde Q_i.
\]
If \(\gcd(U_r,N)\) is proper, some prime divisor of \(N\) has positive
support in the product. Equivalently, the stage GCDs cannot all be one,
because then their product would be a unit modulo \(N\). No stage GCD can be
full either, because then the product GCD would be full. Hence some stage
quotient GCD is proper. Its stage then reduces through the preceding
trichotomy.

The bit length of every prefix product \(M_i\) is at most \(L\). Three
binary evaluators per stage therefore use \(O(L)\) modular operations each,
for \(O(rL)\) total. Prefix multiplication, base reduction, GCDs, inversions,
the final product, and extraction are polynomial in the charged input
lengths. The quotient monomials at stage \(i\) have exponents
\[
0,M_{i-1},\ldots,(A_i-1)M_{i-1},
\]
which proves the degree, sparse count, dense length, and output-bit charges.
This proves BAR-015.

## Refuted statement

`REF-016` states that a DEF-020 iterated chain can create a proper stage or
final-product success unaccounted for by every charged prefix numerator,
proper prefix denominator, composed denominator, and public multiplier.
BAR-015 refutes it only for the exact public factor-chain model above.
