from flask import request, render_template
from docxtpl import DocxTemplate
import os

def redazionefatturesenzafile():
    risultato = None
    risultatobis = None
    compenso = None
    cpa = None
    imponibileiva = None
    iva = None
    totalefattura = None
    ritenuta = None
    importodapagare = None


    if request.method == "POST":
        try:
            tipologia = request.form["tipologia"]
            importo = float(request.form["importo"])
            ritenutairpef = request.form["ritenutairpef"]
            percentualeiva = request.form["percentualeiva"]
            spesegenerali = request.form["spesegenerali"]
            anticipazioni = float(request.form["anticipazioni"])
            bollo = request.form["bollo"]
            solodatoeconomico = request.form.get("solodatoeconomico")

            azione = request.form.get("azione")
            if tipologia == "compenso_coniva_conpa":
                compenso = (importo / (1.04) / (1 + float(percentualeiva))) * (1 - (float(spesegenerali)) )
                spesegenerali = (importo / (1.04) / (1 + float(percentualeiva))) *  (float( (request.form["spesegenerali"])))

            if tipologia == "compenso_senzaiva_senzacpa":
                compenso = importo
                spesegenerali = round(compenso * float(spesegenerali), 2)

            if tipologia == "compenso_coniva_senzacpa":
                compenso = (importo/(1 + float(percentualeiva))) * (1 - (float(spesegenerali)) )
                spesegenerali = (importo / (1.04) / (1 + float(percentualeiva))) * (float((request.form["spesegenerali"])))


            if tipologia == "compenso_concpa_senzaiva":
                compenso = importo/(1.04)
                spesegenerali = round(compenso * float(spesegenerali), 2)


            cpa = round((compenso + spesegenerali) * 0.04, 2)
            imponibileiva = round(compenso + spesegenerali + cpa, 2)
            iva = round(imponibileiva * float(percentualeiva), 2)
            totalefattura = round(imponibileiva + iva, 2)
            bollo = round(float(bollo), 2)
            ritenuta = round(float(ritenutairpef) * (compenso + spesegenerali), 2)
            importodapagare = round(totalefattura - ritenuta + anticipazioni + bollo, 2)

            if tipologia == "compenso_coniva_conpa" and totalefattura > importo: # Questo blocco di codice serve per scalare il compenso quando es. totalefattura = 1000.01 dopo i vari arrotondamenti
                compenso = compenso - 0.01
                spesegenerali = imponibileiva - cpa - compenso - 0.01
                cpa = round((compenso + spesegenerali) * 0.04, 2)
                imponibileiva = round(compenso + spesegenerali + cpa, 2)
                iva = round(imponibileiva * float(percentualeiva), 2)
                totalefattura = round(imponibileiva + iva, 2)
                bollo = round(float(bollo), 2)
                ritenuta = round(float(ritenutairpef) * (compenso + spesegenerali), 2)
                importodapagare = round(totalefattura - ritenuta + anticipazioni + bollo, 2)

            if azione == "Procedi":
                risultato = f"""
                <table class="fattura-table">
                    <tr><td>Compensi</td><td>{compenso:.2f}</td></tr>
                    <tr><td>Spese generali</td><td>{spesegenerali:.2f}</td></tr>
                    <tr><td>Cassa Previdenza Forense</td><td>{cpa:.2f}</td></tr>
                    <tr><td>Imponibile IVA</td><td>{imponibileiva:.2f}</td></tr>
                    <tr><td>IVA</td><td>{iva:.2f}</td></tr>
                    <tr><td><strong>TOTALE FATTURA</strong></td><td><strong>{totalefattura:.2f}</strong></td></tr>
                    <tr><td>Ritenuta IRPEF</td><td>{ritenuta:.2f}</td></tr>
                    <tr><td>Anticipazioni</td><td>{anticipazioni:.2f}</td></tr>
                    <tr><td>Bollo</td><td>{bollo:.2f}</td></tr>
                    <tr><td><strong>NETTO A PAGARE</strong></td><td><strong>{importodapagare:.2f}</strong></td></tr>
                </table>
                """


        except ValueError:
            risultato = "L'importo deve essere un numero valido (usa il punto per i decimali)"
    return render_template("redazionefatturesenzafile.html", risultato=risultato)

