import os
from collections import deque
from itertools import combinations

import numpy as np

from ciphers.simple_substitution import SimpleSubstitution


def simple_substitution_pshc(text, cipher=SimpleSubstitution(), frequency_alphabet="ETAOINSRHLDCUMFGPWYBVKJXZQ",
                             data_file=None):
    if data_file is None:
        data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "..\\data\\ngram_counts\\english_trigrams.txt")

    with open(data_file) as data_input:
        ngram_size = len(data_input.readline().split()[0])
    reference_distribution = _generate_reference_distribution(data_file, cipher, ngram_size)
    initial_key = _seed_key(text, frequency_alphabet)
    initial_distribution = _generate_text_distribution(_decrypt(text, initial_key), cipher, ngram_size)
    best = (np.sum(np.absolute(initial_distribution - reference_distribution)), initial_key, initial_distribution)
    swap_pairs = list(combinations(cipher.alphabet, 2))
    while True:
        best_child = best
        for a, b in swap_pairs:
            current_key, current_distribution = _mutate(a, b, best[1], best[2], cipher, ngram_size)
            current_fitness = np.sum(np.absolute(current_distribution - reference_distribution))
            if current_fitness < best_child[0]:
                best_child = (current_fitness, current_key, current_distribution)
        if best_child[0] < best[0]:
            best = best_child
        else:
            break
    readable_key = ["" for _ in range(cipher.alphabet_length)]
    for k, v in best[1].items():
        readable_key[cipher.alphabet_index[v]] = k
    return _decrypt(text, best[1]), "".join(readable_key)


def _generate_reference_distribution(data_file, cipher, ngram_size):
    distribution = np.zeros([cipher.alphabet_length for _ in range(ngram_size)], dtype=np.float32)
    total = 0
    with open(data_file) as data_input:
        for line in data_input:
            ngram, count = line.split()
            distribution[tuple(cipher.alphabet_index[c] for c in ngram)] = count
            total += int(count)
    return distribution / total


def _generate_text_distribution(text, cipher, ngram_size):
    distribution = np.zeros([cipher.alphabet_length for _ in range(ngram_size)])
    ngram = deque(cipher.alphabet_index[c] for c in text[:ngram_size - 1])
    for i in range(ngram_size - 1, len(text)):
        ngram.append(cipher.alphabet_index[text[i]])
        distribution[tuple(ngram)] += 1
        ngram.popleft()
    return distribution / (len(text) - ngram_size + 1)


def _seed_key(text, frequency_alphabet):
    counts = {c: 0 for c in frequency_alphabet}
    for c in text:
        counts[c] += 1
    counts = sorted([(k, v) for k, v in counts.items()], key=lambda x: x[1], reverse=True)
    key = {}
    for i, c in enumerate(frequency_alphabet):
        key[counts[i][0]] = c
    return key


def _decrypt(text, key):
    return "".join(key[c] for c in text)


def _mutate(a, b, old_key, old_distribution, cipher, ngram_size):
    key, distribution = old_key.copy(), np.copy(old_distribution)
    x, y = key[a], key[b]
    key[b], key[a] = x, y
    i, j = cipher.alphabet_index[x], cipher.alphabet_index[y]
    for n in range(ngram_size):
        distribution[tuple([i, j] if m == n else slice(cipher.alphabet_length) for m in range(ngram_size))] = \
            distribution[tuple([j, i] if m == n else slice(cipher.alphabet_length) for m in range(ngram_size))]
    return key, distribution
