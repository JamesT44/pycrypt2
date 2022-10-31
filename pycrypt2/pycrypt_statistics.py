import os
from collections import Counter, defaultdict
from statistics import mean, pstdev
from string import ascii_uppercase

from math import log10

from statistics_data import bigram_discrepancy_data, log_bigram_data


class Statistics(object):
    def __init__(self, alphabet=ascii_uppercase, max_period=20, monogram_data=None,  ngram_data=None):
        self.alphabet = alphabet
        self.alphabet_index = {c: i for i, c in enumerate(alphabet)}
        self.alphabet_length = len(alphabet)
        self.max_period = max_period

        directory = os.path.dirname(os.path.abspath(__file__))
        if monogram_data is None:
            monogram_data = "data\\ngram_counts\\english_monograms.txt"
        if ngram_data is None:
            ngram_data = "data\\ngram_counts\\english_quadgrams.txt"

        self.monogram_frequencies = {}
        with open(os.path.join(directory, monogram_data)) as monogram_input:
            total = 0
            for line in monogram_input:
                c, count = line.split()
                count = int(count)
                self.monogram_frequencies[c] = count
                total += count
            for c in self.monogram_frequencies:
                self.monogram_frequencies[c] /= total

        self.ngram_frequencies = {}
        with open(os.path.join(directory, ngram_data)) as ngram_input:
            total = 0
            for line in ngram_input:
                ngram, count = line.split()
                count = int(count)
                self.ngram_frequencies[ngram] = count
                total += count
            self.ngram_frequencies = {ngram: log10(count / total) for ngram, count in self.ngram_frequencies.items()}
            self.ngram_floor = log10(0.5 / total)
            self.ngram_length = len(ngram)

        self.log_bigram_data = log_bigram_data
        self.bigram_discrepancy_data = bigram_discrepancy_data

    @staticmethod
    def base_ioc(chunks, length, norm_factor):
        counts = Counter(chunks)
        res = 0
        for count in counts.values():
            res += count * (count - 1)
        return norm_factor * res / (length * (length - 1))

    def index_of_coincidence(self, text):
        return self.base_ioc(text, len(text), self.alphabet_length)

    def periodic_ioc(self, text):
        if len(text) <= 2:
            return [0]
        res = [0]
        for period in range(1, min(self.max_period, len(text) // 2) + 1):
            substrings = (text[i::period] for i in range(period))
            res.append(sum(self.index_of_coincidence(substring) for substring in substrings) / period)
        return res

    def bigram_ioc(self, text):
        if len(text) <= 2:
            return 0
        return self.base_ioc((text[i:i + 2] for i in range(len(text) - 1)), len(text) - 1, self.alphabet_length ** 2)

    def even_bigram_ioc(self, text):
        if len(text) <= 3:
            return 0
        if len(text) % 2:
            text = text[:-1]
        return self.base_ioc((text[i:i + 2] for i in range(0, len(text), 2)), len(text) // 2, self.alphabet_length ** 2)

    @staticmethod
    def monogram_counts(text):
        return Counter(text)

    def monogram_chi_english(self, text):
        length = len(text)
        counts = self.monogram_counts(text)
        res = 0
        for c in self.alphabet:
            expected = length * self.monogram_frequencies[c]
            res += ((counts[c] - expected) ** 2) / expected
        return res

    def monogram_chi_uniform(self, text):
        length = len(text)
        counts = self.monogram_counts(text)
        res = 0
        expected = length / self.alphabet_length
        for c in self.alphabet:
            res += ((counts[c] - expected) ** 2)
        return res / expected

    def autocorrelation(self, text):
        length = len(text)
        res = [0]
        for period in range(1, min(self.max_period + 1, length)):
            res.append(sum(c == c2 for c, c2 in zip(text[:-period], text[period:])) / (length - period))
        return res

    @staticmethod
    def odd_repeats(text):
        indices = defaultdict(lambda: [0, 0])
        for i, c in enumerate(text):
            indices[c][i % 2] += 1
        odd = 0
        even = 0
        for even_count, odd_count in indices.values():
            odd += odd_count * even_count
            even += (even_count * (even_count - 1) + odd_count * (odd_count - 1)) / 2
        return odd / (odd + even) if odd or even else 0

    @staticmethod
    def three_spaced_repeats(text):
        indices = defaultdict(lambda: [0, 0, 0])
        for i, c in enumerate(text):
            indices[c][i % 3] += 1
        res = 0
        for a, b, c in indices.values():
            res += (a * (a - 1) + b * (b - 1) + c * (c - 1)) / 2
        return res ** 0.5 / len(text)

    def ngram_fitness(self, text):
        res = 0
        ngram_length = self.ngram_length
        length = len(text) - ngram_length + 1
        floor = self.ngram_floor
        ngram_get = self.ngram_frequencies.get
        for i in range(length):
            res += ngram_get(text[i:i + ngram_length], floor)
        return res / length

    def log_bigram_score(self, text):
        res = 0
        text = [c for c in text if c in self.alphabet_index]
        for a, b in zip(text[:-1], text[1:]):
            res += self.log_bigram_data[self.alphabet_index[a]][self.alphabet_index[b]]
        return res / (len(text) - 1)

    def bigram_discrepancy_score(self, text):
        res = 0
        text = [c for c in text if c in self.alphabet_index]
        for a, b in zip(text[:-1], text[1:]):
            res += self.bigram_discrepancy_data[self.alphabet_index[a]][self.alphabet_index[b]]
        return res / (len(text) - 1)

    def periodic_bigram_cv(self, text):
        if len(text) <= 2:
            return [0]
        res = [0]
        for period in range(1, min(self.max_period, len(text) // 2) + 1):
            counts = Counter([text[i:i + period + 1:period] for i in range(len(text) - period)]).values()
            mu = mean(counts)
            res.append(pstdev(counts, mu) / mu)
        return res

    def id_stats(self, text):
        return (self.monogram_chi_english(text), self.index_of_coincidence(text), max(self.periodic_ioc(text)),
                self.bigram_ioc(text), self.even_bigram_ioc(text), self.odd_repeats(text),
                self.three_spaced_repeats(text), self.log_bigram_score(text), self.bigram_discrepancy_score(text),
                int("J" in text), int("_" in text), any(str(d) in text for d in range(10)), len(text) % 2)
