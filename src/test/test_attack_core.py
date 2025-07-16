import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from attack_core import (
    check_parameters,
    estimate_brute_force_security,
    simulate_brute_force_attack,
    exhaustive_brute_force_attack,
)


class TestAttackCore(unittest.TestCase):
    """

    Test cases for the attack_core module.

    """

    def test_check_parameters_valid(self):
        """

        Test check_parameters() with valid parameters.

        """

        try:
            check_parameters(
                prefix=["abandon", "abandon"],
                word_count=12,
                weak_pool_size=64,
                pool_start=0,
            )
        except AssertionError:
            self.fail("check_parameters() raised AssertionError unexpectedly!")

    def test_check_parameters_invalid_prefix_length(self):
        """

        Test check_parameters() with invalid prefix length.

        """

        with self.assertRaises(AssertionError):
            check_parameters(["abandon"] * 13, 12, 64, 0)

    def test_estimate_security_repeat(self):
        """

        Test estimate_brute_force_security() with allow_repeats=True.

        """

        result = estimate_brute_force_security(
            pool_size=64,
            word_count=12,
            prefix_length=3,
            max_attempts=1000,
            allow_repeats=True,
        )
        self.assertIn("entropy_bits", result)
        self.assertGreater(result["entropy_bits"], 0)
        self.assertLess(result["success_probability"], 1)

    def test_simulate_brute_force_attack_runs(self):
        """

        Test simulate_brute_force_attack() with a small number of attempts.

        """

        result = simulate_brute_force_attack(
            word_count=12,
            weak_pool_size=16,
            pool_start=0,
            prefix=["abandon", "abandon"],
            allow_repeats=True,
            target_coin="ETHEREUM",
            max_attempts=10,
        )
        self.assertIn("attempts", result)
        self.assertIn("success", result)

    def test_exhaustive_brute_force_attack_runs(self):
        """

        Test exhaustive_brute_force_attack() with a small number of attempts.

        """

        result = exhaustive_brute_force_attack(
            word_count=12,
            weak_pool_size=8,
            pool_start=0,
            prefix=["abandon", "abandon"],
            allow_repeats=True,
            target_coin="BITCOIN",
            max_attempts=20,
        )
        self.assertIn("attempts", result)
        self.assertIn("success", result)


if __name__ == "__main__":
    unittest.main()
