from random import shuffle

from ciphers.cipher import Cipher


class SimpleSubstitution(Cipher):
    def encrypt(self, text, key):
        return "".join(key[self.alphabet_index[c]] for c in text)

    def decrypt(self, text, key):
        key_index = {c: i for i, c in enumerate(key)}
        return "".join(self.alphabet[key_index[c]] for c in text)

    def random_key(self):
        key = list(self.alphabet)
        shuffle(key)
        return "".join(key)
