from flask import Flask, render_template, request

def art10():
    compenso = request.form.get('compenso')
    compenso = float(compenso)
    risultato = 145.12 + ((582.05 - 145.12)/100*compenso)
    risultatoformattato = "{:.2f}".format(risultato)
    if compenso == 0:
        tipologiacompenso = "Si è fatta  applicazione dei valori minimi di compenso"
    elif compenso == 50:
        tipologiacompenso = "Si è fatta  applicazione dei valori medi di compenso"
    elif compenso == 100:
        tipologiacompenso = "Si è fatta  applicazione dei valori massimi di compenso"
    ipotesiselezionata = f"""
La fattispecie selezionata è la 'perizia o la consulenza tecnica in materia di accertamento di retribuzioni o di contributi previdenziali, assicurativi, assistenziali e fiscali e ogni altra questione in materia di rapporto di lavoro ', disciplinata dall'art. 10 D.M. 30 maggio 2002.
"""

    esito = f"""
{ipotesiselezionata}<br>
{tipologiacompenso}.<br>
Il compenso complessivo è pari ad € {risultatoformattato}.<br>
"""

    return render_template('risultatocompensidm2002.html', esito=esito)
