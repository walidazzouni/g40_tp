import argparse

if __name__ == '__main__':
    # Création de l'objet parser
    choices = ['choix1', 'choix2']
    parser = argparse.ArgumentParser(description='Programme de test de parcours des arguments')
    parser.add_argument('--choix', choices=choices, help='Choix du programme')
    parser.add_argument('-d', metavar='DECIMAL', type=int, default=40, help='Nombre de calcul')

    # Création des arguments et leur récupération
    args = parser.parse_args()

    # Affichage des résultats
    print('Le choix entré est', args.choix)
    print('Le decimal entré est', args.d)