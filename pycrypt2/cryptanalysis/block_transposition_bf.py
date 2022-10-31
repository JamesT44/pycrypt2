from itertools import chain, permutations, zip_longest

from math import inf

from ciphers.block_transposition import BlockTransposition
from pycrypt_statistics import Statistics


def block_transposition_bf(text, max_length=6, cipher=BlockTransposition(), fitness=Statistics().ngram_fitness,
                           maximise=True):
    best = (-inf if maximise else inf, None, None)
    cmp = max if maximise else min
    for period in range(2, max_length + 1):
        cols = [text[i::period] for i in range(period)]
        for key in permutations(range(period)):
            current_plaintext = "".join(chain.from_iterable(zip_longest(*[cols[i] for i in key], fillvalue="")))
            current_fitness = fitness(current_plaintext)
            best = cmp(best, (current_fitness, key))
    return cipher.decrypt(text, best[1]), best[1]
