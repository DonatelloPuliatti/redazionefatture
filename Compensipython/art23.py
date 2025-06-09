from flask import Flask, render_template, request

def art23():
    numerodicampioni = request.form.get('numerodicampioni')
    numerodicampioni = int(numerodicampioni)
    risultato = 28.92 * numerodicampioni
    risultatoformattato = "{:.2f}".format(risultato)
    ipotesiselezionata = f"""
La fattispecie selezionata è la 'perizia o la consulenza tecnica avente ad oggetto la ricerca del tasso percentuale carbossiemoglobinemico', disciplinata dall'art. 23 D.M. 30 maggio 2002.
"""

    esito = f"""
{ipotesiselezionata}<br>
Sono esaminati n. {numerodicampioni} campioni.<br>
Il compenso complessivo è pari ad € {risultatoformattato}, in quanto per ogni campione è previsto un compenso di € 28.92.<br>
"""

    return render_template('risultatocompensidm2002.html', esito=esito)
