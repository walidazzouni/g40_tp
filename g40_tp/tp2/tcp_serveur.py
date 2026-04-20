import socket

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

# Utilisation du polymorphisme pour exécuter différents types de serveurs
def run_server(server_type):
    server = server_type()  # Dynamically create either a TCPServer or UDPServer
    server.start()
    # Code pour recevoir et envoyer des messages
    data = server.receive_message()
    response = f"Réponse du serveur : {data}"
    server.send_response(response, data)

if __name__ == "__main__":
    run_server(TCPServer)  # Choisir TCPServer ou UDPServer ici