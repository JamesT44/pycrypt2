from random import choice, randint
from string import ascii_uppercase

from ciphers.cipher import Cipher


class Porta(Cipher):
    def __init__(self, alphabet=ascii_uppercase):
        super(Porta, self).__init__(alphabet)
        if self.alphabet_length % 2:
            raise ValueError("Expected alphabet to have even length")
        self.middle = self.alphabet_length // 2
        self.tableau = [self.alphabet[self.middle + shift:] + self.alphabet[self.middle:self.middle + shift] +
                        self.alphabet[self.middle - shift:self.middle] + self.alphabet[:self.middle - shift]
                        for shift in range(self.middle)]

    def encrypt(self, text, key):
        period = len(key)
        rows = [self.tableau[self.alphabet_index[c] // 2] for c in key]
        return "".join(rows[i % period][self.alphabet_index[c]] for i, c in enumerate(text))

    def decrypt(self, text, key):
        return self.encrypt(text, key)

    def random_key(self):
        return "".join(choice(self.alphabet) for _ in range(randint(2, 15)))
