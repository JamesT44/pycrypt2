from random import randint

from math import gcd
from sympy import Matrix

from ciphers.cipher import Cipher


class Hill(Cipher):
    def encrypt(self, text, key, pad="X"):
        if not isinstance(key, Matrix):
            if isinstance(key[0], list):
                key = Matrix(key)
            else:
                key_length = int(len(key) ** 0.5)
                key = Matrix(key_length, key_length, key)
        key_length = int(len(key) ** 0.5)
        text += pad * (-len(text) % key_length)
        res = []
        for i in range(0, len(text), key_length):
            block = Matrix([self.alphabet_index[c] for c in text[i:i + key_length]])
            res.append("".join(self.alphabet[i % self.alphabet_length] for i in key * block))
        return "".join(res)

    def decrypt(self, text, key):
        if not isinstance(key, Matrix):
            if isinstance(key[0], list):
                key = Matrix(key)
            else:
                key_length = int(len(key) ** 0.5)
                key = Matrix(key_length, key_length, key)
        return self.encrypt(text, self.inverse_key(key))

    def random_key(self):
        key_length = randint(2, 6)
        res = Matrix(key_length, key_length, [randint(0, self.alphabet_length - 1) for _ in range(key_length ** 2)])
        if gcd(self.alphabet_length, res.det()) != 1:
            return self.random_key()
        return res

    def inverse_key(self, key):
        if not isinstance(key, Matrix):
            key = Matrix(key)
        return key.inv_mod(self.alphabet_length)
