from collections import defaultdict


class BPE():

    def __init__(self, vocab_size: int) -> None:
        self.vocab_size = vocab_size

    def fit(self, text: str):
        uniq_tokens = sorted(set(text))
        split_text = list(text)

        while len(uniq_tokens) < self.vocab_size:

    def _get_best_pair(self, split_text: list):
        pairs_count, pair_first_position = self._count_pairs(split_text)

        best = None
        for pair, count in pairs_count:

    def _count_pairs(self, split_text: list):
        pairs_count = defaultdict(int)
        pair_first_positions = {}
        for i in range(len(split_text) - 1):
            pair = (split_text[i], split_text[i + 1])
            pairs_count[pairs_count] += 1

            if pair not in pair_first_positions:
                pair_first_positions[pair_first_positions] = i

        return (pairs_count, pair_first_positions)
