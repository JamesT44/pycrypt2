import os
from random import randint

from ciphers.vigenere import Vigenere
from pycrypt_statistics import Statistics

periodic_ioc = Statistics(max_period=20).periodic_ioc
encrypt = Vigenere().encrypt

with open("vigenere_period_reference_data.csv", "w") as output:
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

            text = "".join(cleaned)
        elif plaintext.startswith("wikipedia"):
            f = os.path.join("..\\training_plaintext", plaintext)
            with open(f, encoding="utf8") as inp:
                text = "".join(inp.read().upper().replace(" ", ""))
        else:
            continue

        for period in range(2, 21):
            print(period, *periodic_ioc(encrypt(text, [randint(0, 25) for _ in range(period)]))[1:], sep=",",
                  file=output)
        print(i)
