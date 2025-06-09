from flask import Flask, render_template, request

def vacazione():
    vacazionicompleteentro4 = int(request.form.get('vacazionicompleteentro4'))
    vacazionicompleteoltre4 = int(request.form.get('vacazionicompleteoltre4'))
    vacazionientro1h15mentro4 = int(request.form.get('vacazionientro1h15mentro4'))
    vacazionientro1h15moltre4 = int(request.form.get('vacazionientro1h15moltre4'))
    vacazionioltre1h15mentro4 = int(request.form.get('vacazionioltre1h15mentro4'))
    vacazionioltre1h15moltre4 = int(request.form.get('vacazionioltre1h15moltre4'))
    termine = request.form.get('termine')
    ag = request.form.get('ag')

    vacazionicompletedacomputare = vacazionicompleteentro4 + vacazionicompleteoltre4
    if ag == "no":
        vacazionicompletedacomputare = vacazionicompleteentro4

    vacazionientro1h15mdacomputare = vacazionientro1h15mentro4 + vacazionientro1h15moltre4
    if ag == "no":
        vacazionientro1h15mdacomputare = vacazionientro1h15mentro4

    vacazionioltre1h15mdacomputare = vacazionioltre1h15mentro4 + vacazionioltre1h15moltre4
    if ag == "no":
        vacazionioltre1h15mdacomputare = vacazionioltre1h15mentro4

    compenso = round((vacazionicompletedacomputare + vacazionioltre1h15mdacomputare) * 14.68 + (vacazionientro1h15mdacomputare * 7.34), 2)

    correttivo1 = ""
    if ag == "no" and (vacazionicompleteoltre4 > 0 or vacazionientro1h15moltre4 > 0 or vacazionioltre1h15moltre4 > 0):
        correttivo1 = "Non sono state computate le vacazioni oltre la quarta giornaliera in virtù dell'art. 4, c. 5, L. 319/1980, in quanto l'incarico è espletato alla presenza dell'autorità giudiziaria"
    if ag == "si" and (vacazionicompleteoltre4 > 0 or vacazionientro1h15moltre4 > 0 or vacazionioltre1h15moltre4 > 0):
        correttivo1 = "Sono state computate le vacazioni oltre la quarta giornaliera in virtù dell'art. 4, c. 6, L. 319/1980, in quanto l'incarico è espletato alla presenza dell'autorità giudiziaria"

    correttivo2 = ""
    if termine == "entro5":
        correttivo2 = f"In applicazione dell'art. 4, c. 3, L. 319/1980, poichè il termine fissato non è superiore a 5 gg., il compenso può essere raddoppiato e quindi essere pari ad € {compenso*2}."
    if termine == "da6a15":
        correttivo2 = f"In applicazione dell'art. 4, c. 3, L. 319/1980, poichè il termine fissato è compreso tra 6 e 15 gg., il compenso può essere aumentato fino alla metà e quindi essere pari ad € {compenso*1.5}."



    dettagliocompenso = f"""
Il compenso è pari ad € {compenso} e discende dal seguente calcolo.<br>
Compenso per n. {vacazionicompletedacomputare} vacazioni complete = € {vacazionicompletedacomputare*14.68}<br>
Compenso per n. {vacazionioltre1h15mdacomputare} vacazioni incomplete oltre 1h 15m ed inferiori a 2h = € {vacazionioltre1h15mdacomputare*14.68}<br>
Compenso per n. {vacazionientro1h15mdacomputare} vacazioni incomplete entro 1h 15m = € {vacazionientro1h15mdacomputare*7.34}<br>
Si precisa che per le vacazioni incomplete entro 1h 15m il compenso è dimezzato, mentre per quelle incomplete oltre 1h 15m il compenso è corrisposto per intero, ai sensi dell'art. 4, c. 4, L. 319/1980.
Si precisa inoltre che le vacazioni successive alla prima sono corrisposte per intero secondo quanto derivante da C.Cost. 16/2025.
"""

    ipotesiselezionata = "La fattispecie selezionata è quella del compenso a vacazione, ai sensi del combinato disposto dell'art. 1, seconda proposizione, D.M. 30/5/2002 e dell'art. 4, L. 319/1980"
    esito = f"""
{ipotesiselezionata}<br>
{dettagliocompenso}
{correttivo1}
{correttivo2}
"""
    return render_template('risultatocompensidm2002.html', esito=esito)