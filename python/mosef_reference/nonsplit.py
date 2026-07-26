"""Exact finite-field and composite-modulus semantics for M7."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from .baseline import is_prime, lucas_v
from .multigroup import candidate_succeeds, evaluate_lucas_candidate


@dataclass(frozen=True)
class LucasAsymmetryWitness:
    """One ordered prime-factor witness for a nonsplit Lucas exponent."""

    p: int
    q: int
    exponent: int


def _require_odd_prime(prime: int) -> None:
    if prime < 3 or prime % 2 == 0 or not is_prime(prime):
        raise ValueError("prime must be an odd prime")


def legendre_symbol(value: int, prime: int) -> int:
    """Return the Legendre symbol of ``value`` modulo an odd prime."""
    _require_odd_prime(prime)
    reduced = value % prime
    if reduced == 0:
        return 0
    symbol = pow(reduced, (prime - 1) // 2, prime)
    return -1 if symbol == prime - 1 else symbol


def lucas_root_count(prime: int, exponent: int) -> int:
    """Count parameters ``P`` with ``V_exponent(P,1) == 2 mod prime``."""
    _require_odd_prime(prime)
    if exponent <= 0:
        raise ValueError("exponent must be positive")
    return (
        gcd(exponent, prime - 1) + gcd(exponent, prime + 1)
    ) // 2


def direct_lucas_root_count(prime: int, exponent: int) -> int:
    """Enumerate the same root count independently for bounded checks."""
    _require_odd_prime(prime)
    if exponent <= 0:
        raise ValueError("exponent must be positive")
    return sum(
        lucas_v(exponent, parameter, prime) == 2 % prime
        for parameter in range(prime)
    )


def nonsplit_parameter_count(prime: int) -> int:
    """Count parameters whose discriminant is a nonzero nonsquare."""
    _require_odd_prime(prime)
    return sum(
        legendre_symbol(parameter * parameter - 4, prime) == -1
        for parameter in range(prime)
    )


def nondegenerate_lucas_collision_count(prime: int, exponent: int) -> int:
    """Count root parameters excluding the degenerate values ``P = +/-2``."""
    roots = lucas_root_count(prime, exponent)
    degenerate_roots = 1 + int(exponent % 2 == 0)
    return roots - degenerate_roots


def is_lucas_asymmetry_witness(p: int, q: int, exponent: int) -> bool:
    """Return whether ``p + 1`` divides the exponent but ``q + 1`` does not."""
    _require_odd_prime(p)
    _require_odd_prime(q)
    if p == q:
        raise ValueError("p and q must be distinct")
    if exponent <= 0:
        raise ValueError("exponent must be positive")
    return exponent % (p + 1) == 0 and exponent % (q + 1) != 0


def witness_event_holds(
    modulus: int,
    witness: LucasAsymmetryWitness,
    parameter: int,
) -> bool:
    """Return whether a sampled parameter lies in the proved success event."""
    if modulus < 2 or modulus % (witness.p * witness.q) != 0:
        raise ValueError("modulus must be divisible by both witness primes")
    if not is_lucas_asymmetry_witness(
        witness.p,
        witness.q,
        witness.exponent,
    ):
        raise ValueError("invalid Lucas asymmetry witness")
    reduced_p = parameter % witness.p
    reduced_q = parameter % witness.q
    p_nonsplit = (
        legendre_symbol(reduced_p * reduced_p - 4, witness.p) == -1
    )
    q_discriminant = (reduced_q * reduced_q - 4) % witness.q
    q_safe = (
        q_discriminant == 0
        or lucas_v(witness.exponent, reduced_q, witness.q) != 2
    )
    return p_nonsplit and q_safe


def witness_event_count(witness: LucasAsymmetryWitness) -> int:
    """Count proved success pairs modulo ``p*q`` by the exact formula."""
    if not is_lucas_asymmetry_witness(
        witness.p,
        witness.q,
        witness.exponent,
    ):
        raise ValueError("invalid Lucas asymmetry witness")
    p_choices = (witness.p - 1) // 2
    q_choices = (
        witness.q
        - nondegenerate_lucas_collision_count(
            witness.q,
            witness.exponent,
        )
    )
    return p_choices * q_choices


def direct_witness_event_count(witness: LucasAsymmetryWitness) -> int:
    """Enumerate the event modulo ``p*q`` for bounded falsification."""
    modulus = witness.p * witness.q
    return sum(
        witness_event_holds(modulus, witness, parameter)
        for parameter in range(modulus)
    )


def lucas_split_success_count(modulus: int, exponent: int) -> int:
    """Count parameters exposing a proper factor under exact M5 semantics."""
    if modulus < 2:
        raise ValueError("modulus must be at least 2")
    if exponent <= 0:
        raise ValueError("exponent must be positive")
    return sum(
        candidate_succeeds(
            evaluate_lucas_candidate(modulus, parameter, exponent)
        )
        for parameter in range(modulus)
    )
