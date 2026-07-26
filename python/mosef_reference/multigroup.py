"""Exact multiplicative and Lucas-channel semantics for M5."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import gcd

from .baseline import lucas_v
from .separator import CandidateKind, CandidateOutcome, evaluate_separator_candidate


class LucasCandidateKind(str, Enum):
    """Exhaustive outcomes for one Lucas ``V_d(P,1) - 2`` candidate."""

    DISCRIMINANT_FACTOR = "discriminant_factor"
    DEGENERATE_MISS = "degenerate_miss"
    DEGENERATE_FACTOR = "degenerate_factor"
    DEGENERATE_COLLISION = "degenerate_collision"
    MISS = "miss"
    FACTOR = "factor"
    SIMULTANEOUS_COLLISION = "simultaneous_collision"


@dataclass(frozen=True)
class LucasCandidateOutcome:
    """Result of one Lucas candidate with its discriminant precheck."""

    kind: LucasCandidateKind
    factor: int | None
    residue: int | None
    discriminant_gcd: int


@dataclass(frozen=True)
class ConjugatePairAnalysis:
    """Exact outcomes and identities for the natural conjugate pairing."""

    parameter: int
    multiplicative: CandidateOutcome
    lucas: LucasCandidateOutcome
    multiplicative_gcd: int
    lucas_gcd: int
    discriminant_gcd: int
    discriminant_identity: bool
    lucas_identity: bool


def evaluate_lucas_candidate(n: int, parameter: int, exponent: int) -> LucasCandidateOutcome:
    """Evaluate ``gcd(V_exponent(parameter,1)-2,n)`` with exact branches."""
    if n < 2:
        raise ValueError("n must be at least 2")
    if exponent <= 0:
        raise ValueError("exponent must be positive")
    reduced_parameter = parameter % n
    discriminant_gcd = gcd((reduced_parameter * reduced_parameter - 4) % n, n)
    if 1 < discriminant_gcd < n:
        return LucasCandidateOutcome(
            LucasCandidateKind.DISCRIMINANT_FACTOR,
            discriminant_gcd,
            None,
            discriminant_gcd,
        )
    residue = lucas_v(exponent, reduced_parameter, n)
    candidate_gcd = gcd((residue - 2) % n, n)
    if discriminant_gcd == n and candidate_gcd == 1:
        kind = LucasCandidateKind.DEGENERATE_MISS
        factor = None
    elif discriminant_gcd == n and candidate_gcd == n:
        kind = LucasCandidateKind.DEGENERATE_COLLISION
        factor = None
    elif discriminant_gcd == n:
        kind = LucasCandidateKind.DEGENERATE_FACTOR
        factor = candidate_gcd
    elif candidate_gcd == 1:
        kind = LucasCandidateKind.MISS
        factor = None
    elif candidate_gcd == n:
        kind = LucasCandidateKind.SIMULTANEOUS_COLLISION
        factor = None
    else:
        kind = LucasCandidateKind.FACTOR
        factor = candidate_gcd
    return LucasCandidateOutcome(
        kind,
        factor,
        residue,
        discriminant_gcd,
    )


def conjugate_parameter(n: int, base: int) -> int:
    """Return ``base + base**-1 mod n`` for a unit base."""
    if n < 2:
        raise ValueError("n must be at least 2")
    reduced_base = base % n
    if gcd(reduced_base, n) != 1:
        raise ValueError("base must be coprime to n")
    return (reduced_base + pow(reduced_base, -1, n)) % n


def analyze_conjugate_pair(n: int, base: int, exponent: int) -> ConjugatePairAnalysis:
    """Check the exact conjugate identities and both candidate outcomes."""
    if n < 2:
        raise ValueError("n must be at least 2")
    if exponent <= 0:
        raise ValueError("exponent must be positive")
    reduced_base = base % n
    inverse = pow(reduced_base, -1, n) if gcd(reduced_base, n) == 1 else None
    if inverse is None:
        raise ValueError("base must be coprime to n")
    parameter = (reduced_base + inverse) % n
    multiplicative = evaluate_separator_candidate(n, reduced_base, exponent)
    lucas = evaluate_lucas_candidate(n, parameter, exponent)
    multiplicative_difference = (pow(reduced_base, exponent, n) - 1) % n
    lucas_difference = (lucas_v(exponent, parameter, n) - 2) % n
    discriminant = (parameter * parameter - 4) % n
    multiplicative_gcd = gcd(multiplicative_difference, n)
    lucas_gcd = gcd(lucas_difference, n)
    discriminant_gcd = gcd(discriminant, n)
    return ConjugatePairAnalysis(
        parameter=parameter,
        multiplicative=multiplicative,
        lucas=lucas,
        multiplicative_gcd=multiplicative_gcd,
        lucas_gcd=lucas_gcd,
        discriminant_gcd=discriminant_gcd,
        discriminant_identity=discriminant
        == pow(inverse, 2, n) * pow(reduced_base * reduced_base - 1, 2, n) % n,
        lucas_identity=lucas_difference
        == pow(inverse, exponent, n) * pow(multiplicative_difference, 2, n) % n,
    )


def candidate_succeeds(outcome: CandidateOutcome | LucasCandidateOutcome) -> bool:
    """Return whether an exact channel outcome exposes a proper factor."""
    if isinstance(outcome, CandidateOutcome):
        return outcome.kind in {CandidateKind.DIRECT_FACTOR, CandidateKind.FACTOR}
    return outcome.kind in {
        LucasCandidateKind.DISCRIMINANT_FACTOR,
        LucasCandidateKind.DEGENERATE_FACTOR,
        LucasCandidateKind.FACTOR,
    }
