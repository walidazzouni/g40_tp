import socket
import argparse

# Classe de base
class Server:
    def __init__(self, host='127.0.0.1', port=1060):
        self.host = host
        self.port = port
        self.sock = None

    def start(self):
        raise NotImplementedError("La méthode 'start' doit être implémentée")

    def receive_message(self):
        raise NotImplementedError("La méthode 'receive_message' doit être implémentée")

    def send_response(self, response, client_socket):
        client_socket.sendall(response.encode('utf-8'))

# Serveur TCP
class TCPServer(Server):
    def __init__(self, host='127.0.0.1', port=1060):
        super().__init__(host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def start(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        print(f"Serveur TCP à l'écoute sur {self.sock.getsockname()}")
    
    def receive_message(self, client_socket):
        data = client_socket.recv(65535)
        return data

# Client TCP
class TCPClient:
    def __init__(self, host='127.0.0.1', port=1060):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.sock.connect((self.host, self.port))
        print(f"Connecté au serveur à {self.sock.getsockname()}")

    def send_message(self, message):
        self.sock.sendall(message.encode('ascii'))

    def receive_response(self):
        response = self.sock.recv(65535)
        return response.decode('ascii', errors='ignore')

    def close(self):
        self.sock.close()

    def run(self):
        self.connect()
        message = "Bonjour serveur!"
        self.send_message(message)
        print(f"Message envoyé : {message}")

        response = self.receive_response()  # Réception de la réponse
        print(f"Réponse du serveur : {response}")

        self.close()

# Fonction principale
def run_server():
    server = TCPServer()
    server.start()

    while True:
        client_socket, addr = server.sock.accept()
        print(f"Client connecté depuis {addr}")
        data = server.receive_message(client_socket)
        print(f"Message reçu : {data.decode('utf-8')}")
        response = f"Réponse du serveur : {data.decode('utf-8')}"
        server.send_response(response, client_socket)
        client_socket.close()

def run_client():
    client = TCPClient()
    client.run()

# Utilisation de argparse pour choisir entre serveur et client
def main():
    parser = argparse.ArgumentParser(description="Lancer le client ou le serveur TCP.")
    parser.add_argument('--mode', choices=['server', 'client'], required=True, help="Choisir le mode du programme: 'server' ou 'client'")
    
    args = parser.parse_args()

    if args.mode == 'server':
        run_server()
    elif args.mode == 'client':
        run_client()

if __name__ == "__main__":
    main()