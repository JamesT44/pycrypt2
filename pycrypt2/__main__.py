from pyperclip import copy, paste

from ciphers.beaufort import Beaufort
from ciphers.porta import Porta
from ciphers.vigenere import Vigenere
from classification.cipher.cipher_classification import CipherClassifier
from classification.columnar_transposition_period import columnar_transposition_period
from classification.vigenere_period.vigenere_period_classification import VigenerePeriodClassifier
from cryptanalysis.block_transposition_bf import block_transposition_bf
from cryptanalysis.block_transposition_dc import block_transposition_dc
from cryptanalysis.columnar_transposition_dc import columnar_transposition_dc
from cryptanalysis.hill_pdc_wrapper import hill_pdc
from cryptanalysis.playfair_pfta_wrapper import playfair_pfta
from cryptanalysis.railfence_bf import railfence_bf
from cryptanalysis.simple_substitution_pshc import simple_substitution_pshc
from cryptanalysis.vigenere_variant_pbf import vigenere_variant_pbf
from pycrypt_statistics import Statistics
from utilities import Utilities


def print_truncated(text, label, truncate_length=100):
    print(label + ":", text.replace("\n", " ").replace("\r", "")[:truncate_length] + "...", flush=True)


print("""
`7MM\"\"\"Mq.              .g8\"\"\"bgd                                mm                          
  MM   `MM.           .dP'     `M                                MM                          
  MM   ,M9 `7M'   `MF'dM'       ``7Mb,od8 `7M'   `MF'`7MMpdMAo.mmMMmm     `7M'   `MF'pd*"*b. 
  MMmmdM9    VA   ,V  MM           MM' "'   VA   ,V    MM   `Wb  MM         VA   ,V (O)   j8 
  MM          VA ,V   MM.          MM        VA ,V     MM    M8  MM          VA ,V      ,;j9 
  MM           VVV    `Mb.     ,'  MM         VVV      MM   ,AP  MM           VVV    ,-='    
.JMML.         ,V       `"bmmmd' .JMML.       ,V       MMbmmd'   `Mbmo         W    Ammmmmmm 
              ,V                             ,V        MM                                    
           OOb"                           OOb"       .JMML.                                  
""")

stats = Statistics()
utils = Utilities()
classifier = CipherClassifier()

raw_ciphertext = input("Enter cipher [Leave blank to copy from clipboard]: ")
if not raw_ciphertext:
    raw_ciphertext = paste()
print()
clean_ciphertext = utils.clean(raw_ciphertext)
print()
print_truncated(raw_ciphertext, "Input")
print_truncated(clean_ciphertext, "Cleaned")
print()

print("Identifying Cipher")
cipher_types = classifier.identify(clean_ciphertext)
candidate_ciphers = []
for cipher_name, certainty in cipher_types:
    if certainty < 0.01:
        break
    print("\t{}: {:04.2f}% certainty".format(cipher_name, certainty * 100))
    candidate_ciphers.append(cipher_name)
print()

best_decrypt = clean_ciphertext
best_key = ""
best_score = stats.ngram_fitness(best_decrypt)


def update(curr_decrypt, curr_key, tab_level=1):
    global best_decrypt, best_key, best_score

    tabs = "\t" * tab_level

    print(tabs + "Best key:", curr_key)
    print_truncated(curr_decrypt, tabs + "Best plaintext")

    curr_score = stats.ngram_fitness(curr_decrypt)
    if curr_score > best_score:
        print(tabs + "Replacing best so far")
        best_decrypt, best_key, best_score = curr_decrypt, curr_key, curr_score
    print()


for cipher_name in candidate_ciphers:
    print("Testing", cipher_name)
    if cipher_name == "SimpleSubstitution":
        update(*simple_substitution_pshc(clean_ciphertext))
    elif cipher_name == "VigenereVariant":
        print("\tIdentifying period")
        candidate_periods = []
        for period, certainty in VigenerePeriodClassifier().identify(clean_ciphertext):
            if certainty < 0.01:
                break
            print("\t\t{}: {:04.2f}% certainty".format(period, certainty * 100))
            candidate_periods.append(period)
        print()

        variants = [Vigenere(), Porta(), Beaufort()]
        for period in candidate_periods:
            for variant in variants:
                print("\tTesting", variant.__class__.__name__, "with period", period)
                update(*vigenere_variant_pbf(clean_ciphertext, period, variant), tab_level=2)
    elif cipher_name == "Transposition":
        print("\tTesting Block Transposition (Period 2-6)")
        update(*block_transposition_bf(clean_ciphertext), tab_level=2)
        print("\tTesting Block Transposition (Period 7-15)")
        update(*block_transposition_dc(clean_ciphertext), tab_level=2)

        print("\tTesting Columnar Transposition")
        period = columnar_transposition_period(clean_ciphertext)
        update(*columnar_transposition_dc(clean_ciphertext, period), tab_level=2)

        print("\tTesting Railfence")
        update(*railfence_bf(clean_ciphertext), tab_level=2)
    elif cipher_name == "Playfair":
        if "J" not in clean_ciphertext:
            update(*playfair_pfta(clean_ciphertext))
    elif cipher_name == "Hill":
        try:
            update(*hill_pdc(clean_ciphertext))
        except ValueError:
            pass
    else:
        print("\t" + cipher_name, "not yet implemented\n")
        continue

if set(raw_ciphertext.upper()) - set(stats.alphabet + " \n\r\t"):
    print("Repunctuating text")
    best_decrypt = utils.punctuate(raw_ciphertext, best_decrypt)
    print_truncated(best_decrypt, "\tRepunctuated")
else:
    inds = []
    if " " in raw_ciphertext:
        for i in range(5):
            inds.append(raw_ciphertext[sum(inds) + len(inds):].index(" "))
    if not inds or all(x == inds[0] for x in inds):
        print("Segmenting text")
        best_decrypt = utils.word_segment(best_decrypt)
        print_truncated(best_decrypt, "\tSegmented")
    else:
        print("Repunctuating text")
        best_decrypt = utils.punctuate(raw_ciphertext, best_decrypt)
        print_truncated(best_decrypt, "\tRepunctuated")

print()
print("Copied to clipboard")
copy(best_decrypt)
