from flask import request, render_template
def somma():
    risultato_somma = None
    if request.method == "POST":
        try:
            numero1 = float(request.form["numero1"])
            numero2 = float(request.form["numero2"])
            risultato_somma = numero1 + numero2
            if risultato_somma == int(risultato_somma):
                risultato_somma = int(risultato_somma)
        except ValueError:
            risultato_somma = "Errore: inserisci solo numeri!"
    return render_template("somma.html", risultato=risultato_somma)
