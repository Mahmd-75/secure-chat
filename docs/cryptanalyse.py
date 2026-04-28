import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'server'))
from crypto import vigenere_encrypt

# Fréquences des lettres en français (%)
FRENCH_FREQ = {
    'a': 8.15, 'b': 0.97, 'c': 3.15, 'd': 3.73, 'e': 17.39,
    'f': 1.12, 'g': 0.97, 'h': 0.85, 'i': 7.31, 'j': 0.45,
    'k': 0.02, 'l': 5.69, 'm': 2.87, 'n': 7.12, 'o': 5.28,
    'p': 2.80, 'q': 1.21, 'r': 6.64, 's': 8.14, 't': 7.22,
    'u': 6.38, 'v': 1.64, 'w': 0.03, 'x': 0.41, 'y': 0.28,
    'z': 0.15
}

# -----------------------------------------------
# CASSER CÉSAR — Force brute
# -----------------------------------------------

def cesar_decrypt(message, key):
    """Déchiffre un message César avec une clé donnée."""
    result = ""
    for char in message:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base - key) % 26 + base)
        else:
            result += char
    return result

def crack_cesar(ciphertext):
    """Casse le chiffre de César par force brute (26 essais)."""
    print("\n=== ATTAQUE CÉSAR — Force brute ===")
    print(f"Texte chiffré : {ciphertext}\n")
    for key in range(26):
        decrypted = cesar_decrypt(ciphertext, key)
        print(f"Clé {key:2d} : {decrypted}")

# -----------------------------------------------
# CASSER VIGENÈRE — Indice de coïncidence + fréquences
# -----------------------------------------------

def index_of_coincidence(text):
    """Calcule l'indice de coïncidence d'un texte.
    """
    text = [c.lower() for c in text if c.isalpha()]
    n = len(text)
    if n < 2:
        return 0
    freq = {}
    for c in text:
        freq[c] = freq.get(c, 0) + 1
    ic = sum(f * (f - 1) for f in freq.values()) / (n * (n - 1))
    return ic

def find_key_length(ciphertext, max_len=15):
    """Estime la longueur de la clé Vigenère via l'indice de coïncidence."""
    text = [c.lower() for c in ciphertext if c.isalpha()]
    best_len = 1
    best_ic = 0
    print("\n== RECHERCHE LONGUEUR DE CLÉ ==")
    for length in range(1, max_len + 1):
        avg_ic = 0
        for i in range(length):
            subtext = text[i::length]
            avg_ic += index_of_coincidence(subtext)
        avg_ic /= length
        print(f"Longueur {length:2d} → IC = {avg_ic:.4f}")
        if avg_ic > best_ic:
            best_ic = avg_ic
            best_len = length
    print(f"\n→ Longueur de clé estimée : {best_len}")
    return best_len

def crack_vigenere(ciphertext):
    """Casse Vigenère par analyse de fréquences sur chaque sous-texte."""
    text = [c.lower() for c in ciphertext if c.isalpha()]
    key_len = find_key_length(ciphertext)
    key = ""
    print("\n== RÉCUPÉRATION DE LA CLÉ ==")
    for i in range(key_len):
        subtext = text[i::key_len]
        freq = {}
        for c in subtext:
            freq[c] = freq.get(c, 0) + 1
        most_common = max(freq, key=freq.get)
        shift = (ord(most_common) - ord('e')) % 26
        key_letter = chr(shift + ord('a'))
        print(f"  Sous-texte {i} → lettre la plus fréquente : '{most_common}' → clé[{i}] = '{key_letter}'")
        key += key_letter
    print(f"\n→ Clé trouvée : '{key}'")

    result = ""
    key_index = 0
    for char in ciphertext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shift = ord(key[key_index % len(key)]) - ord('a')
            result += chr((ord(char) - base - shift) % 26 + base)
            key_index += 1
        else:
            result += char
    print(f"\n→ Texte déchiffré : {result}")

# -----------------------------------------------
# DEMO
# -----------------------------------------------

if __name__ == "__main__":

    # --- CÉSAR ---
    ciphertext_cesar = "Erqmrxu, mh fkliiuh ohv phvvdjhv!"
    crack_cesar(ciphertext_cesar)

    print("\n" + "="*50 + "\n")

    # --- VIGENÈRE --- texte long pour que l'analyse de fréquences soit fiable
    plaintext = (
        "la cryptographie est la science qui etudie les techniques "
        "permettant de securiser les communications et de proteger "
        "les donnees contre les personnes non autorisees a y acceder "
        "elle est utilisee partout dans notre vie quotidienne "
        "sans cryptographie nos mots de passe nos messages et nos "
        "donnees bancaires seraient lisibles par nimporte qui sur le reseau "
        "cest pourquoi il est essentiel de comprendre ses forces et ses faiblesses"
    )
    ciphertext_vigenere = vigenere_encrypt(plaintext, "guardia")
    print(f"Texte chiffré (Vigenère, clé=guardia) :\n{ciphertext_vigenere}\n")
    crack_vigenere(ciphertext_vigenere)

