from flask import Flask, render_template, url_for, request, escape, session
from helpers import DECK, premier_tirage, deuxieme_tirage, comptage_main, afficher_resultat_gains,\
    compte_combinaisons_gagnantes

app = Flask(__name__)

app.secret_key = b'mon_video_poker'


@app.route('/')
@app.route('/home')
def hello_world():
    return render_template('app_home.html', title="Home",
                           bankroll=session['bankroll'] if 'bankroll' in session else None)


@app.route('/premier-tirage', methods=['POST'])
def first_draw():
    if session.get('bankroll'):
        bankroll = session['bankroll']
    else:
        bankroll = int(escape(request.form['bankroll']))

    mise = int(escape(request.form['mise']))

    if bankroll is None or bankroll <= 0:
        return render_template('error.html',
                               error="Bankroll non valide, veuillez recommencer.",
                               title="Erreur")

    if mise is None or mise <= 0 or mise > bankroll:
        return render_template('error.html',
                               error="Mise non valide, veuillez recommencer.",
                               title="Erreur")

    session['bankroll'] = bankroll
    session['mise'] = mise

    tirage1, deck_restant = premier_tirage()

    session['deck'] = deck_restant
    return render_template('premier-tirage.html', main=tirage1, title="Premier tirage")


@app.route('/deuxieme-tirage', methods=['POST'])
def second_draw():
    # On récupère les cartes gardées.
    main_restante = []
    for card in request.form:
        if request.form[card] == "option1":
            main_restante.append(card)

    # Deuxième tirage.
    main_finale = deuxieme_tirage(main_restante, session['deck'])

    # Comptage des cartes en main, tri par valeurs/couleurs.
    compte_valeurs, compte_couleurs = comptage_main(main_finale)

    # Recherche des combinaisons gagnantes & calcul du gain.
    message, gain = afficher_resultat_gains(session['mise'], compte_combinaisons_gagnantes(compte_valeurs, compte_couleurs))

    # Déduction de la mise pour la partie.
    session['bankroll'] -= session['mise']

    # Calcul de la nouvelle bankroll
    if gain is not None:
        session['bankroll'] += gain

    # Page de résultat
    return render_template('result.html', main=main_finale,
                           message=message,
                           mise=session['mise'],
                           bankroll=session['bankroll'])


if __name__ == '__main__':
    app.run(debug=True)
