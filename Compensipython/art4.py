from flask import Flask, render_template, request

def art4():
    importo = request.form.get('importo')
    compenso = request.form.get('compenso')
    tabella = request.form.get('tabella')
    ipotesipeculiari = request.form.get('ipotesipeculiari')
    altro = request.form.get('altro')
    importo = float(importo)
    k = 1
    if ipotesipeculiari == "SI":
        k = 2
    risultato = 0
    if tabella == "attività":
        listarisultati = [0, 0, 0, 0, 0, 0, 0]
        primoscaglione = [0, 51645.69, 0.3790, 0.7579]
        secondoscaglione = [51645.70, 103291.38, 0.1405, 0.2811]
        terzoscaglione = [103291.39, 258228.45, 0.0932, 0.1879]
        quartoscaglione = [258228.46, 516456.90, 0.0474, 0.0947]
        quintoscaglione = [516456.91, 1032913.80, 0.0235, 0.0471]
        sestoscaglione = [1032913.81, 2582284.50, 0.0093, 0.0188]
        listascaglioni = [primoscaglione, secondoscaglione, terzoscaglione, quartoscaglione, quintoscaglione,
                      sestoscaglione]
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
                risultatoperscaglione = (percentualedaapplicare / 100 * sommariferimento)/k
                listarisultati[idx] = risultatoperscaglione
        risultato = sum(listarisultati)

        risultatoformattato = "{:.2f}".format(risultato)
        if risultato < 145.12:
            risultatoformattato = "145.12, in quanto ai sensi dell'ultimo comma dell'art. 2 il compenso non può essere inferiore a tale importo"
        if importo > sestoscaglione[1]:
            risultatoformattato = f"{risultatoformattato}, ovvero il compenso da corrispondere quando il valore del bene e/o dell'altra utilità oggetto dell'attività professionale è pari ad € 2.582.284,50. Si tenga presente che nel D.M. non è previsto uno scaglione finale con valore illimitato"
        listarisultati = ["{:.2f}".format(a) for a in listarisultati]

        dettaglio = f"""
Primo scaglione (fino a euro 51.645,69):  € {listarisultati[0]}
Secondo scaglione (da euro 51.645,70 e fino a euro 103.291,38): € {listarisultati[1]}
Terzo scaglione (da euro 103.291,39 e fino a euro 258.228,45): € {listarisultati[2]}
Quarto scaglione (da euro 258.228,46 e fino a euro 516.456,90): € {listarisultati[3]}
Quinto scaglione (da euro 516.456,91 e fino a euro 1.032.913,80): € {listarisultati[4]}
Sesto scaglione (da euro 1.032.913,81 fino e non oltre euro 2.582.284,50): € {listarisultati[5]}       
"""

    if tabella == "ricavilordi":
        listarisultati = [0, 0, 0, 0, 0, 0, 0]
        primoscaglione = [0, 258228.45, 0.0932, 0.1879]
        secondoscaglione = [258228.46, 516456.90, 0.0474, 0.0947]
        terzoscaglione = [516546.91, 1032913.80, 0.0188, 0.0376]
        quartoscaglione = [1032913.81, 5164568.99, 0.0093, 0.0188]
        listascaglioni = [primoscaglione, secondoscaglione, terzoscaglione, quartoscaglione]
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
                risultatoperscaglione = (percentualedaapplicare / 100 * sommariferimento) / k
                listarisultati[idx] = risultatoperscaglione
        risultato = sum(listarisultati)
        risultatoformattato = "{:.2f}".format(risultato)
        if risultato < 145.12:
            risultatoformattato = "145.12, in quanto ai sensi dell'ultimo comma dell'art. 4 il compenso non può essere inferiore a tale importo"
        if importo > quartoscaglione[1]:
            risultatoformattato = f"{risultatoformattato}, ovvero il compenso da corrispondere quando il totale delle attività / dei ricavi lordi è pari al limite massimo dell'ultimo scaglione. Si tenga presente che nel D.M. non è previsto uno scaglione finale con valore illimitato"
        listarisultati = ["{:.2f}".format(a) for a in listarisultati]

        dettaglio = f"""
Primo scaglione (fino a euro 258.228,45):  € {listarisultati[0]}
Secondo scaglione (da euro 258.228,46 e fino a euro 516.456,90): € {listarisultati[1]}
Terzo scaglione (da euro 516.546,91 e fino a euro 1.032.913,80): € {listarisultati[2]}
Quarto scaglione (da euro 1.032.913,81 fino e non oltre euro 5.164.568,99): € {listarisultati[3]}        
"""

    ipotesiselezionata = f"""
La fattispecie selezionata è la 'perizia o la consulenza tecnica in materia di bilancio e relativo conto dei profili e perdite', disciplinata dall'art. 4 D.M. 30 maggio 2002
"""
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
    if ipotesipeculiari == "SI":
        correttivo = "Poichè ricorre l'ipotesi di cui all'art. 4, penultimo comma, D.M. 30 maggio 2002, il compenso è stato dimezzato."
    esito = f"""
{ipotesiselezionata}<br>
Il valore del bene e/o dell'altra utilità oggetto dell'attività professionale è pari ad € {importo}.<br>
{tipologiacompenso}.<br>
Il compenso complessivo è pari ad € {risultatoformattato}. <br>
{correttivo}<br>
Dettaglio delle parti di compenso riferite ai vari scaglioni {dettaglio}
"""

    return render_template('risultatocompensidm2002.html', ipotesiselezionata=ipotesiselezionata, importo=importo,
                           tipologiacompenso=tipologiacompenso, dettaglio=dettaglio, risultato=risultatoformattato,
                           esito=esito)
