import os
import hashlib
import random
import requests


class BIP39MnemonicGenerator:
    """

    BIP39 Mnemonic Generator
    Generates 12 or 24-word mnemonic phrases using BIP39 standard.
    Uses the English wordlist by default.
    The link of the English wordlist file is: https://github.com/bitcoin/bips/blob/master/bip-0039/english.txt

    12-word mnemonic:
    - 128 bits of entropy
    - 12 words

    24-word mnemonic:
    - 256 bits of entropy
    - 24 words

    """

    def __init__(self):
        self.wordlist = self.load_wordlist()

    def download_bip39_wordlist(save_path="data/english.txt"):
        """

        Downloads the BIP39 English wordlist from the official GitHub repository.
        Saves it to the specified path.

        Parameters
            save_path: Path to save the wordlist file.

        """

        # BIP39 English wordlist URL
        url = "https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt"

        # Make sure the data folder exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        print(f"Downloading BIP39 English wordlist from {url}...")
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"Wordlist saved to {save_path}")
        else:
            raise Exception(f"Failed to download wordlist. Status code: {response.status_code}")

    # Load BIP39 English wordlist
    def load_wordlist(self):
        """

        Loads the BIP39 English wordlist from the local file or downloads it if it doesn't exist.

        Returns:
            List of words in the wordlist.

        """

        relative_path = "../data/english.txt"
        path = os.path.join(os.path.dirname(__file__), relative_path)

        # If the wordlist file doesn't exist, download it
        if not os.path.isfile(path):
            print("Wordlist not found. Downloading...")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            self.download_bip39_wordlist(save_path=path)

        with open(path, "r", encoding="utf-8") as f:
            return [word.strip() for word in f.readlines()]

    # Generate entropy of desired bit length
    def generate_entropy(self, bits: int) -> bytes:
        """

        Generates entropy of desired bit length using os.urandom().

        Parameters
            bits: Desired bit length of entropy.

        Returns:
            Entropy bytes.

        """

        if bits not in [128, 256]:
            raise ValueError("Only 128 or 256 bits supported.")
        return os.urandom(bits // 8)

    # Convert entropy + checksum into mnemonic
    def entropy_to_mnemonic(self, entropy: bytes) -> list[str]:
        """

        Converts entropy bytes into a list of BIP39 mnemonic words.
        More information about BIP39: https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki

        Parameters
            entropy: Entropy bytes.

        Returns:
            List of BIP39 mnemonic words.

        """

        ENT = len(entropy) * 8
        checksum_length = ENT // 32
        entropy_bits = bin(int.from_bytes(entropy, "big"))[2:].zfill(ENT)

        # SHA256 to get checksum bits
        hash_digest = hashlib.sha256(entropy).hexdigest()
        hash_bits = bin(int(hash_digest, 16))[2:].zfill(256)
        checksum = hash_bits[:checksum_length]

        # Combined bits
        full_bits = entropy_bits + checksum
        words = []

        for i in range(0, len(full_bits), 11):
            idx = int(full_bits[i : i + 11], 2)
            words.append(self.wordlist[idx])

        return words

    # Entry point to generate final mnemonic
    def generate_mnemonic(self, word_count: int = 12) -> str:
        """

        Generates a BIP39 mnemonic phrase of the specified word count.
        Default is 12-word mnemonic.

        More information about BIP32: https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki

        Parameters
            word_count: Number of words in the mnemonic phrase.

        Returns:
            String of the BIP39 mnemonic phrase.

        """

        if word_count == 12:
            entropy = self.generate_entropy(128)
        elif word_count == 24:
            entropy = self.generate_entropy(256)
        else:
            raise ValueError("Only 12 or 24 words are supported.")

        mnemonic = self.entropy_to_mnemonic(entropy)
        return " ".join(mnemonic)

    # Generate a weak mnemonic with a weak pool of words
    def generate_weak_mnemonic(
        self,
        word_count: int = 12,
        weak_pool_size: int = 128,
        pool_start: int = 0,
        allow_repeats: bool = True,
        prefix: list[str] = None,
    ) -> str:
        """
        Generates a weak BIP39 mnemonic using limited entropy (e.g., leaked or low-randomness scenarios).

        Parameters:
            word_count (int): Number of mnemonic words.
            weak_pool_size (int): Size of the weak word pool to simulate user error.
            pool_start (int): Start index of the weak pool within the full wordlist.
            allow_repeats (bool): If True, words may repeat.
            prefix (list[str]): Optional fixed word prefix.

        Returns:
            str: Space-separated weak mnemonic phrase.
        """

        if word_count not in [12, 24]:
            raise ValueError("Only 12 or 24 words are supported.")

        if pool_start < 0 or pool_start + weak_pool_size > len(self.wordlist):
            raise ValueError("Invalid weak pool range.")

        pool = self.wordlist[pool_start : pool_start + weak_pool_size]
        remaining = word_count - len(prefix) if prefix else word_count

        if not allow_repeats and remaining > len(pool):
            raise ValueError(
                "Not enough unique words in weak pool to fill mnemonic without repeats."
            )

        if allow_repeats:
            chosen = random.choices(pool, k=remaining)
        else:
            chosen = random.sample(pool, k=remaining)

        final_words = (prefix or []) + chosen
        return " ".join(final_words)


if __name__ == "__main__":
    # Example usage
    # Generate 12-word and 24-word mnemonics
    # Generate weak 12-word and 24-word mnemonics with a weak pool of 128 and 256 words, respectively

    generator = BIP39MnemonicGenerator()

    print("Generated 12-word mnemonic:")
    print(generator.generate_mnemonic(12))

    print("\nGenerated 24-word mnemonic:")
    print(generator.generate_mnemonic(24))

    print("\nWeak 12-word mnemonic with fixed prefix and repeats:")
    print(
        generator.generate_weak_mnemonic(
            word_count=12,
            weak_pool_size=64,
            pool_start=0,
            allow_repeats=True,
            prefix=["abandon", "abandon", "abandon"],
        )
    )

    print("\nWeak 24-word mnemonic from a middle pool without repeats:")
    print(
        generator.generate_weak_mnemonic(
            word_count=24, weak_pool_size=64, pool_start=1024, allow_repeats=False
        )
    )
