import os
import csv
from attack_factory import get_attack_strategy


def batch_test_and_save_report(
    test_cases: dict, mode: str, report_path: str = "report/brute_force_results.csv"
) -> None:
    """

    Runs a batch of test cases and saves the results to a CSV file.

    Parameters:
        test_cases (list[dict]): List of test cases.
        mode (str): Attack mode.
        report_path (str): Path to save the report.

    Returns:
        None.

    """

    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    strategy = get_attack_strategy(mode)

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
            result = strategy.run(**case)
            writer.writerow(result)
            print(
                f"Test completed. Success: {result['success']}, Attempts: {result['attempts']}, Time: {result['time_elapsed_sec']}s\n"
            )


def generate_multiple_test_cases(base_case: dict, repeat: int = 4) -> list[dict]:
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

    batch_test_and_save_report(test_cases, "exhaustive")
