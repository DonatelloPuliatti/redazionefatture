from flask import Flask, render_template, request

def art28c3():
    compenso = request.form.get('compenso')
    compenso = float(compenso)
    risultato = 48.03 + ((484.95 - 48.03)/100*compenso)
    risultatoformattato = "{:.2f}".format(risultato)
    if compenso == 0:
        tipologiacompenso = "Si è fatta  applicazione dei valori minimi di compenso"
    elif compenso == 50:
        tipologiacompenso = "Si è fatta  applicazione dei valori medi di compenso"
    elif compenso == 100:
        tipologiacompenso = "Si è fatta  applicazione dei valori massimi di compenso"
    ipotesiselezionata = f"""
La fattispecie selezionata è la 'la perizia o la consulenza tecnica in materia di inquinamento acustico ', disciplinata dall'art. 28, c. 3, D.M. 30 maggio 2002.
"""

    esito = f"""
{ipotesiselezionata}<br>
{tipologiacompenso}.<br>
Il compenso complessivo è pari ad € {risultatoformattato}.<br>
"""

    return render_template('risultatocompensidm2002.html', esito=esito)
