import socket

MAX_BYTES = 65535

def client(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = 'Bonjour serveur'
    sock.sendto(message.encode('ascii'), ('127.0.0.1', port))

    data, address = sock.recvfrom(MAX_BYTES)
    text = data.decode('ascii', errors='ignore')
    print('Le serveur {} répond {!r}'.format(address, text))

    sock.close()

if __name__ == '__main__':
    client(1060)