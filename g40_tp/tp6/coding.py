def nb_facons(n):
    if n < 0:
        return 0
    if n == 0 or n == 1:
        return 1

    a, b = 1, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def compter_mots(texte):
    mots = texte.split()
    return len(mots)


# Tests
print("Exercice 1 :")
print("Pour 4 marches ->", nb_facons(4))

print("\nExercice 2 :")
texte = "Bonjour tout le monde, commencez à coder."
print("Nombre de mots ->", compter_mots(texte))