from collections import defaultdict
import dill


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
            while i < len(split_text) - 1:
                if new_pair == (split_text[i], split_text[i + 1]):
                    buff_split_text.append(new_token)
                    i += 2
                else:
                    buff_split_text.append(split_text[i])
                    i += 1

            if i < len(split_text):
                buff_split_text.append(split_text[i])

            split_text = buff_split_text

        for i in range(len(uniq_tokens)):
            token = uniq_tokens[i]
            self.id2token[i] = token
            self.token2id[token] = i

    def decode(self, token_ids):
        text = ''
        for token_id in token_ids:
            text += self.id2token[token_id]

        return text

    def encode(self, text: str):
        encoded_text = []
        while len(text) > 0:
            symbol = text[0]

            suitable_token_keys = [
                key for key in self.token2id if key.startswith(symbol)]

            suitable_token_keys = sorted(
                suitable_token_keys, key=len, reverse=True)

            for token_key in suitable_token_keys:
                if text.startswith(token_key):
                    encoded_text.append(self.token2id[token_key])
                    text = text[len(token_key):]

        return encoded_text

    def save(self, filename):
        with open(filename, 'wb') as f:
            dill.dump(self, f)
        print(f"Объект сохранён в {filename}")

    @classmethod
    def load(cls, filename):
        with open(filename, 'rb') as f:
            obj = dill.load(f)

        print(f"Объект загружен из {filename}")
        return obj

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
