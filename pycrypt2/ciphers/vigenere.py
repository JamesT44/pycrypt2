from random import choice, randint

from ciphers.cipher import Cipher


class Vigenere(Cipher):
    def encrypt(self, text, key):
        period = len(key)
        shifts = [self.alphabet_index[c] for c in key] if isinstance(key, str) else key
        return "".join(self.alphabet[(self.alphabet_index[c] + shifts[i % period]) % self.alphabet_length]
                       for i, c in enumerate(text))

    def decrypt(self, text, key):
        period = len(key)
        shifts = [self.alphabet_index[c] for c in key] if isinstance(key, str) else key
        return "".join(self.alphabet[(self.alphabet_index[c] - shifts[i % period]) % self.alphabet_length]
                       for i, c in enumerate(text))

    def random_key(self):
        return "".join(choice(self.alphabet) for _ in range(randint(2, 15)))
