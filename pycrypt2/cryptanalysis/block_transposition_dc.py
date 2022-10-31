import os
from collections import deque

import numpy as np
from math import inf

from ciphers.block_transposition import BlockTransposition
from pycrypt_statistics import Statistics


def block_transposition_dc(text, min_period=7, max_period=15,
                           bigram_data="..\\data\\transposition_dc_data.txt", cipher=BlockTransposition(),
                           fitness=Statistics().ngram_fitness):
    bigram_table = np.empty(cipher.alphabet_length ** 2, dtype=np.float_)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), bigram_data)) as bigram_input:
        for i, score in enumerate(bigram_input):
            bigram_table[i] = float(score)
    bigram_table = bigram_table.reshape((cipher.alphabet_length, cipher.alphabet_length))

    best_key, best_fitness = None, -inf
    for period in range(min_period, max_period + 1):
        extra = len(text) % period
        text_array = [cipher.alphabet_index[c] for c in text[:-extra]]
        columns = [text_array[i::period] for i in range(period)]

        adjacency_matrix = np.empty((period, period), dtype=np.float_)
        start_point = (-inf, None, None)
        for i in range(period):
            for j in range(period):
                if i == j:
                    adjacency_matrix[i][j] = -1
                    continue

                score = 0
                for a, b in zip(columns[i], columns[j]):
                    score += bigram_table[a][b]
                adjacency_matrix[i][j] = score
                start_point = max(start_point, (score, i, j))

        key = deque([start_point[1], start_point[2]])
        remaining = set(range(period)) - set(start_point[1:])
        while remaining:
            next_point = (-inf, None, None)
            for i in remaining:
                next_point = max(next_point, (adjacency_matrix[i][key[0]], i, False))
                next_point = max(next_point, (adjacency_matrix[key[-1]][i], i, True))

            if next_point[-1]:
                key.append(next_point[1])
            else:
                key.appendleft(next_point[1])
            remaining.remove(next_point[1])

        parent_key = list(key)
        parent_fitness = fitness(cipher.decrypt(text, parent_key))
        improved = True
        while improved:
            improved = False
            for segment_size in range(period, 1, -1):
                for start in range(period - segment_size + 1):
                    for slide in range(1, segment_size):
                        child_key = parent_key[:]
                        segment = parent_key[start:start + segment_size]
                        child_key[start:start + segment_size] = segment[slide:] + segment[:slide]

                        child_fitness = fitness(cipher.decrypt(text, child_key))
                        if child_fitness > parent_fitness:
                            improved = True
                            parent_fitness, parent_key = child_fitness, child_key
            for segment_size in range(1, period // 2 + 1):
                for first in range(period - 2 * segment_size + 1):
                    for second in range(first + segment_size, period - segment_size + 1):
                        child_key = parent_key[:]
                        child_key[first:first + segment_size], child_key[second:second + segment_size] = \
                            child_key[second:second + segment_size], child_key[first:first + segment_size]

                        child_fitness = fitness(cipher.decrypt(text, child_key))
                        if child_fitness > parent_fitness:
                            improved = True
                            parent_fitness, parent_key = child_fitness, child_key
        if parent_fitness > best_fitness:
            best_fitness, best_key = parent_fitness, parent_key
    return cipher.decrypt(text, best_key), best_key
