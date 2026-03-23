# g40_tp

# Application de chat

# 1) Analyse des programmes client / serveur
🔹 Programme 1 : Client socket

Ce programme met en œuvre un client réseau basé sur le protocole TCP.

Dans un premier temps, il crée un socket réseau permettant d’établir une communication avec un serveur distant. Il se connecte ensuite au serveur maps.google.com via le port 80, qui correspond au protocole HTTP.

Une fois la connexion établie, le client envoie une requête HTTP de type GET afin de solliciter une ressource spécifique. Le serveur distant traite cette requête et renvoie une réponse, qui est reçue sous forme de données brutes par le client. Ces données sont ensuite affichées à l’écran.

Ainsi, ce programme illustre le fonctionnement d’un client HTTP simple, capable d’établir une connexion TCP avec un serveur web et de récupérer une ressource via une requête HTTP.

🔹 Programme 2 : Serveur UDP

Ce programme implémente un serveur réseau utilisant le protocole UDP.

Il commence par créer un socket UDP, puis l’associe à l’adresse locale 127.0.0.1 et au port 1060. Cette opération permet au serveur de se mettre en attente de messages entrants sur cette interface.

Le serveur fonctionne ensuite en boucle infinie, dans laquelle il attend la réception de datagrammes envoyés par des clients. À chaque message reçu, il décode les données afin de les convertir en texte, puis affiche le contenu du message ainsi que l’adresse du client émetteur.

Le serveur génère ensuite une réponse contenant la taille, en octets, des données reçues. Cette réponse est encodée puis renvoyée au client à l’aide du protocole UDP.

En résumé, ce programme constitue un serveur local simple permettant de recevoir, traiter et répondre à des messages envoyés par des clients via des datagrammes UDP.

# 2) Explication des fonctions utilisées

🔹 Fonctions du programme client
socket.socket()
Permet de créer un socket réseau. En l’absence de paramètres, il s’agit par défaut d’un socket utilisant le protocole TCP.
sock.connect((hôte, port))
Établit une connexion avec le serveur distant en spécifiant son adresse et son port.
sock.sendall(...)
Envoie l’intégralité des données au serveur via la connexion TCP.
sock.recv(4096)
Reçoit les données envoyées par le serveur, avec une taille maximale de 4096 octets.
print(...)
Affiche les données reçues à l’écran.
connect_to_google()
Fonction définie par le programmeur permettant de regrouper les différentes étapes de la communication client.
🔹 Fonctions du programme serveur
socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
Crée un socket réseau :
AF_INET : utilisation du protocole IPv4
SOCK_DGRAM : utilisation du protocole UDP
sock.bind((hôte, port))
Associe le socket à une adresse et un port afin de permettre l’écoute des messages entrants.
sock.getsockname()
Retourne l’adresse IP et le port utilisés par le socket.
sock.recvfrom(MAX_BYTES)
Attend la réception d’un message UDP et retourne :
les données reçues
l’adresse du client émetteur
data.decode('ascii')
Convertit les données reçues (octets) en chaîne de caractères.
len(data)
Calcule la taille des données reçues en nombre d’octets.
text.encode('ascii')
Convertit une chaîne de caractères en données binaires (octets) afin de pouvoir l’envoyer sur le réseau.
sock.sendto(data, address)
Envoie les données au client spécifié par son adresse.
server(port)
Fonction définie par le programmeur permettant d’initialiser et de lancer le serveur.
while True

Met en place une boucle infinie afin de permettre au serveur de fonctionner en continu et de traiter plusieurs messages successifs.
3) Les programmes de client serveur avec des classes sont mit en piéce jointe.


## Chat entre deux clients 

1) Dans le cas d’une communication entre plusieurs clients, il est nécessaire de modifier le serveur afin qu’il assure une fonction de routage. Pour cela, le serveur doit maintenir une structure de données contenant les différents clients connectés ainsi que leurs identifiants respectifs. Lorsqu’un message est reçu, il doit analyser le destinataire visé puis retransmettre le message uniquement au client concerné. Cette approche permet à un client A d’échanger avec un client B de manière ciblée, tout en conservant une architecture centralisée.
  
3) Cette architecture présente plusieurs limites. Tout d’abord, le serveur constitue un point central dont dépend l’ensemble des communications : toute panne ou indisponibilité du serveur interrompt les échanges. Ensuite, lorsque le nombre de clients augmente, la charge du serveur devient plus importante, ce qui peut dégrader les performances globales. De plus, le transit systématique des messages par le serveur ajoute un délai supplémentaire et augmente la complexité de gestion des connexions, des identifiants et du routage. Enfin, cette centralisation soulève également des questions de sécurité et de confidentialité des échanges.
 
