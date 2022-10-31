from itertools import chain
from random import randint, shuffle

from ciphers.cipher import Cipher


class Digrafid(Cipher):
    def __init__(self, alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ_", pad="X"):
        super(Digrafid, self).__init__(alphabet)
        if self.alphabet_length != 27:
            raise ValueError("Expected alphabet to have length 27")
        self.pad = pad

    def encrypt(self, text, key, period=None):
        if period is None:
            period = len(text)
        grid_index = [{c: (j % 9, j // 9) for j, c in enumerate(key[i])} for i in range(2)]
        if len(text) % 2:
            text += self.pad
        cols, mids, rows = [], [], []
        for a, b in zip(text[::2], text[1::2]):
            (cola, rowa), (rowb, colb) = grid_index[0][a], grid_index[1][b]
            cols.append(cola)
            mids.append(rowa * 3 + colb)
            rows.append(rowb)

        indices = list(chain.from_iterable(chain.from_iterable(list(zip(
            (cols[i:i + period] for i in range(0, len(text), period)),
            (mids[i:i + period] for i in range(0, len(text), period)),
            (rows[i:i + period] for i in range(0, len(text), period)))))))
        return "".join(key[0][9 * (j // 3) + i] + key[1][9 * (j % 3) + k]
                       for i, j, k in zip(indices[::3], indices[1::3], indices[2::3]))

    def decrypt(self, text, key, period=None):
        if period is None:
            period = len(text)
        grid_index = [{c: (j % 9, j // 9) for j, c in enumerate(key[i])} for i in range(2)]
        indices = []
        for a, b in zip(text[::2], text[1::2]):
            (cola, rowa), (rowb, colb) = grid_index[0][a], grid_index[1][b]
            indices.extend((cola, rowa * 3 + colb, rowb))

        double = period * 2
        triple = period * 3
        start = 0
        res = []
        for start in range(0, len(indices) - triple, triple):
            chunk = indices[start:start + triple]
            res.extend([key[0][9 * (j // 3) + i] + key[1][9 * (j % 3) + k]
                        for i, j, k in zip(chunk[:period], chunk[period:double], chunk[double:])])
        chunk = indices[start + triple:]
        period = len(chunk) // 3
        double = period * 2
        res.extend([key[0][9 * (j // 3) + i] + key[1][9 * (j % 3) + k]
                    for i, j, k in zip(chunk[:period], chunk[period:double], chunk[double:])])
        return "".join(res)

    def random_key(self):
        key = list(self.alphabet)
        shuffle(key)
        key2 = key[:]
        shuffle(key)
        return ("".join(key), "".join(key2)), randint(2, 15)
