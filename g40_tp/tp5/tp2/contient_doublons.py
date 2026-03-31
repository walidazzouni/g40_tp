def contient_doublons(t):
    # Vérifie si la taille du tableau est différente de la taille de l'ensemble (qui supprime les doublons)
    return len(t) != len(set(t))

# Exemples donnés
print(contient_doublons([1, 2, 3, 1]))  # Sortie attendue: True (car il y a un doublon)
print(contient_doublons([1, 2, 3, 4]))  # Sortie attendue: False (aucun doublon)