from random import shuffle

from ciphers.cipher import Cipher


class Playfair(Cipher):
    def __init__(self, alphabet="ABCDEFGHIKLMNOPQRSTUVWXYZ", sub_character="X"):
        super(Playfair, self).__init__(alphabet)
        self.grid_length = int(len(alphabet) ** 0.5)
        if self.grid_length ** 2 != self.alphabet_length:
            raise ValueError("Expected alphabet to have square length")
        self.sub_character = sub_character

    def encrypt(self, text, key):
        grid_length = self.grid_length
        grid_index = {key[i * grid_length + j]: (i, j) for i in range(grid_length)
                      for j in range(grid_length)}
        if len(text) % 2:
            text += self.sub_character
        text = "".join(self.sub_character if i % 2 and c == text[i - 1] else c for i, c in enumerate(text))
        res = []
        for a, b in zip(text[::2], text[1::2]):
            (ai, aj), (bi, bj) = grid_index[a], grid_index[b]
            if ai == bi:
                aj += 1
                aj %= grid_length
                bj += 1
                bj %= grid_length
            elif aj == bj:
                ai += 1
                ai %= grid_length
                bi += 1
                bi %= grid_length
            else:
                aj, bj = bj, aj
            res.extend((key[ai * grid_length + aj], key[bi * grid_length + bj]))
        return "".join(res)

    def decrypt(self, text, key):
        grid_length = self.grid_length
        grid_index = {key[i * grid_length + j]: (i, j) for i in range(grid_length)
                      for j in range(grid_length)}
        res = []
        for a, b in zip(text[::2], text[1::2]):
            (ai, aj), (bi, bj) = grid_index[a], grid_index[b]
            if ai == bi:
                aj -= 1
                aj %= grid_length
                bj -= 1
                bj %= grid_length
            elif aj == bj:
                ai -= 1
                ai %= grid_length
                bi -= 1
                bi %= grid_length
            else:
                aj, bj = bj, aj
            res.extend((key[ai * grid_length + aj], key[bi * grid_length + bj]))
        return "".join(res)

    def random_key(self):
        key = list(self.alphabet)
        shuffle(key)
        return "".join(key)

    def align_keyword(self, key):
        assert len(key) == self.alphabet_length
        rows = [key[i:i + self.grid_length] for i in range(0, self.alphabet_length, self.grid_length)]
        best = (0, "")
        for _ in range(self.grid_length):
            for _ in range(self.grid_length):
                shifted_key = "".join(rows)
                prev = self.alphabet_index[shifted_key[-1]]
                count = 1

                for c in shifted_key[-2::-1]:
                    curr = self.alphabet_index[c]
                    if curr < prev:
                        count += 1
                        prev = curr
                    else:
                        break
                best = max((count, shifted_key), best)
                rows.append(rows.pop(0))
            rows = [row[1:] + row[0] for row in rows]

        return best[1]
