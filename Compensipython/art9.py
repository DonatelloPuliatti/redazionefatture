from flask import Flask, render_template, request

def art9():
    compenso = request.form.get('compenso')
    compenso = float(compenso)
    reperti = request.form.get('reperti')
    reperti = int(reperti)
    riduzione = request.form.get('riduzione')
    riduzione = float(riduzione)
    risultato = 145.12 + ((970.42 - 145.12)/100*compenso)
    primoreperto = 96.58 + ((484.05 - 96.58)/100*compenso)
    primorepertoformattato = "{:.2f}".format(primoreperto)
    repertisuccessivi = (reperti -1) * (96.58 + ((484.05 - 96.58)/100*compenso))*riduzione
    repertisuccessiviformattato = "{:.2f}".format(repertisuccessivi)
    risultato = primoreperto + repertisuccessivi
    risultatoformattato = "{:.2f}".format(risultato)
    if compenso == 0:
        tipologiacompenso = "Si è fatta  applicazione dei valori minimi di compenso"
    elif compenso == 50:
        tipologiacompenso = "Si è fatta  applicazione dei valori medi di compenso"
    elif compenso == 100:
        tipologiacompenso = "Si è fatta  applicazione dei valori massimi di compenso"
    tipologiariduzione = ""
    dettagliocompensi = ""
    if reperti > 1:
        dettagliocompensi = f"""
Il primo reperto dà luogo ad un compenso di € {primorepertoformattato}.
Gli altri reperti danno luogo ad un compenso complessivo di € {repertisuccessiviformattato}.
"""
        if riduzione == 0.667:
            tipologiariduzione = " ed è stata applicata la riduzione di un terzo per i reperti successivi al primo"
        elif riduzione == 0.5:
            tipologiariduzione = " ed è stata applicata la riduzione della metà per i reperti successivi al primo"
        elif riduzione == 0.333:
            tipologiariduzione = " ed è stata applicata la riduzione di due terzi per i reperti successivi al primo"


    ipotesiselezionata = f"""
La fattispecie selezionata è la 'perizia o la consulenza tecnica in materia di opere di pittura, scultura e simili ', disciplinata dall'art. 9 D.M. 30 maggio 2002.
"""

    esito = f"""
{ipotesiselezionata}<br>
Sono esaminati n. {reperti} reperti {tipologiariduzione}
{tipologiacompenso}.<br>
Il compenso complessivo è pari ad € {risultatoformattato}.<br>
{dettagliocompensi}
"""

    return render_template('risultatocompensidm2002.html', esito=esito)
