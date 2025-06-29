import hashlib
import binascii
import unicodedata
from bip_utils import (
    Bip44,
    Bip44Coins,
    Bip44Changes,
)


class UnsafeWalletKeyDeriver:
    """

    Unsafe version of WalletKeyDeriver that bypasses BIP39 checksum validation.
    Allows seed and key derivation from weak or non-standard mnemonics.

    This is just used for testing purposes and should not be used in production.

    """

    def __init__(self, mnemonic: str, passphrase: str = ""):
        self.mnemonic = mnemonic
        self.passphrase = passphrase
        self.seed_bytes = self.generate_seed(mnemonic, passphrase)

    def generate_seed(self, mnemonic: str, passphrase: str) -> bytes:
        """

        Generate BIP39 seed without validating the mnemonic checksum.

        Parameters:
            mnemonic (str): Mnemonic phrase (may be invalid).
            passphrase (str): Optional passphrase.

        Returns:
            bytes: Seed bytes.

        """

        mnemonic_normalized = unicodedata.normalize("NFKD", mnemonic)
        passphrase_normalized = unicodedata.normalize("NFKD", "mnemonic" + passphrase)
        return hashlib.pbkdf2_hmac(
            "sha512",
            mnemonic_normalized.encode("utf-8"),
            passphrase_normalized.encode("utf-8"),
            2048,
            dklen=64,
        )

    def derive_eth_address(
        self, account: int = 0, change: int = 0, address_index: int = 0
    ) -> dict:
        """

        Derives an Ethereum address and private key from the BIP39 mnemonic phrase.

        Parameters
            account: BIP44 account index.
            change: BIP44 change index (0 for external chain, 1 for internal chain).
            address_index: BIP44 address index.

        Returns:
            Dictionary containing the Ethereum address, private key, and public key.

        """

        bip44 = Bip44.FromSeed(self.seed_bytes, Bip44Coins.ETHEREUM)
        change_enum = Bip44Changes.CHAIN_EXT if change == 0 else Bip44Changes.CHAIN_INT
        addr = (
            bip44.Purpose().Coin().Account(account).Change(change_enum).AddressIndex(address_index)
        )
        return {
            "coin": "ETHEREUM",
            "path": f"m/44'/60'/{account}'/{change}/{address_index}",
            "address": addr.PublicKey().ToAddress(),
            "private_key": addr.PrivateKey().Raw().ToHex(),
            "public_key": addr.PublicKey().RawCompressed().ToHex(),
        }

    def derive_btc_address(
        self, account: int = 0, change: int = 0, address_index: int = 0
    ) -> dict:
        """

        Derives a Bitcoin address and private key from the BIP39 mnemonic phrase.

        Parameters
            account: BIP44 account index.
            change: BIP44 change index (0 for external chain, 1 for internal chain).
            address_index: BIP44 address index.

        Returns:
            Dictionary containing the Bitcoin address, private key, and public key.

        """

        bip44 = Bip44.FromSeed(self.seed_bytes, Bip44Coins.BITCOIN)
        change_enum = Bip44Changes.CHAIN_EXT if change == 0 else Bip44Changes.CHAIN_INT
        addr = (
            bip44.Purpose().Coin().Account(account).Change(change_enum).AddressIndex(address_index)
        )
        return {
            "coin": "BITCOIN",
            "path": f"m/44'/0'/{account}'/{change}/{address_index}",
            "address": addr.PublicKey().ToAddress(),
            "private_key": addr.PrivateKey().Raw().ToHex(),
            "public_key": addr.PublicKey().RawCompressed().ToHex(),
        }

    def get_seed_hex(self) -> str:
        return binascii.hexlify(self.seed_bytes).decode()
