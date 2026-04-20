def produit_autres(tableau):
    resultat = []
    for i in range(len(tableau)):
        produit = 1
        for j in range(len(tableau)):
            if j != i:
                produit *= tableau[j]
        resultat.append(produit)
    return resultat


def test_unitaire():
    assert produit_autres([1, 2, 3, 4, 5]) == [120, 60, 40, 30, 24]
    assert produit_autres([3, 2, 1]) == [2, 3, 6]
    print("Tous les tests sont passes !")


if __name__ == '__main__':
    test_unitaire()
    print(produit_autres([1, 2, 3, 4, 5]))
    print(produit_autres([3, 2, 1]))