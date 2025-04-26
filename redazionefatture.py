from flask import request, render_template
from docxtpl import DocxTemplate
import os

def redazionefatture():
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
            nomedebitore = str(request.form["nomedebitore"])
            indirizzodebitore = str(request.form["indirizzodebitore"])
            partitaivacodicefiscaledebitore = str(request.form["partitaivacodicefiscaledebitore"])
            nomecreditore = str(request.form["nomecreditore"])
            indirizzocreditore = str(request.form["indirizzocreditore"])
            partitaivacodicefiscalecreditore = str(request.form["partitaivacodicefiscalecreditore"])
            descrizioneattivita = str(request.form["descrizioneattivita"])
            numeronotula = str(request.form["numeronotula"])
            datanotula = str(request.form["datanotula"])
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
                if solodatoeconomico == None:
                    doc = DocxTemplate("modellonotula.docx")

                    context = {
                        'nomecreditore': nomecreditore,
                        'indirizzocreditore': indirizzocreditore,
                        'partitaivacodicefiscalecreditore': partitaivacodicefiscalecreditore,
                        'nomedebitore': nomedebitore,
                        'indirizzodebitore': indirizzodebitore,
                        'partitaivacodicefiscaledebitore': partitaivacodicefiscaledebitore,
                        'numeronotula': numeronotula,
                        'datanotula': datanotula,
                        'descrizioneattivita': descrizioneattivita,
                        'compenso': f"{compenso:.2f}",
                        'spesegenerali': f"{spesegenerali:.2f}",
                        'cpa': f"{cpa:.2f}",
                        'imponibileiva': f"{imponibileiva:.2f}",
                        'iva': f"{iva:.2f}",
                        'totalefattura': f"{totalefattura:.2f}",
                        'ritenuta': f"{ritenuta:.2f}",
                        'anticipazioni': f"{anticipazioni:.2f}",
                        'bollo': f"{bollo:.2f}",
                        'importodapagare': f"{importodapagare:.2f}"
                    }


                    doc.render(context)

                    # 4. Salva il nuovo documento

                    os.makedirs('static/uploads', exist_ok=True)
                    doc.save("static/uploads/bozzadinotula.docx")
                    risultatobis = '<div class="result"><a class="button-link" href="/static/uploads/bozzadinotula.docx" download style="background-color: #28a745; color: white; padding: 10px 20px; border-radius: 5px; text-decoration: none;">Clicca qui per scaricare la bozza di notula</a></div>'


        except ValueError:
            risultato = "L'importo deve essere un numero valido (usa il punto per i decimali)"
    return render_template("redazionefatture.html", risultato=risultato, risultatobis=risultatobis)

