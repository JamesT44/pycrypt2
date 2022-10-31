from itertools import chain, combinations, permutations
from operator import gt, lt

from math import inf

from pycrypt_statistics import Statistics


def columnar_transposition_bf(text, max_length=7, fitness=Statistics().ngram_fitness, maximise=True):
    text_length = len(text)
    best = (-inf if maximise else inf, None, None)
    cmp = max if maximise else min
    op = gt if maximise else lt
    for period in range(2, max_length + 1):
        extra = text_length % period
        col_length = text_length // period
        if extra:
            for extra_inds in combinations(range(period), r=extra):
                extra_cols = []
                normal_cols = []
                normal_inds = []
                extra_index = 0
                start, end = 0, col_length
                for i in range(period):
                    if extra_index < extra and i == extra_inds[extra_index]:
                        end += 1
                        extra_cols.append(text[start:end])
                        extra_index += 1
                    else:
                        normal_inds.append(i)
                        normal_cols.append(text[start:end])
                    start, end = end, end + col_length
                best = (-inf if maximise else inf, None, None)
                for extra_key in permutations(range(extra), extra):
                    for normal_key in permutations(range(period - extra), period - extra):
                        current_plaintext = "".join(chain.from_iterable(zip(*[extra_cols[i] for i in extra_key] +
                                                                             [normal_cols[i] for i in normal_key])))
                        current_fitness = fitness(current_plaintext)
                        if op(current_fitness, best[0]):
                            best = (current_fitness, current_plaintext, tuple([extra_inds[i] for i in extra_key] +
                                                                              [normal_inds[i] for i in normal_key]))

        else:
            cols = [text[i:i + col_length] for i in range(0, text_length, col_length)]
            for key in permutations(range(period), period):
                current_plaintext = "".join(chain.from_iterable(zip(*[cols[i] for i in key])))
                current_fitness = fitness(current_plaintext)
                best = cmp(best, (current_fitness, current_plaintext, key))
    return best[1:]
