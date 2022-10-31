from random import randint, shuffle

from ciphers.cipher import Cipher
from ciphers.columnar_transposition import ColumnarTransposition


class ADFGX(Cipher):
    def __init__(self, alphabet="ABCDEFGHIKLMNOPQRSTUVWXYZ", key_letters="ADFGX"):
        super(ADFGX, self).__init__(alphabet)
        self.grid_length = int(len(alphabet) ** 0.5)
        if self.grid_length ** 2 != self.alphabet_length:
            raise ValueError("Expected alphabet to have square length")
        if self.grid_length != len(key_letters):
            raise ValueError("Expected key_letters to have length {}".format(self.grid_length))
        self.key_letters = key_letters
        self.key_letters_index = {c: i for i, c in enumerate(key_letters)}
        self.transpo = ColumnarTransposition(alphabet)

    def encrypt(self, text, key):
        grid_index = {c: self.key_letters[i // self.grid_length] + self.key_letters[i % self.grid_length]
                      for i, c in enumerate(key[0])}
        return self.transpo.encrypt("".join(grid_index[c] for c in text), key[1], None)

    def decrypt(self, text, key):
        res = self.transpo.decrypt(text, key[1])
        return "".join(key[0][self.key_letters_index[a] * self.grid_length + self.key_letters_index[b]]
                       for a, b in zip(res[::2], res[1::2]))

    def random_key(self):
        key = [list(self.alphabet), list(range(randint(2, 15)))]
        shuffle(key[0])
        shuffle(key[1])
        return ["".join(key[0]), key[1]]
