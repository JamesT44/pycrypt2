from random import choice, randint

from ciphers.cipher import Cipher


class Autokey(Cipher):
    def encrypt(self, text, key):
        return "".join(self.alphabet[(self.alphabet_index[c] + self.alphabet_index[k]) % self.alphabet_length]
                       for c, k in zip(text, key + text))

    def decrypt(self, text, key):
        res = [self.alphabet[(self.alphabet_index[c] - self.alphabet_index[k]) % self.alphabet_length]
               for c, k in zip(text, key)]
        for i, c in enumerate(text[len(key):]):
            res.append(self.alphabet[(self.alphabet_index[c] - self.alphabet_index[res[i]]) % self.alphabet_length])
        return "".join(res)

    def random_key(self):
        return "".join(choice(self.alphabet) for _ in range(randint(2, 15)))
