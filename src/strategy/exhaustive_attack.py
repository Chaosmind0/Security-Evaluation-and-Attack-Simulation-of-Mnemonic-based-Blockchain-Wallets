from strategy.base_strategy import BruteForceAttackStrategy
from attack_core import exhaustive_brute_force_attack


class ExhaustiveAttackStrategy(BruteForceAttackStrategy):
    """

    Exhaustive brute-force attack strategy.

    """

    def run(self, **kwargs) -> dict:
        return exhaustive_brute_force_attack(**kwargs)
