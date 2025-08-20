from flask import Flask, render_template, request

def art13():
    importo = request.form.get('importo')
    compenso = request.form.get('compenso')
    altro = request.form.get('altro')
    importo = float(importo)
    ipotesipeculiari = float(request.form.get('ipotesipeculiari'))
    risultato = 0
    listarisultati = [0, 0, 0, 0, 0, 0, 0]
    primoscaglione = [0, 5164.57, 1.0264, 2.0685]
    secondoscaglione = [5164.58, 10329.14, 0.9316, 1.8790]
    terzoscaglione = [10329.15, 25822.84, 0.8369, 1.6895]
    quartoscaglione = [25822.85, 51645.69, 0.5684, 1.1211]
    quintoscaglione = [51645.70, 103291.38, 0.3790, 0.7579]
    sestoscaglione = [103291.39, 258228.45, 0.2842, 0.5684]
    settimoscaglione = [258228.46, 516456.90, 0.0474, 0.0947]
    listascaglioni = [primoscaglione, secondoscaglione, terzoscaglione, quartoscaglione, quintoscaglione,
                      sestoscaglione, settimoscaglione]
    if compenso == 'altro' and altro:
        compenso = float(altro)  # Usa il valore inserito in "altro" se "altro" è selezionato
    else:
        compenso = float(compenso)  # Altrimenti usa il compenso selezionato
    for idx, i in enumerate(listascaglioni):
        if importo > i[0]:
            if importo <= i[1]:
                sommariferimento = importo - i[0]
            else:
                sommariferimento = i[1] - i[0]
            intervallopercentuale = (i[3] - i[2])
            percentualedaapplicare = ((compenso / 100) * intervallopercentuale) + (i[2])
            risultatoperscaglione = (percentualedaapplicare / 100 * sommariferimento)/ipotesipeculiari
            listarisultati[idx] = risultatoperscaglione
    risultato = sum(listarisultati)
    risultatoformattato = "{:.2f}".format(risultato)
    if risultato < 145.12:
        risultatoformattato = "145.12, in quanto ai sensi dell'ultimo comma dell'art. 13, il compenso non può essere inferiore a tale importo"
    if importo > settimoscaglione[1]:
        risultatoformattato = f"{risultatoformattato}, ovvero il compenso da corrispondere quando il valore della perizia/consulenza è pari ad € 516.456.90. Si tenga presente che nel D.M. non è previsto uno scaglione finale con valore illimitato"
    listarisultati = ["{:.2f}".format(a) for a in listarisultati]

    dettaglio = f"""
Primo scaglione (fino a euro 5.164,57):  € {listarisultati[0]}
Secondo scaglione (da euro 5.164,58 e fino a euro 10.329,14): € {listarisultati[1]}
Terzo scaglione (da euro 10.329,15 e fino a euro 25.822,84): € {listarisultati[2]}
Quarto scaglione (da euro 25.822,85 e fino a euro 51.645,69): € {listarisultati[3]}
Quinto scaglione (da euro 51.645,70 e fino a euro 103.291,38): € {listarisultati[4]}
Sesto scaglione (da euro 103.291,39 e fino a euro 258.228,45): € {listarisultati[5]}
Settimo scaglione (da euro 258.228,46 fino e non oltre euro 516.456,90): € {listarisultati[6]}         
"""

    ipotesiselezionata = f"""La fattispecie selezionata è la 'perizia o la consulenza tecnica in materia di estimo'"""
    if compenso == 0:
        tipologiacompenso = """
Si è fatta  applicazione dei valori minimi di compenso
"""
    elif compenso == 50:
        tipologiacompenso = "Si è fatta  applicazione dei valori medi di compenso"
    elif compenso == 100:
        tipologiacompenso = "Si è fatta  applicazione dei valori massimi di compenso"
    else:
        if compenso == int(compenso):
            compenso = int(compenso)
            tipologiacompenso = f"Si è ritenuto di collocarsi nel range normativo applicando la seguente percentuale: {compenso}%"
        if compenso != int(compenso):
            tipologiacompenso = f"Si è ritenuto di collocarsi nel range normativo applicando la seguente percentuale: {compenso}%"

    importo = "{:.2f}".format(importo)

    correttivo = ""
    if ipotesipeculiari == 3:
        correttivo = "Poichè si tratta di un semplice giudizio di stima, ai sensi dell'art. 13, c. 2, seconda proposizione, D.M. 30 maggio 2002, si è fatta applicazione della riduzione dei due terzi."
    if ipotesipeculiari == 2:
        correttivo = "Poichè si tratta di una stima sommaria, ai sensi dell'art. 13, c. 2, prima proposizione, D.M. 30 maggio 2002, si è fatta applicazione della riduzione della metà."

    esito = f"""
{ipotesiselezionata}<br>
Il valore del bene e/o dell'altra utilità oggetto dell'attività professionale è pari ad € {importo}.<br>
{tipologiacompenso}.<br>
{correttivo}<br>
Il compenso complessivo è pari ad € {risultatoformattato}.<br>
Dettaglio delle parti di compenso riferite ai vari scaglioni {dettaglio}
"""

    return render_template('risultatocompensidm2002.html', esito=esito)
