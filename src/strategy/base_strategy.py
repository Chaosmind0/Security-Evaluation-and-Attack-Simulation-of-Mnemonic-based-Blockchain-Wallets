from abc import ABC, abstractmethod


class BruteForceAttackStrategy(ABC):
    """

    Abstract base class for brute-force attack strategies.

    """

    @abstractmethod
    def run(self, **kwargs) -> dict:
        """Run the attack and return result dict"""
        pass
