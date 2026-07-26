# SRC-007 - Shifted primes without large prime factors

## Source

Jared Duker Lichtman, *Primes in arithmetic progressions to large moduli, and
shifted primes without large prime factors*, arXiv:2211.09641v1 [math.NT],
submitted 14 November 2022. The inspected arXiv record exposes only version 1.

Primary source: <https://arxiv.org/abs/2211.09641>

## Inspected statement

Theorem 1.1 states that, for fixed nonzero \(a\in\mathbb Z\) and fixed
\[
\beta>\frac{15}{32\sqrt e}=0.2843\ldots,
\]
there exists \(C>1\) such that
\[
\#\{x<p\le2x:P^+(p-a)\le x^\beta\}
\gg \frac{x}{(\log x)^C}.
\]
The theorem is asymptotic and the constants may depend on the fixed
parameters.

## Scope audit for M12

This is related context only. It does not imply any M12 yield claim:

- the cutoff \(x^\beta\) is a fixed positive power and is much larger than
  \(\operatorname{poly}(\log p)\);
- no squarefreeness condition is imposed on \(p-a\);
- neither \(p-a\mid P_r\) nor \(P_r\mid p-a\) follows;
- the theorem applies separately to a fixed \(a=1\) or \(a=-1\), not to a
  simultaneous two-channel condition;
- it supplies no stipulated external-population promise-density guarantee.

BAR-007 is instead an elementary upper bound for divisors of a square-free
first-primes primorial at target-factor scale. It does not depend on this
external theorem.

## Verification

The arXiv abstract/version record, PDF page 1 (Introduction and Theorem 1.1),
and the Section 3 proof setup were inspected. An independent source reviewer
confirmed the exact threshold, strict inequality, dyadic interval, fixed
shift, and the exclusions above.
