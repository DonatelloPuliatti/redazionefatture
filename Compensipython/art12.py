from flask import Flask, render_template, request

def art12():
    fattispecie = request.form.get('fattispecie')
    compenso = request.form.get('compenso')
    compenso = float(compenso)
    if fattispecie == "1":
        risultato = 145.12 + ((970.42 - 145.12)/100*compenso)
        risultatoformattato = "{:.2f}".format(risultato)
    if fattispecie == "2":
        risultato = 145.12 + ((970.42 - 145.12)/100*compenso)
        risultatoformattato = "{:.2f}".format(risultato)
    if compenso == 0:
        tipologiacompenso = "Si è fatta  applicazione dei valori minimi di compenso"
    elif compenso == 50:
        tipologiacompenso = "Si è fatta  applicazione dei valori medi di compenso"
    elif compenso == 100:
        tipologiacompenso = "Si è fatta  applicazione dei valori massimi di compenso"
    if fattispecie == "1":
        ipotesiselezionata = f"""
La fattispecie selezionata è la 'perizia o la consulenza tecnica in materia di verifica di rispondenza tecnica alle prescrizioni di progetto e/o di contratto, capitolati e norme, di collaudo di lavori e forniture, di misura e contabilità di lavori, di aggiornamento e revisione dei prezzi', disciplinata dall'art. 12, c. 1, D.M. 30 maggio 2002
"""

    if fattispecie == "2":
        ipotesiselezionata = f"""
La fattispecie selezionata è la 'perizia o consulenza tecnica in materia di rilievi topografici, planimetrici e altimetrici, compresi le triangolazioni e poligonazione, la misura dei fondi rustici, i rilievi di strade, canali, fabbricati, centri abitati e aree fabbricabili', disciplinata dall'art. 12, c. 2, D.M. 30 maggio 2002
"""

    esito = f"""
{ipotesiselezionata}<br>
{tipologiacompenso}.<br>
Il compenso complessivo è pari ad € {risultatoformattato}.<br>
"""

    return render_template('risultatocompensidm2002.html', esito=esito)
