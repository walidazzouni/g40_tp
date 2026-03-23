import socket

class UDPServer:
    MAX_BYTES = 65535

    def __init__(self, host='127.0.0.1', port=1060):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start(self):
        self.sock.bind((self.host, self.port))
        print('En écoute sur {}'.format(self.sock.getsockname()))

    def receive_message(self):
        data, address = self.sock.recvfrom(self.MAX_BYTES)
        return data, address

    def process_message(self, data, address):
        text = data.decode('ascii', errors='ignore')
        print('Le client {} dit {!r}'.format(address, text))

        response = 'les donnees ont une taille de {} octets'.format(len(data))
        return response.encode('ascii')

    def send_response(self, response, address):
        self.sock.sendto(response, address)

    def run(self):
        self.start()
        try:
            while True:
                data, address = self.receive_message()
                response = self.process_message(data, address)
                self.send_response(response, address)
        except KeyboardInterrupt:
            print('\nServeur arrêté')
        finally:
            self.sock.close()

if __name__ == '__main__':
    server = UDPServer()
    server.run()