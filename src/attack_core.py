import time
from bip39_mnemonic_generator import BIP39MnemonicGenerator
from unsafe_wallet_key_deriver import UnsafeWalletKeyDeriver
from tqdm import tqdm
import itertools
import math
from typing import List

def check_parameters(prefix: list[str], word_count: int, weak_pool_size: int, pool_start: int) -> None:
    """

    Checks the validity of the attack parameters.

    Parameters:
        prefix (list[str]): Known prefix words in mnemonic.
        word_count (int): Number of words in the mnemonic.
        weak_pool_size (int): Size of weak entropy pool.
        pool_start (int): Start index of weak pool.
    
    Returns:
        None.

    """

    assert len(prefix) <= word_count, "Prefix length exceeds word count"
    assert word_count in [12, 24], "Word count must be 12 or 24"
    assert weak_pool_size <= 2048, "Weak pool size must be <= 2048"
    assert pool_start >= 0, "Pool start index must be >= 0"
    assert pool_start + weak_pool_size <= 2048, "Pool start + weak pool size must be <= 2048"


def estimate_brute_force_security(pool_size: int, word_count: int, prefix_length: int, max_attempts: int, allow_repeats: bool = True) -> dict:
    """
    
    Calculates the success probability and entropy of a brute-force attack.

    Parameters:
        pool_size (int): Size of weak entropy pool.
        word_count (int): Number of words in the mnemonic.
        prefix_length (int): Length of known prefix in the mnemonic.
        max_attempts (int): Max number of attempts before stopping.
        allow_repeats (bool): Allow repeated words.

    Returns:
        Dictionary with the results of the attack.

    """
    
    r = word_count - prefix_length
    N = pool_size
    T = max_attempts

    # Total combinations calculation
    if allow_repeats:
        total_combinations = N ** r
    else:
        if N < r:
            return {"success_probability": 0, "entropy": 0}
        total_combinations = math.perm(N, r)  # Number of combinations without repetitions

    # Success probability calculation
    success_prob = T / total_combinations

    # Entropy value calculation (in bits)
    entropy = r * math.log2(N) if N > 0 else 0

    print("Total combinations: " + str(total_combinations))
    print("Success probability: " + str(success_prob))
    print("entropy bits: " + str(entropy))

    return {
        "total_combinations": total_combinations,
        "success_probability": success_prob,
        "entropy_bits": entropy
    }


# Define a function to simulate an exhaustive brute-force attack using itertools.product
def exhaustive_brute_force_attack(
    word_count: int = 6,
    weak_pool_size: int = 16,
    pool_start: int = 0,
    prefix: List[str] = None,
    allow_repeats: bool = True,
    target_coin: str = "ETHEREUM",
    max_attempts: int = 10**6,
    progress_callback=None
) -> dict:
    """
    
    Simulates an exhaustive brute-force attack to recover a low-entropy wallet mnemonic.

    Parameters:
        word_count (int): Number of words in the mnemonic.
        weak_pool_size (int): Size of weak entropy pool.
        pool_start (int): Start index of weak pool.
        prefix (list[str]): Known prefix words in mnemonic.
        allow_repeats (bool): Allow repeated words.
        target_coin (str): "ETHEREUM" or "BITCOIN".
        max_attempts (int): Max number of attempts before stopping.
        progress_callback (function): Callback function to report progress.

    Returns:
        Dictionary with the results of the attack.

    """
    
    generator = BIP39MnemonicGenerator()

    result = {
        "word_count": word_count,
        "weak_pool_size": weak_pool_size,
        "pool_start": pool_start,
        "prefix": " ".join(prefix),
        "allow_repeats": allow_repeats,
        "target_coin": target_coin,
        "max_attempts": max_attempts,
        "success": False,
        "attempts": 0,
        "time_elapsed_sec": 0,
        "target_address": "",
        "recovered_mnemonic": "",
    }
    
    wordlist = generator.wordlist
    pool = wordlist[pool_start : pool_start + weak_pool_size]

    if prefix is None:
        prefix = []

    remaining = word_count - len(prefix)
    total_combinations = len(pool) ** remaining
    print(f"Total combinations to search: {total_combinations}")

    # Generate the target mnemonic
    target_mnemonic = generator.generate_weak_mnemonic(
        word_count=word_count,
        weak_pool_size=weak_pool_size,
        pool_start=pool_start,
        allow_repeats=allow_repeats,
        prefix=prefix,
    )
    print(f"Target mnemonic: {target_mnemonic}")
    target_wallet = UnsafeWalletKeyDeriver(target_mnemonic)
    target_address = (
        target_wallet.derive_eth_address()["address"]
        if target_coin == "ETHEREUM"
        else target_wallet.derive_btc_address()["address"]
    )
    print(f"Target {target_coin} address: {target_address}")

    start_time = time.time()
    attempts = 0

    for idx, combo in tqdm(itertools.product(pool, repeat=remaining), total=total_combinations, desc="Exhaustive search"):
        mnemonic = prefix + list(combo)
        mnemonic_str = " ".join(mnemonic)
        try:
            # Send progress update to callback function
            if progress_callback:
                progress_callback(idx + 1, max_attempts)

            wallet = UnsafeWalletKeyDeriver(mnemonic_str)
            guess_address = (
                wallet.derive_eth_address()["address"]
                if target_coin == "ETHEREUM"
                else wallet.derive_btc_address()["address"]
            )
            attempts += 1
            if guess_address == target_address:
                elapsed = time.time() - start_time

                result["success"] = True
                result["attempts"] = attempts
                result["time_elapsed_sec"] = round(time.time() - start_time, 2)
                result["recovered_mnemonic"] = target_mnemonic
                return result
            if attempts >= max_attempts:
                break
        except Exception:
            continue

    elapsed = time.time() - start_time

    result["success"] = False
    result["attempts"] = attempts
    result["time_elapsed_sec"] = elapsed
    result["mnemonic"] = None
    result["target_address"] = target_address
    return result


def simulate_brute_force_attack(
    word_count: int = 12,
    weak_pool_size: int = 64,
    pool_start: int = 0,
    prefix: list[str] = ["abandon", "abandon", "abandon"],
    allow_repeats: bool = True,
    target_coin: str = "ETHEREUM",
    max_attempts: int = 10**6,
    progress_callback=None
) -> dict:
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
        progress_callback (function): Callback function to report progress.

    Returns:
        Dictionary with the results of the attack.

    """

    generator = BIP39MnemonicGenerator()
    result = {
        "word_count": word_count,
        "weak_pool_size": weak_pool_size,
        "pool_start": pool_start,
        "prefix": " ".join(prefix),
        "allow_repeats": allow_repeats,
        "target_coin": target_coin,
        "max_attempts": max_attempts,
        "success": False,
        "attempts": 0,
        "time_elapsed_sec": 0,
        "target_address": "",
        "recovered_mnemonic": "",
    }

    # Step 1: Generate a target weak mnemonic and derive its address
    target_mnemonic = generator.generate_weak_mnemonic(
        word_count=word_count,
        weak_pool_size=weak_pool_size,
        pool_start=pool_start,
        allow_repeats=allow_repeats,
        prefix=prefix,
    )

    target_wallet = UnsafeWalletKeyDeriver(target_mnemonic)
    if target_coin == "ETHEREUM":
        target_address = target_wallet.derive_eth_address()["address"]
    elif target_coin == "BITCOIN":
        target_address = target_wallet.derive_btc_address()["address"]
    else:
        raise ValueError("Unsupported coin type")

    result["target_address"] = target_address

    print(f"Target {target_coin} address: {target_address}")
    print(f"Target mnemonic: {target_mnemonic}")
    print("Starting brute-force attack...\n")

    # Step 2: Start brute-force attempts
    start_time = time.time()
    for attempt in tqdm(range(1, max_attempts + 1), desc="Brute-force progress"):
        guess_mnemonic = generator.generate_weak_mnemonic(
            word_count=word_count,
            weak_pool_size=weak_pool_size,
            pool_start=pool_start,
            allow_repeats=allow_repeats,
            prefix=prefix,
        )
        try:
            # Send progress update to callback function
            if progress_callback:
                progress_callback(attempt, max_attempts)

            guess_wallet = UnsafeWalletKeyDeriver(guess_mnemonic)
            guess_address = (
                guess_wallet.derive_eth_address()["address"]
                if target_coin == "ETHEREUM"
                else guess_wallet.derive_btc_address()["address"]
            )

            if guess_address == target_address:
                elapsed = time.time() - start_time
                result["success"] = True
                result["attempts"] = attempt
                result["time_elapsed_sec"] = round(time.time() - start_time, 2)
                result["recovered_mnemonic"] = guess_mnemonic

                print("Address match found!")
                print(f"Recovered mnemonic: {guess_mnemonic}")
                print(f"Attempts: {attempt}")
                print(f"Time elapsed: {elapsed:.2f} seconds")
                break
        except Exception as e:
            continue  # Invalid mnemonic
    if not result["success"]:
        result["attempts"] = max_attempts
        result["time_elapsed_sec"] = round(time.time() - start_time, 2)

        print("Failed to recover mnemonic within max attempts.")

    return result