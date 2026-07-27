"""Correctness-first factorization primitives.

The Python layer uses arbitrary-precision integers and is the semantic oracle
for small exact inputs. These algorithms are deliberately simple and make no
polynomial-time claim in the binary input length.
"""

from __future__ import annotations

from math import gcd


def mod_pow(base: int, exponent: int, modulus: int) -> int:
    """Return ``base**exponent mod modulus`` by exact square-and-multiply."""
    if exponent < 0:
        raise ValueError("exponent must be nonnegative")
    if modulus <= 0:
        raise ValueError("modulus must be positive")
    result = 1 % modulus
    factor = base % modulus
    remaining = exponent
    while remaining:
        if remaining & 1:
            result = result * factor % modulus
        factor = factor * factor % modulus
        remaining >>= 1
    return result


def trial_division(n: int) -> int | None:
    """Return the least prime factor of composite ``n``, or ``None``."""
    if n < 2:
        return None
    if n % 2 == 0:
        return 2 if n != 2 else None
    divisor = 3
    while divisor <= n // divisor:
        if n % divisor == 0:
            return divisor
        divisor += 2
    return None


def is_prime(n: int) -> bool:
    """Deterministically decide primality by trial division.

    This function is an exact validation oracle for small test inputs. Its
    running time is not polynomial in the binary input length.
    """
    return n >= 2 and trial_division(n) is None


def _power_leq(base: int, exponent: int, limit: int) -> tuple[bool, int]:
    value = 1
    for _ in range(exponent):
        value *= base
        if value > limit:
            return False, value
    return True, value


def _integer_nth_root(n: int, exponent: int) -> int:
    """Return floor(n**(1/exponent)) using integer comparisons only."""
    low = 1
    high = 1 << ((n.bit_length() + exponent - 1) // exponent)
    while low <= high:
        middle = (low + high) // 2
        within, _value = _power_leq(middle, exponent, n)
        if within:
            low = middle + 1
        else:
            high = middle - 1
    return high


def perfect_power(n: int) -> tuple[int, int] | None:
    """Return ``(base, maximal exponent)`` for ``n = base**exponent``."""
    if n < 4:
        return None
    for exponent in range(n.bit_length(), 1, -1):
        root = _integer_nth_root(n, exponent)
        if root >= 2 and pow(root, exponent) == n:
            return root, exponent
    return None


def _primes_up_to(bound: int) -> list[int]:
    primes: list[int] = []
    for candidate in range(2, bound + 1):
        if all(candidate % prime for prime in primes if prime <= candidate // prime):
            primes.append(candidate)
    return primes


def _prime_power_at_most(prime: int, bound: int) -> int:
    power = prime
    while power <= bound // prime:
        power *= prime
    return power


def _stage_one_exponent(bound: int) -> int:
    exponent = 1
    for prime in _primes_up_to(bound):
        exponent *= _prime_power_at_most(prime, bound)
    return exponent


def pollard_p_minus_one(n: int, bound: int, base: int = 2) -> int | None:
    """Run deterministic Pollard p-1 stage 1 and return a nontrivial factor."""
    if n < 4 or bound < 2:
        return None
    initial_gcd = gcd(base, n)
    if 1 < initial_gcd < n:
        return initial_gcd
    if initial_gcd == n:
        return None
    residue = base % n
    for prime in _primes_up_to(bound):
        residue = mod_pow(residue, _prime_power_at_most(prime, bound), n)
    factor = gcd(residue - 1, n)
    return factor if 1 < factor < n else None


Matrix2 = tuple[tuple[int, int], tuple[int, int]]


def _matrix_multiply(left: Matrix2, right: Matrix2, modulus: int) -> Matrix2:
    return (
        (
            (left[0][0] * right[0][0] + left[0][1] * right[1][0]) % modulus,
            (left[0][0] * right[0][1] + left[0][1] * right[1][1]) % modulus,
        ),
        (
            (left[1][0] * right[0][0] + left[1][1] * right[1][0]) % modulus,
            (left[1][0] * right[0][1] + left[1][1] * right[1][1]) % modulus,
        ),
    )


def lucas_v(index: int, parameter: int, modulus: int) -> int:
    """Return ``V_index(parameter, 1) mod modulus`` by matrix powering."""
    if index < 0:
        raise ValueError("index must be nonnegative")
    if modulus <= 0:
        raise ValueError("modulus must be positive")
    result: Matrix2 = ((1 % modulus, 0), (0, 1 % modulus))
    factor: Matrix2 = ((parameter % modulus, -1 % modulus), (1 % modulus, 0))
    remaining = index
    while remaining:
        if remaining & 1:
            result = _matrix_multiply(result, factor, modulus)
        factor = _matrix_multiply(factor, factor, modulus)
        remaining >>= 1
    return (result[0][0] + result[1][1]) % modulus


def pollard_p_plus_one(n: int, bound: int, parameter: int = 3) -> int | None:
    """Run a scoped Williams-style p+1 stage 1 with ``Q = 1``.

    The method returns a factor when the selected Lucas parameter separates one
    prime divisor. A return value of ``None`` is an ordinary method failure.
    """
    if n < 4 or bound < 2:
        return None
    discriminant_gcd = gcd(parameter * parameter - 4, n)
    if 1 < discriminant_gcd < n:
        return discriminant_gcd
    if discriminant_gcd == n:
        return None
    exponent = _stage_one_exponent(bound)
    value = lucas_v(exponent, parameter, n)
    factor = gcd(value - 2, n)
    return factor if 1 < factor < n else None


def pollard_rho(n: int, seed: int = 0, max_steps: int = 10_000) -> int | None:
    """Run a deterministic, bounded Pollard-rho search."""
    if n < 4 or max_steps <= 0:
        return None
    if n % 2 == 0:
        return 2
    if is_prime(n):
        return None
    for attempt in range(8):
        offset = seed + attempt
        value = 2 + offset % (n - 3)
        tortoise = value
        hare = value
        constant = 1 + (2 * offset + 1) % (n - 1)
        for _ in range(max_steps):
            tortoise = (tortoise * tortoise + constant) % n
            hare = (hare * hare + constant) % n
            hare = (hare * hare + constant) % n
            factor = gcd(abs(tortoise - hare), n)
            if 1 < factor < n:
                return factor
            if factor == n:
                break
    return None


def batch_gcd(values: list[int], modulus: int) -> list[int]:
    """Return exact per-value GCDs for a research batch."""
    if modulus <= 0:
        raise ValueError("modulus must be positive")
    return [gcd(value, modulus) for value in values]
