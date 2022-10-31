from itertools import chain, zip_longest
from random import choice, randint

from ciphers.cipher import Cipher


class Myszkowski(Cipher):
    def encrypt(self, text, key):
        key_length = len(key)
        key_index = {}
        for i, c in enumerate(key):
            if c in key_index:
                key_index[c].append(i)
            else:
                key_index[c] = [i]
        res = []
        for c in sorted(key_index.keys()):
            res.extend(chain(*zip_longest(*(text[col::key_length] for col in key_index[c]), fillvalue="")))
        return "".join(res)

    def decrypt(self, text, key):
        key_length = len(key)
        key_index = {}
        for i, c in enumerate(key):
            if c in key_index:
                key_index[c].append(i)
            else:
                key_index[c] = [i]
        col_length = len(text) // key_length
        extra = len(text) % key_length
        res = ["" for _ in range(key_length)]
        for c in sorted(key_index.keys()):
            cols = key_index[c]
            cols_length = len(cols)
            chunk_length = col_length * cols_length + sum(col < extra for col in cols)
            chunk = text[:chunk_length]
            text = text[chunk_length:]
            for i, col in enumerate(cols):
                res[col] = chunk[i::cols_length]
        res = list(chain(*zip_longest(*res, fillvalue="")))
        return "".join(res)

    def random_key(self):
        return "".join(choice(self.alphabet) for _ in range(randint(2, 15)))
