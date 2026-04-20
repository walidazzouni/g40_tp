# Corrigé — Examen G40 Python 2025


---

## I. QCM

## 1. Le langage Python

### a. Le langage python est un langage

* **Interprété**

### b. Un script écrit en python

* **Peut tourner sur n’importe quelle machine grâce à la machine virtuelle**

> Réponse attendue dans l’esprit du cours : le code Python s’exécute via l’interpréteur / machine virtuelle Python disponible sur la machine cible.

### c. PiP est un programme qui permet

* **D’installer et de supprimer des libraries python sur une machine**

### d. Python dans sa version 3

* **Est un langage typé**

### e. Un script écrit en python

* **Dépend fortement de la version de python avec laquelle il est écrit**

> Certaines syntaxes et comportements changent selon la version de Python.

---

## 2. Structures de données et fonctions

### a. Les chaines de caractères en Python sont

* **Immuables et homogènes dans leur contenu**

> Une chaîne est immuable et contient des caractères.

### b. Soit `ma_liste = [1, 2, 3, 4, 5, 6]`, choisir les deux derniers éléments

* **`ma_liste[-2:]`**

### c. Soit la liste suivante `ma_liste = [1, 3, 1, 5, 5, 7, 11, 13]`

Avec :

```python
mon_set = set(ma_liste)
```

La bonne idée attendue est :

* **on obtient l’ensemble des valeurs sans doublons**

> Le sujet propose des réponses sous forme de listes, ce qui est techniquement imprécis : `set(...)` retourne un **ensemble** et non une liste. La réponse la plus proche attendue est donc celle qui élimine les doublons.

### d. Les annotations dans le langage python permettent

* **D’enregistrer des définitions des variables**

> Ici il s’agit des annotations de type, utilisées pour documenter les types attendus.

### e. Programme avec fonctions / décorateur

* **`registring <function func1>`**
* **`running func1`**

> Le décorateur s’exécute lors de la définition de la fonction, puis la fonction décorée s’exécute ensuite.

---

## 3. Orienté objet

### a. Python est un langage de programmation

* **Hybride**

### b. Python permet de déclarer des membres privés dans une classe

* **En précédant le nom par le symbole `_`**

> Plus exactement : `_nom` est une convention de protection, et `__nom` déclenche un name mangling. Python n’a pas de vrai mot-clé `private`.

### c. Python permet

* **Un héritage multiple**

### d. Pour construire une nouvelle instance d’une classe

* **On utilise la fonction `__new__`**
* **On utilise la fonction `__init__`**

> `__new__` crée l’instance, puis `__init__` l’initialise. Dans beaucoup de cours, on retient surtout `__init__`, mais techniquement les deux interviennent.

### e. La fonction `__del__`, destructeur d’une classe, permet de

* **Décrémenter le compteur mémoire de l’objet, c’est le garbage collector qui s’occupera de la destruction de toutes les occurrences**

> Formulation du sujet un peu approximative, mais l’idée attendue est que `__del__` n’est pas un “delete” direct de toutes les occurrences.

---

## VI. Programmation

L’énoncé demande de développer un serveur assistant IA capable de gérer plusieurs clients TCP, de tokeniser les messages, d’interroger un LLM, puis de calculer une note moyenne d’évaluation.

---

## 1. Définition de la classe `LeChat`

Le constructeur doit recevoir :

* `max_client`
* `max_message_len`
* `ip_address`
* `port`

### Proposition de correction

```python
import socket
import threading


class LeChat(object):
    def __init__(self, max_client, max_message_len, ip_address, port):
        self.max_client = max_client
        self.max_message_len = max_message_len
        self.ip_address = ip_address
        self.port = port

        self.server_socket = None
        self.clients = []
        self.vocab = {}

        self.total_notes = 0
        self.nb_notes = 0
        self.evaluation = 0.0

        self.lock = threading.Lock()
```

### Pourquoi ces attributs ?

En plus des paramètres demandés, il faut stocker :

* la socket serveur
* la liste des clients connectés
* le vocabulaire si le serveur doit tokeniser
* les variables de calcul de la moyenne des notes
* un verrou (`Lock`) pour protéger les accès concurrents

---

## 2. Fonction `manage_connexions`

L’énoncé demande de gérer des connexions TCP et de faire les modifications nécessaires dans le constructeur. Comme plusieurs clients doivent être gérés, on ouvre une socket serveur, on la met en écoute, puis on accepte les connexions jusqu’à la limite `max_client`.

### Proposition d’implémentation

```python
def manage_connexions(self):
    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server_socket.bind((self.ip_address, self.port))
    self.server_socket.listen()

    while len(self.clients) < self.max_client:
        client_socket, client_address = self.server_socket.accept()
        self.clients.append(client_socket)

        t = threading.Thread(target=self.handle_client, args=(client_socket,))
        t.start()
```

### Remarque

Une autre version acceptable consiste à ne faire ici que l’acceptation des connexions, puis à lancer les threads ailleurs dans une méthode principale.

---

## 3. Fonction `tokenizer`

### Ce que demande l’énoncé

La fonction prend :

* un dictionnaire `vocab` dont les clés sont des chaînes de caractères
* un message contenant plusieurs mots

Elle doit retourner une **liste d’entiers** correspondant aux identifiants des mots du message.

L’énoncé est un peu ambigu sur la signature exacte, car il dit que la fonction prend `vocab` en paramètre mais parle aussi du “message”. La solution la plus logique est de faire une fonction prenant `message` et `vocab`.

### Proposition d’implémentation

```python
def tokenizer(self, message, vocab):
    tokens = []
    mots = message.split()

    for mot in mots:
        if mot in vocab:
            tokens.append(vocab[mot])

    return tokens
```

### Exemple

```python
vocab = {
    "bonjour": 1,
    "comment": 2,
    "ça": 3,
    "va": 4
}

message = "bonjour comment ça va"
# Résultat : [1, 2, 3, 4]
```

### Variante acceptable

Si le sujet voulait absolument un seul paramètre explicite `vocab`, on peut supposer que `message` est déjà disponible dans l’objet. Mais la version la plus propre reste celle ci-dessus.

---

## 4. Fonction `handle_client`

### Règles demandées

Dans une boucle infinie, le serveur doit :

1. recevoir un texte avec `recv`
2. rejeter le message si :

   * il ne finit pas par `?`
   * sa taille dépasse `max_message_len`
   * il contient le mot `merci`
3. si message invalide : envoyer `Texte invalide`
4. sinon :

   * tokeniser le texte
   * envoyer la liste d’entiers à `handle_llm`
   * récupérer une chaîne de caractères en réponse
   * renvoyer cette réponse au client

### Proposition d’implémentation

```python
def handle_client(self, client_socket):
    while True:
        msg = client_socket.recv(1024).decode()

        if not msg:
            break

        if (not msg.endswith("?")) or (len(msg) > self.max_message_len) or ("merci" in msg.lower()):
            client_socket.send("Texte invalide".encode())
            continue

        tokens = self.tokenizer(msg, self.vocab)
        response = handle_llm(tokens)
        client_socket.send(response.encode())
```

---

## 5. Ajout de l’évaluation instantanée et fonction `get_evaluation`

### Ce que demande l’énoncé

Après chaque réponse envoyée au client, le serveur reçoit une note sur 10.
Il faut :

* intégrer cette note dans le calcul instantané de la moyenne
* ajouter une fonction `get_evaluation()` qui renvoie cette moyenne

### Modification de `handle_client`

```python
def handle_client(self, client_socket):
    while True:
        msg = client_socket.recv(1024).decode()

        if not msg:
            break

        if (not msg.endswith("?")) or (len(msg) > self.max_message_len) or ("merci" in msg.lower()):
            client_socket.send("Texte invalide".encode())
            continue

        tokens = self.tokenizer(msg, self.vocab)
        response = handle_llm(tokens)
        client_socket.send(response.encode())

        note_msg = client_socket.recv(1024).decode()

        if note_msg.isdigit():
            note = int(note_msg)
            if 0 <= note <= 10:
                with self.lock:
                    self.total_notes += note
                    self.nb_notes += 1
                    self.evaluation = self.total_notes / self.nb_notes
```

### Fonction `get_evaluation`

```python
def get_evaluation(self):
    return self.evaluation
```

### Variante un peu plus robuste

```python
def get_evaluation(self):
    with self.lock:
        if self.nb_notes == 0:
            return 0
        return self.total_notes / self.nb_notes
```

Cette deuxième version est meilleure, car elle évite de dépendre d’une variable dérivée et gère le cas sans note.

---

## 6. Proposition d’implémentation complète

```python
import socket
import threading


def handle_llm(tokens):
    return f"Réponse du LLM pour {tokens}"


class LeChat(object):
    def __init__(self, max_client, max_message_len, ip_address, port):
        self.max_client = max_client
        self.max_message_len = max_message_len
        self.ip_address = ip_address
        self.port = port

        self.server_socket = None
        self.clients = []
        self.vocab = {}

        self.total_notes = 0
        self.nb_notes = 0
        self.lock = threading.Lock()

    def manage_connexions(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip_address, self.port))
        self.server_socket.listen()

        while len(self.clients) < self.max_client:
            client_socket, client_address = self.server_socket.accept()
            self.clients.append(client_socket)

            t = threading.Thread(target=self.handle_client, args=(client_socket,))
            t.start()

    def tokenizer(self, message, vocab):
        tokens = []
        mots = message.split()

        for mot in mots:
            if mot in vocab:
                tokens.append(vocab[mot])

        return tokens

    def handle_client(self, client_socket):
        while True:
            msg = client_socket.recv(1024).decode()

            if not msg:
                break

            if (not msg.endswith("?")) or (len(msg) > self.max_message_len) or ("merci" in msg.lower()):
                client_socket.send("Texte invalide".encode())
                continue

            tokens = self.tokenizer(msg, self.vocab)
            response = handle_llm(tokens)
            client_socket.send(response.encode())

            note_msg = client_socket.recv(1024).decode()
            if note_msg.isdigit():
                note = int(note_msg)
                if 0 <= note <= 10:
                    with self.lock:
                        self.total_notes += note
                        self.nb_notes += 1

        client_socket.close()

    def get_evaluation(self):
        with self.lock:
            if self.nb_notes == 0:
                return 0
            return self.total_notes / self.nb_notes
```

---

## Points importants à retenir pour l’examen

### Sur la partie réseau

* TCP = `socket.AF_INET` + `socket.SOCK_STREAM`
* `bind()` pour attacher l’adresse
* `listen()` pour écouter
* `accept()` pour accepter un client
* `recv()` pour recevoir
* `send()` pour envoyer

### Sur la partie threads

Les threads sont utiles ici pour gérer plusieurs clients en parallèle.
Sans threads, un client bloquerait les autres pendant l’attente de réception.

### Sur la moyenne des notes

Comme plusieurs clients peuvent envoyer des notes en même temps, il faut protéger la mise à jour des variables partagées avec un `Lock`.


