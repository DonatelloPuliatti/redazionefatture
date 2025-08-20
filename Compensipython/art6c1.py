from flask import Flask, render_template, request

def art6c1():
    importo = request.form.get('importo')
    compenso = request.form.get('compenso')
    altro = request.form.get('altro')
    importo = float(importo)
    risultato = 0
    listarisultati = [0, 0, 0, 0, 0, 0, 0, 0]
    primoscaglione = [0, 3098.74, 4.6896, 9.3951]
    secondoscaglione = [3098.75, 5164.57, 3.7580, 7.5160]
    terzoscaglione = [5164.58, 10329.14, 3.2843, 6.5686]
    quartoscaglione = [10329.15, 25822.84, 2.8106, 5.6370]
    quintoscaglione = [25822.85, 51645.69, 1.8790, 3.7580]
    sestoscaglione = [51645.70, 103291.38, 1.4053, 2.8106]
    settimoscaglione = [103291.39, 258228.45, 0.7042, 1.4085]
    ottavoscaglione = [258228.46, 516456.90, 0.2353, 0.4705]
    listascaglioni = [primoscaglione, secondoscaglione, terzoscaglione, quartoscaglione, quintoscaglione,
                      sestoscaglione, settimoscaglione, ottavoscaglione]

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
            risultatoperscaglione = percentualedaapplicare / 100 * sommariferimento
            listarisultati[idx] = risultatoperscaglione
    risultato = sum(listarisultati)
    risultatoformattato = "{:.2f}".format(risultato)
    if risultato < 145.12:
        risultatoformattato = "145.12, in quanto ai sensi dell'ultimo comma dell'art. 6, c. 2, il compenso non può essere inferiore a tale importo"
    if importo > ottavoscaglione[1]:
        risultatoformattato = f"{risultatoformattato}, ovvero il compenso da corrispondere quando l'ammontare complessivo della somma ammessa è pari ad € 516.456.90. Si tenga presente che nel D.M. non è previsto uno scaglione finale con valore illimitato"
    listarisultati = ["{:.2f}".format(a) for a in listarisultati]

    dettaglio = f"""
Primo scaglione (fino a euro 3.098,74):  € {listarisultati[0]}
Secondo scaglione (da euro 3.098,75 e fino a euro 5.164,57): € {listarisultati[1]}
Terzo scaglione (da euro 5.164,58 fino e non oltre euro 10.329,14): € {listarisultati[2]} 
Quarto scaglione (da euro 10.329,15 e fino a euro 25.822,84): € {listarisultati[3]}
Quinto scaglione (da euro 25.822,85 e fino a euro 51.645,69): € {listarisultati[4]}
Sesto scaglione (da euro 51.645,70 e fino a euro 103.291,38): € {listarisultati[5]}
Settimo scaglione (da euro 103.291,39 e fino a euro 258.228,45): € {listarisultati[6]}
Ottavo scaglione (da euro 258.228,46 fino e non oltre euro 516.456,90): € {listarisultati[7]}         
"""

    ipotesiselezionata = "La fattispecie selezionata è la 'perizia o la consulenza tecnica in materia di avarie comuni ', disciplinata dall'art. 6 cc. 1 e 2 D.M. 30 maggio 2002"
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
L'ammontare complessivo della somma ammessa è pari ad € {importo}.<br>
{tipologiacompenso}.<br>
Il compenso complessivo è pari ad € {risultatoformattato}.<br>
Dettaglio delle parti di compenso riferite ai vari scaglioni {dettaglio}
"""

    return render_template('risultatocompensidm2002.html', esito=esito)
