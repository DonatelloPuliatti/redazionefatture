from flask import request, render_template

def moltiplicazione():
    risultato_moltiplicazione = None
    if request.method == "POST":
        try:
            numero1 = float(request.form["numero1"])
            numero2 = float(request.form["numero2"])
            risultato_moltiplicazione = numero1 * numero2
            if risultato_moltiplicazione == int(risultato_moltiplicazione):
                risultato_moltiplicazione = int(risultato_moltiplicazione)
        except ValueError:
            risultato_moltiplicazione = "Errore: inserisci solo numeri!"
    return render_template("moltiplicazione.html", risultato=risultato_moltiplicazione)
