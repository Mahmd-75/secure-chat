import socket
import threading

HOST = '0.0.0.0'
PORT = 5555

clients = []
nicknames = []

def broadcast(message):
    for client in clients[:]:
        try:
            client.send(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            nicknames.pop(index)
            client.close()

def handle_client(client, address):
    print(f"[+] Nouvelle connexion de {address}")
    while True:
        try:
            message = client.recv(1024)
            if not message:
                break
            broadcast(message)
        except:
            if client in clients:
                index = clients.index(client)
                nickname = nicknames[index]
                clients.remove(client)
                nicknames.remove(nickname)
                broadcast(f"[Serveur] {nickname} a quitté le chat.\n".encode())
                print(f"[-] {nickname} déconnecté")
            client.close()
            break

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[*] Serveur en écoute sur {HOST}:{PORT}")

    while True:
        client, address = server.accept()
        client.send("[Serveur] Entrez votre pseudo : ".encode())
        nickname = client.recv(1024).decode().strip()
        nicknames.append(nickname)
        clients.append(client)
        print(f"[+] Pseudo enregistré : {nickname}")
        broadcast(f"[Serveur] {nickname} a rejoint le chat !\n".encode())
        client.send("[Serveur] Connecté au chat.\n".encode())
        thread = threading.Thread(target=handle_client, args=(client, address))
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    start_server()
