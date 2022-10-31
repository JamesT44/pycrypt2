from string import ascii_uppercase


class Cipher(object):
    def __init__(self, alphabet=ascii_uppercase):
        self.alphabet = alphabet
        self.alphabet_length = len(alphabet)
        self.alphabet_index = {c: i for i, c in enumerate(alphabet)}

    def encrypt(self, text, key):
        pass

    def decrypt(self, text, key):
        pass
