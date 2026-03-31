import socket

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
        self.send_message(message)  # Envoi du message
        print(f"Message envoyé : {message}")

        response = self.receive_response()  # Réception de la réponse
        print(f"Réponse du serveur : {response}")

        self.close()

if __name__ == '__main__':
    client = TCPClient()
    client.run()