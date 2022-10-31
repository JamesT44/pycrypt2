from itertools import chain, zip_longest
from random import randint, shuffle

from ciphers.cipher import Cipher


class ColumnarTransposition(Cipher):
    def encrypt(self, text, key, pad="X"):
        if isinstance(key, str):
            key = self.keyword_to_numbers(key)
        key_length = len(key)
        if pad:
            text += pad * (-len(text) % key_length)
        res = ["" for _ in range(key_length)]
        for i, col in enumerate(key):
            res[col] = text[i::key_length]
        return "".join(res)

    def decrypt(self, text, key, x=None, ):
        if isinstance(key, str):
            key = self.keyword_to_numbers(key)
        inv_key = {j: i for i, j in enumerate(key)}
        key_length = len(key)
        extra = len(text) % key_length
        col_length = len(text) // key_length
        res = ["" for _ in range(key_length)]
        for i in range(len(key)):
            chunk_length = col_length + int(inv_key[i] < extra)
            res[inv_key[i]] = text[:chunk_length]
            text = text[chunk_length:]
        return "".join(chain.from_iterable(zip_longest(*res, fillvalue="")))

    def keyword_to_numbers(self, key):
        res = [0 for _ in range(len(key))]
        idx = 0
        for c in self.alphabet:
            for i, x in enumerate(key):
                if x == c:
                    res[i] = idx
                    idx += 1
        return res

    @staticmethod
    def random_key():
        key = list(range(randint(2, 15)))
        shuffle(key)
        return key
