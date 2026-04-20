# Corrigé — Examen G40 Python 2024

## Source

Corrigé rédigé à partir du sujet **Examen G40 Python 2024**.

---

## I. QCM

### 1. Le langage Python

#### a. Le langage python est un langage typé

* ✅ **Vrai**

#### b. Un script écrit en python

* ✅ **Peut ne pas contenir une fonction main**

#### c. Sur une seule machine on peut

* ✅ **Installer plusieurs versions de python**

#### d. Le programme pip, permet

* ✅ **De gérer l’installation des paquets python**

#### e. Dans python, GIL (Global Interpreter Lock), permet

* ✅ **Protéger les objets pythons lors de l’exécution des threads concurrentiels**

---

### 2. Structures de données et fonctions

#### a. Une fonction python qui reçoit en paramètre un objet de ce type `**args`

* ✅ **Un dictionnaire**

> Remarque : en pratique on écrit plutôt `**kwargs`.

#### b. `my_str = 'Bonjour'` puis `print(f'{my_str[::-1]}')`

* ✅ **`ruojnoB` est affiché**

#### c. `my_str = '2022'` puis `print(set(my_str))`

* ✅ **`{'0', '2'}` est affiché à l’écran**

> L’ordre peut varier : `{'2', '0'}` est équivalent.

#### d. Une fonction dans python

* ✅ **Est un objet**

#### e. Programme avec décorateur `accept_function`

* ✅ **La fonction `addition` provoque une erreur, la fonction `__addition` est valide**

> Le décorateur vérifie que `fn.__name__.startswith('__')`.

---

### 3. Orienté objet

#### a. Le type `real` dans python est

* ✅ **Inexistant**

#### b. Une classe en python

* ✅ **Peut être déclarée sans définir aucune fonction y compris le constructeur**
* ✅ **Peut ne pas définir un destructeur**

#### c. En python, une classe A qui hérite d’une classe B et d’une classe C

* ✅ **Se réfère aux classes mères avec leur nom**

> L’héritage multiple est autorisé, et `super()` existe aussi.

#### d. Classes `A`, `B`, `C(A, B)`

* ✅ **Rien, le code est valide**

#### e. Classe `Node` et variables `node_1`, `node_2`, `node_3`

* ✅ **`1`**

> `node_3 = node_1` référence le même objet. `del(node_1)` supprime seulement le nom, pas l’objet lui-même.

---

## VI. Programmation

## 1. Constructeur de `Game`

L’énoncé demande de sauvegarder les paramètres d’entrée dans les attributs de l’objet.

```python
class Game(object):
    def __init__(self, max_gamers, nbr_sticks) -> None:
        """
        max_gamers : le nombre maximal de joueurs
        nbr_sticks : nombre de bâtons dans le jeu
        """
        self.max_gamers = max_gamers
        self.nbr_sticks = nbr_sticks
```

---

## 2. Fonction `listen` en pseudo-code

### Ce qu’il faut ajouter au constructeur

Pour écouter des connexions, il faut aussi prévoir :

* l’adresse du serveur (`host`)
* le port (`port`)
* la liste des joueurs connectés
* éventuellement la socket d’écoute

Exemple :

```python
class Game(object):
    def __init__(self, max_gamers, nbr_sticks, host, port) -> None:
        self.max_gamers = max_gamers
        self.nbr_sticks = nbr_sticks
        self.host = host
        self.port = port
        self.players = []
        self.server_socket = None
```

### Pseudo-code de `listen`

```text
fonction listen():
    créer une socket TCP d’écoute
    associer la socket à (host, port)
    mettre la socket en mode écoute

    tant que le nombre de joueurs connectés < max_gamers:
        accepter une nouvelle connexion
        récupérer la socket de communication du client
        récupérer l’adresse du client
        créer un joueur ou enregistrer la socket du joueur
        ajouter ce joueur dans la liste des joueurs connectés

    quand le nombre maximal est atteint:
        arrêter l’acceptation de nouvelles connexions
```

### Version proche de Python

```python
def listen(self):
    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server_socket.bind((self.host, self.port))
    self.server_socket.listen()

    while len(self.players) < self.max_gamers:
        client_socket, client_addr = self.server_socket.accept()
        self.players.append((client_socket, client_addr))
```

---

## 3. Méthode `communicate_with_client`

### Énoncé résumé

Le serveur :

1. envoie au joueur : `Choisissez 1, 2 ou 3 bâtonnets à retirer`
2. lit la réponse
3. vérifie qu’elle est valide
4. retire le nombre de bâtonnets demandé
5. si le joueur n’a pas pris le dernier bâtonnet : envoyer `vous restez dans le jeu`
6. sinon : envoyer `perdu` au joueur concerné et `gagné` à tous les autres

### Proposition d’implémentation

```python
def communicate_with_client(self, client_id):
    send(client_id, "Choisissez 1, 2 ou 3 bâtonnets à retirer")
    msg = read()

    if not msg.isdigit():
        send(client_id, "erreur")
        return

    nb = int(msg)

    if nb < 1 or nb > 3:
        send(client_id, "erreur")
        return

    if nb > self.nbr_sticks:
        send(client_id, "erreur")
        return

    self.nbr_sticks -= nb

    if self.nbr_sticks > 0:
        send(client_id, "vous restez dans le jeu")
    else:
        send(client_id, "perdu")
        for other_id in self.players:
            if other_id != client_id:
                send(other_id, "gagné")
```

---

## 4. Amélioration : informer les joueurs du nombre de bâtonnets restants

### Modification de `communicate_with_client`

```python
def communicate_with_client(self, client_id):
    send(client_id, f"Il reste {self.nbr_sticks} bâtonnets")
    send(client_id, "Choisissez 1, 2 ou 3 bâtonnets à retirer")
    msg = read()

    if not msg.isdigit():
        send(client_id, "erreur")
        return

    nb = int(msg)

    if nb < 1 or nb > 3:
        send(client_id, "erreur")
        return

    if nb > self.nbr_sticks:
        send(client_id, "erreur")
        return

    self.nbr_sticks -= nb

    if self.nbr_sticks > 0:
        for player_id in self.players:
            send(player_id, f"Il reste {self.nbr_sticks} bâtonnets")
        send(client_id, "vous restez dans le jeu")
    else:
        send(client_id, "perdu")
        for other_id in self.players:
            if other_id != client_id:
                send(other_id, "gagné")
```

### Où utiliser les threads ?

On utilise les **threads** au niveau de la communication avec les clients.

### Pourquoi ?

Parce que :

* plusieurs joueurs peuvent être connectés en même temps
* le serveur ne doit pas être bloqué par un seul joueur
* chaque client peut être géré indépendamment

Un thread par client permet donc de traiter plusieurs communications en parallèle.

### Fonction principale de `Game`

```python
import socket
import threading

class Game(object):
    def __init__(self, max_gamers, nbr_sticks, host, port) -> None:
        self.max_gamers = max_gamers
        self.nbr_sticks = nbr_sticks
        self.host = host
        self.port = port
        self.players = []
        self.server_socket = None

    def listen(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

        while len(self.players) < self.max_gamers:
            client_socket, client_addr = self.server_socket.accept()
            self.players.append(client_socket)

    def communicate_with_client(self, client_id):
        send(client_id, f"Il reste {self.nbr_sticks} bâtonnets")
        send(client_id, "Choisissez 1, 2 ou 3 bâtonnets à retirer")
        msg = read()

        if not msg.isdigit():
            send(client_id, "erreur")
            return

        nb = int(msg)

        if nb < 1 or nb > 3 or nb > self.nbr_sticks:
            send(client_id, "erreur")
            return

        self.nbr_sticks -= nb

        if self.nbr_sticks > 0:
            for player_id in self.players:
                send(player_id, f"Il reste {self.nbr_sticks} bâtonnets")
            send(client_id, "vous restez dans le jeu")
        else:
            send(client_id, "perdu")
            for other_id in self.players:
                if other_id != client_id:
                    send(other_id, "gagné")

    def run(self):
        self.listen()

        threads = []
        for player in self.players:
            t = threading.Thread(target=self.communicate_with_client, args=(player,))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()
```

> En pratique, il faudrait aussi gérer l’ordre des tours, la synchronisation et l’accès concurrent à `self.nbr_sticks`.

---

## 5. Passage de TCP à UDP

### Changements à apporter

Avec UDP :

* on crée une socket avec `SOCK_DGRAM`
* on n’utilise pas `listen()` ni `accept()`
* on communique avec `sendto()` et `recvfrom()`
* il faut gérer explicitement l’adresse du client

### Exemple d’adaptation

```python
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((self.host, self.port))

message, client_addr = server_socket.recvfrom(1024)
server_socket.sendto("message".encode(), client_addr)
```

### Comparatif TCP / UDP

| Critère                            | TCP                         | UDP                               |
| ---------------------------------- | --------------------------- | --------------------------------- |
| Type                               | orienté connexion           | non orienté connexion             |
| Fiabilité                          | fiable                      | non garantie                      |
| Ordre des messages                 | garanti                     | non garanti                       |
| Contrôle d’erreur / retransmission | oui                         | non                               |
| Vitesse                            | plus lourd                  | plus rapide                       |
| Usage typique                      | chat, web, transfert fiable | streaming, jeux, voix, temps réel |

### Conclusion

Pour ce jeu, **TCP** est plus simple et plus adapté si on veut une communication fiable.
UDP peut être utilisé, mais il faut gérer soi-même davantage d’éléments : pertes, ordre, suivi des clients.

---

## Remarques finales

Ce corrigé propose une **solution raisonnable d’examen** :

* correcte sur le plan Python
* cohérente avec l’énoncé
* suffisamment claire pour une rédaction sur copie

Pour une vraie application réseau complète, il faudrait en plus :

* gérer précisément les tours de jeu
* protéger `nbr_sticks` avec synchronisation (`Lock`)
* identifier clairement chaque joueur
* gérer les déconnexions et erreurs réseau
