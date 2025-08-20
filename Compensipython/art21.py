from flask import Flask, render_template, request

def art21():
    compenso = request.form.get('compenso')
    compenso = float(compenso)
    risultato = 48.03 + ((290.77 - 48.03)/100*compenso)
    risultatoformattato = "{:.2f}".format(risultato)
    if compenso == 0:
        tipologiacompenso = "Si è fatta  applicazione dei valori minimi di compenso"
    elif compenso == 50:
        tipologiacompenso = "Si è fatta  applicazione dei valori medi di compenso"
    elif compenso == 100:
        tipologiacompenso = "Si è fatta  applicazione dei valori massimi di compenso"
    ipotesiselezionata = f"""
La fattispecie selezionata è la 'consulenza tecnica avente ad oggetto accertamenti medici, diagnostici, identificazione di agenti patogeni, riguardanti la persona', disciplinata dall'art. 21 D.M. 30 maggio 2002.
"""

    esito = f"""
{ipotesiselezionata}<br>
{tipologiacompenso}.<br>
Il compenso complessivo è pari ad € {risultatoformattato}.<br>
"""

    return render_template('risultatocompensidm2002.html', esito=esito)
