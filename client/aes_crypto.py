"""
Étape 4 — Chiffrement AES-GCM
Chiffrement symétrique authentifié (AEAD) avec clé 256 bits.
"""

import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def generate_aes_key():
    """Génère une clé AES-256 aléatoire (32 octets)."""
    return os.urandom(32)

def aes_encrypt(key, plaintext):
    """Chiffre un message avec AES-GCM.
    Retourne nonce + ciphertext (le nonce est envoyé en clair avec le message).
    """
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # 96 bits, unique par message
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)
    return nonce + ciphertext  # on préfixe le nonce au message chiffré

def aes_decrypt(key, data):
    """Déchiffre un message AES-GCM.
    Attend nonce (12 premiers octets) + ciphertext.
    """
    aesgcm = AESGCM(key)
    nonce = data[:12]       # on extrait le nonce
    ciphertext = data[12:]  # le reste c'est le message chiffré
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext.decode()
