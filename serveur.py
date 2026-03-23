import socket

MAX_BYTES = 65535

def server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', port))
    print('En écoute sur {}'.format(sock.getsockname()))

    try:
        while True:
            data, address = sock.recvfrom(MAX_BYTES)
            text = data.decode('ascii', errors='ignore')
            print('Le client {} dit {!r}'.format(address, text))

            response = 'Les donnees ont une taille de {} octets'.format(len(data))
            sock.sendto(response.encode('ascii'), address)

    except KeyboardInterrupt:
        print('\nServeur arrêté')
    finally:
        sock.close()

if __name__ == '__main__':
    server(1060)