from flask import Flask, render_template, request

def art28c2():
    compenso = request.form.get('compenso')
    compenso = float(compenso)
    risultato = 48.03 + ((407.48 - 48.03)/100*compenso)
    risultatoformattato = "{:.2f}".format(risultato)
    if compenso == 0:
        tipologiacompenso = "Si è fatta  applicazione dei valori minimi di compenso"
    elif compenso == 50:
        tipologiacompenso = "Si è fatta  applicazione dei valori medi di compenso"
    elif compenso == 100:
        tipologiacompenso = "Si è fatta  applicazione dei valori massimi di compenso"
    ipotesiselezionata = f"""
La fattispecie selezionata è 'la perizia o la consulenza ecotossicologica volta ad accertare le alterazioni e le impurità di qualsiasi sostanza o ad identificare gli agenti patogeni infettanti, infestanti e inquinanti', disciplinata dall'art. 28, c. 2, D.M. 30 maggio 2002.
"""

    esito = f"""
{ipotesiselezionata}<br>
{tipologiacompenso}.<br>
Il compenso complessivo è pari ad € {risultatoformattato}.<br>
"""

    return render_template('risultatocompensidm2002.html', esito=esito)
