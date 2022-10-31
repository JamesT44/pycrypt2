from itertools import chain
from random import randint, shuffle

from ciphers.cipher import Cipher


class Bifid(Cipher):
    def __init__(self, alphabet="ABCDEFGHIKLMNOPQRSTUVWXYZ"):
        super(Bifid, self).__init__(alphabet)
        self.grid_length = int(len(alphabet) ** 0.5)
        if self.grid_length ** 2 != self.alphabet_length:
            raise ValueError("Expected alphabet to have square length")

    def encrypt(self, text, key, period=None):
        if not period:
            period = len(text)
        grid_index = {key[i * self.grid_length + j]: (i, j) for i in range(self.grid_length)
                      for j in range(self.grid_length)}
        rows, cols = [], []
        for i, j in (grid_index[c] for c in text):
            rows.append(i)
            cols.append(j)
        indices = list(chain.from_iterable(chain.from_iterable(list(zip(
            (rows[i:i + period] for i in range(0, len(text), period)),
            (cols[i:i + period] for i in range(0, len(text), period)))))))
        return "".join(key[i * self.grid_length + j] for i, j in zip(indices[::2], indices[1::2]))

    def decrypt(self, text, key, period=None):
        if not period:
            period = len(text)
        grid_index = {key[i * self.grid_length + j]: (i, j) for i in range(self.grid_length)
                      for j in range(self.grid_length)}
        indices = []
        for i, j in (grid_index[c] for c in text):
            indices.extend((i, j))
        double = period * 2
        start = 0
        res = []
        for start in range(0, len(indices) - double, double):
            chunk = indices[start:start + double]
            res.extend([key[i * self.grid_length + j] for i, j in zip(chunk[:period], chunk[period:])])
        chunk = indices[start + double:]
        period = len(chunk) // 2
        res.extend([key[i * self.grid_length + j] for i, j in zip(chunk[:period], chunk[period:])])
        return "".join(res)

    def random_key(self):
        key = list(self.alphabet)
        shuffle(key)
        return "".join(key), randint(0, 20)
