# M91 - Table-wide clean-room semantic certificate

## Status and scope

This milestone supplies one standard-library-only semantic checker for all 26
frozen finite rows \(9\le m\le34\). It strengthens the executable evidence
behind THM-004--THM-019 and BAR-026--BAR-040 without changing any theorem
status or range.

The result is a reproducible computer-assisted validation of one exact
selector family and 26 finite balanced-prime populations. It does not
recognize the factor-dependent promise, prove a threshold for \(m>34\),
establish an asymptotic rate, minimize over other selector families, or solve
general classical polynomial-time factoring.

## Clean-room boundary

`scripts/check_m91_all_rows_semantic_certificate.py` has 987 lines and imports
only the Python standard library. It does not import:

- an M31--M50 generator;
- `python/mosef_reference`;
- an earlier M85/M86 checker;
- a differential verifier; or
- a repository serialization or arithmetic helper.

An AST regression test enforces the import set and the 1,000-line source
budget. The checker hard-codes the 26-to-16 source-path map but obtains caps,
populations, certificates, and repair records from the frozen artifacts. It
independently verifies all 16 file digests registered by M50.

## Shared mathematical reconstruction

For every input length, the checker independently sieves

\[
 \mathcal P_m=\{p\text{ prime}:2^{m-1}\le p^2<2^m\}.
\]

For cap \(L\), it streams the public descriptor grammar

\[
\begin{aligned}
i=4 &: A\equiv B\equiv3\pmod4,\quad A\ne B,\\
i=6 &: A\equiv5\pmod6,\quad B\equiv3\pmod6,
\end{aligned}
\qquad 2\le A,B,g\le L.
\]

If \(n_4,n_{6,5},n_{6,3}\) count the three congruence classes in
\([2,L]\), the independently evaluated descriptor count is

\[
 (L-1)\bigl(n_4(n_4-1)+n_{6,5}n_{6,3}\bigr).
\]

Every selected source has the canonical form
`family:A:B:g:kind`. The checker evaluates the same eight publicly defined
primitive exits as the theorem:

1. base;
2. first geometric stage;
3. second geometric stage;
4. first public bound;
5. second public bound;
6. direct cyclotomic value;
7. cyclotomic/cofactor resultant;
8. cofactor.

For \(S_k(x)=1+x+\cdots+x^{k-1}\), it uses the finite-field formula

\[
 S_k(x)=
 \begin{cases}
 k,&x=1,\\
 (x^k-1)(x-1)^{-1},&x\ne1.
 \end{cases}
\]

The cofactor formula includes the simple-root derivative branch from M85, so
the implementation is total at valid small cyclotomic roots. A regression
test compares that branch with the exact integer quotient for
\((\Phi_4,A,B,g,p)=(\Phi_4,3,7,2,5)\).

## Streaming certificate invariant

For selected sources \((d_j,k_j)\), the checker retains one integer
\(\sigma(p)\) per population prime. Processing source \(j\) sets bit \(j\)
exactly when the requested primitive exit is nonzero modulo \(p\). Induction
on \(j\) gives

\[
 \sigma(p)=\sum_j
 \mathbf1[h(d_j,k_j,p)\ne0]2^j.
\]

Thus the exact registered packed signatures are reconstructed without
materializing a prime-by-coordinate matrix. Across all 26 rows this performs
28,245,185 selected coordinate/prime evaluations for 17,515 coordinates and
12,245 population entries. Every reconstructed signature list equals the
frozen list and is injective.

Because every selected certificate source belongs to the full public
selector, injectivity of the subcertificate implies injectivity of the full
selector at the registered cap.

## Exact predecessor collisions

The predecessor obligations split into two verified cases.

For \(16\le m\le25\), the checker streams every descriptor at
\(L_m^\star-1\) and repeatedly refines the complete population partition.
Singleton classes are safely discarded because later coordinates cannot
merge classes. The final nontrivial classes agree exactly with the frozen
M50 predecessor buckets.

For \(26\le m\le34\), masking later selected columns from the injective
subcertificate gives at most the registered predecessor buckets. The checker
then evaluates every raw predecessor descriptor on every prime in those
buckets and proves that none splits. Therefore the complete raw selector has
at least those collisions. The upper and lower directions establish exact
equality.

The selector family is nested in \(L\). Hence noninjectivity at
\(L_m^\star-1\) implies noninjectivity at every smaller admissible cap, while
the reconstructed certificate proves injectivity at \(L_m^\star\). This
establishes the registered family-relative finite minimum, not a minimum over
other selectors.

## Certified incremental repair

Let the baseline partition have nontrivial buckets \(B_1,\ldots,B_s\).
Create one universe element for every unordered pair inside a bucket. A new
binary coordinate covers exactly the pairs on which its bits differ.
Therefore a set of new coordinates refines every bucket to singletons if and
only if its coverage sets cover the pair universe. The exact minimum
incremental repair size is consequently the minimum set-cover cardinality for
this finite pair universe.

The checker enumerates every descriptor newly admitted between the registered
baseline and repair caps, evaluates all eight primitive coordinates on the
tracked primes, deduplicates their pair-coverage masks, and solves the exact
finite cover by dynamic programming.

For \(m=26\) and \(29\le m\le34\), the baseline is the adjacent predecessor
cap. For \(m=27\) and \(m=28\), the published five-coordinate claim instead
starts from the explicitly public cap-72 and cap-88 six-prime buckets. The
checker treats these two baselines separately rather than silently replacing
them with caps 86 and 103. It obtains exactly the registered minima:

\[
 (2,5,5,1,2,1,1,1,1)
\]

for \(m=26,\ldots,34\).

## Result

The complete execution reconstructs:

- 26 rows bound to 16 frozen source artifacts;
- 12,245 population entries;
- 17,515 selected certificate coordinates;
- 28,245,185 selected coordinate/prime evaluations; and
- 7,520,669 raw descriptor-mask evaluations.

The measured run completed in 155.31 seconds with a 29.15 MiB peak working
set, within the declared reviewer budget of 1,000 source lines, 300 seconds,
and 128 MiB. Eleven tests cover the full result, import and size boundaries,
descriptor and population endpoints, a simple-root quotient, and rehashed
mutations of signatures, predecessor buckets, repair patterns, source paths,
and M50 cap projection.

This is stronger executable evidence for the frozen finite theorem, not
formal proof-assistant verification or external peer review.
