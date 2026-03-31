import socket
import threading

# Serveur TCP
class TCPServer:
    def __init__(self, host='127.0.0.1', port=1060):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = []  # Liste pour stocker les sockets des clients

    def start(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(2)  # Limite à 2 clients pour cet exemple
        print(f"Serveur TCP à l'écoute sur {self.sock.getsockname()}")

    def handle_client(self, client_socket, client_address):
        print(f"Client connecté depuis {client_address}")
        while True:
            data = client_socket.recv(65535)
            if not data:
                break
            print(f"Message reçu de {client_address}: {data.decode('utf-8')}")
            # Broadcast du message à tous les autres clients
            self.broadcast_message(client_socket, data)
        client_socket.close()
        self.clients.remove(client_socket)  # Enlève le client de la liste lors de la déconnexion

    def broadcast_message(self, sender_socket, message):
        for client_socket in self.clients:
            if client_socket != sender_socket:
                client_socket.sendall(message)

    def run(self):
        self.start()
        try:
            while True:
                client_socket, client_address = self.sock.accept()
                self.clients.append(client_socket)  # Ajoute le nouveau client à la liste
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_thread.start()
        except KeyboardInterrupt:
            print("\nServeur arrêté.")
        finally:
            self.sock.close()

if __name__ == '__main__':
    server = TCPServer()
    server.run()