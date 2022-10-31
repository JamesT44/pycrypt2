from itertools import chain
from random import randint

from ciphers.cipher import Cipher


class Railfence(Cipher):
    def encrypt(self, text, period):
        m = period * 2 - 2
        res = []
        for i in range(period):
            if i == 0 or i == period - 1:
                res.append(text[i::m])
            else:
                a, b = text[i::m], text[m - i::m]
                res.append("".join(chain.from_iterable(list(zip(a, b)))))
                if len(b) < len(a):
                    res.append(a[-1])
        return "".join(res)

    def decrypt(self, text, period):
        res = ["" for _ in range(len(text))]
        idx = 0
        for i in range(0, len(text), 2 * (period - 1)):
            res[i] = text[idx]
            idx += 1
        for row in range(1, period):
            i = row
            even = True
            while i < len(text):
                res[i] = text[idx]
                if even and row != period - 1:
                    i += 2 * (period - row - 1)
                else:
                    i += 2 * row
                even = not even
                idx += 1
        return "".join(res)

    @staticmethod
    def random_key():
        return randint(2, 15)
