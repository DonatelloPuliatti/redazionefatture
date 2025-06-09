from flask import Flask, render_template, request

def art27():
    compenso = request.form.get('compenso')
    compenso = float(compenso)
    reperti = request.form.get('reperti')
    reperti = int(reperti)
    fattispecie = request.form.get('fattispecie')

    primoreperto = 48.03 + ((145.12 - 48.03)/100*compenso)
    primorepertoformattato = "{:.2f}".format(primoreperto)
    repertisuccessivi = (reperti - 1) * (48.03 + ((145.12 - 48.03)/100*compenso))*0.5
    repertisuccessiviformattato = "{:.2f}".format(repertisuccessivi)
    risultato = primoreperto + repertisuccessivi
    risultatoformattato = "{:.2f}".format(risultato)

    if fattispecie == "2":
        primoreperto = 67.66 + ((193.67 - 67.66) / 100 * compenso)
        primorepertoformattato = "{:.2f}".format(primoreperto)
        repertisuccessivi = (reperti - 1) * (67.66 + ((193.67 - 67.66) / 100 * compenso)) * 0.5
        repertisuccessiviformattato = "{:.2f}".format(repertisuccessivi)
        risultato = primoreperto + repertisuccessivi
        risultatoformattato = "{:.2f}".format(risultato)

    if fattispecie == "3":
        primoreperto = 67.66 + ((193.67 - 67.66) / 100 * compenso)
        primorepertoformattato = "{:.2f}".format(primoreperto)
        repertisuccessivi = (reperti - 1) * (67.66 + ((193.67 - 67.66) / 100 * compenso)) * 0.5
        repertisuccessiviformattato = "{:.2f}".format(repertisuccessivi)
        risultato = primoreperto + repertisuccessivi
        risultatoformattato = "{:.2f}".format(risultato)

    if fattispecie == "4":
        primoreperto = 48.03 + ((145.12 - 48.03) / 100 * compenso)
        primorepertoformattato = "{:.2f}".format(primoreperto)
        repertisuccessivi = (reperti - 1) * (48.03 + ((145.12 - 48.03) / 100 * compenso)) * 0.5
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
La fattispecie selezionata è la perizia o consulenza tecnica tossicologica su reperti non biologici a campione per la ricerca qualitativa di una sostanza. Il dato normativo è costituito dall'art. 27 c. 1 D.M. 30 maggio 2002.
"""

    if fattispecie == "2":
        ipotesiselezionata = f"""
La fattispecie selezionata è la perizia o consulenza tecnica tossicologica su reperti non biologici a campione per la ricerca quantitativa di una sostanza. Il dato normativo è costituito dall'art. 27 c. 1 D.M. 30 maggio 2002.
"""

    if fattispecie == "3":
        ipotesiselezionata = f"""
La fattispecie selezionata è la perizia o consulenza tecnica tossicologica su reperti biologici a campione per la ricerca quantitativa di ciascuna sostanza. Il dato normativo è costituito dall'art. 27 c. 2 D.M. 30 maggio 2002.
"""

    if fattispecie == "4":
        ipotesiselezionata = f"""
La fattispecie selezionata è la perizia o consulenza tecnica tossicologica su reperti biologici a campione per la ricerca quantitativa di ciascuna sostanza. Il dato normativo è costituito dall'art. 27 c. 2 D.M. 30 maggio 2002.
"""


    esito = f"""
{ipotesiselezionata}<br>
Sono esaminati n. {reperti} sostanze e/o campioni.
{tipologiacompenso}.<br>
Il compenso complessivo è pari ad € {risultatoformattato}.<br>
{dettagliocompensi}
"""

    return render_template('risultatocompensidm2002.html', esito=esito)
