from math import inf

from ciphers.caesar import Caesar
from pycrypt_statistics import Statistics


def caesar_bf(text, cipher=Caesar(), fitness=Statistics().monogram_chi_english, maximise=False):
    best = (-inf if maximise else inf, None, None)
    cmp = max if maximise else min
    for key in range(cipher.alphabet_length):
        current_plaintext = cipher.decrypt(text, key)
        current_fitness = fitness(current_plaintext)
        best = cmp(best, (current_fitness, current_plaintext, key))
    return best[1:]
