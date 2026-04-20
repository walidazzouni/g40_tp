# TP3
1. Lorsque qu'un client se connecte, le serveur lui envoie la liste des clients déjà connectés :

Lorsqu'un client se connecte au serveur, le serveur doit lui fournir une liste des autres clients déjà connectés. Cela permet au client de savoir quels utilisateurs sont actuellement disponibles pour la communication. Cette liste peut être composée d'adresses IP ou de pseudos des clients.

Le serveur gère une liste des clients connectés.
Dès qu'un client se connecte, le serveur lui envoie cette liste, excluant son propre nom de la liste. Cela lui permet de savoir à qui il peut envoyer des messages.
Comment ça fonctionne :
Lorsqu'un client se connecte, le serveur récupère les informations de connexion (par exemple, l'adresse IP du client).
Le serveur génère la liste des clients déjà connectés et l'envoie au nouveau client.

Exemple :
Si un client se connecte, il pourrait recevoir une réponse comme :
"Clients connectés : client1, client2, client3"
Cela l'informe des autres utilisateurs en ligne.

2. Lorsque qu'un client se déconnecte, le serveur envoie une notification aux autres clients. Que contient cette notification ?

Lorsqu'un client se déconnecte du serveur, il est important que les autres clients soient informés de cette déconnexion afin qu'ils sachent que ce client n'est plus disponible pour la communication. Cette notification est envoyée à tous les clients restants.

Contenu de la notification :

La notification pourrait inclure :

Le nom ou l'adresse IP du client qui se déconnecte.
Un message simple comme "Le client [nom] s'est déconnecté."

Cela informe les autres clients qu'un utilisateur a quitté la conversation et qu'il n'est plus actif. La notification peut être envoyée sous forme de texte simple.

Exemple :
Si le client "client2" se déconnecte, les autres clients pourraient recevoir la notification :
"Le client client2 s'est déconnecté."

Cette notification permet aux autres utilisateurs de savoir que ce client est parti et qu'il ne recevra plus de messages.

3. Au moment de l’envoi d’un message, un client choisit son interlocuteur :

Dans une application de chat, il peut être souhaitable qu'un client choisisse un interlocuteur spécifique à qui envoyer un message, plutôt que d'envoyer un message à tous les clients. Cela permet de créer des conversations privées entre deux utilisateurs.

Fonctionnement de l'envoi de messages à un interlocuteur spécifique :
Lorsqu'un client veut envoyer un message privé, il spécifie le destinataire (par exemple, en utilisant un pseudo ou une adresse IP).
Le message sera envoyé uniquement à cet interlocuteur spécifique, et non à tous les clients connectés.
