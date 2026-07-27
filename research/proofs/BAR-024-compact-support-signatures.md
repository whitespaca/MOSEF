# BAR-024: compact multi-support signature criterion

## Status

`PROVED` in the exact model below.

## Definition and quantifier order

Fix an input length \(m\). Before the particular input \(N\) is received, a
factorization-independent constructor emits a finite ordered list of public
compact exceptional-cofactor descriptors
\[
\mathcal T_m=(T_{m,1},\ldots,T_{m,r_m}).
\]
Descriptor \(T_{m,j}\) has a total compact modular evaluator and denotes a
nonzero exact integer lift \(z_{m,j}\). The public algorithm may compute
\(z_{m,j}\bmod N\), its GCD with \(N\), and a factor extraction, but it does
not receive a prime factor of \(N\), the factorization of \(z_{m,j}\), or its
prime support.

For a finite population \(\mathcal P_m\) of \(s_m\ge2\) distinct odd primes,
define the analytical signature
\[
\sigma_m(p)=
  \bigl(\mathbf 1_{p\mid z_{m,1}},\ldots,
        \mathbf 1_{p\mid z_{m,r_m}}\bigr)
  \in\{0,1\}^{r_m}.
\]
This is a proof object, not a claimed factorization-free recognizer. The
square-free pair model consists of \(N=pq\) for distinct
\(p,q\in\mathcal P_m\).

The compact ledger charges construction of every descriptor, every modular
operation needed by every compact evaluator, all \(r_m\) GCDs, retained
outputs, and extraction. Listing \(\sigma_m\), enumerating
\(\mathcal P_m\), factoring exact lifts, or emitting support certificates is
not free and is not part of the public algorithm.

## Theorem

Let \(n_u=|\{p\in\mathcal P_m:\sigma_m(p)=u\}|\) for
\(u\in\{0,1\}^{r_m}\). Then:

1. candidate \(j\) gives a proper GCD on \(N=pq\) exactly when the \(j\)-th
   bits of \(\sigma_m(p)\) and \(\sigma_m(q)\) differ;
2. the whole list exposes a proper factor of \(pq\) exactly when
   \(\sigma_m(p)\ne\sigma_m(q)\);
3. the number of failed pairs is exactly
   \[
   F_m=\sum_u\binom{n_u}{2},
   \]
   and the number of successful pairs is
   \[
   \binom{s_m}{2}-F_m;
   \]
4. universal pair separation holds if and only if \(\sigma_m\) is injective;
5. injectivity requires
   \[
   r_m\ge\lceil\log_2s_m\rceil.
   \]
   If every population prime must also have a nonzero signature, then
   \[
   r_m\ge\lceil\log_2(s_m+1)\rceil;
   \]
6. among all assignments of \(s_m\) primes to \(t=2^{r_m}\) signatures, the
   minimum possible failed-pair count is
   \[
   (t-a)\binom b2+a\binom{b+1}{2},
   \qquad s_m=bt+a,\quad0\le a<t.
   \]
   If zero signatures are forbidden, the same formula holds with
   \(t=2^{r_m}-1\).

## Proof

For square-free \(N=pq\),
\[
\gcd(z_{m,j},N)
=p^{\mathbf 1_{p\mid z_{m,j}}}
 q^{\mathbf 1_{q\mid z_{m,j}}}.
\]
Thus equal zero bits give GCD \(1\), equal one bits give the full collision
\(pq\), and unequal bits give exactly one of \(p,q\). This proves parts 1
and 2.

A pair fails for the whole list precisely when its two signatures are equal.
The bucket with signature \(u\) contributes \(\binom{n_u}{2}\) failed pairs.
Summing proves part 3. Every distinct prime pair succeeds precisely when no
bucket contains two primes, which is precisely injectivity and proves part
4.

There are at most \(2^{r_m}\) binary signatures. An injective map from an
\(s_m\)-element population therefore requires \(s_m\le2^{r_m}\), proving
the first lower bound in part 5. If the zero signature is forbidden, only
\(2^{r_m}-1\) cells remain, so
\(s_m\le2^{r_m}-1\), proving the second bound.

For part 6, suppose two occupied buckets have sizes \(x\ge y+2\). Moving one
prime from the first to the second changes their collision contribution by
\[
\binom{x-1}{2}+\binom{y+1}{2}
-\binom x2-\binom y2
=y-x+1<0.
\]
Hence a minimizing assignment has bucket sizes differing by at most one.
Writing \(s_m=bt+a\) yields \(a\) buckets of size \(b+1\) and \(t-a\) of
size \(b\), which gives the stated formula. The same exchange proof applies
after removing the zero bucket.

## Tight abstract construction and its cost boundary

The information bounds are combinatorially tight if prime support can be
materialized with factor knowledge. Assign distinct binary labels to the
population primes and set
\[
z_j=\prod_{\substack{p\in\mathcal P_m\\\text{label}_j(p)=1}}p.
\]
Then divisibility by \(z_j\) reproduces the chosen label coordinate. Labels
\(0,\ldots,s_m-1\) use
\(\lceil\log_2s_m\rceil\) coordinates; labels
\(1,\ldots,s_m\) give nonzero signatures using
\(\lceil\log_2(s_m+1)\rceil\) coordinates.

This construction enumerates the population primes, uses their values, and
materializes products containing them. It is therefore not a compact,
factorization-independent exceptional-cofactor schedule and is not a
factoring algorithm. It only proves tightness of the information bound in
the unrestricted support-assignment abstraction.

## Coverage is not separation

Take population \(\{3,5,7\}\) and candidates \(z_1=15,z_2=7\). Their
signatures are
\[
\sigma(3)=(1,0),\qquad
\sigma(5)=(1,0),\qquad
\sigma(7)=(0,1).
\]
Every prime is covered and the two candidates meet even the nonzero-signature
lower bound
\(\lceil\log_2(3+1)\rceil=2\). Nevertheless, on \(N=3\cdot5=15\),
\[
\gcd(z_1,N)=15,\qquad\gcd(z_2,N)=1.
\]
The duplicate signatures create one failed pair. Thus union coverage plus
the numerical candidate lower bound is not sufficient; actual injectivity
is indispensable.

## Canonical compact prefix

For the M29 family, define the public prefix at input length \(m\) by
\[
\mathcal T_m=(C_2,C_3,\ldots,C_m).
\]
It has \(r_m=m-1\) candidates. Candidate \(C_\ell\) has
\(O(\ell)\)-bit public integers and its M26 binary evaluator uses
\(O(\ell)\) modular composition steps. Consequently the complete prefix has
\(O(m^2)\) descriptor bits and modular steps, plus \(m-1\) GCDs. This is a
genuine polynomial compact schedule.

Its analytical signature is computed for proof and audit from BAR-023:
for \(p>7\), coordinate \(\ell\) is one exactly when
\[
2^{3\cdot2^\ell+5}\equiv-3\pmod p,
\]
with the proved special rules for \(2,3,5,7\). The finite EXP-0029 audit
shows that this particular prefix is noninjective at every registered input
length \(9\le m\le40\). This observation is empirical and does not prove
noninjectivity at later lengths or for other polynomial compact schedules.

## Recognition boundary

Injectivity is an exact semantic condition once the population primes and
candidate supports are known. The public algorithm does not know those
primes. BAR-024 supplies neither:

- a factorization-free certificate that the signatures are injective;
- a constructor for compact descriptors realizing prescribed labels;
- an asymptotic lower bound for balanced-prime population size;
- a density theorem for the M29 congruence supports.

## Adversarial review

The proof and implementation were checked against:

- all-unit and full-collision coordinates;
- duplicate nonzero signatures despite complete union coverage;
- insufficient candidate counts and the exact balanced-bucket collision
  minimum;
- empty and zero-signature boundary cases;
- repeated candidate coordinates, which add no distinguishing information;
- special denominator primes \(2,3,5,7\);
- the distinction between an analytical signature oracle and public compact
  modular evaluation;
- the distinction between a finite prefix obstruction and a theorem about
  all schedules;
- square-free distinct-prime scope versus repeated-prime inputs.

No step assumes a general classical polynomial-time factoring algorithm or a
general arithmetic-circuit lower bound.
