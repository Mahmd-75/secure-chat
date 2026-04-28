"""
Cryptanalyse — Chiffre de Vigenère
Casse n'importe quel texte chiffré par Vigenère par analyse de fréquences.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'server'))
from crypto import vigenere_encrypt

def index_of_coincidence(text):
    """Calcule l'indice de coïncidence d'un texte.
    Texte français normal → IC ≈ 0.074
    Texte aléatoire → IC ≈ 0.038
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

def find_key_length(ciphertext, max_len=20):
    """Estime la longueur de la clé via l'indice de coïncidence.
    Retourne le plus petit pic significatif pour éviter les multiples.
    """
    text = [c.lower() for c in ciphertext if c.isalpha()]
    results = []
    print("\n=== RECHERCHE LONGUEUR DE CLÉ ===")
    for length in range(1, max_len + 1):
        avg_ic = 0
        for i in range(length):
            subtext = text[i::length]
            avg_ic += index_of_coincidence(subtext)
        avg_ic /= length
        results.append((length, avg_ic))
        print(f"Longueur {length:2d} → IC = {avg_ic:.4f}")

    # Cherche le plus petit pic au dessus du seuil 0.060
    seuil = 0.060
    for length, ic in results:
        if ic >= seuil:
            print(f"\n→ Longueur de clé estimée : {length}")
            return length

    # Si aucun pic clair, prend le meilleur
    best = max(results, key=lambda x: x[1])
    print(f"\n→ Longueur de clé estimée : {best[0]} (meilleur IC)")
    return best[0]

def crack_vigenere(ciphertext):
    """Casse Vigenère par analyse de fréquences sur chaque sous-texte."""
    text = [c.lower() for c in ciphertext if c.isalpha()]
    key_len = find_key_length(ciphertext)
    key = ""
    print("\n=== RÉCUPÉRATION DE LA CLÉ ===")
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

    # Déchiffrement avec la clé trouvée
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

if __name__ == "__main__":
    # Change le texte et la clé ici ou passe-les en argument
    # Usage : python3 crack_vigenere.py "ma clé" mon texte a chiffrer ici
    if len(sys.argv) > 2:
        cle = sys.argv[1]
        texte = " ".join(sys.argv[2:])
    else:
        cle = "guardia"
        texte = (
            "la cryptographie est la science qui etudie les techniques "
            "permettant de securiser les communications et de proteger "
            "les donnees contre les personnes non autorisees a y acceder "
            "elle est utilisee partout dans notre vie quotidienne "
            "sans cryptographie nos mots de passe nos messages et nos "
            "donnees bancaires seraient lisibles par nimporte qui sur le reseau "
            "cest pourquoi il est essentiel de comprendre ses forces et ses faiblesses"
        )

    chiffre = vigenere_encrypt(texte, cle)
    print(f"Texte original  : {texte[:80]}...")
    print(f"Clé utilisée    : {cle}")
    print(f"Texte chiffré   : {chiffre[:80]}...")
    crack_vigenere(chiffre)
