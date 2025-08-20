from flask import Flask, render_template, request

def art7():
    fattispecie = request.form.get('fattispecie')
    compenso = request.form.get('compenso')
    compenso = float(compenso)
    if fattispecie == "1":
        risultato = 145.12 + ((484.95 - 145.12)/100*compenso)
        risultatoformattato = "{:.2f}".format(risultato)
    if fattispecie == "2":
        risultato = 193.67 + ((582.05 - 193.67)/100*compenso)
        risultatoformattato = "{:.2f}".format(risultato)
    if compenso == 0:
        tipologiacompenso = "Si è fatta  applicazione dei valori minimi di compenso"
    elif compenso == 50:
        tipologiacompenso = "Si è fatta  applicazione dei valori medi di compenso"
    elif compenso == 100:
        tipologiacompenso = "Si è fatta  applicazione dei valori massimi di compenso"
    if fattispecie == "1":
        ipotesiselezionata = f"""
La fattispecie selezionata è la 'perizia o la consulenza tecnica espletata con metodo attuariale in materia di ricostruzione di posizioni retributive o previdenziali, di prestiti, di nude proprietà e usufrutti, di ammortamenti finanziari, di adeguamento al costo della vita e rivalutazione monetaria', disciplinata dall'art. 7, c. 1, D.M. 30 maggio 2002
"""

    if fattispecie == "2":
        ipotesiselezionata = f"""
La fattispecie selezionata è la 'perizia o la consulenza tecnica in materia di verifica di basi tecniche di gestioni previdenziali e assistenziali, di riserve matematiche individuali e valori di riscatto di anzianità pregressa ai fini del trattamento di previdenza e quiescenza', disciplinata dall'art. 7, c. 1, D.M. 30 maggio 2002
"""

    esito = f"""
{ipotesiselezionata}<br>
{tipologiacompenso}.<br>
Il compenso complessivo è pari ad € {risultatoformattato}.<br>
"""

    return render_template('risultatocompensidm2002.html', esito=esito)
