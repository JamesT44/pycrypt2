from ciphers.adfgx import ADFGX


class ADFGVX(ADFGX):
    def __init__(self, alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", key_letters="ADFGVX"):
        super().__init__(alphabet, key_letters)
