from flask import Flask, render_template, request

def art8c3():
    importo = request.form.get('importo')
    compenso = request.form.get('compenso')
    importo = float(importo)
    compenso = float(compenso)
    risultato = 0
    listarisultati = [0, 0, 0, 0, 0, 0, 0, 0]
    primoscaglione = [0, 103291.38, 0.3284, 0.6569]
    secondoscaglione = [103291.39, 258228.45, 0.1405, 0.2811]
    terzoscaglione = [258228.46, 516456.90, 0.0474, 0.0947]
    quartoscaglione = [516456.91, 5164568.99, 0.0141, 0.0281]
    quintoscaglione = [5164569, 51645689.91, 0.00235, 0.0047]
    listascaglioni = [primoscaglione, secondoscaglione, terzoscaglione, quartoscaglione, quintoscaglione]

    for idx, i in enumerate(listascaglioni):
        if importo > i[0]:
            if importo <= i[1]:
                sommariferimento = importo - i[0]
            else:
                sommariferimento = i[1] - i[0]
            intervallopercentuale = (i[3] - i[2])
            percentualedaapplicare = ((compenso / 100) * intervallopercentuale) + (i[2])
            risultatoperscaglione = percentualedaapplicare / 100 * sommariferimento
            listarisultati[idx] = risultatoperscaglione
    risultato = sum(listarisultati)
    risultatoformattato = "{:.2f}".format(risultato)
    if risultato < 145.12:
        risultatoformattato = "145.12, in quanto ai sensi dell'art. 8, c. 5, il compenso non può essere inferiore a tale importo"
    if importo > quintoscaglione[1]:
        risultatoformattato = f"{risultatoformattato}, ovvero il compenso da corrispondere quando l'entità del bilancio preventivo o consuntivo esaminato è pari ad € 51.645.689,91. Si tenga presente che nel D.M. non è previsto uno scaglione finale con valore illimitato"
    listarisultati = ["{:.2f}".format(a) for a in listarisultati]

    dettaglio = f"""
Primo scaglione (fino a euro 103.291,38):  € {listarisultati[0]}
Secondo scaglione (da euro 103.291,39 e fino a euro 258.228,45): € {listarisultati[1]}
Terzo scaglione (da euro 258.228,46 fino a euro 516.456,90): € {listarisultati[2]} 
Quarto scaglione (da euro 516.456,91 e fino a euro 5.164.568,99): € {listarisultati[3]}
Quinto scaglione (da euro 5.164.569 e fino a euro 51.645.689,91): € {listarisultati[4]}      
"""

    ipotesiselezionata = "La fattispecie selezionata è la 'perizia o la consulenza tecnica in materia di analisi tecniche sui bilanci consuntivi o preventivi di enti previdenziali, assicurativi o finanziari', disciplinata dall'art. 8 cc. 3 e 4 D.M. 30 maggio 2002"
    if compenso == 0:
        tipologiacompenso = "Si è fatta  applicazione dei valori minimi di compenso"
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

    esito = f"""
{ipotesiselezionata}.<br>
L'entità del bilancio consuntivo o preventivo esaminato è pari ad € {importo}.<br>
{tipologiacompenso}.<br>
Il compenso complessivo è pari ad € {risultatoformattato}.<br>
Dettaglio delle parti di compenso riferite ai vari scaglioni {dettaglio}
"""

    return render_template('risultatocompensidm2002.html', esito=esito)
