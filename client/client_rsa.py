"""
Étape 6 — Client de chat RSA + AES-GCM
Protocole :
- Le client génère sa paire RSA
- Envoie sa clé publique au serveur
- Reçoit la clé AES chiffrée avec sa clé publique
- Déchiffre avec sa clé privée
"""

import socket
import threading
from aes_crypto import aes_encrypt, aes_decrypt
from rsa_crypto import generate_rsa_keys, serialize_public_key, rsa_decrypt

HOST = '127.0.0.1'
PORT = 5558

aes_key = None
nickname = ""

def recv_msg(sock):
    """Reçoit un message préfixé par sa taille (4 octets)."""
    raw_size = b''
    while len(raw_size) < 4:
        chunk = sock.recv(4 - len(raw_size))
        if not chunk:
            return None
        raw_size += chunk
    size = int.from_bytes(raw_size, 'big')
    data = b''
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            return None
        data += chunk
    return data

def send_msg(sock, data):
    """Envoie un message préfixé par sa taille (4 octets)."""
    sock.send(len(data).to_bytes(4, 'big') + data)

def receive_messages(client):
    """Écoute les messages entrants, les déchiffre et les affiche."""
    while True:
        try:
            data = recv_msg(client)
            if not data:
                break
            message = aes_decrypt(aes_key, data)
            print(message)
        except:
            print("[!] Connexion perdue.")
            client.close()
            break

def start_client():
    """Initialise la connexion RSA+AES et démarre le chat."""
    global aes_key, nickname

    # Génère la paire RSA du client
    private_key, public_key = generate_rsa_keys()
    print(f"[*] Paire RSA-2048 générée")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    # 1. Pseudo
    msg = recv_msg(client)
    if msg == b"NICK":
        nickname = input("Entrez votre pseudo : ")
        send_msg(client, nickname.encode())

    # 2. Envoie la clé publique RSA au serveur
    pub_key_bytes = serialize_public_key(public_key)
    send_msg(client, pub_key_bytes)
    print(f"[*] Clé publique RSA envoyée au serveur")

    # 3. Reçoit la clé AES chiffrée avec notre clé publique RSA
    encrypted_aes = recv_msg(client)
    aes_key = rsa_decrypt(private_key, encrypted_aes)
    print(f"[*] Clé AES reçue et déchiffrée avec RSA : {aes_key.hex()[:16]}...")
    print(f"[*] Chiffrement RSA+AES-GCM actif")
    print("[*] Chat démarré. Tapez vos messages :\n")

    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.daemon = True
    thread.start()

    while True:
        try:
            message = input()
            full_message = f"{nickname}: {message}"
            encrypted = aes_encrypt(aes_key, full_message)
            send_msg(client, encrypted)
        except KeyboardInterrupt:
            client.close()
            break

if __name__ == "__main__":
    start_client()
