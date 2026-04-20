import socket
import threading

# Liste des clients connectés, chaque client est un tuple (adresse, socket)
clients = []

# Verrou pour protéger l'accès à la liste des clients
print_lock = threading.Lock()

def thread_ecoute():
    host = "127.0.0.1"  # Adresse IP du serveur
    port = 12345         # Port du serveur
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    print(f"Serveur à l'écoute sur {host}:{port}...")

    while True:
        c, addr = s.accept()
        print(f"Client connecté depuis {addr[0]} : {addr[1]}")
        
        # Envoie la liste des clients connectés à ce client
        send_client_list(c)
        
        # Ajout du client à la liste des clients connectés
        print_lock.acquire()
        clients.append((addr, c))
        print_lock.release()

        # Création d'un thread pour chaque client
        client_thread = threading.Thread(target=communication_client, args=(c, addr))
        client_thread.start()

    s.close()

def send_client_list(client_socket):
    # Récupérer la liste des clients connectés (en excluant le client actuel)
    client_list = [addr[0] for addr, _ in clients]
    client_list_str = "Clients connectés: " + ", ".join(client_list)
    client_socket.send(client_list_str.encode())

def communication_client(c, addr):
    while True:
        try:
            data = c.recv(1024)
            if not data:
                break

            message = data.decode('utf-8')
            print(f"Message reçu de {addr}: {message}")

            # Vérifier si le message contient un destinataire spécifique
            if message.startswith("/msg "):
                # Format : "/msg <client> <message>"
                parts = message.split(" ", 2)
                if len(parts) == 3:
                    dest_client = parts[1]
                    msg_content = parts[2]
                    send_message_to_client(dest_client, msg_content, addr)
            else:
                # Si le message ne spécifie pas de destinataire, on l'envoie à tous les clients
                broadcast_message(message)

        except:
            break

    # Lorsque le client se déconnecte, on le retire de la liste et on notifie les autres clients
    print_lock.acquire()
    clients.remove((addr, c))  # Retirer le client de la liste des clients
    print_lock.release()
    broadcast_message(f"Le client {addr} s'est déconnecté.")  # Notifier les autres clients

    c.close()

def broadcast_message(message):
    # Envoie le message à tous les autres clients
    for _, client_socket in clients:
        try:
            client_socket.send(message.encode())
        except:
            pass

def send_message_to_client(client_name, message, sender_address):
    # Envoie le message à un client spécifique
    for addr, client_socket in clients:
        if addr[0] == client_name:
            client_socket.send(f"Message de {sender_address}: {message}".encode())
            break

if __name__ == '__main__':
    thread_ecoute()