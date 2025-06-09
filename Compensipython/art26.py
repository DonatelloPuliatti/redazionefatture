from flask import Flask, render_template, request

def art26():
    fattispecie = request.form.get('fattispecie')
    fattispeciepeculiare = request.form.get('fattispeciepeculiare')
    ipotesiselezionata = ""
    risultatoformattato = ""

    if fattispecie == "1":
        ipotesiselezionata = f"""
La fattispecie selezionata è la visita clinica relativa a perizia o  consulenza tecnica avente ad oggetto accertamenti diagnostici su animali, nel caso di immediata espressione del giudizio raccolta a verbale: l'ipotesi è disciplinata dall'art. 26, c. 1, D.M. 30 maggio 2002.
"""
        risultatoformattato = "Il compenso è pari ad € 19,11."

    if fattispecie == "2":
        ipotesiselezionata = f"""
La fattispecie selezionata è l'esame necroscopioco relativo a perizia o  consulenza tecnica avente ad oggetto accertamenti diagnostici su animali, nel caso di immediata espressione del giudizio raccolta a verbale: l'ipotesi è disciplinata dall'art. 26, c. 1, D.M. 30 maggio 2002.
"""
        risultatoformattato = "Il compenso è pari ad € 67,66."

    if fattispecie == "3":
        ipotesiselezionata = f"""
La fattispecie selezionata è la visita clinica relativa a perizia o  consulenza tecnica avente ad oggetto accertamenti diagnostici su animali, quando il parere non può essere dato immediatamente e viene presentata una relazione scritta: l'ipotesi è disciplinata dall'art. 20, c. 2, D.M. 30 maggio 2002.
"""
        risultatoformattato = "Va riconosciuto un compenso da € 48,03 ad € 145,12."

    if fattispecie == "4":
        ipotesiselezionata = f"""
La fattispecie selezionata è l'esame necroscopico relativo a perizia o consulenza tecnica avente ad oggetto accertamenti diagnostici su animali,  quando il parere non può essere dato immediatamente e viene presentata una relazione scritta: l'ipotesi è disciplinata dall'art. 20, c. 2, D.M. 30 maggio 2002.
"""
        risultatoformattato = "Va riconosciuto un compenso da € 96,58 ad € 290,77"

    if fattispeciepeculiare == "SI" and fattispecie == "1":
        risultatoformattato = "Il compenso è pari ad € 38,22"

    if fattispeciepeculiare == "SI" and fattispecie == "2":
        risultatoformattato = "Il compenso è pari ad € 135,22"

    if fattispeciepeculiare == "SI" and fattispecie == "3":
        risultatoformattato = "Va riconosciuto un compenso da € 96,06 ad € 290,24."

    if fattispeciepeculiare == "SI" and fattispecie == "4":
        risultatoformattato = "Va riconosciuto un compenso da € 193,16 ad € 581,54."

    esito = f"""
{ipotesiselezionata}<br>
{risultatoformattato}<br>
"""

    return render_template('risultatocompensidm2002.html', esito=esito)
