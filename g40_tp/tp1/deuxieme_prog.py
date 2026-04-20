import socket

def connect_to_google():
    sock = socket.socket()
    sock.connect(('maps.google.com', 80))
    
    sock.sendall = (
        "GET /maps/geo?q=207+N.+Defiance+St%2C+Archbold%2C+OH"
        "&output=json&oe=utf8&sensor=false HTTP/1.1\r\n"
        "Host: maps.google.com\r\n"
        "User-Agent: search4.py\r\n"
        "Connection: close\r\n"
        "\r\n"
    ).encode()
    
    sock.sendall(request.encode())
    
    rawreply = sock.recv(4096)
    print(rawreply)

if __name__ == '__main__':
    connect_to_google()