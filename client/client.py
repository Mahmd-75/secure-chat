import socket
import threading
from crypto import cesar_encrypt, cesar_decrypt, vigenere_encrypt, vigenere_decrypt

HOST = '127.0.0.1'
PORT = 5555

# Choix de l'algorithme et de la clé
ALGO = "vigenere"   # "cesar" ou "vigenere"
CESAR_KEY = 3
VIGENERE_KEY = "guardia"

def encrypt(message):
    """Chiffre un message selon l'algorithme choisi."""
    if ALGO == "cesar":
        return cesar_encrypt(message, CESAR_KEY)
    elif ALGO == "vigenere":
        return vigenere_encrypt(message, VIGENERE_KEY)
    return message

def decrypt(message):
    """Déchiffre un message selon l'algorithme choisi."""
    if ALGO == "cesar":
        return cesar_decrypt(message, CESAR_KEY)
    elif ALGO == "vigenere":
        return vigenere_decrypt(message, VIGENERE_KEY)
    return message

def receive_messages(client):
    """Écoute en continu les messages entrants, les déchiffre et les affiche."""
    while True:
        try:
            message = client.recv(1024).decode()
            # On déchiffre uniquement la partie après "pseudo: "
            if ": " in message:
                prefix, content = message.split(": ", 1)
                decrypted = decrypt(content.strip())
                print(f"{prefix}: {decrypted}")
            else:
                print(message, end='')
        except:
            print("[!] Connexion perdue.")
            client.close()
            break

def start_client():
    """Initialise la connexion, enregistre le pseudo et démarre le chat chiffré."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    prompt = client.recv(1024).decode()
    print(prompt, end='')
    nickname = input()
    client.send(nickname.encode())

    print(f"[*] Chiffrement actif : {ALGO.upper()}")

    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.daemon = True
    thread.start()

    while True:
        try:
            message = input()
            encrypted = encrypt(message)
            client.send(f"{nickname}: {encrypted}\n".encode())
        except KeyboardInterrupt:
            client.close()
            break

if __name__ == "__main__":
    start_client()
