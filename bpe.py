from collections import defaultdict


class BPE():

    def __init__(self, vocab_size: int) -> None:
        self.vocab_size = vocab_size
        self.id2token = {}
        self.token2id = {}

    def fit(self, text: str):
        uniq_tokens = sorted(set(text))
        split_text = list(text)

        while len(uniq_tokens) < self.vocab_size:
            new_pair = self._get_best_pair(split_text)
            new_token = f'{new_pair[0]}{new_pair[1]}'
            uniq_tokens.append(new_token)
            buff_split_text = []
            i = 0
            while i < len(split_text):
                if new_pair == (split_text[i], split_text[i + 1]):
                    buff_split_text.append(new_token)
                    i += 2
                else:
                    buff_split_text.append(split_text[i])

            split_text = buff_split_text

        for i in range(len(uniq_tokens)):
            token = uniq_tokens[i]
            self.id2token[i] = token
            self.token2id[token] = i

    def _get_best_pair(self, split_text: list):
        pairs_count, pair_first_position = self._count_pairs(split_text)

        best_pair = None
        for pair, count in pairs_count.items():
            if best_pair is None or count > pairs_count[best_pair] \
                or (count == pairs_count[best_pair]
                    and pair_first_position[pair] < pair_first_position[best_pair]):
                best_pair = pair

        return best_pair

    def _count_pairs(self, split_text: list):
        pairs_count = defaultdict(int)
        pair_first_positions = {}
        for i in range(len(split_text) - 1):
            pair = (split_text[i], split_text[i + 1])
            pairs_count[pair] += 1

            if pair not in pair_first_positions:
                pair_first_positions[pair] = i

        return (pairs_count, pair_first_positions)
