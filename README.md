# g40_tp
Application de chat

1) Analyse des programmes client / serveur
Programme 1 : Client socket

Ce programme implémente un client réseau utilisant le protocole TCP.

Dans un premier temps, il crée un socket réseau permettant d’établir une communication avec un serveur distant. Ensuite, il se connecte au serveur maps.google.com via le port 80, correspondant au protocole HTTP.

Une fois la connexion établie, le programme envoie une requête HTTP de type GET afin de demander une ressource spécifique. Il reçoit ensuite la réponse du serveur sous forme de données brutes, qu’il affiche directement à l’écran.

En résumé, ce programme permet d’établir une communication avec un serveur web et d’effectuer une requête HTTP simple afin de récupérer une ressource.

🔹Programme 2 : Serveur UDP

Ce programme implémente un serveur réseau utilisant le protocole UDP.

Il commence par créer un socket UDP, puis l’associe à l’adresse locale 127.0.0.1 et au port 1060, ce qui lui permet d’écouter les messages entrants sur cette interface.

Le serveur fonctionne ensuite en boucle infinie, dans laquelle il attend la réception de messages envoyés par un client. À chaque réception, il décode les données reçues, affiche le contenu du message ainsi que l’adresse du client, puis génère une réponse.

Cette réponse correspond à une chaîne de caractères indiquant la taille, en octets, des données reçues. Elle est ensuite renvoyée au client à l’aide du protocole UDP.

En résumé, ce programme constitue un serveur local simple capable de recevoir des datagrammes UDP, de traiter les messages entrants et de répondre au client avec une information basée sur les données reçues.
2) Explication des fonction : 
client :
socket.socket()

Crée un socket réseau.
Dans ce cas, comme aucun type n’est précisé, c’est un socket TCP par défaut.

sock.connect((hote, port))

Établit une connexion avec le serveur distant.

sock.sendall(...)

Envoie toutes les données au serveur.

sock.recv(4096)

Reçoit jusqu’à 4096 octets depuis le serveur.

print(...)

Affiche le résultat.

connect_to_google()

Fonction définie par le programmeur pour regrouper les instructions du client.

serveur : 

socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

Crée un socket :

AF_INET : IPv4
SOCK_DGRAM : UDP
sock.bind((hote, port))

Associe le socket à une adresse et un port pour écouter les messages.

sock.getsockname()

Retourne l’adresse et le port utilisés par le socket.

sock.recvfrom(MAX_BYTES)

Attend la réception d’un message UDP et retourne :

les données
l’adresse du client
data.decode('ascii')

Transforme les octets reçus en texte.

len(data)

Retourne la taille des données reçues en octets.

text.encode('ascii')

Transforme le texte en octets pour pouvoir l’envoyer.

sock.sendto(data, address)

Envoie les données à l’adresse du client.

server(port)

Fonction définie par le programmeur pour lancer le serveur.

while True

Boucle infinie pour que le serveur continue à écouter.

3) Les programmes de client serveur avec des classes sont mit en piéce jointe.


Chat entre deux clients 

1) Dans le cas d’une communication entre plusieurs clients, il est nécessaire de modifier le serveur afin qu’il assure une fonction de routage. Pour cela, le serveur doit maintenir une structure de données contenant les différents clients connectés ainsi que leurs identifiants respectifs. Lorsqu’un message est reçu, il doit analyser le destinataire visé puis retransmettre le message uniquement au client concerné. Cette approche permet à un client A d’échanger avec un client B de manière ciblée, tout en conservant une architecture centralisée.
  
3) Cette architecture présente plusieurs limites. Tout d’abord, le serveur constitue un point central dont dépend l’ensemble des communications : toute panne ou indisponibilité du serveur interrompt les échanges. Ensuite, lorsque le nombre de clients augmente, la charge du serveur devient plus importante, ce qui peut dégrader les performances globales. De plus, le transit systématique des messages par le serveur ajoute un délai supplémentaire et augmente la complexité de gestion des connexions, des identifiants et du routage. Enfin, cette centralisation soulève également des questions de sécurité et de confidentialité des échanges.
 
