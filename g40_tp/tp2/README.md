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


