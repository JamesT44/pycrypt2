# Pycrypt2

Pycrypt2 is an automated classical cryptanalysis tool written in Python (and C++).

## Quickstart

Make sure you have a working C++ compiler which is recognised by Python distutils.

```bash
git clone https://github.com/JamesT44/pycrypt2.git
cd pycrypt2
pip3 install -r requirements.txt
python3 pycrypt2
```

Note that the initial startup will be slower since classification models are trained on first run.

Here is an example ciphertext to try:

```text
CFZKSUDMTENOKWVIZCUIRNZKIDLTKGEDPGAADAQQUNPUYRAZKWEOBJETQWTXHPUQQEYBULEBCKXEQWTKOEPQATZARIAVOQSDPVIPIDPPSWTUQTEYQPKOFBNMKPBJILLZIISEBGPEDKQTEEPCXEGMTAADOQSDMGGJEPBHSRHPGRSSMNSOVMFHOHVCXHPZHIEEBJIYDMGQEOBQFELTOSSEWWXOQAKKHEBJIYHMTIGPBVMNRAQJACWHJOSUATOZZNMTETGJEPBKAOYLGVWSWYMLWXWXOYGQYRDPQISLVFWTZKMMNRAHSRJWWROHLGERDQOWUCMKWHLVVFELJNIIDPCPLMMCKRPIVHELTVSOQITSFQBQXRZCDPEXGUILQIDSUEGQYYZCOYSEUCRARMVLEMMUXWLGASUNIPFUEQOYSEJGOIYLVSTSMOXHZCILTLTKGEZZRIRSIRWTSMAAOYBYELVBJIWLGKAAYBVSGZTGXMPAGIIWTIMVPBJIMLVGAPLQTSFMWQXSPDGVYNPTMSEUCW
```

## Features

- Robust implementations of 20+ classical ciphers.
- Automated cryptanalysis of common cipher types:
    - Simple substitution ciphers with shotgun hill climbing
    - Vigenere (and similar variant) ciphers with a periodic brute force
    - Railfence ciphers with brute force
    - Column/block transposition ciphers with a hybrid brute-force/divide-and-conquer algorithm
    - Playfair ciphers with a parallelized simulated annealing algorithm (in C++)
    - Hill ciphers with a parallelized divide and conquer algorithm (in C++)
- Machine learning-based classifiers for determining:
    - Type of cipher used (random forest classifier)
    - Period of Vigenere (variant) cipher (quadratic classifier)
    - Period of Bifid cipher (quadratic classifier)
- Automatic word boundary segmentation of resulting plaintext using [`wordsegment`](https://pypi.org/project/wordsegment/).
