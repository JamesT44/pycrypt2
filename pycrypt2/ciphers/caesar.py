from random import randint

from ciphers.cipher import Cipher


class Caesar(Cipher):
    def encrypt(self, text, key):
        return "".join(self.alphabet[(self.alphabet_index[c] + key) % self.alphabet_length] for c in text)

    def decrypt(self, text, key):
        return "".join(self.alphabet[(self.alphabet_index[c] - key) % self.alphabet_length] for c in text)

    def random_key(self):
        return randint(1, len(self.alphabet))
