import socket
import threading

class TCPClient:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect(self):
        # Connexion au serveur
        self.sock.connect((self.host, self.port))
        print(f"Connecté au serveur à {self.sock.getsockname()}")

    def send_message(self, message):
        # Envoi du message au serveur
        self.sock.sendall(message.encode('utf-8'))

    def receive_response(self):
        # Réception des messages du serveur
        while True:
            response = self.sock.recv(65535)
            if response:
                print(f"Réponse du serveur: {response.decode('utf-8')}")
            else:
                break

    def close(self):
        self.sock.close()

    def run(self):
        # Se connecter au serveur
        self.connect()

        # Lancer un thread pour recevoir les réponses du serveur en continu
        receive_thread = threading.Thread(target=self.receive_response)
        receive_thread.daemon = True  # Le thread se ferme quand le programme principal se termine
        receive_thread.start()

        # Envoyer des messages en continu
        while True:
            message = input("Entrez votre message : ")  # Saisie de message
            self.send_message(message)  # Envoi du message
            if message.lower() == "exit":  # Quitter le client si l'utilisateur tape "exit"
                break
        
        self.close()


if __name__ == "__main__":
    client = TCPClient()
    client.run()