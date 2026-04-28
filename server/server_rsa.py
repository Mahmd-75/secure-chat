"""
Étape 6 — Serveur de chat RSA + AES-GCM
Protocole :
- Chaque client envoie sa clé publique RSA
- Le serveur chiffre la clé AES avec la clé publique de chaque client
- La clé AES ne circule jamais en clair
"""

import socket
import threading
from rsa_crypto import generate_rsa_keys, serialize_public_key, rsa_decrypt, rsa_encrypt, deserialize_public_key
from aes_crypto import aes_decrypt, generate_aes_key

HOST = '0.0.0.0'
PORT = 5558

clients = []
nicknames = []
aes_key = None

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

def broadcast(data, sender=None):
    """Envoie des données à tous les clients sauf l'expéditeur."""
    for client in clients[:]:
        if client != sender:
            try:
                send_msg(client, data)
            except:
                if client in clients:
                    idx = clients.index(client)
                    clients.remove(client)
                    nicknames.pop(idx)
                    client.close()

def handle_client(client, address):
    """Gère la réception et diffusion des messages chiffrés."""
    while True:
        try:
            data = recv_msg(client)
            if not data:
                break
            try:
                message = aes_decrypt(aes_key, data)
                print(f"[MSG] {message}")
            except:
                pass
            broadcast(data, sender=client)
        except:
            if client in clients:
                idx = clients.index(client)
                nickname = nicknames[idx]
                clients.remove(client)
                nicknames.remove(nickname)
                print(f"[-] {nickname} déconnecté")
            client.close()
            break

def start_server():
    """Démarre le serveur, génère la clé AES et la distribue via RSA."""
    global aes_key

    # Le serveur génère la clé AES une fois pour tous
    aes_key = generate_aes_key()
    print(f"[*] Clé AES générée : {aes_key.hex()[:16]}...")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[*] Serveur RSA+AES en écoute sur {HOST}:{PORT}")

    while True:
        client, address = server.accept()

        # 1. Pseudo
        send_msg(client, b"NICK")
        nickname = recv_msg(client).decode().strip()
        nicknames.append(nickname)
        clients.append(client)
        print(f"[+] {nickname} connecté")

        # 2. Recevoir la clé publique RSA du client
        client_pub_key_bytes = recv_msg(client)
        client_pub_key = deserialize_public_key(client_pub_key_bytes)
        print(f"[*] Clé publique RSA reçue de {nickname}")

        # 3. Chiffrer la clé AES avec la clé publique du client et l'envoyer
        encrypted_aes = rsa_encrypt(client_pub_key, aes_key)
        send_msg(client, encrypted_aes)
        print(f"[*] Clé AES envoyée à {nickname} (chiffrée RSA)")

        thread = threading.Thread(target=handle_client, args=(client, address))
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    start_server()
