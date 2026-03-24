import socket

MAX_BYTES = 65535

class Server:
    def __init__(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('127.0.0.1', port))
        self.clients = set()  # stocke les clients
        print('En écoute sur {}'.format(self.sock.getsockname()))

    def run(self):
        try:
            while True:
                data, address = self.sock.recvfrom(MAX_BYTES)

                # Ajouter le client s'il est nouveau
                if address not in self.clients:
                    self.clients.add(address)
                    print("Nouveau client :", address)

                text = data.decode('ascii', errors='ignore')
                print('Message de {} : {}'.format(address, text))

                # Envoyer le message à tous les autres clients
                for client in self.clients:
                    if client != address:  # ne pas renvoyer au même client
                        self.sock.sendto(
                            f"{address} : {text}".encode('ascii'),
                            client
                        )

        except KeyboardInterrupt:
            print('\nServeur arrêté')
        finally:
            self.sock.close()

if __name__ == '__main__':
    server = Server(1060)
    server.run()