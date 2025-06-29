import time
from bip39_mnemonic_generator import BIP39MnemonicGenerator
from wallet_key_deriver import WalletKeyDeriver


def simulate_brute_force_attack(
    word_count: int = 12,
    weak_pool_size: int = 64,
    pool_start: int = 0,
    prefix: list[str] = ["abandon", "abandon", "abandon"],
    allow_repeats: bool = True,
    target_coin: str = "ETHEREUM",
    max_attempts: int = 1000000,  # 10^6
):
    """

    Simulates a brute-force attack to recover a low-entropy wallet mnemonic.

    Parameters:
        word_count (int): Number of words in the mnemonic.
        weak_pool_size (int): Size of weak entropy pool.
        pool_start (int): Start index of weak pool.
        prefix (list[str]): Known prefix words in mnemonic.
        allow_repeats (bool): Allow repeated words.
        target_coin (str): "ETHEREUM" or "BITCOIN".
        max_attempts (int): Max number of attempts before stopping.

    Returns:
        None. Prints result to console.

    """
    generator = BIP39MnemonicGenerator()

    # Step 1: Generate a target weak mnemonic and derive its address
    target_mnemonic = generator.generate_weak_mnemonic(
        word_count=word_count,
        weak_pool_size=weak_pool_size,
        pool_start=pool_start,
        allow_repeats=allow_repeats,
        prefix=prefix,
    )

    target_wallet = WalletKeyDeriver(target_mnemonic, validate=False)
    if target_coin == "ETHEREUM":
        target_address = target_wallet.derive_eth_address()["address"]
    elif target_coin == "BITCOIN":
        target_address = target_wallet.derive_btc_address()["address"]
    else:
        raise ValueError("Unsupported coin type")

    print(f"Target {target_coin} address: {target_address}")
    print(f"Target mnemonic: {target_mnemonic}")
    print("Starting brute-force attack...\n")

    # Step 2: Start brute-force attempts
    start_time = time.time()
    for attempt in range(1, max_attempts + 1):
        guess_mnemonic = generator.generate_weak_mnemonic(
            word_count=word_count,
            weak_pool_size=weak_pool_size,
            pool_start=pool_start,
            allow_repeats=allow_repeats,
            prefix=prefix,
        )
        try:
            guess_wallet = WalletKeyDeriver(guess_mnemonic, validate=False)
            guess_address = (
                guess_wallet.derive_eth_address()["address"]
                if target_coin == "ETHEREUM"
                else guess_wallet.derive_btc_address()["address"]
            )

            if guess_address == target_address:
                elapsed = time.time() - start_time
                print("Address match found!")
                print(f"Recovered mnemonic: {guess_mnemonic}")
                print(f"Attempts: {attempt}")
                print(f"Time elapsed: {elapsed:.2f} seconds")
                return
        except Exception as e:
            continue  # Invalid mnemonic

    print("Failed to recover mnemonic within max attempts.")


if __name__ == "__main__":
    simulate_brute_force_attack()
