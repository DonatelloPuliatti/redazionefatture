from flask import Flask, render_template, request

def art22():
    numerodicampioni = request.form.get('numerodicampioni')
    numerodicampioni = int(numerodicampioni)
    risultato = 14.46 * numerodicampioni
    risultatoformattato = "{:.2f}".format(risultato)
    ipotesiselezionata = f"""
La fattispecie selezionata è la 'perizia o la consulenza tecnica avente ad oggetto l'esame alcoolimetrico', disciplinata dall'art. 22 D.M. 30 maggio 2002.
"""

    esito = f"""
{ipotesiselezionata}<br>
Sono esaminati n. {numerodicampioni} campioni.<br>
Il compenso complessivo è pari ad € {risultatoformattato}, in quanto per ogni campione è previsto un compenso di € 14,46.<br>
"""

    return render_template('risultatocompensidm2002.html', esito=esito)
