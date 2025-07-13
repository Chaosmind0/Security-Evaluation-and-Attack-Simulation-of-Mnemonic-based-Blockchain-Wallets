from strategy.random_attack import RandomAttackStrategy
from strategy.exhaustive_attack import ExhaustiveAttackStrategy


def get_attack_strategy(mode: str):
    """

    Get the brute-force attack strategy based on the mode.

    Parameters:
        mode (str): "random" or "exhaustive".

    Returns:
        BruteForceAttackStrategy: The brute-force attack strategy.

    """

    if mode == "random":
        return RandomAttackStrategy()
    elif mode == "exhaustive":
        return ExhaustiveAttackStrategy()
    else:
        raise ValueError(f"Unsupported attack mode: {mode}")
