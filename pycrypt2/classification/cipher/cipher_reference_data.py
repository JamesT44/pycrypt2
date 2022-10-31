import os

from ciphers.adfgvx import ADFGVX
from ciphers.adfgx import ADFGX
from ciphers.autokey import Autokey
from ciphers.beaufort import Beaufort
from ciphers.bifid import Bifid
from ciphers.block_transposition import BlockTransposition
from ciphers.columnar_transposition import ColumnarTransposition
from ciphers.condi import Condi
from ciphers.digrafid import Digrafid
from ciphers.foursquare import Foursquare
from ciphers.fractionated_morse import FractionatedMorse
from ciphers.hill import Hill
from ciphers.myszkowski import Myszkowski
from ciphers.playfair import Playfair
from ciphers.porta import Porta
from ciphers.railfence import Railfence
from ciphers.simple_substitution import SimpleSubstitution
from ciphers.trifid import Trifid
from ciphers.vigenere import Vigenere
from pycrypt_statistics import Statistics

spaces_ciphers = [FractionatedMorse()]
j_ciphers = [ADFGVX(), Autokey(), Beaufort(), BlockTransposition(), ColumnarTransposition(), Condi(), Digrafid(),
             Hill(), Myszkowski(), Porta(), Railfence(), SimpleSubstitution(), Trifid(), Vigenere()]
noj_ciphers = [ADFGX(), Bifid(), Foursquare(), Playfair()]
remap_names = {"Beaufort"          : "VigenereVariant", "Porta": "VigenereVariant", "Vigenere": "VigenereVariant",
               "BlockTransposition": "Transposition", "ColumnarTransposition": "Transposition",
               "Myszkowski"        : "Transposition", "Railfence": "Transposition"}

stats = Statistics()
with open("cipher_reference_data.csv", "w") as output:
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
                    elif cleaned and cleaned[-1] != " " and c != "'":
                        cleaned.append(" ")

            text = "".join(cleaned)
        elif plaintext.startswith("wikipedia"):
            f = os.path.join("..\\training_plaintext", plaintext)
            with open(f, encoding="utf8") as inp:
                text = "".join(inp.read().upper())
        else:
            continue

        for cipher in spaces_ciphers:
            key = cipher.random_key()
            if isinstance(key, tuple):
                ciphertext = cipher.encrypt(text, *key)
            else:
                ciphertext = cipher.encrypt(text, key)
            name = cipher.__class__.__name__
            if name in remap_names:
                name = remap_names[name]
            print(name, *stats.id_stats(ciphertext), sep=",", file=output)
        text = text.replace(" ", "")
        for cipher in j_ciphers:
            key = cipher.random_key()
            if isinstance(key, tuple):
                ciphertext = cipher.encrypt(text, *key)
            else:
                ciphertext = cipher.encrypt(text, key)
            name = cipher.__class__.__name__
            if name in remap_names:
                name = remap_names[name]
            print(name, *stats.id_stats(ciphertext), sep=",", file=output)
        text = text.replace("J", "I")
        for cipher in noj_ciphers:
            key = cipher.random_key()
            if isinstance(key, tuple):
                ciphertext = cipher.encrypt(text, *key)
            else:
                ciphertext = cipher.encrypt(text, key)
            print(cipher.__class__.__name__, *stats.id_stats(ciphertext), sep=",", file=output)
        print(i)
