from flask import Flask, render_template, request

def art8c1():
    importo = request.form.get('importo')
    compenso = request.form.get('compenso')
    importo = float(importo)
    compenso = float(compenso)
    risultato = 0
    listarisultati = [0, 0, 0, 0, 0, 0, 0, 0]
    primoscaglione = [0, 103291.38, 0.6632, 1.3106]
    secondoscaglione = [103291.39, 258228.45, 0.3790, 0.7579]
    terzoscaglione = [258228.46, 516456.90, 0.2842, 0.5684]
    quartoscaglione = [516456.91, 5164568.99, 0.0379, 0.0758]
    quintoscaglione = [5164569, 25822844.95, 0.0093, 0.0188]
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
        risultatoformattato = "145.12, in quanto ai sensi dell'art. 8, c. 2, il compenso non può essere inferiore a tale importo"
    if importo > quintoscaglione[1]:
        risultatoformattato = f"{risultatoformattato}, ovvero il compenso da corrispondere quando l'ammontare delle entrate effettive o presunte dell'anno cui si riferisce la valutazione è pari ad € 25.822.844,95. Si tenga presente che nel D.M. non è previsto uno scaglione finale con valore illimitato"
    listarisultati = ["{:.2f}".format(a) for a in listarisultati]

    dettaglio = f"""
Primo scaglione (fino a euro 103.291,38):  € {listarisultati[0]}
Secondo scaglione (da euro 103.291,39 e fino a euro 258.228,45): € {listarisultati[1]}
Terzo scaglione (da euro 258.228,46 fino a euro 516.456,90): € {listarisultati[2]} 
Quarto scaglione (da euro 516.456,91 e fino a euro 5.164.568,99): € {listarisultati[3]}
Quinto scaglione (da euro 5.164.569 e fino a euro 25.822.844,95): € {listarisultati[4]}      
"""

    ipotesiselezionata = "La fattispecie selezionata è la 'perizia o la consulenza tecnica in materia di accertamento di stato di equilibrio tecnico finanziario di gestioni previdenziali e assistenziali', disciplinata dall'art. 8 cc. 1 e 2 D.M. 30 maggio 2002"
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
L'ammontare delle entrate, effettive o presunte, dell'anno cui si riferisce la valutazione è pari ad € {importo}.<br>
{tipologiacompenso}.<br>
Il compenso complessivo è pari ad € {risultatoformattato}.<br>
Dettaglio delle parti di compenso riferite ai vari scaglioni {dettaglio}
"""

    return render_template('risultatocompensidm2002.html', esito=esito)
