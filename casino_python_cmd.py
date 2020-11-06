# import pandas as pd
import random

deck = ['2-h', '3-h', '4-h', '5-h', '6-h', '7-h', '8-h', '9-h', '10-h', 'J-h', 'Q-h', 'K-h', 'A-h', '2-d', '3-d', '4-d',
        '5-d', '6-d', '7-d', '8-d', '9-d', '10-d', 'J-d', 'Q-d', 'K-d', 'A-d', '2-c', '3-c', '4-c', '5-c', '6-c', '7-c',
        '8-c', '9-c', '10-c', 'J-c', 'Q-c', 'K-c', 'A-c', '2-s', '3-s', '4-s', '5-s', '6-s', '7-s', '8-s', '9-s',
        '10-s', 'J-s', 'Q-s', 'K-s', 'A-s']


def premier_tirage():
    tirage = []
    nouveau_deck = deck.copy()
    for x in range(5):
        tirage.append(nouveau_deck.pop(random.randint(0, len(nouveau_deck) - 1)))
    return tirage, nouveau_deck


def choix_carte(tirage):
    command = ''
    result = []
    print(tirage)
    for x in range(len(tirage)):
        print(tirage[x])
        command = input("Voulez vous garder cette carte? y/n ")
        if command.lower() == 'y':
            result.append(tirage[x])
            print("carte gardée\n")
        elif command.lower() == 'n':
            print("carte retirée\n")
        else:
            print("commande invalide\n")
            pass
    return result


def deuxieme_tirage(jeu, deck):
    nb_tirage = (5 - len(jeu))
    tirage_final = jeu.copy()

    if nb_tirage > 0:
        for x in range(nb_tirage):
            tirage_final.append(deck.pop(random.randint(0, len(deck) - 1)))

    return tirage_final


def machine():
    tirage1, deck_restant = premier_tirage()
    choix1 = choix_carte(tirage1)
    tirage2 = deuxieme_tirage(choix1, deck_restant)
    print('Main finale: {}'.format(tirage2))
    return tirage2


# Compte les cartes en main et regroupe en 2 dictionnaires : Valeurs et Couleurs
def comptage_main(main):
    valeurs = {}
    couleurs = {}
    for x in range(len(main)):
        values = main[x].split("-")
        if values[0] in valeurs:
            valeurs[values[0]] += 1
        else:
            valeurs[values[0]] = 1

        if values[1] in couleurs:
            couleurs[values[1]] += 1
        else:
            couleurs[values[1]] = 1

    return valeurs, couleurs


# Converti J/Q/K/A en valeurs numériques
def convertir_valeurs(compte_valeurs):
    valeurs = {}
    for x in compte_valeurs:
        if x.lower() == 'j':
            valeurs['11'] = compte_valeurs[x]
        elif x.lower() == 'q':
            valeurs['12'] = compte_valeurs[x]
        elif x.lower() == 'k':
            valeurs['13'] = compte_valeurs[x]
        elif x.lower() == 'a':
            valeurs['14'] = compte_valeurs[x]
        else:
            valeurs[x] = compte_valeurs[x]

    return valeurs


def compter_paires(compte_main):
    paires = 0
    for x in compte_main:
        if compte_main[x] == 2:
            if x == "h" or x == "d" or x == "c" or x == "s":
                pass
            else:
                paires += 1
    return paires


def compter_brelan(compte_main):
    brelan = 0
    for x in compte_main:
        if compte_main[x] == 3:
            if x == "h" or x == "d" or x == "c" or x == "s":
                pass
            else:
                brelan += 1
    return brelan


def compter_carre(compte_main):
    carre = 0
    for x in compte_main:
        if compte_main[x] == 4:
            if x == "h" or x == "d" or x == "c" or x == "s":
                pass
            else:
                carre += 1
    return carre


def compter_flush(compte_main):
    flush = 0
    for x in compte_main:
        if compte_main[x] == 5:
            if x == "h" or x == "d" or x == "c" or x == "s":
                flush += 1
    return flush


def compter_full(compte_main):
    brelan = 0
    paire = 0

    for x in compte_main:
        if compte_main[x] == 3:
            if x == "h" or x == "d" or x == "c" or x == "s":
                pass
            else:
                brelan += 1
        elif compte_main[x] == 2:
            if x == "h" or x == "d" or x == "c" or x == "s":
                pass
            else:
                paire += 1

    if brelan > 0 and paire > 0:
        return True
    else:
        return False


def compter_quinte(compte_valeurs):
    valeurs = convertir_valeurs(compte_valeurs)
    keys = valeurs.keys()
    int_keys = []
    suite = []

    for x in keys:
        int_keys.append(int(x))

    int_keys.sort()

    if len(int_keys) == 5:
        for x in range(len(int_keys) - 1):
            if int_keys[x + 1] == (int_keys[x] + 1):
                suite.append(True)

        if int_keys[4] == 14:
            if int_keys[0] == 2 and int_keys[1] == 3 and int_keys[2] == 4 and int_keys[3] == 5:
                suite.append(True)

    if suite.count(True) == 4:
        return True
    else:
        return False


def compter_quinte_flush(compte_valeurs, compte_couleurs):
    if compter_quinte(compte_valeurs) and compter_flush(compte_couleurs):
        return True
    else:
        return False


def compter_quinte_flush_royale(compte_valeurs, compte_couleurs):
    combinaison_gagnante = ['10', 'J', 'Q', 'K', 'A']
    ma_combinaison = compte_valeurs.keys()

    if sorted(ma_combinaison) == sorted(combinaison_gagnante):
        for x in compte_couleurs:
            if compte_couleurs[x] == 5:
                return True
            else:
                pass
    else:
        return False


# Teste les différentes combinaisons et renvoie la combinaison la plus forte
def compte_combinaisons_gagnantes(compte_valeurs, compte_couleurs):
    combinaisons = {'paire': 0,
                    'double_paire': 0,
                    'brelan': 0,
                    'carre': 0,
                    'flush': 0,
                    'full': 0,
                    'quinte': 0,
                    'quinte_flush': 0,
                    'quinte_flush_royale': 0}

    combinaison_gagnante = None

    if compter_paires(compte_valeurs):
        combinaisons['paire'] = 1

    if compter_paires(compte_valeurs) == 2:
        combinaisons['double_paire'] = 1

    if compter_brelan(compte_valeurs):
        combinaisons['brelan'] = 1

    if compter_carre(compte_valeurs):
        combinaisons['carre'] = 1

    if compter_flush(compte_couleurs):
        combinaisons['flush'] = 1

    if compter_full(compte_valeurs):
        combinaisons['full'] = 1

    if compter_quinte(compte_valeurs):
        combinaisons['quinte'] = 1

    if compter_quinte_flush(compte_valeurs, compte_couleurs):
        combinaisons['quinte_flush'] = 1

    if compter_quinte_flush_royale(compte_valeurs, compte_couleurs):
        combinaisons['quinte_flush_royale'] = 1

    for combi in combinaisons:
        if combinaisons[combi] == 1:
            combinaison_gagnante = combi

    return combinaison_gagnante

# Affiche et retourne les gains
def afficher_resultat_gains(mise, combinaison_gagnante=''):
    if combinaison_gagnante == "paire":
        print("Vous avez une Paire, vous récupérez votre mise!")
        return mise
    elif combinaison_gagnante == "double_paire":
        print("Vous avez une Double Paire, vous doublez votre mise!")
        return mise * 2
    elif combinaison_gagnante == "brelan":
        print("Vous avez un Brelan, vous triplez votre mise!")
        return mise * 3
    elif combinaison_gagnante == "carre":
        print("Vous avez un Carré, vous remportez 25 fois votre mise!")
        return mise * 25
    elif combinaison_gagnante == "flush":
        print("Vous avez un Flush, vous remportez 6 fois votre mise!")
        return mise * 6
    elif combinaison_gagnante == "full":
        print("Vous avez un Full, vous remportez 9 fois votre mise!")
        return mise * 9
    elif combinaison_gagnante == "quinte":
        print("Vous avez une Quinte, vous remportez 4 fois votre mise!")
        return mise * 4
    elif combinaison_gagnante == "quinte_flush":
        print("Vous avez une Quinte Flush, vous remportez 50 fois votre mise!")
        return mise * 50
    elif combinaison_gagnante == "quinte_flush_royale":
        print("Vous avez une Quinte Flush Royale, vous remportez 250 fois votre mise!")
        return mise * 250
    else:
        print("Aucune combinaison, vous perdez votre mise!")
        return 0


def partie(mise, bankroll):
    if mise > bankroll:
        print("Bankroll insuffisante pour votre mise")
        return

    print("Vous misez {}".format(mise))
    bankroll -= mise

    # Premier tirage, choix des cartes à garder, et tirage final
    main_finale = machine()

    # Comptage des cartes en main, tri par valeurs/couleurs
    compte_valeurs, compte_couleurs = comptage_main(main_finale)

    # Recherche des combinaisons gagnantes, calcul du gain
    gain = afficher_resultat_gains(mise, compte_combinaisons_gagnantes(compte_valeurs, compte_couleurs))

    if gain is not None:
        bankroll += gain

    print("Bankroll: {}".format(bankroll))

    return bankroll


def video_poker():
    bankroll = None
    mise = None

    # Insérer de l'argent
    while bankroll is None or bankroll <= 0:
        bankroll = int(input("Bankroll: Combien insérez-vous? "))

    # Choix de mise & jeu
    while bankroll > 0:
        mise = int(input("Combien miser? "))
        if mise is None or mise <= 0 or mise > bankroll:
            print("Mise invalide, veuillez réessayer")
        else:
            bankroll = partie(mise, bankroll)

    print("Partie terminée, vous avez perdu!")
    return


video_poker()
