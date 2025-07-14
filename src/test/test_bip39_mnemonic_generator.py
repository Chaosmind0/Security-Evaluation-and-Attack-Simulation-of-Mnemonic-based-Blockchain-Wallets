import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from bip39_mnemonic_generator import BIP39MnemonicGenerator


class TestBIP39MnemonicGenerator(unittest.TestCase):
    """

    Test suite for the BIP39MnemonicGenerator class.

    """

    def setUp(self):
        """

        Set up the test suite.S

        """

        self.generator = BIP39MnemonicGenerator()

    def test_generate_12_word_mnemonic(self):
        """

        Test that a 12-word mnemonic can be generated.

        """

        mnemonic = self.generator.generate_mnemonic(12)
        words = mnemonic.split()
        self.assertEqual(len(words), 12)
        self.assertTrue(all(word in self.generator.wordlist for word in words))

    def test_generate_24_word_mnemonic(self):
        """

        Test that a 24-word mnemonic can be generated.

        """

        mnemonic = self.generator.generate_mnemonic(24)
        words = mnemonic.split()
        self.assertEqual(len(words), 24)

    def test_generate_weak_mnemonic_with_prefix_and_repeats(self):
        """

        Test that a weak 12-word mnemonic can be generated with a prefix and repeats.

        """

        prefix = ["abandon", "abandon", "abandon"]
        mnemonic = self.generator.generate_weak_mnemonic(
            word_count=12,
            weak_pool_size=64,
            pool_start=0,
            allow_repeats=True,
            prefix=prefix,
        )
        words = mnemonic.split()
        self.assertEqual(len(words), 12)
        self.assertEqual(words[:3], prefix)

    def test_generate_weak_mnemonic_without_repeats(self):
        """

        Test that a weak 12-word mnemonic can be generated without repeats.

        """

        mnemonic = self.generator.generate_weak_mnemonic(
            word_count=12,
            weak_pool_size=64,
            pool_start=0,
            allow_repeats=False,
        )
        words = mnemonic.split()
        self.assertEqual(len(words), 12)
        self.assertEqual(len(set(words)), 12)  # No repeats

    def test_invalid_word_count_raises_error(self):
        """

        Test that an error is raised when an invalid word count is specified.

        """

        with self.assertRaises(ValueError):
            self.generator.generate_mnemonic(15)

        with self.assertRaises(ValueError):
            self.generator.generate_weak_mnemonic(word_count=15)

    def test_invalid_weak_pool_range_raises_error(self):
        """

        Test that an error is raised when an invalid weak pool range is specified.

        """

        with self.assertRaises(ValueError):
            self.generator.generate_weak_mnemonic(
                word_count=12, weak_pool_size=100, pool_start=2000  # Overflows the wordlist
            )


if __name__ == "__main__":
    unittest.main()
