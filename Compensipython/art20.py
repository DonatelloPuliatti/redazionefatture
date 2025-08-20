from flask import Flask, render_template, request

def art20():
    fattispecie = request.form.get('fattispecie')
    ipotesiselezionata = ""
    risultatoformattato = ""

    if fattispecie == "1":
        ipotesiselezionata = f"""
La fattispecie selezionata è la 'visita medico-legale nel caso di immediata espressione del giudizio raccolta a verbale', disciplinata dall'art. 20, c. 1, D.M. 30 maggio 2002.
"""
        risultatoformattato = "Il compenso è pari ad € 19,11."

    if fattispecie == "2":
        ipotesiselezionata = f"""
La fattispecie selezionata è l'ispezione esterna di cadavere nel caso di immediata espressione del giudizio raccolta a verbale, disciplinata dall'art. 20, c. 1, D.M. 30 maggio 2002.
"""
        risultatoformattato = "Il compenso è pari ad € 19,11."

    if fattispecie == "3":
        ipotesiselezionata = f"""
La fattispecie selezionata è l'autopsia nel caso di immediata espressione del giudizio raccolta a verbale, disciplinata dall'art. 20, c. 1, D.M. 30 maggio 2002.
"""
        risultatoformattato = "Il compenso è pari ad € 67,66."

    if fattispecie == "4":
        ipotesiselezionata = f"""
La fattispecie selezionata è l'autopsia su cadavere esumato nel caso di immediata espressione del giudizio raccolta a verbale, disciplinata dall'art. 20, c. 1, D.M. 30 maggio 2002.
"""
        risultatoformattato = "Il compenso è pari ad € 96,58"

    if fattispecie == "5":
        ipotesiselezionata = f"""
La fattispecie selezionata è la visita medico-legale quando il parere non può essere dato immediatamente e viene presentata una relazione scritta, disciplinata dall'art. 20, c. 2, D.M. 30 maggio 2002.
"""
        risultatoformattato = "Va riconosciuto un compenso da € 48,03 ad € 145,12."

    if fattispecie == "6":
        ipotesiselezionata = f"""
La fattispecie selezionata è l'accertamento su cadavere quando il parere non può essere dato immediatamente e viene presentata una relazione scritta, disciplinata dall'art. 20, c. 2, D.M. 30 maggio 2002.
"""
        risultatoformattato = "Va riconosciuto un compenso da €116,20 ad € 387,86."


    esito = f"""
{ipotesiselezionata}<br>
{risultatoformattato}<br>
"""

    return render_template('risultatocompensidm2002.html', esito=esito)
