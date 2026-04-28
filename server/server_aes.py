"""
Étape 4 — Serveur de chat AES-GCM
"""

import socket
import threading
from aes_crypto import aes_decrypt

HOST = '0.0.0.0'
PORT = 5556

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
    """Démarre le serveur, distribue la clé AES et gère les connexions."""
    global aes_key

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[*] Serveur AES-GCM en écoute sur {HOST}:{PORT}")

    while True:
        client, address = server.accept()

        # 1. Demande le pseudo
        send_msg(client, b"NICK")
        nickname = recv_msg(client).decode().strip()
        nicknames.append(nickname)
        clients.append(client)
        print(f"[+] {nickname} connecté")

        if aes_key is None:
            # 2a. Premier client — lui demande de générer la clé
            send_msg(client, b"GENKEY")
            aes_key = recv_msg(client)
            print(f"[*] Clé AES reçue : {aes_key.hex()}")
            send_msg(client, b"OK")
        else:
            # 2b. Clients suivants — leur envoie la clé
            send_msg(client, b"RECVKEY")
            send_msg(client, aes_key)
            print(f"[*] Clé AES envoyée à {nickname}")

        thread = threading.Thread(target=handle_client, args=(client, address))
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    start_server()
