import os

from cppimport import imp

from ciphers.playfair import Playfair

playfair_pfta_cpp = imp("cryptanalysis.playfair_pfta")


def playfair_pfta(text, cipher=Playfair(), playfair_quadgram_file="..\\data\\ngram_counts\\playfair_quadgrams.dat",
                  max_length=700):
    key = cipher.align_keyword(playfair_pfta_cpp.playfair_pfta_cpp(
        text[:min(len(text), max_length)], os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                        playfair_quadgram_file)))
    return cipher.decrypt(text, key), key
