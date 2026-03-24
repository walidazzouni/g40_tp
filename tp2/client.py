import socket

HOST = '127.0.0.1'
PORT = 1060

def recv_all(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError("La socket a ete fermee")
        data += more
    return data

def client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    print("Le serveur a assigne {} comme socket pour le client".format(s.getsockname()))

    s.sendall(b"Bonjour !")
    reply = recv_all(s, 9)

    print("Le serveur a repondu :", repr(reply))

    s.close()


if __name__ == '__main__':
    client()