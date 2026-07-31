# THM-022 - Subset-obstruction and cardinality repair certificates

## Status and scope

`THM-022` is an unconditional finite combinatorial theorem extending
`THM-021`. It supplies two lower-certificate forms when a minimum pair cover
does not have one private pair per selected type:

1. a bucket-cardinality lower bound; and
2. an explicit uncovered universe element for every type subset of size one
   below the proposed minimum.

The theorem assumes that the declared coverage-type set is complete. The M93
application independently reconstructs that complete finite set from the
public descriptor grammar and the frozen M50 rows. No statement here supplies
a factor-promise recognizer, a result beyond input length 34, an asymptotic
selector law, or a general classical polynomial-time factoring algorithm.

## DEF-049: lower-witness portfolio

Use the repair instance of `DEF-048`. Let \(U\) be its unresolved pair
universe, let \(T\) be the complete set of distinct nonzero coverage types,
and let \(t=|T|\). A proposed exact repair certificate of size \(k\) contains:

- an **upper witness** \(W\subseteq T\), \(|W|=k\), whose union is \(U\); and
- one of the following lower witnesses:
  - a `private_pairs` witness as in `THM-021`;
  - a `cardinality` witness exhibiting a block of size \(b_{\max}\) with
    \(\lceil\log_2 b_{\max}\rceil=k\); or
  - a `subset_obstructions` witness that, for every
    \(S\in\binom{T}{k-1}\), gives a pair
    \(u_S\in U\setminus\bigcup_{a\in S}a\).

The type list must be complete for the private-pair and subset-obstruction
lower directions. The cardinality lower bound is independent of the available
type family.

## Cardinality lower certificate

**Lemma 1.** If a block has \(b_{\max}\) points, every binary-coordinate repair
uses at least \(\lceil\log_2 b_{\max}\rceil\) coordinates.

**Proof.** With \(r\) binary coordinates, the points in one original block
receive at most \(2^r\) distinct signatures. Singleton refinement of a
\(b_{\max}\)-point block therefore requires
\(2^r\ge b_{\max}\), hence
\(r\ge\lceil\log_2 b_{\max}\rceil\). \(\square\)

Together with a covering upper witness of the same size, this proves the exact
repair number.

## Subset-obstruction exact-minimum certificate

**Theorem 2.** Suppose \(W\subseteq T\) is a \(k\)-type cover of \(U\), and for
every \(S\in\binom{T}{k-1}\) an explicitly recorded
\(u_S\in U\setminus\bigcup_{a\in S}a\) exists. Then the repair number is
exactly \(k\).

**Proof.** The upper witness gives a repair of size \(k\). The obstruction
entries prove that no \((k-1)\)-element subset of \(T\) covers \(U\).
If a smaller cover \(R\) of size \(r<k-1\) existed, the \(k\) distinct types in
the upper witness imply \(t\ge k\), so \(R\) could be extended by distinct
types to some \(S\in\binom{T}{k-1}\). Coverage is monotone under adding types,
so \(S\) would cover \(U\), contradicting its recorded uncovered pair.
Therefore every cover has size at least \(k\), and the matching upper witness
proves equality. \(\square\)

This theorem is more general than the private-pair criterion. A private pair
forces one specified type into every cover. A subset obstruction may instead
show that every undersized combination fails without forcing any individual
selected type.

## Verifier and payload cost

Retain the notation from `THM-021`:

\[
 b=\sum_i|B_i|,\qquad q=|U|,\qquad t=|T|,
\]

and let \(\lambda\) be the total bit length of the point labels. Store the
\(t\) normalized \(b\)-bit patterns and \(q\)-bit coverage masks, and store
the \(k\) upper-witness type indices.

For a subset-obstruction certificate put
\(e=\binom{t}{k-1}\). Its additional abstract payload is

\[
 e\left((k-1)\lceil\log_2t\rceil+\lceil\log_2q\rceil\right)
\]

bits. Its lower-bound bit checks cost \(e(k-1)\), apart from bounded index and
combination-order checks. Including mask reconstruction and the upper
witness, the core verifier uses

\[
 O(tb+tq+kq+e(k-1)+\lambda)
\]

bit operations and

\[
 O\!\left(
 t(b+q)+k\log t+e((k-1)\log t+\log q)+\lambda
 \right)
\]

bits. This is polynomial in the explicit certificate length. It is not a
claim that \(e\) is polynomial in an external asymptotic input parameter.

For a cardinality witness, the additional payload is the ordinary binary
encoding of \(b_{\max}\) and its bound, and one arithmetic comparison replaces
the obstruction checks. For private pairs, the `THM-021` cost applies.

The registered checker also redundantly enumerates all \(2^t\) type subsets.
This bounded defense is not part of either polynomial certificate theorem.
In M93, \(t\le4\).

## Ten frozen applications

The source-bound schema
`schemas/m93-early-repair-certificates-v1.json` records:

| \(m\) | base cap | repair cap | \(b\) | \(q\) | \(t\) | \(k\) | lower witness | payload bits |
|---:|---:|---:|---:|---:|---:|---:|:---|---:|
| 16 | 18 | 19 | 3 | 3 | 3 | 2 | cardinality | 50 |
| 17 | 18 | 19 | 4 | 2 | 2 | 2 | private pairs | 54 |
| 18 | 26 | 27 | 2 | 1 | 1 | 1 | private pair | 21 |
| 19 | 26 | 27 | 2 | 1 | 1 | 1 | private pair | 23 |
| 20 | 30 | 31 | 2 | 1 | 1 | 1 | private pair | 23 |
| 21 | 32 | 33 | 4 | 6 | 3 | 3 | private pairs | 95 |
| 22 | 38 | 39 | 2 | 1 | 1 | 1 | private pair | 25 |
| 23 | 46 | 47 | 2 | 1 | 1 | 1 | private pair | 27 |
| 24 | 50 | 51 | 4 | 6 | 4 | 3 | subset obstructions | 136 |
| 25 | 64 | 65 | 2 | 1 | 1 | 1 | private pair | 29 |

The exact minima are

\[
 (2,2,1,1,1,3,1,1,3,1).
\]

At \(m=16\), the three masks are \(3,5,6\) in hexadecimal. No selected type
has a private pair, but the three-point bucket requires two binary
coordinates and the selected two types cover all three pairs.

At \(m=24\), the four masks are \(07,19,2a,34\). The upper witness
\(\{T0,T1,T2\}\) covers all six pairs, but none of its types has a private
pair. Each of the six two-type subsets has an explicit uncovered pair:

| two-type subset | uncovered pair |
|:---|:---|
| \(T0,T1\) | \(\{3863,4057\}\) |
| \(T0,T2\) | \(\{3643,4057\}\) |
| \(T0,T3\) | \(\{3643,3863\}\) |
| \(T1,T2\) | \(\{3049,4057\}\) |
| \(T1,T3\) | \(\{3049,3863\}\) |
| \(T2,T3\) | \(\{3049,3643\}\) |

Thus no two types cover the universe, while three do. These two cases refute
the claim that private-pair certificates are complete for all finite exact
repair instances; they do not refute `THM-021`.
