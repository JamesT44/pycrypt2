from math import inf

from ciphers.railfence import Railfence
from pycrypt_statistics import Statistics


def railfence_bf(text, max_period=15, cipher=Railfence(), fitness=Statistics().ngram_fitness, maximise=True):
    best = (-inf if maximise else inf, None, None)
    cmp = max if maximise else min
    for period in range(2, max_period + 1):
        current_plaintext = cipher.decrypt(text, period)
        current_fitness = fitness(current_plaintext)
        best = cmp(best, (current_fitness, current_plaintext, period))
    return best[1:]
