from flask import Flask, render_template, request

def art25():
    compenso = request.form.get('compenso')
    compenso = float(compenso)
    reperti = request.form.get('reperti')
    reperti = int(reperti)
    risultato = 145.12 + ((970.42 - 145.12)/100*compenso)
    primoreperto = 28.92 + ((290.77 - 28.92)/100*compenso)
    primorepertoformattato = "{:.2f}".format(primoreperto)
    repertisuccessivi = (reperti - 1) * (28.92 + ((290.77 - 28.92)/100*compenso))*0.5
    repertisuccessiviformattato = "{:.2f}".format(repertisuccessivi)
    risultato = primoreperto + repertisuccessivi
    risultatoformattato = "{:.2f}".format(risultato)
    if compenso == 0:
        tipologiacompenso = "Si è fatta  applicazione dei valori minimi di compenso"
    elif compenso == 50:
        tipologiacompenso = "Si è fatta  applicazione dei valori medi di compenso"
    elif compenso == 100:
        tipologiacompenso = "Si è fatta  applicazione dei valori massimi di compenso"

    dettagliocompensi = ""
    if reperti > 1:
        dettagliocompensi = f"""
Il primo reperto dà luogo ad un compenso di € {primorepertoformattato}.
Gli altri reperti danno luogo ad un compenso complessivo di € {repertisuccessiviformattato}."""


    ipotesiselezionata = f"""
La fattispecie selezionata è quella della perizia o della consulenza tecnica avente ad oggetto diagnosi su materiale biologico o su tracce biologiche ovvero delle indagini biologiche o valutazioni sui risultati di indagini di laboratorio su tracce biologiche. Il dato normativo è costituito dall'art. 25 D.M. 30 maggio 2002.
"""

    esito = f"""
{ipotesiselezionata}<br>
Sono esaminati n. {reperti} reperti e/o marcatori.
{tipologiacompenso}.<br>
Il compenso complessivo è pari ad € {risultatoformattato}.<br>
{dettagliocompensi}
"""

    return render_template('risultatocompensidm2002.html', esito=esito)
