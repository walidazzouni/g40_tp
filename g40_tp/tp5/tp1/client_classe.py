import socket

class GoogleClient:
    def __init__(self, host='maps.google.com', port=80):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def send_request(self):
        request = (
            "GET /maps/geo?q=207+N.+Defiance+St%2C+Archbold%2C+OH"
            "&output=json&oe=utf8&sensor=false HTTP/1.1\r\n"
            "Host: maps.google.com:80\r\n"
            "User-Agent: search4.py\r\n"
            "Connection: close\r\n"
            "\r\n"
        )
        self.sock.sendall(request.encode('ascii'))

    def receive_response(self):
        response = self.sock.recv(4096)
        return response

    def close(self):
        if self.sock:
            self.sock.close()

    def run(self):
        self.connect()
        self.send_request()
        response = self.receive_response()
        print(response)
        self.close()

if __name__ == '__main__':
    client = GoogleClient()
    client.run()