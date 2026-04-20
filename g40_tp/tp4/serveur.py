import socket
import threading
import json

HOST = '127.0.0.1'
PORT = 12345

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = {}  # nom -> {"socket": ..., "lieu": ..., "etat": ..., "date_connexion": ...}
        self.lock = threading.Lock()

    def send_json(self, client_socket, data):
        message = json.dumps(data) + '\n'
        client_socket.sendall(message.encode('utf-8'))

    def broadcast(self, data, exclude=None):
        with self.lock:
            for nom, info in self.clients.items():
                if exclude is not None and nom == exclude:
                    continue
                try:
                    self.send_json(info["socket"], data)
                except:
                    pass

    def send_client_list(self, client_socket):
        with self.lock:
            liste = []
            for nom, info in self.clients.items():
                liste.append({
                    "nom": nom,
                    "lieu": info["lieu"],
                    "etat": info["etat"],
                    "date_connexion": info["date_connexion"]
                })

        self.send_json(client_socket, {
            "type": "liste_clients",
            "clients": liste
        })

    def notify_client_count(self):
        with self.lock:
            count = len(self.clients)

        self.broadcast({
            "type": "notification",
            "evenement": "nombre_clients",
            "nombre": count
        })

    def handle_client(self, client_socket, client_address):
        buffer = ""
        client_name = None

        try:
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break

                buffer += data.decode('utf-8')

                while '\n' in buffer:
                    raw_message, buffer = buffer.split('\n', 1)
                    if not raw_message.strip():
                        continue

                    message = json.loads(raw_message)
                    msg_type = message.get("type")

                    if msg_type == "identification":
                        client_name = message["nom"]

                        with self.lock:
                            self.clients[client_name] = {
                                "socket": client_socket,
                                "lieu": message.get("lieu", ""),
                                "etat": "LIBRE",
                                "date_connexion": message.get("date_connexion", "")
                            }

                        print(f"{client_name} connecté depuis {client_address}")

                        self.send_client_list(client_socket)

                        self.broadcast({
                            "type": "notification",
                            "evenement": "connexion",
                            "nom": client_name,
                            "lieu": message.get("lieu", "")
                        }, exclude=client_name)

                        self.notify_client_count()

                    elif msg_type == "notification":
                        evenement = message.get("evenement")

                        if evenement == "etat":
                            new_state = message.get("etat", "LIBRE")

                            with self.lock:
                                if client_name in self.clients:
                                    self.clients[client_name]["etat"] = new_state

                            self.broadcast({
                                "type": "notification",
                                "evenement": "etat",
                                "nom": client_name,
                                "etat": new_state
                            }, exclude=client_name)

                        elif evenement == "ecriture":
                            destinataire = message.get("destinataire")
                            with self.lock:
                                if destinataire in self.clients:
                                    self.send_json(self.clients[destinataire]["socket"], {
                                        "type": "notification",
                                        "evenement": "ecriture",
                                        "nom": client_name
                                    })

                    elif msg_type == "message":
                        destinataire = message.get("destinataire")
                        contenu = message.get("contenu", "")

                        with self.lock:
                            if destinataire in self.clients:
                                self.send_json(self.clients[destinataire]["socket"], {
                                    "type": "message",
                                    "expediteur": client_name,
                                    "contenu": contenu
                                })

                    elif msg_type == "deconnexion":
                        raise ConnectionResetError

        except:
            pass

        finally:
            if client_name:
                with self.lock:
                    if client_name in self.clients:
                        del self.clients[client_name]

                self.broadcast({
                    "type": "notification",
                    "evenement": "deconnexion",
                    "nom": client_name
                })

                self.notify_client_count()

                print(f"{client_name} déconnecté")

            client_socket.close()

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Serveur en écoute sur {self.host}:{self.port}")

        while True:
            client_socket, client_address = self.server_socket.accept()
            thread = threading.Thread(
                target=self.handle_client,
                args=(client_socket, client_address),
                daemon=True
            )
            thread.start()


if __name__ == '__main__':
    server = ChatServer(HOST, PORT)
    server.start()