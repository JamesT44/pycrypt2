import os

from ciphers.bifid import Bifid
from pycrypt_statistics import Statistics

periodic_bigram_cv = Statistics(max_period=20).periodic_bigram_cv
cipher = Bifid()

with open("bifid_period_reference_data.csv", "w") as output:
    for i, plaintext in enumerate(os.listdir("..\\training_plaintext")):
        if not plaintext.endswith(".txt"):
            continue
        if plaintext.startswith("plaintext"):
            f = os.path.join("..\\training_plaintext", plaintext)
            cleaned = []
            with open(f, encoding="utf8") as inp:
                for c in inp.read():
                    x = c.upper()
                    if "A" <= x <= "Z":
                        cleaned.append(x)

            text = "".join(cleaned).replace("J", "I")
        elif plaintext.startswith("wikipedia"):
            f = os.path.join("..\\training_plaintext", plaintext)
            with open(f, encoding="utf8") as inp:
                text = "".join(inp.read().upper().replace(" ", "")).replace("J", "I")
        else:
            continue

        for period in range(21):
            print(period, *periodic_bigram_cv(cipher.encrypt(text, cipher.random_key()[0], period))[1:], sep=",",
                  file=output)
        print(i)
