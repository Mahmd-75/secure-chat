"""
Étape 4 — Client de chat AES-GCM
"""

import socket
import threading
from aes_crypto import aes_encrypt, aes_decrypt, generate_aes_key

HOST = '127.0.0.1'
PORT = 5556

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
    """Initialise la connexion, récupère la clé AES et démarre le chat."""
    global aes_key, nickname

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    # 1. Pseudo
    msg = recv_msg(client)
    if msg == b"NICK":
        nickname = input("Entrez votre pseudo : ")
        send_msg(client, nickname.encode())

    # 2. Clé AES
    key_msg = recv_msg(client)

    if key_msg == b"GENKEY":
        aes_key = generate_aes_key()
        send_msg(client, aes_key)
        recv_msg(client)  # attend OK
        print(f"[*] Clé AES générée et envoyée au serveur")

    elif key_msg == b"RECVKEY":
        aes_key = recv_msg(client)
        print(f"[*] Clé AES reçue du serveur")

    if aes_key is None:
        print("[!] Erreur : clé AES non reçue")
        client.close()
        return

    print(f"[*] Chiffrement AES-GCM actif — clé : {aes_key.hex()[:16]}...")
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
