import socket
import threading  # Ajout de l'importation de la librairie threading

class TCPClient:
    def __init__(self, host='127.0.0.1', port=1060):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect(self):
        self.sock.connect((self.host, self.port))
        print(f"Connecté au serveur à {self.sock.getsockname()}")

    def send_message(self, message):
        self.sock.sendall(message.encode('utf-8'))

    def receive_response(self):
        while True:
            response = self.sock.recv(65535)
            print(f"Réponse du serveur: {response.decode('utf-8')}")
    
    def close(self):
        self.sock.close()

    def run(self):
        self.connect()
        # Lancer un thread pour recevoir les messages du serveur
        receive_thread = threading.Thread(target=self.receive_response)
        receive_thread.daemon = True
        receive_thread.start()
        
        while True:
            message = input("Entrez votre message: ")  # Demander à l'utilisateur de saisir un message
            self.send_message(message)  # Envoyer le message
            if message.lower() == "exit":  # Quitter la boucle
                break
        
        self.close()

if __name__ == "__main__":
    client = TCPClient()
    client.run()