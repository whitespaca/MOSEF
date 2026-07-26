"""Falsify the M7 Lucas root count and nonsplit splitter bound."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import (  # noqa: E402
    LucasAsymmetryWitness,
    candidate_succeeds,
    direct_lucas_root_count,
    evaluate_lucas_candidate,
    is_lucas_asymmetry_witness,
    is_prime,
    lucas_root_count,
    nonsplit_parameter_count,
    witness_event_count,
    witness_event_holds,
)


def canonical_json(value: Any) -> bytes:
    """Serialize a value deterministically for hashing."""
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def ratio_record(value: Fraction, witness: LucasAsymmetryWitness) -> dict[str, Any]:
    """Serialize one exact minimum ratio and its ordered witness."""
    return {
        "fraction": f"{value.numerator}/{value.denominator}",
        "numerator": value.numerator,
        "denominator": value.denominator,
        "p": witness.p,
        "q": witness.q,
        "exponent": witness.exponent,
    }


def search(prime_max: int, exponent_max: int) -> dict[str, Any]:
    """Run the registered deterministic finite-field and splitter search."""
    if prime_max < 5:
        raise ValueError("prime_max must be at least 5")
    if exponent_max < 4:
        raise ValueError("exponent_max must be at least 4")
    primes = [value for value in range(3, prime_max + 1, 2) if is_prime(value)]

    root_formula_checks = 0
    root_parameter_evaluations = 0
    nonsplit_count_checks = 0
    for prime in primes:
        if nonsplit_parameter_count(prime) != (prime - 1) // 2:
            raise AssertionError(("nonsplit count", prime))
        nonsplit_count_checks += 1
        for exponent in range(1, exponent_max + 1):
            formula = lucas_root_count(prime, exponent)
            direct = direct_lucas_root_count(prime, exponent)
            if formula != direct:
                raise AssertionError(
                    ("root count", prime, exponent, formula, direct)
                )
            root_formula_checks += 1
            root_parameter_evaluations += prime

    witness_count = 0
    witness_parameter_evaluations = 0
    event_success_checks = 0
    minimum_event: tuple[Fraction, LucasAsymmetryWitness] | None = None
    minimum_actual: tuple[Fraction, LucasAsymmetryWitness] | None = None
    smallest_witness: dict[str, int] | None = None

    for p in primes:
        for q in primes:
            if p == q:
                continue
            modulus = p * q
            for exponent in range(1, exponent_max + 1):
                if not is_lucas_asymmetry_witness(p, q, exponent):
                    continue
                witness = LucasAsymmetryWitness(p, q, exponent)
                formula_event = witness_event_count(witness)
                direct_event = 0
                actual_success = 0
                for parameter in range(modulus):
                    event = witness_event_holds(modulus, witness, parameter)
                    outcome = evaluate_lucas_candidate(
                        modulus,
                        parameter,
                        exponent,
                    )
                    success = candidate_succeeds(outcome)
                    direct_event += int(event)
                    actual_success += int(success)
                    if event and not success:
                        raise AssertionError(
                            ("event failure", p, q, exponent, parameter)
                        )
                if formula_event != direct_event:
                    raise AssertionError(
                        (
                            "event count",
                            p,
                            q,
                            exponent,
                            formula_event,
                            direct_event,
                        )
                    )
                if 12 * formula_event < modulus:
                    raise AssertionError(
                        ("one-twelfth bound", p, q, exponent, formula_event)
                    )
                if actual_success < formula_event:
                    raise AssertionError(
                        ("success superset", p, q, exponent, actual_success)
                    )
                event_ratio = Fraction(formula_event, modulus)
                actual_ratio = Fraction(actual_success, modulus)
                if minimum_event is None or event_ratio < minimum_event[0]:
                    minimum_event = (event_ratio, witness)
                if minimum_actual is None or actual_ratio < minimum_actual[0]:
                    minimum_actual = (actual_ratio, witness)
                if smallest_witness is None:
                    smallest_witness = {
                        "n": modulus,
                        "p": p,
                        "q": q,
                        "exponent": exponent,
                        "proved_event_count": formula_event,
                        "actual_success_count": actual_success,
                    }
                witness_count += 1
                witness_parameter_evaluations += modulus
                event_success_checks += direct_event

    if minimum_event is None or minimum_actual is None or smallest_witness is None:
        raise AssertionError("registered box contained no Lucas asymmetry witness")

    summary: dict[str, Any] = {
        "bounds": {
            "odd_prime": [3, prime_max],
            "exponent": [1, exponent_max],
        },
        "seed": None,
        "odd_prime_count": len(primes),
        "root_formula_checks": root_formula_checks,
        "root_parameter_evaluations": root_parameter_evaluations,
        "nonsplit_count_checks": nonsplit_count_checks,
        "ordered_witness_count": witness_count,
        "witness_parameter_evaluations": witness_parameter_evaluations,
        "proved_event_success_checks": event_success_checks,
        "smallest_witness": smallest_witness,
        "minimum_proved_event_probability": ratio_record(*minimum_event),
        "minimum_actual_split_probability": ratio_record(*minimum_actual),
        "checked": {
            "root_count_formula": True,
            "nonsplit_parameter_count": True,
            "crt_event_count_formula": True,
            "one_twelfth_bound": True,
            "proved_event_implies_exact_split": True,
            "actual_success_contains_proved_event": True,
        },
    }
    summary["summary_sha256"] = hashlib.sha256(canonical_json(summary)).hexdigest()
    return summary


def main() -> int:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prime-max", type=int, default=43)
    parser.add_argument("--exponent-max", type=int, default=80)
    args = parser.parse_args()
    print(
        json.dumps(
            search(args.prime_max, args.exponent_max),
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
