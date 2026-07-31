# THM-029 - Public coverer-graph construction and explicit-size boundary

## Status and scope

`THM-029` is an unconditional finite construction theorem. It separates
three objects that M95--M99 had deliberately kept distinct:

1. a public finite population and public binary-coordinate families;
2. a certificate proving the exact baseline collision partition; and
3. the complete incremental coverage types, coverer graph, and public OCT
   cap derived from those objects.

No hidden factor of an integer is an input to the construction. The theorem
is polynomial in the complete explicit population, coordinate families, and
certificate. It does not say that those objects have bit-polynomial size in
the original integer length \(m\).

## DEF-056: public collision-to-graph contract

Let \(X\) be a finite public labeled set. Let
\(\mathcal H_0\subseteq\mathcal H_1\) be finite public families of binary
coordinates \(h:X\to\{0,1\}\), each with an exact evaluation algorithm.
A **public collision-completeness certificate** consists of:

- a public subfamily \(S\subseteq\mathcal H_0\);
- pairwise-disjoint nontrivial blocks
  \(\Pi=\{B_1,\ldots,B_s\}\); and
- the following two verifiable conditions:
  1. the equal-\(S\)-signature classes are exactly the listed blocks and
     singletons;
  2. every \(h\in\mathcal H_0\) is constant on every \(B_i\).

The tracked set is \(B=\bigcup_iB_i\), with \(b=|B|\), and the unresolved
pair universe is

\[
U(\Pi)=\bigcup_i\binom{B_i}{2},\qquad q=|U(\Pi)|.
\]

For every newly admitted coordinate
\(h\in\mathcal H_1\setminus\mathcal H_0\), form its coverage set

\[
C(h)=\{\{x,y\}\in U(\Pi):h(x)\ne h(y)\}.
\]

Discard the zero set and deduplicate equal sets. The result \(T\) is the
complete nonzero coverage-type family. Its coverer columns
\[
D(u)=\{A\in T:u\in A\}
\]
give the looped coverer graph whenever every column has rank at most two.
Forced loops are removed before applying an OCT procedure.

An OCT cap is **public** only when it is a fixed function of public inputs,
not a supplied per-instance set or integer chosen after seeing the graph. In
the M100 frozen application the schedule is
\[
k(m)=\lceil\log_2m\rceil.
\]

## Exact collision reconstruction

**Lemma 1.** The nontrivial equivalence classes of equal
\(\mathcal H_0\)-signature are exactly \(B_1,\ldots,B_s\).

**Proof.** Because \(S\subseteq\mathcal H_0\), equality on all of
\(\mathcal H_0\) implies equality on \(S\). Condition 1 therefore confines
every nontrivial \(\mathcal H_0\)-class to one listed \(B_i\). Condition 2
states that all coordinates in \(\mathcal H_0\) are constant on \(B_i\), so
each whole block is an \(\mathcal H_0\)-class. The two inclusions agree.
\(\square\)

The first direction is the selected-coordinate confinement used by M91. The
second is its exhaustive raw-selector persistence check. A digest of a
claimed block list supplies neither direction.

## Factor-independent graph construction

**Theorem 1.** Under DEF-056, the complete incremental type family \(T\),
every coverer column \(D(u)\), the looped coverer graph when its rank is at
most two, and the residual loopless graph are constructible without access
to a factorization of any integer.

**Proof.** Lemma 1 reconstructs the exact baseline partition using only
public coordinate evaluations. The algorithm enumerates every member of
\(\mathcal H_1\setminus\mathcal H_0\), evaluates it on the public tracked
labels, and computes its pair coverage by bit inequality. Exhaustive
enumeration followed by removal of zero and duplicate masks gives exactly
the realized nonzero coverage types, not a subfamily. Scanning every
type/pair incidence constructs every \(D(u)\). A singleton column identifies
a forced loop endpoint, and a two-element column identifies an ordinary
edge. Deleting the forced endpoints and their incident edges is purely
combinatorial. None of these operations queries the factors of an input
integer. \(\square\)

This theorem corrects the informal phrase “factor-dependent graph” when
applied to the frozen balanced-prime population. The point labels are primes,
but they are publicly enumerable candidate labels; they are not supplied as
the unknown factors of a particular input \(N\).

## Explicit-size cost

Let:

- \(P\) charge enumeration and representation of \(X\);
- \(n=|X|\);
- \(C=|S|\);
- \(D_0\) count public baseline descriptors checked on the candidate blocks;
- \(D_1\) count newly admitted public descriptors;
- \(E\) bound one selected-coordinate evaluation or one full eight-exit
  descriptor evaluation (a constant-factor distinction);
- \(t=|T|\); and
- \(k\) be the public OCT cap.

Selected-signature confinement costs \(O(CnE)\).
Baseline persistence costs \(O(D_0bE)\), and complete new-type enumeration
costs \(O(D_1bE)\). Pattern and coverer reconstruction costs
\(O(t(b+q))\). With THM-028, capped OCT discovery has conservative cost
\(O(3^kkt(t+q))\), suppressing the harmless \(k+1\) normalization.
Thus the composed registered route has the explicit-size bound

\[
O\!\left(
P+CnE+D_0bE+D_1bE+t(b+q)+3^kkt(t+q)
\right).
\]

This is polynomial in the expanded objects when \(k=O(\log m)\) and all
expanded parameters are polynomial in \(m\). Those hypotheses are separate;
the theorem does not infer them from factor independence.

## Registered balanced-population boundary

The M91/M100 path takes
\[
X=\mathcal P_m
=\{p\text{ prime}:2^{m-1}\le p^2<2^m\}.
\]
BAR-041 proves from the inspected Rosser--Schoenfeld bounds that
\[
|\mathcal P_m|=\Omega(2^{m/2}/m).
\]
The registered constructor explicitly enumerates this population, and its
selected-coordinate gate evaluates \(C\) coordinates on every population
point. Consequently this particular public route is not polynomial in
\(m\), even though it is factor-independent and polynomial in its explicit
population/certificate representation. This is an accounting result about
the registered algorithm, not a lower bound against every possible compact
proof of type completeness.

## Hash-only counterexample

`REF-069` claimed that a recomputed digest of a compact type/graph payload
could replace semantic completeness. Take universe
\(U=\{u_0,u_1\}\) and a claimed family
\[
T_0=\{u_0\},\qquad T_1=\{u_1\}.
\]
The claimed minimum is two, and any digest can bind those bytes exactly.
If the realized but omitted type is
\[
T_2=\{u_0,u_1\},
\]
the actual minimum is one. Recomputing the digest after serializing the
incomplete claim changes no fact about the omission. Therefore hashing
provides byte identity, not semantic exhaustiveness. This refutes REF-069
without relying on a collision attack against SHA-256.

## Frozen M100 application

The implementation derives every baseline block before opening the M95
comparison graph. For the nine M92 rows, public selected coordinates confine
the blocks and every raw baseline descriptor is checked for persistence. For
the ten M93 rows, the full raw baseline family itself is the selected family
and refines the public population to its exact nontrivial classes. Only after
types, columns, forced loops, and residual edges have been constructed are
they compared to M95 modulo bucket and type ordering.

For all nineteen M95 repairs at \(16\le m\le34\), M100:

- enumerates all 12,209 public population entries in the nineteen rows;
- uses 421,541 baseline public coordinates and 39,426,052 selected or raw
  primitive evaluations;
- performs 5,253,406 separate descriptor/point persistence evaluations,
  or 42,027,248 primitive tests, on the selected-subfamily rows;
- evaluates 152,879 newly admitted descriptors on 55 tracked points,
  totaling 581,361 descriptor/prime evaluations and 4,650,888 primitive
  coordinate tests;
- materializes the 19 derived block families, exactly 37 complete nonzero
  coverage types, and all 64 coverer columns in the M100 schema;
- removes 30 forced types, leaving only \(K_3\) and \(K_4\), with seven
  residual vertices and nine edges in aggregate; and
- derives \(k(m)=\lceil\log_2m\rceil\) from \(m\) alone. The two nonzero
  exact OCT numbers are one and two, so all nineteen frozen graphs pass.

The cap result is `EMPIRICAL` on the frozen window. No theorem states that
future graphs from the grammar have logarithmic OCT number.

## Remaining original-goal boundary

The construction is offline over a public balanced-prime population.
Applying it to a particular input still requires the applicable restricted
input promise and does not recognize arbitrary factor structure. The
exponential population route, absence of an asymptotic logarithmic OCT
theorem, and lack of a general promise recognizer prevent composition into a
classical polynomial-time algorithm for arbitrary integers. The original
general factoring goal remains `OPEN`.
