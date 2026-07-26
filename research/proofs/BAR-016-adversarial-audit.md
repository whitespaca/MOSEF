# Adversarial audit of BAR-016

## Scope

This audit challenges only the exact DEF-021 model and BAR-016 counterexample.
It is not an independent theorem or a claim about general factoring.

## Exact arithmetic reconstruction

For \(N=9\), \(g=2\), factors \((5,5)\), and coefficients \((-1,1)\):

- \(2^5\equiv5\pmod9\) and \(2^{25}\equiv2\pmod9\).
- \(S_5(2)\equiv1+2+4+8+7\equiv4\pmod9\).
- \(S_5(5)\equiv1+5+7+8+4\equiv7\pmod9\).
- The prefix product is \(4\cdot7\equiv1\pmod9\).
- The weighted residues are \(-4\equiv5\) and \(7\), both units.
- Their sum is \(12\equiv3\pmod9\), with GCD \(3\).

The rational prefixes \(1,4\), prefix numerators \(4,1\), composed
denominators \(1,4\), endpoints \(4,1\), public multipliers \(5,5\),
coefficients \(-1,1\), quotients \(4,7\), and weighted residues \(5,7\) all
have GCD one with \(9\). Thus no omitted DEF-020 or DEF-021 component already
contains the proper factor.

## Formal-output reconstruction

Direct subtraction gives
\[
S_5(X^5)-S_5(X)
=-X-X^2-X^3-X^4+X^5+X^{10}+X^{15}+X^{20}.
\]
The constant terms cancel. The eight displayed exponent-coefficient pairs
are exactly the collected sparse output; the degree bound is \(20\), and the
uncollected representation has ten term records. No hidden expansion or
coefficient oracle is used.

## Implementation separation and edge cases

- Python evaluates the compact chain and independently expands the sparse
  polynomial; exhaustive bounded checks found zero disagreements.
- Rust uses bounded `u64` modular arithmetic and signed `i64` coefficients.
- C# independently reconstructs each quotient with `BigInteger`.
- Six canonical vectors produced 12 identical Rust/C# protocol results
  against the Python oracle.
- Tests cover factor one, exact cancellation to a full GCD, an already proper
  component, even moduli, repeated prime powers, invalid alignment, and
  nonunit bases.

## Scope challenge

The witness refutes only the proposed component-to-signed-aggregate
implication. It supplies no factorization-independent schedule that succeeds
on all composites, no success probability or density theorem, and no lower
bound for adaptive coefficients, multiple aggregates, multiplication or
division between aggregates, unrelated bases, other groups, or general
arithmetic circuits. With those boundaries explicit, the audit finds no
remaining defect in BAR-016.
