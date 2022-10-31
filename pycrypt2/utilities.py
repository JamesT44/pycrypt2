from functools import reduce
from string import ascii_uppercase

import numpy as np
import wordsegment


class Utilities(object):
    def __init__(self, alphabet=ascii_uppercase, excluded="_0123456789"):
        self.keep_chars = set(alphabet.upper() + alphabet.lower())
        self.alphabet = alphabet
        self.alphabet_index = {c: i for i, c in enumerate(alphabet)}
        self.case = str.upper if alphabet == ascii_uppercase else str.lower
        wordsegment.load()

    def clean(self, text):
        return "".join(c for c in self.case(text) if c in self.keep_chars)

    def punctuate(self, original_string, new_string, recapitalise=True):
        new_chars = list(new_string)[::-1]
        res = []
        for c in original_string:
            if c not in self.keep_chars:
                res.append(c)
            elif not recapitalise:
                res.append(new_chars.pop())
            elif c.upper() == c:
                res.append(new_chars.pop().upper())
            else:
                res.append(new_chars.pop().lower())
        return "".join(res)

    def keyword_key(self, keyword):
        res = []
        rem = set(self.alphabet)
        for c in keyword:
            if c in rem:
                res.append(c)
                res.remove(c)
        return "".join(res + [c for c in self.alphabet if c in rem])

    def inverse_key(self, key):
        return "".join(self.alphabet[key.index(c)] for c in self.alphabet)

    @staticmethod
    def factors(n):
        return set(reduce(list.__add__, ([i, n // i] for i in range(1, int(n ** 0.5) + 1) if n % i == 0)))

    def word_segment(self, text):
        return " ".join(wordsegment.segment(self.clean(text))).upper()

    def text_to_arr(self, text):
        return np.array([self.alphabet_index[c] for c in text], dtype=np.uint8)

    def arr_to_text(self, arr):
        return "".join(self.alphabet[n] for n in arr)
