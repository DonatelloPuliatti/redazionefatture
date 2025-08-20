from flask import Flask, render_template, request

def art17():
    importo = request.form.get('importo')
    compenso = request.form.get('compenso')
    altro = request.form.get('altro')
    importo = float(importo)
    tipologiaprestazione = request.form.get('tipologiaprestazione')
    risultato = 0
    listarisultati = [0, 0, 0, 0, 0, 0, 0]
    primoscaglione = [0, 258.23, 7.5160, 15.0321]
    secondoscaglione = [258.24, 516.46, 5.6370, 11.2741]
    terzoscaglione = [516.47, 2582.28, 3.7580, 7.5160]
    quartoscaglione = [2582.29, 25822.84, 1.4053, 2.8106]
    quintoscaglione = [25822.85, 51645.69, 0.9316, 1.8790]
    listascaglioni = [primoscaglione, secondoscaglione, terzoscaglione, quartoscaglione, quintoscaglione]
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
    if risultato < 38.73:
        risultatoformattato = "38.73, in quanto ai sensi dell'art. 17, c. 2, il compenso non può essere inferiore a tale importo"
    if importo > quintoscaglione[1]:
        risultatoformattato = f"{risultatoformattato}, ovvero il compenso da corrispondere quando il valore del bene e/o dell'altra utilità oggetto dell'attività professionale è pari ad € 51.645,69. Si tenga presente che nel D.M. non è previsto uno scaglione finale con valore illimitato"
    listarisultati = ["{:.2f}".format(a) for a in listarisultati]

    dettaglio = f"""
Primo scaglione (fino a euro 258,23):  € {listarisultati[0]}
Secondo scaglione (da euro 258,23 e fino a euro 516,46): € {listarisultati[1]}
Terzo scaglione (da euro 516,47 e fino a euro 2.582,28): € {listarisultati[2]}
Quarto scaglione (da euro 2.582,29 e fino a euro 25.822,84): € {listarisultati[3]}
Quinto scaglione (da euro 25.822,85 e fino e non oltre 51.645,69): € {listarisultati[4]}        
"""

    ipotesiselezionata = "La fattispecie selezionata è la 'consulenza tecnica in materia di infortunistica del traffico e della circolazione ', disciplinata dall'art. 17, cc. 1 e 2, D.M. 30 maggio 2002"
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
Il valore del bene e/o dell'altra utilità oggetto dell'attività professionale è pari ad € {importo}.<br>
{tipologiacompenso}.<br>
Il compenso complessivo è pari ad € {risultatoformattato}.<br>
Dettaglio delle parti di compenso riferite ai vari scaglioni {dettaglio}
"""
    if tipologiaprestazione == "perizia":
        esito = """
Ai sensi dell'art. 17, c. 3, D.M. 30 maggio 2002, in caso di perizia l'onorario è commisurato al tempo ritenuto necessario allo svolgimento dell'incarico ed è determinato in base alle vacazioni."
Cliccando su 'Torna indietro' e selezionando 'art. 1', è disponibile il form per il calcolo degli onorari a vacazione.
"""


    return render_template('risultatocompensidm2002.html', esito=esito)
