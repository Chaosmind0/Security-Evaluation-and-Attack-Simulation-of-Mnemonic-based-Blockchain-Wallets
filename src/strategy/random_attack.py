from strategy.base_strategy import BruteForceAttackStrategy
from simulate_brute_force_attack import simulate_brute_force_attack

class RandomAttackStrategy(BruteForceAttackStrategy):
    """
    
    Random brute-force attack strategy.

    """
    
    def run(self, **kwargs) -> dict:
        return simulate_brute_force_attack(**kwargs)
