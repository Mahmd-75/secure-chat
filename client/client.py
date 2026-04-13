import socket
import threading
#Utilisation HOST & PORT car fonction socket stream
HOST = '127.0.0.1'
PORT = 5555

#Fonction d'écoute en continu les messages d'autres utilisateurs et les affiches
def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode()
            print(message, end='')
        except:
            print("[!] Connexion perdue.")
            client.close()
            break

#Fonction de création d'un utilisateur et demarre le chat
def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    prompt = client.recv(1024).decode()
    print(prompt, end='')
    nickname = input()
    client.send(nickname.encode())

    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.daemon = True
    thread.start()

    while True:
        try:
            message = input()
            client.send(f"{nickname}: {message}\n".encode())
        except KeyboardInterrupt:
            client.close()
            break

if __name__ == "__main__":
    start_client()
