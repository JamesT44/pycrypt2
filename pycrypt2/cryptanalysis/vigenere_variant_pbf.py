from math import inf

from ciphers.vigenere import Vigenere
from pycrypt_statistics import Statistics


def vigenere_variant_pbf(text, period, cipher=Vigenere(), fitness=Statistics().monogram_chi_english, maximise=False):
    cmp = max if maximise else min
    key = []
    for i in range(period):
        substring = text[i::period]
        best = (-inf if maximise else inf, None)
        for shift in cipher.alphabet:
            current_fitness = fitness(cipher.decrypt(substring, shift))
            best = cmp(best, (current_fitness, shift))
        key.append(best[1])
    key = "".join(key)
    return cipher.decrypt(text, key), key
