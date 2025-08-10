import os
import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import pandas as pd
from openpyxl.utils import get_column_letter
from openpyxl import load_workbook
from datetime import datetime
import numpy as np
from flask import request, render_template

def _make_driver():
    """Crea un driver Chrome/Chromium valido su Windows (locale) e Linux (Render)."""
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")

    system = platform.system()

    if system == "Linux":
        # Render: browser e driver installati via Aptfile
        # Prova vari path comuni per Chromium/Chrome e chromedriver
        browser_candidates = [
            "/usr/bin/chromium",
            "/usr/bin/chromium-browser",
            "/usr/bin/google-chrome",
        ]
        driver_candidates = [
            "/usr/bin/chromedriver",
            "/usr/lib/chromium/chromedriver",
            "/usr/local/bin/chromedriver",
        ]

        for p in browser_candidates:
            if os.path.exists(p):
                opts.binary_location = p
                break

        service_path = None
        for d in driver_candidates:
            if os.path.exists(d):
                service_path = d
                break

        if not getattr(opts, "binary_location", None):
            raise RuntimeError("Chromium/Chrome non trovato su Linux. Hai aggiunto 'chromium' in Aptfile?")
        if not service_path:
            raise RuntimeError("chromedriver non trovato su Linux. Hai aggiunto 'chromium-driver' in Aptfile?")

        return webdriver.Chrome(service=Service(service_path), options=opts)

    else:
        # Windows locale: usa il tuo chromedriver
        # Modifica questo percorso se hai chromedriver altrove
        win_driver = "C:/webdriver/chromedriver.exe"
        if not os.path.exists(win_driver):
            raise RuntimeError(
                f"chromedriver non trovato su Windows in {win_driver}. "
                "Scaricalo o aggiorna il percorso."
            )
        return webdriver.Chrome(service=Service(win_driver), options=opts)

def borsa():
    if request.method == "GET":
        return render_template("borsa.html")

    tipologia = request.form.get("tipologia")

    if tipologia == "BTP":
        try:
            driver = _make_driver()
            wait = WebDriverWait(driver, 15)

            tutti_dati = []
            for pagina in range(1, 9):
                url = f"https://www.borsaitaliana.it/borsa/obbligazioni/mot/btp/lista.html?&page={pagina}"
                driver.get(url)
                righe = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
                for riga in righe:
                    celle = riga.find_elements(By.TAG_NAME, "td")
                    dati = [c.text for c in celle]
                    if dati:
                        tutti_dati.append(dati)

        finally:
            # chiudi il browser anche in caso di errore
            try:
                driver.quit()
            except Exception:
                pass

        # Costruzione DataFrame
        colonne = ['ISIN', 'Nome', 'Prezzo', 'Cedola %', 'Scadenza', 'Altro']
        df = pd.DataFrame(tutti_dati, columns=colonne)

        # Pulizia/Tipi
        df['ISIN'] = df['ISIN'].astype(str)
        df['Nome'] = df['Nome'].astype(str)
        df['Prezzo'] = pd.to_numeric(df['Prezzo'].str.replace(',', '.'), errors='coerce')
        df['Cedola %'] = pd.to_numeric(df['Cedola %'].str.replace(',', '.'), errors='coerce')
        df['Scadenza'] = pd.to_datetime(df['Scadenza'], dayfirst=True, errors='coerce').dt.normalize()

        # Calcoli
        df['Cedola annuale %'] = df['Cedola %'] * 2
        df['Prezzo valore nominale € 10 K'] = df['Prezzo'] * 100
        df['Cedola semestrale su € 10 K'] = df['Cedola %'] * 100
        df['Cedola semestrale su € 10 K con ritenuta'] = df['Cedola semestrale su € 10 K'] * 0.875
        df['Cedola annuale su € 10 K'] = df['Cedola annuale %'] * 100
        df['Cedola annuale su € 10 K con ritenuta'] = df['Cedola annuale su € 10 K'] * 0.875
        df['Rendimento attuale %'] = np.trunc((df['Cedola annuale %'] / df['Prezzo'] * 100) * 1000) / 1000

        oggi = pd.to_datetime(datetime.today()).normalize()
        df['Scadenza numerica'] = (df['Scadenza'] - oggi).dt.days
        df['Scadenza'] = df['Scadenza'].dt.strftime('%d-%m-%y')
        df['Numero cedole'] = df['Scadenza numerica'] // 182.5 + 1
        df['Ricavo totale'] = df['Numero cedole'] * df['Cedola %'] + 100
        df['Guadagno totale lordo'] = df['Ricavo totale'] - df['Prezzo']
        df['Guadagno totale netto'] = np.trunc((df['Guadagno totale lordo'] * 0.875) * 1000) / 1000
        df['Guadagno medio lordo'] = np.trunc((df['Guadagno totale lordo'] / df['Scadenza numerica'] * 365) * 1000) / 1000
        df['Guadagno medio netto'] = np.trunc((df['Guadagno medio lordo'] * 0.875) * 1000) / 1000

        # Rimuovi colonna non usata
        df = df.drop(columns=['Altro'])

        colonne_da_esportare = [
            'ISIN', 'Nome', 'Prezzo', 'Cedola %', 'Scadenza', 'Cedola annuale %',
            'Rendimento attuale %', 'Numero cedole', 'Ricavo totale',
            'Guadagno totale lordo', 'Guadagno totale netto',
            'Guadagno medio lordo', 'Guadagno medio netto'
        ]

        # Esporta Excel
        nome_file = "btp_dati.xlsx"
        df[colonne_da_esportare].to_excel(nome_file, index=False)

        # Allarga colonne
        wb = load_workbook(nome_file)
        ws = wb.active
        for col_idx, col_cells in enumerate(ws.columns, start=1):
            max_length = 0
            col_letter = get_column_letter(col_idx)
            for cell in col_cells:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            ws.column_dimensions[col_letter].width = max_length * 1.2
        wb.save(nome_file)

        # Tabella HTML
        tabella_html = df.to_html(classes="tabella-risultati", index=False)

        return render_template(
            "borsa.html",
            risultato=f"Elaborazione {tipologia} completata. File salvato come {nome_file}",
            tabella=tabella_html
        )

    # Default: se la tipologia non è gestita
    return render_template("borsa.html", risultato="Seleziona una tipologia valida.", tabella=None)
