from typing import Dict, List, Iterable, Optional
from collections import Counter
from bip_utils import Bip39MnemonicValidator

class ConstrainedSpec:

    def __init__(
        self,
        word_count: int,
        per_slot_candidates: List[List[str]],
        known_positions: Optional[Dict[int, str]] = None,
        bag_of_words: Optional[List[str]] = None,
        allow_repeats: bool = True,
        enforce_checksum: bool = True,
    ):
        """
        Specification for constrained candidate generation.

        Parameters:
            word_count: target mnemonic length (12/15/18/21/24)
            per_slot_candidates: per-position candidate lists (already filtered by first-letter/prefix)
            known_positions: fixed words at positions (0-based)
            bag_of_words: multiset of words to be used unordered across unknown slots (optional)
            allow_repeats: whether words can repeat across slots
            enforce_checksum: validate with BIP39 checksum before yielding

        """

        self.word_count = word_count
        self.per_slot_candidates = per_slot_candidates
        self.known_positions = known_positions or {}
        self.bag_of_words = bag_of_words
        self.allow_repeats = allow_repeats
        self.enforce_checksum = enforce_checksum

def iter_candidates(spec: ConstrainedSpec) -> Iterable[List[str]]:
    """

    Backtracking generator that yields ONLY valid candidates under constraints.
    For bag_of_words: we keep a multiset counter and ensure counts don't go negative.
    For allow_repeats=False: maintain a 'used' set.
    BIP39 checksum is checked only on full-length sequences for performance.

    Parameters:
        spec: ConstrainedSpec class object

    Returns:
        Iterable of list

    """
    wc = spec.word_count
    kp = spec.known_positions
    bag_counter = Counter(spec.bag_of_words) if spec.bag_of_words else None
    used = set()

    cur: List[str] = []

    def backtrack(pos: int):
        if pos == wc:
            phrase = " ".join(cur)
            if not spec.enforce_checksum or Bip39MnemonicValidator().IsValid(phrase):
                yield list(cur)
            return

        # fixed position
        if pos in kp:
            w = kp[pos]
            # bag_of_words constraint if provided
            if bag_counter is not None and bag_counter[w] <= 0:
                return
            cur.append(w)
            if not spec.allow_repeats:
                if w in used:
                    cur.pop()
                    return
                used.add(w)
            if bag_counter is not None:
                bag_counter[w] -= 1

            yield from backtrack(pos + 1)

            if bag_counter is not None:
                bag_counter[w] += 1
            if not spec.allow_repeats:
                used.discard(w)
            cur.pop()
            return

        # variable position: iterate its candidate list
        for w in spec.per_slot_candidates[pos]:
            if not spec.allow_repeats and w in used:
                continue
            if bag_counter is not None and bag_counter[w] <= 0:
                continue

            cur.append(w)
            if not spec.allow_repeats:
                used.add(w)
            if bag_counter is not None:
                bag_counter[w] -= 1

            yield from backtrack(pos + 1)

            if bag_counter is not None:
                bag_counter[w] += 1
            if not spec.allow_repeats:
                used.discard(w)
            cur.pop()

    yield from backtrack(0)