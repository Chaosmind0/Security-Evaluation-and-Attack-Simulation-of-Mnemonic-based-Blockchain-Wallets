import time
from typing import Dict, List, Optional
from bip39_mnemonic_generator import BIP39MnemonicGenerator
from wallet_key_deriver import WalletKeyDeriver
from constrained_generator import ConstrainedSpec, iter_candidates

class ConstrainedAttackStrategy:
    """
    Enumerate constrained candidates and try to match the target address.
    """

    def run(self,
            word_count: int,
            per_slot_candidates: List[List[str]],
            known_positions: Dict[int, str] | None,
            bag_of_words: Optional[List[str]],
            allow_repeats: bool,
            enforce_checksum: bool,
            target_coin: str,
            max_attempts: int = 10**6,
            progress_callback=None) -> dict:

        generator = BIP39MnemonicGenerator()
        # For demo: generate a target weak mnemonic that satisfies known_positions when possible
        # (In practice, you'd pass a real target or reconstruct from partial info)
        target_mnemonic = generator.generate_mnemonic(word_count)
        target_wallet = WalletKeyDeriver(target_mnemonic)  # validates checksum
        target_addr = (target_wallet.derive_eth_address()["address"]
                       if target_coin == "ETHEREUM"
                       else target_wallet.derive_btc_address()["address"])

        spec = ConstrainedSpec(
            word_count=word_count,
            per_slot_candidates=per_slot_candidates,
            known_positions=known_positions or {},
            bag_of_words=bag_of_words,
            allow_repeats=allow_repeats,
            enforce_checksum=enforce_checksum,
        )

        attempts = 0
        start = time.time()
        for cand in iter_candidates(spec):
            attempts += 1
            if progress_callback:
                progress_callback(attempts, max_attempts)
            phrase = " ".join(cand)
            try:
                wallet = WalletKeyDeriver(phrase)  # validate=true by default
                guess_addr = (wallet.derive_eth_address()["address"]
                              if target_coin == "ETHEREUM"
                              else wallet.derive_btc_address()["address"])
                if guess_addr == target_addr:
                    elapsed = time.time() - start
                    return {
                        "success": True,
                        "attempts": attempts,
                        "time_elapsed_sec": round(elapsed, 2),
                        "target_address": target_addr,
                        "recovered_mnemonic": phrase,
                        "word_count": word_count,
                    }
            except Exception:
                # invalid mnemonic shouldn't appear because enforce_checksum=True,
                # but keep safety net
                continue

            if attempts >= max_attempts:
                break

        elapsed = time.time() - start
        return {
            "success": False,
            "attempts": attempts,
            "time_elapsed_sec": round(elapsed, 2),
            "target_address": target_addr,
            "recovered_mnemonic": "",
            "word_count": word_count,
        }