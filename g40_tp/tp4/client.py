import socket
import threading
import json
from datetime import datetime

HOST = '127.0.0.1'
PORT = 12345

class ChatClient:
    def __init__(self, host, port, nom, lieu):
        self.host = host
        self.port = port
        self.nom = nom
        self.lieu = lieu
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True

    def send_json(self, data):
        message = json.dumps(data) + '\n'
        self.sock.sendall(message.encode('utf-8'))

    def receive_messages(self):
        buffer = ""

        while self.running:
            try:
                data = self.sock.recv(4096)
                if not data:
                    break

                buffer += data.decode('utf-8')

                while '\n' in buffer:
                    raw_message, buffer = buffer.split('\n', 1)
                    if not raw_message.strip():
                        continue

                    message = json.loads(raw_message)
                    self.handle_message(message)

            except:
                break

        self.running = False
        print("\nConnexion fermée.")

    def handle_message(self, message):
        msg_type = message.get("type")

        if msg_type == "liste_clients":
            print("\n--- Liste des clients connectés ---")
            for client in message["clients"]:
                print(
                    f"Nom: {client['nom']}, "
                    f"Lieu: {client['lieu']}, "
                    f"Etat: {client['etat']}, "
                    f"Date: {client['date_connexion']}"
                )
            print("-----------------------------------")

        elif msg_type == "notification":
            evenement = message.get("evenement")

            if evenement == "nombre_clients":
                print(f"\n[Notification] Nombre de clients connectés : {message['nombre']}")

            elif evenement == "connexion":
                print(f"\n[Notification] {message['nom']} vient de se connecter depuis {message['lieu']}.")

            elif evenement == "deconnexion":
                print(f"\n[Notification] {message['nom']} s'est déconnecté.")

            elif evenement == "ecriture":
                print(f"\n[Notification] {message['nom']} est en train d'écrire...")

            elif evenement == "etat":
                print(f"\n[Notification] {message['nom']} est maintenant {message['etat']}.")

        elif msg_type == "message":
            print(f"\n[Message de {message['expediteur']}] {message['contenu']}")

    def identify(self):
        self.send_json({
            "type": "identification",
            "nom": self.nom,
            "date_connexion": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "lieu": self.lieu
        })

    def run(self):
        self.sock.connect((self.host, self.port))
        self.identify()

        receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        receive_thread.start()

        print("\nCommandes disponibles :")
        print("/msg nom_du_client votre message")
        print("/etat LIBRE")
        print("/etat OCCUPE")
        print("/etat INACTIF")
        print("/quit\n")

        while self.running:
            try:
                texte = input("> ").strip()

                if not texte:
                    continue

                if texte == "/quit":
                    self.send_json({"type": "deconnexion"})
                    break

                elif texte.startswith("/etat "):
                    etat = texte.split(" ", 1)[1].strip().upper()
                    if etat in ["LIBRE", "OCCUPE", "INACTIF"]:
                        self.send_json({
                            "type": "notification",
                            "evenement": "etat",
                            "nom": self.nom,
                            "etat": etat
                        })
                    else:
                        print("Etat invalide.")

                elif texte.startswith("/msg "):
                    morceaux = texte.split(" ", 2)
                    if len(morceaux) < 3:
                        print("Usage : /msg nom_du_client votre message")
                        continue

                    destinataire = morceaux[1]
                    contenu = morceaux[2]

                    self.send_json({
                        "type": "notification",
                        "evenement": "ecriture",
                        "nom": self.nom,
                        "destinataire": destinataire
                    })

                    self.send_json({
                        "type": "message",
                        "expediteur": self.nom,
                        "destinataire": destinataire,
                        "contenu": contenu
                    })

                else:
                    print("Commande inconnue.")

            except KeyboardInterrupt:
                self.send_json({"type": "deconnexion"})
                break
            except:
                break

        self.running = False
        self.sock.close()


if __name__ == '__main__':
    nom = input("Entrez votre nom : ").strip()
    lieu = input("Entrez votre lieu de connexion : ").strip()

    client = ChatClient(HOST, PORT, nom, lieu)
    client.run()