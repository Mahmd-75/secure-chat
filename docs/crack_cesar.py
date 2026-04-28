"""
Cryptanalyse — Chiffre de César
Casse n'importe quel texte chiffré par César par force brute.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'server'))
from crypto import cesar_encrypt

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

if __name__ == "__main__":
    # Change le texte ici ou passe-le en argument
    if len(sys.argv) > 1:
        texte = " ".join(sys.argv[1:])
    else:
        texte = "Bonjour, je chiffre les messages!"

    cle = 3
    chiffre = cesar_encrypt(texte, cle)
    print(f"Texte original  : {texte}")
    print(f"Clé utilisée    : {cle}")
    print(f"Texte chiffré   : {chiffre}")
    crack_cesar(chiffre)
