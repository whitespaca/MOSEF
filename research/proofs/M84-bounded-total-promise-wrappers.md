# M84 - Bounded total wrappers for the hereditary promise algorithms

Status: `PROVED` as a bounded corollary of `THM-001` and `THM-002`, after
exact branch tests and adversarial recursion review.

## Public result semantics

Fix valid public schedule functions \(B(k),R(k)\) from `DEF-004` or `DEF-007`
and a positive integer budget \(s\). At every randomized composite node, the
bounded wrapper executes at most \(s\) complete schedule cycles. Its only
public outcomes are:

- `FACTORED(factors)`, where `factors` is a complete sorted list of primes
  whose product is the input; or
- `UNRESOLVED`, which means only that one local cycle budget was exhausted.

The implementation may retain the unresolved divisor for diagnostics, but it
returns no partial factor list. `UNRESOLVED` is not a primality result, a
promise-membership result, or evidence that no separator exists.

Both wrappers first recognize prime inputs and exact maximal perfect powers.
They split an even composite by the verified factor \(2\). The remaining
odd composite non-perfect-power nodes use either:

1. the fresh-residue \(p-1\) cycle from `THM-001`; or
2. the fresh-parameter nonsplit Lucas \(p+1\) cycle from `THM-002`.

Every candidate factor is accepted only after checking
\(1<h<K\) and \(h\mid K\).

## Totality and no-wrong-factor theorem

For every positive input \(N\), every valid public schedule pair, every
positive finite budget \(s\), and every stream of sampler outputs, each
bounded wrapper terminates and returns exactly one of the two public
outcomes. Whenever it returns `FACTORED`, the factors are prime and their
product is exactly \(N\).

### Proof

Every schedule cycle and candidate loop has a declared finite bound. Prime,
perfect-power, even-factor, proper-factor, and exhausted-budget branches are
therefore individually total. A proper split replaces \(K\) by two strictly
smaller positive divisors. Exact maximal-perfect-power preprocessing replaces
\(K=b^e\) by \(b<K\) and restores the multiplicity \(e\) only after the base
has been completely factored. Thus recursion terminates by strong induction
on \(K\).

Prime leaves are accepted only by an exact primality decision. A
perfect-power node repeats an already verified prime factorization of its
base. An even node contributes the verified prime factor \(2\). A randomized
node recurses only after verifying a proper divisor and its exact complement.
The induction hypothesis therefore proves primality and product equality for
every `FACTORED` result. If any child is unresolved, the wrapper returns
`UNRESOLVED` and discards partial factors, so it cannot expose an incomplete
list as a complete factorization. \(\square\)

The Python module is a small exact semantic reference. Its trial-division
primality oracle is not the polynomial-time primality algorithm assumed by
the theorem.

## Exact on-promise local tails

Condition on reaching a composite non-perfect-power node \(K\) satisfying
the corresponding hereditary promise and on the entire preceding execution
history.

For the semismooth \(p-1\) wrapper, one witness trial in every complete cycle
succeeds with conditional probability at least \(5/12\), by `THM-001`.
Every cycle uses a fresh sample. Hence

\[
 \Pr[\text{local `UNRESOLVED' after \(s\) cycles}\mid\text{history}]
 \le \left(\frac7{12}\right)^s.                    \tag{1}
\]

For the nonsplit Lucas \(p+1\) wrapper, the corresponding conditional
success probability is at least \(1/12\), by `THM-002`. Therefore

\[
 \Pr[\text{local `UNRESOLVED' after \(s\) cycles}\mid\text{history}]
 \le \left(\frac{11}{12}\right)^s.                 \tag{2}
\]

These are local node bounds. They do not assert that an arbitrary
outside-promise input has either success probability.

## Complete-factorization union bound

Let \(m=\operatorname{bitlength}(N)\). A binary split tree has fewer than
\(2m\) nodes because the number of prime leaves counted with multiplicity is
at most \(m\). Maximal-perfect-power preprocessing cannot occur at two
consecutive unary nodes, so charging every unary node to the following
binary-tree node gives fewer than \(4m\) total invocations. Deterministic
even splits are ordinary binary nodes and do not change this count.

Index randomized composite nodes by their visitation order. Conditional on
reaching any such node, (1) or (2) bounds the probability that its local
budget fails. A union bound over fewer than \(4m\) possible positions gives

\[
\Pr[\text{complete wrapper returns `UNRESOLVED'}]
\le
\min\left\{1,\;4m\left(\frac7{12}\right)^s\right\} \tag{3}
\]

on the hereditary semismooth promise, and

\[
\Pr[\text{complete wrapper returns `UNRESOLVED'}]
\le
\min\left\{1,\;4m\left(\frac{11}{12}\right)^s\right\} \tag{4}
\]

on the hereditary nonsplit Lucas promise. This argument does not assume that
different recursive nodes are mutually independent; the conditional local
tail is sufficient.

## Cost and recognition scope

With deterministic polynomial-time primality and exact perfect-power
preprocessing, one local cycle has the bit cost already charged in
`THM-001` or `THM-002`. The bounded wrapper costs \(O(s)\) such cycles per
randomized node. It is polynomial in \(m\) whenever the public schedule
functions and \(s\) are polynomially bounded in \(m\); a fixed \(s\) is the
main finite-budget case.

Neither wrapper recognizes its hereditary promise. Equations (1)--(4) are
conditional guarantees for inputs already in the declared class. On every
other input, totality and no-wrong-factor correctness still hold, but
`UNRESOLVED` may occur with arbitrary probability. Thus M84 supplies no
general classical polynomial-time factoring theorem.
