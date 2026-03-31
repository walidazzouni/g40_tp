
# g40_tp
# TP1
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

a) Fonctions du programme client
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
b) Fonctions du programme serveur
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

 ## Encoding

 L’objectif de cet exercice est de construire un tableau résultat dans lequel chaque élément correspond au produit de tous les autres éléments du tableau d’entrée, à l’exception de celui situé à la même position.

La solution proposée repose sur l’utilisation de deux boucles imbriquées. Pour chaque indice du tableau, on calcule le produit de tous les éléments sauf celui de l’indice courant. Ce résultat est ensuite ajouté dans un nouveau tableau.

Cette approche respecte la contrainte de l’exercice, qui interdit l’utilisation de la division.


# TP2

# Exercices

1) Dans le cadre de ce TP, il est possible d'utiliser le polymorphisme, mais uniquement si une hiérarchie de classes est mise en place, avec une classe de base commune et des classes dérivées spécifiques (par exemple, une classe Server et des sous-classes TCPServer et UDPServer). Actuellement, il n'y a pas de relation d'héritage entre les classes du serveur et du client, ce qui empêche l'application du polymorphisme par héritage.

En l'absence de hiérarchie de classes, le polymorphisme par héritage n'est pas utilisé dans ce projet. Cependant, en réorganisant le code avec une classe de base commune et des classes dérivées, il serait possible de manipuler différentes variantes de serveurs (TCP et UDP) de manière uniforme, tout en maintenant des comportements spécifiques à chaque type de serveur.

En résumé, le polymorphisme peut être appliqué dans ce projet si une structure d’héritage est introduite.

#Application de chat 

Dans le cadre de notre application de chat, l'utilisation de sockets TCP est clairement plus adaptée que l'utilisation de sockets UDP. Voici les raisons principales de ce choix :

1. Fiabilité et ordre des messages

Le protocole TCP (Transmission Control Protocol) est un protocole orienté connexion et fiable. Il garantit que les données sont transmises correctement, dans le bon ordre, et sans perte. Cela est essentiel pour une application de chat où il est crucial que les messages arrivent dans le bon ordre et sans erreur. En effet, si un message est perdu en UDP, il n'y a aucune garantie de récupération, ce qui peut entraîner des incohérences dans la conversation.

En revanche, UDP (User Datagram Protocol) est un protocole sans connexion et non fiable. Il n'assure ni l'ordre des messages ni leur livraison, ce qui peut provoquer des pertes de messages ou des réceptions dans un ordre incorrect. Bien que UDP soit plus rapide, cette absence de fiabilité le rend inadapté pour des applications comme un chat où la transmission correcte des messages est essentielle.

2. Contrôle de la congestion et retransmission

TCP inclut des mécanismes de contrôle de congestion et de retransmission des paquets en cas de perte. Cela garantit que si des paquets sont perdus en raison de problèmes de réseau, ils seront retransmis, ce qui est une fonctionnalité importante pour maintenir une communication stable.

UDP, en revanche, ne dispose d'aucun de ces mécanismes. Il est conçu pour des applications où la rapidité prime sur la fiabilité, comme dans le streaming vidéo ou les jeux en ligne, mais il est inapproprié pour des applications nécessitant un échange fiable de données, comme le chat.

3. Simplicité et gestion des connexions

TCP gère automatiquement les connexions entre les clients et le serveur, ce qui simplifie grandement le développement d'une application de chat. Avec TCP, nous savons que la connexion entre le client et le serveur est établie et maintenue tout au long de la communication.

En revanche, UDP ne garantit pas la création d'une connexion, ce qui complique la gestion des communications dans le cadre de notre application de chat.

Conclusion

Pour une application de chat où la fiabilité, l'ordre des messages, et la garantie de livraison sont des critères essentiels, le choix du protocole TCP est clairement plus adapté. UDP pourrait être une option dans des scénarios où la vitesse prime sur la fiabilité, mais pour notre cas d'utilisation, TCP est la solution optimale.


