def romain_vers_entier(s):
    valeurs = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }

    total = 0

    for i in range(len(s)):
        if i < len(s) - 1 and valeurs[s[i]] < valeurs[s[i + 1]]:
            total -= valeurs[s[i]]
        else:
            total += valeurs[s[i]]

    return total


def entier_vers_romain(n):
    valeurs = [
        (1000, 'M'),
        (900, 'CM'),
        (500, 'D'),
        (400, 'CD'),
        (100, 'C'),
        (90, 'XC'),
        (50, 'L'),
        (40, 'XL'),
        (10, 'X'),
        (9, 'IX'),
        (5, 'V'),
        (4, 'IV'),
        (1, 'I')
    ]

    resultat = ""

    for valeur, symbole in valeurs:
        while n >= valeur:
            resultat += symbole
            n -= valeur

    return resultat


# Exemples demandés
print(romain_vers_entier("III"))       # 3
print(romain_vers_entier("MCMXCIV"))   # 1994

# Bonus
print(entier_vers_romain(3))           # III
print(entier_vers_romain(1994))        # MCMXCIV