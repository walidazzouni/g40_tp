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

def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)

    while True:
        print("Le serveur ecoute a cette adresse :", s.getsockname())
        sc, sockname = s.accept()
        print("Le serveur a accepte une connexion de", sockname)
        print("Une connexion a ete etablie entre", sc.getsockname(), "et", sc.getpeername())

        message = recv_all(sc, 9)
        print("Les 10 octets recus :", repr(message))

        sc.sendall(b"Au revoir")
        sc.close()
        print("Une reponse a ete envoyee, la socket est fermee")

if __name__ == '__main__':
    server()