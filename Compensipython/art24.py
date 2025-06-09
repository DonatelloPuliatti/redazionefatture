from flask import Flask, render_template, request

def art24():
    compenso = request.form.get('compenso')
    compenso = float(compenso)
    risultato = 96.58 + ((387.86 - 96.58)/100*compenso)
    risultatoformattato = "{:.2f}".format(risultato)
    if compenso == 0:
        tipologiacompenso = "Si è fatta  applicazione dei valori minimi di compenso"
    elif compenso == 50:
        tipologiacompenso = "Si è fatta  applicazione dei valori medi di compenso"
    elif compenso == 100:
        tipologiacompenso = "Si è fatta  applicazione dei valori massimi di compenso"
    ipotesiselezionata = f"""
La fattispecie selezionata è la 'perizia o la consulenza tecnica in materia psichiatrica o criminologica', disciplinata dall'art. 24 D.M. 30 maggio 2002.
"""

    esito = f"""
{ipotesiselezionata}<br>
{tipologiacompenso}.<br>
Il compenso complessivo è pari ad € {risultatoformattato}.<br>
"""

    return render_template('risultatocompensidm2002.html', esito=esito)
