from random import shuffle
from string import ascii_uppercase

from ciphers.cipher import Cipher


class FractionatedMorse(Cipher):
    def __init__(self, alphabet=ascii_uppercase, morse_map=None, symbols=".-X"):
        super().__init__(alphabet)
        if morse_map is None:
            self.morse_map = {"A": ".-X", "B": "-...X", "C": "-.-.X", "D": "-..X", "E": ".X", "F": "..-.X", "G": "--.X",
                              "H": "....X", "I": "..X", "J": ".---X", "K": "-.-X", "L": ".-..X", "M": "--X", "N": "-.X",
                              "O": "---X", "P": ".--.X", "Q": "--.-X", "R": ".-.X", "S": "...X", "T": "-X", "U": "..-X",
                              "V": "...-X", "W": ".--X", "X": "-..-X", "Y": "-.--X", "Z": "--..X", " ": "X"}
        else:
            self.morse_map = morse_map
        self.inv_morse_map = {v[:-1]: k for k, v in self.morse_map.items()}
        self.symbols = symbols
        self.symbol_index = {c: i for i, c in enumerate(symbols)}

    def encrypt(self, text, key):
        text = text.strip()
        morse = "".join([self.morse_map[c] for c in (text + " ")])
        morse += self.symbols[0] * (-len(morse) % 3)
        return "".join(key[9 * self.symbol_index[a] + 3 * self.symbol_index[b] + self.symbol_index[c]]
                       for a, b, c in zip(morse[::3], morse[1::3], morse[2::3]))

    def decrypt(self, text, key):
        key_index = {c: self.symbols[i // 9] + self.symbols[(i // 3) % 3] + self.symbols[i % 3]
                     for i, c in enumerate(key)}
        morse = "".join(key_index[c] for c in text)
        return "".join(self.inv_morse_map[c] for c in morse.split(self.morse_map[" "]))

    def random_key(self):
        key = list(self.alphabet)
        shuffle(key)
        return "".join(key)
