"""
Étape 6 — Chiffrement asymétrique RSA
Génération de paires de clés, chiffrement et déchiffrement RSA-OAEP.
"""

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

def generate_rsa_keys():
    """Génère une paire de clés RSA-2048 (privée + publique)."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    return private_key, public_key

def serialize_public_key(public_key):
    """Sérialise la clé publique en bytes (format PEM) pour l'envoyer sur le réseau."""
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

def deserialize_public_key(public_key_bytes):
    """Désérialise une clé publique reçue depuis le réseau."""
    return serialization.load_pem_public_key(public_key_bytes)

def rsa_encrypt(public_key, data):
    """Chiffre des données avec la clé publique RSA (OAEP + SHA256).
    Utilisé pour chiffrer la clé AES avant envoi.
    """
    return public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def rsa_decrypt(private_key, ciphertext):
    """Déchiffre des données avec la clé privée RSA (OAEP + SHA256).
    Utilisé par le serveur pour récupérer la clé AES.
    """
    return private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
