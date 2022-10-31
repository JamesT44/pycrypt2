import os

from cppimport import imp

from ciphers.hill import Hill

hill_pdc_cpp = imp("cryptanalysis.hill_pdc")


def hill_pdc(text, key_len=2, cipher=Hill(), hill_data_file="..\\data\\hill_pdc_data.txt"):
    key = cipher.inverse_key(
        hill_pdc_cpp.hill_pdc_cpp(text, key_len, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                              hill_data_file)))
    return cipher.decrypt(text, key), list(key)
