from flask import Flask, render_template, request

def art16():
    compenso = request.form.get('compenso')
    compenso = float(compenso)
    risultato = 145.12 + ((970.42 - 145.12)/100*compenso)
    risultatoformattato = "{:.2f}".format(risultato)
    if compenso == 0:
        tipologiacompenso = "Si è fatta  applicazione dei valori minimi di compenso"
    elif compenso == 50:
        tipologiacompenso = "Si è fatta  applicazione dei valori medi di compenso"
    elif compenso == 100:
        tipologiacompenso = "Si è fatta  applicazione dei valori massimi di compenso"
    ipotesiselezionata = f"""
La fattispecie selezionata è la 'perizia o la consulenza tecnica in materia di funzioni contabili amministrative di case e beni rustici, di curatele di aziende agrarie, di equo canone, di fitto di fondi urbani e rustici, di redazione di stima dei danni da incendio e grandine, di tabelle millesimali e riparto di spese condominiali', disciplinata dall'art. 5 D.M. 30 maggio 2002.
"""

    esito = f"""
{ipotesiselezionata}<br>
{tipologiacompenso}.<br>
Il compenso complessivo è pari ad € {risultatoformattato}.<br>
"""

    return render_template('risultatocompensidm2002.html', esito=esito)
