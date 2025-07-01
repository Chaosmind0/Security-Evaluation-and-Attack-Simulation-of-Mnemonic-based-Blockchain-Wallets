import os
import csv
import time
from bip39_mnemonic_generator import BIP39MnemonicGenerator
from unsafe_wallet_key_deriver import UnsafeWalletKeyDeriver
from tqdm import tqdm


def simulate_brute_force_attack(
    word_count: int = 12,
    weak_pool_size: int = 64,
    pool_start: int = 0,
    prefix: list[str] = ["abandon", "abandon", "abandon"],
    allow_repeats: bool = True,
    target_coin: str = "ETHEREUM",
    max_attempts: int = 10**4,
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


def batch_test_and_save_report(
    test_cases: dict, report_path: str = "report/brute_force_results.csv"
) -> None:
    """

    Runs a batch of test cases and saves the results to a CSV file.

    Parameters:
        test_cases (list[dict]): List of test cases.
        report_path (str): Path to save the report.

    Returns:
        None.

    """

    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    with open(report_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "word_count",
                "weak_pool_size",
                "pool_start",
                "prefix",
                "allow_repeats",
                "target_coin",
                "max_attempts",
                "success",
                "attempts",
                "time_elapsed_sec",
                "target_address",
                "recovered_mnemonic",
            ],
        )
        writer.writeheader()

        for case in test_cases:
            print(f"Running test case: {case}")
            result = simulate_brute_force_attack(**case)
            writer.writerow(result)
            print(
                f"Test completed. Success: {result['success']}, Attempts: {result['attempts']}, Time: {result['time_elapsed_sec']}s\n"
            )


def generate_test_cases(base_case: dict, repeat: int = 4) -> list[dict]:
    """

    Uses a base case to generate multiple test cases with different parameters.

    Parameters:
        base_case (dict): Base case parameters.
        repeat (int): Number of test cases to generate.

    Returns:
        List of test cases.

    """

    return [base_case.copy() for _ in range(repeat)]


if __name__ == "__main__":
    test_cases = []

    for word_count in [12, 24]:
        for weak_pool_size in [32, 64]:
            for prefix_len in range(3, 7):
                for allow_repeats in [True, False]:
                    for target_coin in ["ETHEREUM", "BITCOIN"]:
                        case = {
                            "word_count": word_count,
                            "weak_pool_size": weak_pool_size,
                            "pool_start": 0,
                            "prefix": ["abandon"] * prefix_len,
                            "allow_repeats": allow_repeats,
                            "target_coin": target_coin,
                        }
                        test_cases.extend(generate_test_cases(case, repeat=4))

    batch_test_and_save_report(test_cases)
