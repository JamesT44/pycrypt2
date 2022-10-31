from math import inf

from ciphers.autokey import Autokey
from pycrypt_statistics import Statistics


def autokey_period(text, max_period=20, cipher=Autokey(), fitness=Statistics().periodic_ioc, maximise=True):
    best = (-inf if maximise else inf, None)
    cmp = max if maximise else min
    for period in range(2, max_period + 1):
        best = cmp(best, (fitness(cipher.decrypt(text, cipher.alphabet[0] * period))[period], period))
    return best[1]
