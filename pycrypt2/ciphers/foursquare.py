from random import shuffle

from ciphers.cipher import Cipher


class Foursquare(Cipher):
    def __init__(self, alphabet="ABCDEFGHIKLMNOPQRSTUVWXYZ", pad="X"):
        super(Foursquare, self).__init__(alphabet)
        self.grid_length = int(len(alphabet) ** 0.5)
        if self.grid_length ** 2 != self.alphabet_length:
            raise ValueError("Expected alphabet to have square length")
        self.grid_index = {self.alphabet[i * self.grid_length + j]: (i, j) for i in range(self.grid_length)
                           for j in range(self.grid_length)}
        self.pad = pad

    def encrypt(self, text, key):
        if len(text) % 2:
            text += self.pad
        res = []
        for a, b in zip(text[::2], text[1::2]):
            (ai, aj), (bi, bj) = self.grid_index[a], self.grid_index[b]
            res.extend((key[0][ai * self.grid_length + bj], key[1][bi * self.grid_length + aj]))
        return "".join(res)

    def decrypt(self, text, key):
        key_index = [{key[k][i * self.grid_length + j]: (i, j) for i in range(self.grid_length)
                      for j in range(self.grid_length)} for k in range(2)]
        res = []
        for a, b in zip(text[::2], text[1::2]):
            (ai, aj), (bi, bj) = key_index[0][a], key_index[1][b]
            res.extend((self.alphabet[ai * self.grid_length + bj], self.alphabet[bi * self.grid_length + aj]))
        return "".join(res)

    def random_key(self):
        key = list(self.alphabet)
        shuffle(key)
        key2 = key[:]
        shuffle(key)
        return ["".join(key), "".join(key2)]
