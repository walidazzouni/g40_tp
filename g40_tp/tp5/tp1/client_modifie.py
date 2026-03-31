import socket
import threading

MAX_BYTES = 65535

class Client:
    def __init__(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = ('127.0.0.1', port)

    def send_messages(self):
        while True:
            message = input("Vous : ")
            data = message.encode('ascii')
            self.sock.sendto(data, self.server_address)

    def receive_messages(self):
        while True:
            data, address = self.sock.recvfrom(MAX_BYTES)
            text = data.decode('ascii', errors='ignore')
            print("\nMessage reçu :", text)

    def run(self):
        print("Client démarré. Vous pouvez écrire des messages.")

        # Thread pour recevoir
        thread_receive = threading.Thread(target=self.receive_messages, daemon=True)
        thread_receive.start()

        # Envoi des messages
        self.send_messages()

if __name__ == '__main__':
    client = Client(1060)
    client.run()