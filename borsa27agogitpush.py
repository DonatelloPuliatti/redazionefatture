# borsa.py
import os
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from flask import request, render_template
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager


logging.basicConfig(level=logging.INFO)


# ---------- Selenium helper: compatibile Windows locale + Render (Linux) ----------
def _find_first_existing(paths):
    """Ritorna il primo path esistente nella lista, altrimenti None."""
    for p in paths:
        if p and os.path.exists(p):
            return p
    return None



def make_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=it-IT")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )

    # 1) prova con i binari di sistema (Render + Aptfile)
    chrome_candidates = [
        os.getenv("CHROME_BIN"),
        os.getenv("GOOGLE_CHROME_BIN"),
        "/usr/bin/chromium-browser",
        "/usr/bin/chromium",
        "/usr/bin/google-chrome",
        "/snap/bin/chromium",
    ]
    driver_candidates = [
        os.getenv("CHROMEDRIVER_PATH"),
        "/usr/bin/chromedriver",
        "/usr/local/bin/chromedriver",
    ]

    def first_existing(paths):
        for p in paths:
            if p and os.path.exists(p):
                return p
        return None

    chrome_path = first_existing(chrome_candidates)
    if chrome_path:
        options.binary_location = chrome_path

    try:
        # Se esiste un chromedriver di sistema, usalo
        sys_driver = first_existing(driver_candidates)
        if sys_driver:
            service = Service(executable_path=sys_driver)
            return webdriver.Chrome(service=service, options=options)
        # Altrimenti lascia che Selenium Manager o WebDriverManager facciano il loro lavoro
        # (Selenium Manager prova da solo se non forniamo Service)
        return webdriver.Chrome(options=options)

    except (SessionNotCreatedException, WebDriverException):
        # 2) fallback: scarica il driver giusto a runtime
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)




# ---------- Route ----------
def borsa():
    if request.method == "GET":
        return render_template("borsa.html")

    tipologia = request.form.get("tipologia")
    investimento = request.form.get("investimento")
    investimento = float(investimento.replace(",", "."))
    inflazione = request.form.get("inflazione")
    inflazione = float(inflazione.replace(",", "."))

    driver = None
    try:
        driver = make_driver()

        tutti_dati = []
        # Pagine BTP su Borsa Italiana
        for pagina in range(1, 9):
            url = f"https://www.borsaitaliana.it/borsa/obbligazioni/mot/btp/lista.html?&page={pagina}"
            driver.get(url)

            html = driver.page_source
            soup = BeautifulSoup(html, "lxml")
            for tr in soup.select("table tbody tr"):
                celle = [td.get_text(strip=True) for td in tr.find_all("td")]
                if celle:
                    tutti_dati.append(celle)



        # Colonne attese dalla tabella corrente
        colonne = ["ISIN", "Nome", "Prezzo", "Cedola (%)", "Scadenza", "Altro"]
        df = pd.DataFrame(tutti_dati, columns=colonne)

        # Tipi
        df["ISIN"] = df["ISIN"].astype(str).str.strip().str[0:12]

        df["Nome"] = df["Nome"].astype(str)

        df["Cedola (%)"] = (
            df["Cedola (%)"]
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
        )
        df["Cedola (%)"] = pd.to_numeric(df["Cedola (%)"], errors="coerce").fillna(0.0)
        pd.set_option("display.float_format", lambda x: f"{x:.5f}")

        df["Scadenza"] = pd.to_datetime(df["Scadenza"], dayfirst=True, errors="coerce").dt.normalize()
        oggi = pd.to_datetime(datetime.today()).normalize()

        mesi_diff = ((df["Scadenza"].dt.year - oggi.year) * 12
                     + (df["Scadenza"].dt.month - oggi.month)
                     - (df["Scadenza"].dt.day < oggi.day).astype("int64"))

        delta_giorni = (df["Scadenza"] - oggi).dt.days
        anni_diff = delta_giorni / 365.25





        # --- qui definiamo i mesi per intervallo ---
        nome_norm = df["Nome"].fillna("").str.strip().str.lower()
        cond_coupon = nome_norm.str.startswith("btp coupon") | nome_norm.str.startswith("btpstripital")
        cond_speciali = nome_norm.str.startswith("btp piu") | nome_norm.str.startswith("btp valore sc")
        df["MesiPerIntervallo"] = np.where(cond_speciali, 3, 6).astype("int64")
        # ------------------------------------

        # CedNUM = 0 per coupon/stripital, altrimenti il calcolo normale
        df["CedNUM"] = np.where(cond_coupon, 0, (mesi_diff // df["MesiPerIntervallo"]).astype("int64"))

        # Calcola l'ultimo intervallo (se CedNUM=0 resta uguale alla scadenza)
        ultimo_intervallo = df.apply(
            lambda r: r["Scadenza"] - pd.DateOffset(months=r["CedNUM"] * r["MesiPerIntervallo"]),
            axis=1
        )
        df["CedNUM"] = df["CedNUM"] + 1

        df["GG"] = (ultimo_intervallo - oggi).dt.days



        df["Scadenza"] = df["Scadenza"].dt.strftime("%d-%m-%y")

        # Prezzo e Cedola: da "113.500" o "113,50" a float
        df["Prezzo"] = (
            df["Prezzo"]
            .str.replace(".", "", regex=False)   # rimuove puntini come mille/format
            .str.replace(",", ".", regex=False)  # virgola -> punto decimale
        )
        df["Prezzo"] = pd.to_numeric(df["Prezzo"], errors="coerce")

        


        conditions = [
            df["ISIN"] == "IT0005497000",
            df["ISIN"] == "IT0005648255",
            df["ISIN"] == "IT0005332835",

            df["ISIN"] == "IT0005532723",
            df["ISIN"] == "IT0005517195",
            df["ISIN"] == "IT0005388175",

            df["ISIN"] == "IT0005657348",
            df["ISIN"] == "IT0005588881",
            df["ISIN"] == "IT0005647273",

            df["ISIN"] == "IT0005482994",
            df["ISIN"] == "IT0005436701",
            df["ISIN"] == "IT0005387052",
            df["ISIN"] == "IT0005415416",
            df["ISIN"] == "IT0005138828",
            df["ISIN"] == "IT0005246134",
            df["ISIN"] == "IT0005543803",
            df["ISIN"] == "IT0005547812",
            df["ISIN"] == "IT0004735152",
            df["ISIN"] == "IT0003745541",
            df["ISIN"] == "IT0004545890",
        ]

        values = [
            1.088,
            1.004,
            1.194,
            1.145,
            1.213,
            1.223,

            1.002,
            1.028,
            1.005,

            1.145,
            1.213,
            1.223,



            1.224,
            1.281,
            1.264,
            1.049,
            1.048,
            1.375,
            1.392,
            1.391
        ]

        df["Ind."] = np.select(conditions, values, default=1)

        df["ValNOM (€)"] = investimento * 100 / df["Prezzo"]

        df["CedLRD (€)"] = df["ValNOM (€)"] / 100 * df["Cedola (%)"] * df["Ind."]
        df["CedNTT (€)"] = df["CedLRD (€)"] * 0.875

        nome_norm = df["Nome"].fillna("").str.strip().str.lower()
        cond_speciali = nome_norm.str.startswith("btp piu") | nome_norm.str.startswith("btp valore")

        # 2) 'a' per riga: 190 se speciale, altrimenti 180 (usiamo una Series per l'allineamento riga-a-riga)
        a = pd.Series(np.where(cond_speciali, 93, 184), index=df.index)

        # 3) gg_mod = GG % a (con .mod per gestire correttamente tipi nullable e NA)
        gg_mod = df["GG"].mod(a)

        # 4) frazione di periodo maturata: (GG % a) / a
        frazione = gg_mod / a

        # 5) formula: Rateo = CedLRD - (frazione * CedLRD)
        df["RateoLRD (€)"] = df["CedLRD (€)"] - (frazione * df["CedLRD (€)"])
        df["RateoNTT (€)"] = df["RateoLRD (€)"] * 0.875
        df["EsbINIZ"] = investimento + df["RateoNTT (€)"] + (df["ValNOM (€)"] * (df["Ind."] - 1))



        SEMESTRE_GIORNI = 182.0
        ANNO_GIORNI = 365.25
        i = inflazione / 100.0
        r = df["Cedola (%)"] * df["Ind."]/ 100.0
        fattore_prima = np.power(1.0 + i, df["GG"] / ANNO_GIORNI)
        q = np.power(1.0 + i, SEMESTRE_GIORNI / ANNO_GIORNI)
        geom_sum = np.where(
            np.isclose(q, 1.0),
            df["CedNUM"],
            (np.power(q, df["CedNUM"]) - 1.0) / (q - 1.0)
        )
        df["TotCedole (€)"] = r * df["ValNOM (€)"] * fattore_prima * geom_sum
        df["Capitalerimborsatospeciale"] = df["ValNOM (€)"] * df["Ind."] * ((1 + (inflazione/100.0)) ** anni_diff)
        df["Capitalerimborsatogenerale"] = df["ValNOM (€)"]

        cond_speciale = df["ISIN"].isin([
            "IT0005497000", "IT0005648255", "IT0005332835",
            "IT0005532723", "IT0005517195", "IT0005388175",
            "IT0005657348", "IT0005588881", "IT0005647273",
            "IT0005482994", "IT0005436701", "IT0005387052",
            "IT0005415416", "IT0005138828", "IT0005246134",
            "IT0005543803", "IT0005547812", "IT0004735152",
            "IT0003745541", "IT0004545890"
        ])

        # Condizione "generale" (negazione della prima)
        cond1 = df["ISIN"].isin(["IT0005583486"])
        cond2 = df["ISIN"].isin(["IT0005594483"])
        cond3 = df["ISIN"].isin(["IT0005565400"])
        cond4 = df["ISIN"].isin(["IT0005442097"])
        cond5 = df["ISIN"].isin(["IT0005415291"])
        cond6 = df["ISIN"].isin(["IT0005425761"])
        cond7 = df["ISIN"].isin(["IT0005466351"])






        valoregenerale = (df["CedLRD (€)"] * df["CedNUM"]) + df["Capitalerimborsatogenerale"]
        # Uso di np.select
        df["RicTOT (€)"] = np.select(
            [cond_speciale, cond1, cond2, cond3, cond4, cond5, cond6, cond7],
            [
                df["TotCedole (€)"] + df["Capitalerimborsatospeciale"],  # per ISIN speciali
                (4/4 * df["CedNUM"] * df["ValNOM (€)"] /100 ) - (0.75/4 * (df["CedNUM"] - 12).clip(lower=0)) * df["ValNOM (€)"]/100 + df["Capitalerimborsatogenerale"],
                (3.9/4 * df["CedNUM"] * df["ValNOM (€)"] / 100) - (0.55/4 * (df["CedNUM"] - 12).clip(lower=0)) * df[
                    "ValNOM (€)"] / 100 + df["Capitalerimborsatogenerale"],
                (4.5/ 4 * df["CedNUM"] * df["ValNOM (€)"] / 100) - (0.40/ 4 * (df["CedNUM"] - 8).clip(lower=0)) * df[
                    "ValNOM (€)"] / 100 + df["Capitalerimborsatogenerale"],

                (2 / 2 * df["CedNUM"] * df["ValNOM (€)"] / 100) - (0.35 / 2 * (df["CedNUM"] - 8).clip(lower=0)) * df[
                    "ValNOM (€)"] / 100      -  (0.45 / 2 * (df["CedNUM"] - 16).clip(lower=0)) * df[
                    "ValNOM (€)"] / 100                       + df["Capitalerimborsatogenerale"], # 4

                (1.45/ 2 * df["CedNUM"] * df["ValNOM (€)"] / 100) - (0.15 / 2 * (df["CedNUM"] - 6).clip(lower=0)) * df[
                    "ValNOM (€)"] / 100 + df["Capitalerimborsatogenerale"],
                (1 / 2 * df["CedNUM"] * df["ValNOM (€)"] / 100) - (0.4/ 2 * (df["CedNUM"] - 4).clip(lower=0)) * df[
                    "ValNOM (€)"] / 100 + df["Capitalerimborsatogenerale"],

                (1.7 / 2 * df["CedNUM"] * df["ValNOM (€)"] / 100) - (0.45 / 2 * (df["CedNUM"] - 8).clip(lower=0)) * df[
                    "ValNOM (€)"] / 100 - (0.5 / 2 * (df["CedNUM"] - 16).clip(lower=0)) * df[
                    "ValNOM (€)"] / 100 + df["Capitalerimborsatogenerale"] # 7
            ],
            default= valoregenerale
        )






        df["GuadTOTLRD (€)"] = df["RicTOT (€)"] - df["EsbINIZ"]
        df["GuadTOTNTT (€)"] = df["GuadTOTLRD (€)"] * 0.875
        df["RendLRD (%)"] = df["GuadTOTLRD (€)"] / df["EsbINIZ"] * 100
        df["RendNTT (%)"] = df["GuadTOTNTT (€)"] / df["EsbINIZ"] * 100
        df["Inflazione"] = ((1 + (inflazione/100.0)) ** anni_diff)
        df["ValoreATT"] = df["EsbINIZ"] * ((1 + (inflazione/100.0)) ** anni_diff)
        df["RendLRDdefl (%)"] = (df["RicTOT (€)"] / df["ValoreATT"] - 1) * 100
        df["RendNTTdefl (%)"] = np.where(
            df["RendLRDdefl (%)"] < 0,  # condizione: se il rendimento è negativo
            0,  # allora metti 0
            df["RendLRDdefl (%)"] * 0.875  # altrimenti calcola normalmente
        )
        df["RendLRDdeflANN (%)"] = df["RendLRDdefl (%)"] / anni_diff
        df["RendNTTdeflANN (%)"] = df["RendNTTdefl (%)"] / anni_diff

        # Elimina "Altro" se presente
        if "Altro" in df.columns:
            df = df.drop(columns=["Altro"])

        colonne_da_esportare = [
            "ISIN",
            "Nome",
            "Prezzo",
            "Cedola (%)",
            "Scadenza",
        ]

        # Salvataggio XLSX: preferisci /tmp se scrivibile (Render)


        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df = df.fillna('')

        if "ISIN" in df.columns:
            def isin_link(x):
                if pd.isna(x) or str(x).strip() == "":
                    return ""
                s = str(x).strip().upper()
                return (
                    f'<a href="https://www.borsaitaliana.it/borsa/obbligazioni/mot/btp/scheda/{s}.html?lang=it" '
                    f'target="_blank" rel="noopener noreferrer">{s}</a>'
                )

            df["ISIN"] = df["ISIN"].map(isin_link)

        def aggiungi_info(nome):
            if not isinstance(nome, str):
                return nome
            info = None

            if nome.lower().startswith("btp coupon"):
                info = (
                    "Indicizzato all'inflazione: NO&#10;"
                    "Premio finale/intermedio: NO&#10;"
                    "Periodicità cedola: NO&#10;"
                    "Cedola fissa/variabile: NO&#10;"
                    "Note particolari: il titolo non prevede l'erogazione di cedole periodiche ed è caratterizzato dal coupon stripping"
                )

            if nome.lower().startswith("btp futura"):
                info = (
                    "Indicizzato all'inflazione: NO&#10;"
                    "Premio finale/intermedio: SI, finale e intermedio, ma solo per coloro che hanno acquistato il titolo all'emissione&#10;"
                    "Periodicità cedola: 6 mesi&#10;"
                    "Cedola fissa/variabile: variabile&#10;"
                    "Note particolari: caratterizzato dallo step-up, con cedole che aumentano periodicamente; la cedola riportata è quella attuale, ma il calcolo del rimborso finale tiene conto della diversità delle cedole per ogni specifico ISIN"
                )

            if nome.lower().startswith("btp fx"):
                info = (
                    "Indicizzato all'inflazione: NO&#10;"
                    "Premio finale/intermedio: NO&#10;"
                    "Periodicità cedola: 6 mesi&#10;"
                    "Cedola fissa/variabile: fissa&#10;"
                    "Note particolari: la cedola è erogata in valuta estera"
                )

            if nome.lower().startswith("btp green fx"):
                info = (
                    "Indicizzato all'inflazione: NO&#10;"
                    "Premio finale/intermedio: NO&#10;"
                    "Periodicità cedola: 6 mesi&#10;"
                    "Cedola fissa/variabile: fissa&#10;"
                    "Note particolari: il titolo è destinato a finanziare progetti ambientali"
                )

            if nome.lower().startswith("btp italia"):
                info = (
                    "Indicizzato all'inflazione: SI&#10;"
                    "Premio finale/intermedio: SI, solo finale, esclusivamente per coloro che hanno acquistato il titolo all'emissione&#10;"
                    "Periodicità cedola: 6 mesi&#10;"
                    "Cedola fissa/variabile: variabile perchè dipendente dall'inflazione&#10;"
                    "Note particolari: il titolo è indicizzato al FOI senza tabacchi e l'indicizzazione riguarda il capitale cui applicare la cedola"
                )

            if nome.lower().startswith("btp più"):
                info = (
                    "Indicizzato all'inflazione: NO&#10;"
                    "Premio finale/intermedio: NO&#10;"
                    "Periodicità cedola: 3 mesi&#10;"
                    "Cedola fissa/variabile: variabilee&#10;"
                    "Note particolari: caratterizzato dallo step-up, con cedole che aumentano periodicamente; la cedola è quella attualela cedola riportata è quella attuale, ma il calcolo del rimborso finale tiene conto della diversità delle cedole per ogni specifico ISIN"
                )


            if nome.lower().startswith("btp tf"):
                info = (
                    "Indicizzato all'inflazione: NO&#10;"
                    "Premio finale/intermedio: NO&#10;"
                    "Periodicità cedola: 6 mesi&#10;"
                    "Cedola fissa/variabile: fissa&#10;"
                    "Note particolari: si tratta dei titoli aventi una struttura tradizionale semplice, con cedole periodiche fisse, nessuna indicizzazione e nessun meccanismo premiale"
                )

            if nome.lower().startswith("btp più"):
                info = (
                    "Indicizzato all'inflazione: NO&#10;"
                    "Premio finale/intermedio: NO&#10;"
                    "Periodicità cedola: 3 mesi&#10;"
                    "Cedola fissa/variabile: variabilee&#10;"
                    "Note particolari: caratterizzato dallo step-up, con cedole che aumentano periodicamente; la cedola è quella attualela cedola riportata è quella attuale, ma il calcolo del rimborso finale tiene conto della diversità delle cedole per ogni specifico ISIN"
                )

            if nome.lower().startswith("btp valore"):
                info = (
                    "Indicizzato all'inflazione: NO&#10;"
                    "Premio finale/intermedio: SI, solo finale, esclusivamente per coloro che hanno acquistato il titolo all'emissione&#10;"
                    "Periodicità cedola: 6 mesi&#10;"
                    "Cedola fissa/variabile: variabilee&#10;"
                    "Note particolari: caratterizzato dallo step-up, con cedole che aumentano periodicamente; la cedola è quella attuale, ma il calcolo del rimborso finale tiene conto della diversità delle cedole per ogni specifico ISIN"
                )

            if nome.lower().startswith("btp valore sc"):
                info = (
                    "Indicizzato all'inflazione: NO&#10;"
                    "Premio finale/intermedio: SI, solo finale, esclusivamente per coloro che hanno acquistato il titolo all'emissione&#10;"
                    "Periodicità cedola: 3 mesi&#10;"
                    "Cedola fissa/variabile: variabilee&#10;"
                    "Note particolari: caratterizzato dallo step-up, con cedole che aumentano periodicamente; la cedola è quella attuale, ma il calcolo del rimborso finale tiene conto della diversità delle cedole per ogni specifico ISIN"
                )

            if nome.lower().startswith("btp-"):
                info = (
                    "Indicizzato all'inflazione: NO&#10;"
                    "Premio finale/intermedio: NO&#10;"
                    "Periodicità cedola: 6 mesi&#10;"
                    "Cedola fissa/variabile: fissa&#10;"
                    "Note particolari: si tratta dei titoli aventi una struttura tradizionale semplice, con cedole periodiche fisse, nessuna indicizzazione e nessun meccanismo premiale"
                )

            if nome.lower().startswith("btpgreen"):
                info = (
                    "Indicizzato all'inflazione: NO&#10;"
                    "Premio finale/intermedio: NO&#10;"
                    "Periodicità cedola: 6 mesi&#10;"
                    "Cedola fissa/variabile: fissa&#10;"
                    "Note particolari: il titolo è destinato a finanziare progetti ambientali"
                )

            if nome.lower().startswith("btpi fx"):
                info = (
                    "Indicizzato all'inflazione: SI&#10;"
                    "Premio finale/intermedio: NO&#10;"
                    "Periodicità cedola: 6 mesi&#10;"
                    "Cedola fissa/variabile: variabile&#10;"
                    "Note particolari: il titolo è indicizzato all'inflazione area euro, ex tabacchi; il titolo è negoziato in valuta estera"
                )

            if nome.lower().startswith("btpi tf"):
                info = (
                    "Indicizzato all'inflazione: SI&#10;"
                    "Premio finale/intermedio: NO&#10;"
                    "Periodicità cedola: 6 mesi&#10;"
                    "Cedola fissa/variabile: variabile&#10;"
                    "Note particolari: il titolo è indicizzato all'inflazione area euro, ex tabacchi"
                )

            if nome.lower().startswith("btpi-"):
                info = (
                    "Indicizzato all'inflazione: SI&#10;"
                    "Premio finale/intermedio: NO&#10;"
                    "Periodicità cedola: 6 mesi&#10;"
                    "Cedola fissa/variabile: variabile&#10;"
                    "Note particolari: il titolo è indicizzato all'inflazione area euro, ex tabacchi"
                )

            if nome.lower().startswith("btpstripital"):
                info = (
                    "Indicizzato all'inflazione: NO&#10;"
                    "Premio finale/intermedio: NO&#10;"
                    "Periodicità cedola: NO&#10;"
                    "Cedola fissa/variabile: NO&#10;"
                    "Note particolari: il titolo non prevede l'erogazione di cedole periodiche ed è caratterizzato dal coupon stripping"
                )

            if info:
                return (
                    f'{nome} '
                    f'<span title="{info}" '
                    f'style="display:inline-block; width:16px; height:16px; '
                    f'border-radius:50%; background-color:#4CAF50; color:#fff; '
                    f'text-align:center; font-size:12px; line-height:16px; '
                    f'cursor:help; font-weight:bold;">i</span>'
                )
            return nome

        df["Nome"] = df["Nome"].apply(aggiungi_info)

        # Tabella HTML (id per DataTables) eliminando le colonne che non vanno visualizzate
        df_vis = df.drop(columns=["Inflazione", "Capitalerimborsato", "TotCedole (€)", "Capitalerimborsatogenerale", "Capitalerimborsatospeciale", "MesiPerIntervallo"], errors="ignore")
        tabella_html = df_vis.to_html(
            classes="tabella-risultati display nowrap",
            table_id="btpTable",
            index=False,
            escape=False
        )

        return render_template(
            "borsa.html",
            risultato=f"Elaborazione completata.",
            tabella=tabella_html,
        )

    except Exception as e:
        logging.exception("Errore durante scraping/elaborazione BTP")
        # Mostra l'errore completo anche a video per debug
        return render_template(
            "borsa.html",
            risultato=f"Si è verificato un errore: {type(e).__name__} - {e}",
            tabella=None
        ), 500


    finally:
        try:
            if driver:
                driver.quit()
        except Exception:
            pass
