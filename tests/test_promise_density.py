"""Exact and exhaustive tests for the M8 combined-promise density barrier."""

from __future__ import annotations

import itertools
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import (  # noqa: E402
    analyze_combined_density,
    combined_asymmetry,
    combined_signature,
    direct_combined_asymmetry,
    divisor_count,
    hit_primes,
    is_prime,
)


class CombinedPromiseDensityTests(unittest.TestCase):
    def test_registered_signatures_and_both_channels(self) -> None:
        exponents = (4, 6)
        self.assertEqual(
            combined_signature(3, exponents),
            ((True, True), (True, False)),
        )
        self.assertEqual(
            combined_signature(5, exponents),
            ((True, False), (False, True)),
        )
        self.assertTrue(combined_asymmetry(3, 5, exponents))
        self.assertTrue(direct_combined_asymmetry(3, 5, exponents))

    def test_signature_characterization_exhaustively(self) -> None:
        primes = tuple(value for value in range(3, 48, 2) if is_prime(value))
        for size in range(1, 4):
            for exponents in itertools.combinations(range(1, 13), size):
                for left, right in itertools.combinations(primes, 2):
                    self.assertEqual(
                        combined_asymmetry(left, right, exponents),
                        direct_combined_asymmetry(left, right, exponents),
                        (left, right, exponents),
                    )

    def test_density_and_hit_bounds_exhaustively(self) -> None:
        primes = tuple(value for value in range(3, 80, 2) if is_prime(value))
        for size in range(1, 4):
            for exponents in itertools.combinations(range(1, 13), size):
                analysis = analyze_combined_density(primes, exponents)
                self.assertLessEqual(
                    analysis.promised_pairs,
                    analysis.hit_intersecting_pairs,
                    exponents,
                )
                self.assertLessEqual(
                    analysis.hit_count,
                    analysis.divisor_hit_bound,
                    exponents,
                )
                self.assertLessEqual(
                    analysis.hit_count,
                    analysis.square_root_hit_bound,
                    exponents,
                )

    def test_exact_pair_intersection_count(self) -> None:
        primes = (3, 5, 7, 11, 13, 17, 19)
        exponents = (4, 6)
        hits = hit_primes(primes, exponents)
        analysis = analyze_combined_density(primes, exponents)
        expected = analysis.total_pairs - (
            (len(primes) - len(hits)) * (len(primes) - len(hits) - 1) // 2
        )
        self.assertEqual(analysis.hit_count, len(hits))
        self.assertEqual(analysis.hit_intersecting_pairs, expected)

    def test_magnitude_barrier_gives_zero_signatures(self) -> None:
        exponents = (4, 6, 12)
        primes = (17, 19, 23, 29, 31)
        for prime in primes:
            self.assertGreater(prime, max(exponents) + 1)
            self.assertEqual(
                combined_signature(prime, exponents),
                ((False, False),) * len(exponents),
            )
        analysis = analyze_combined_density(primes, exponents)
        self.assertEqual(analysis.hit_count, 0)
        self.assertEqual(analysis.promised_pairs, 0)

    def test_refuted_smallest_unrestricted_schedule(self) -> None:
        self.assertFalse(combined_asymmetry(3, 5, (1,)))
        self.assertEqual(hit_primes((3, 5), (1,)), ())

    def test_divisor_count(self) -> None:
        expected = {1: 1, 2: 2, 4: 3, 6: 4, 12: 6, 16: 5, 36: 9}
        for value, count in expected.items():
            self.assertEqual(divisor_count(value), count)

    def test_invalid_domains_raise(self) -> None:
        invalid_calls = (
            lambda: combined_signature(2, (1,)),
            lambda: combined_signature(9, (1,)),
            lambda: combined_signature(3, ()),
            lambda: combined_signature(3, (0,)),
            lambda: combined_asymmetry(3, 3, (1,)),
            lambda: direct_combined_asymmetry(3, 5, (False,)),
            lambda: divisor_count(0),
            lambda: hit_primes((), (1,)),
            lambda: analyze_combined_density((3,), (1,)),
        )
        for invalid_call in invalid_calls:
            with self.subTest(invalid_call=invalid_call):
                with self.assertRaises(ValueError):
                    invalid_call()


if __name__ == "__main__":
    unittest.main()
