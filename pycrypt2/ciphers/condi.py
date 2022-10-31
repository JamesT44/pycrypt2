from random import randint, shuffle

from ciphers.cipher import Cipher


class Condi(Cipher):
    def encrypt(self, text, key, offset=0):
        key_index = {c: i for i, c in enumerate(key)}
        key_length = len(key)
        res = [key[(key_index[text[0]] + offset) % key_length]]
        for i, c in enumerate(text[1:]):
            res.append(key[(key_index[text[i]] + key_index[c] + 1) % key_length])
        return "".join(res)

    def decrypt(self, text, key, offset=0):
        key_index = {c: i for i, c in enumerate(key)}
        key_length = len(key)
        res = [key[(key_index[text[0]] - offset) % key_length]]
        for i, c in enumerate(text[1:]):
            res.append(key[(key_index[c] - key_index[res[-1]] - 1) % key_length])
        return "".join(res)

    def random_key(self):
        key = list(self.alphabet)
        shuffle(key)
        return "".join(key), randint(0, 25)
