from itertools import chain
from random import randint, shuffle

from ciphers.cipher import Cipher


class Trifid(Cipher):
    def __init__(self, alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ_"):
        super(Trifid, self).__init__(alphabet)
        self.cube_length = int(len(alphabet) ** (1 / 3))
        self.cube_length2 = self.cube_length ** 2
        if self.cube_length ** 3 != self.alphabet_length:
            raise ValueError("Expected alphabet to have cube length")

    def encrypt(self, text, key, period=None):
        if not period:
            period = len(text)
        cube_index = {key[i * self.cube_length2 + j * self.cube_length + k]: (i, j, k)
                      for i in range(self.cube_length) for j in range(self.cube_length)
                      for k in range(self.cube_length)}
        slices, rows, cols = [], [], []
        for i, j, k in (cube_index[c] for c in text):
            slices.append(i)
            rows.append(j)
            cols.append(k)
        indices = list(chain.from_iterable(chain.from_iterable(list(zip(
            (slices[i:i + period] for i in range(0, len(text), period)),
            (rows[i:i + period] for i in range(0, len(text), period)),
            (cols[i:i + period] for i in range(0, len(text), period)))))))
        return "".join(key[i * self.cube_length2 + j * self.cube_length + k]
                       for i, j, k in zip(indices[::3], indices[1::3], indices[2::3]))

    def decrypt(self, text, key, period=None):
        if not period:
            period = len(text)
        cube_index = {key[i * self.cube_length2 + j * self.cube_length + k]: (i, j, k)
                      for i in range(self.cube_length) for j in range(self.cube_length)
                      for k in range(self.cube_length)}
        indices = []
        for i, j, k in (cube_index[c] for c in text):
            indices.extend((i, j, k))
        double = period * 2
        triple = period * 3
        start = 0
        res = []
        for start in range(0, len(indices) - triple, triple):
            chunk = indices[start:start + triple]
            res.extend([key[i * self.cube_length2 + j * self.cube_length + k]
                        for i, j, k in zip(chunk[:period], chunk[period:double], chunk[double:])])
        chunk = indices[start + triple:]
        period = len(chunk) // 3
        double = period * 2
        res.extend([key[i * self.cube_length2 + j * self.cube_length + k]
                    for i, j, k in zip(chunk[:period], chunk[period:double], chunk[double:])])
        return "".join(res)

    def random_key(self):
        key = list(self.alphabet)
        shuffle(key)
        return "".join(key), randint(0, 15)
