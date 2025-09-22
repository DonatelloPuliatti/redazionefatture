from flask import request, render_template
from docxtpl import DocxTemplate
import os
import json
from openai import OpenAI
import pandas as pd
import re
import ast
from dotenv import load_dotenv



def configurazionegiuridicafattispecie():
    # --- Impostazioni conversione (ramo "conversione") ---
    load_dotenv()
    API_KEY = os.getenv("OPENAI_API_KEY")
    if not API_KEY:
        raise RuntimeError("OPENAI_API_KEY non impostata. Configurala nell'ambiente.")
    MODEL = "gpt-4o"
    client = OpenAI(api_key=API_KEY)
    PROMPT = """Per ciascun periodo del testo estrai le formule logiche nella forma "P1, P2.., Pn -> E1, E2..., En".
    - P = presupposti; E = effetti giuridici.
    - Il numero di presupposti (P1…Pn) ed effetti (E1…Em) NON ha limiti: aumenta n in base a quanti elementi sono necessari.
    - Usa congiunzione, disgiunzione, negazione (simboli consentiti: &, |, ¬, -> oppure AND, OR, NOT, ->).
    - Analizza TUTTI i periodi, anche se sembrano definitori o indicativi (nel diritto spesso indicano doveri).
    - Mantieni coerenza tra variabili nelle formule e nel dizionario (se una variabile ricorre, definiscila una volta sola).
    - Definizioni P*/E* massimamente dettagliate e granulari.
    - Considera che i periodi successivi possono introdurre deroghe: riprendi i presupposti della regola di base.
    - Rispetta la struttura sintattica del testo.
    Devi restituire SOLO JSON valido con esattamente le chiavi "Formule" e "Dizionario"."""

    # esempi per il prompt
    EXCEL_PATH = "esempioformulelogiche.xlsx"
    try:
        df_esempi = pd.read_excel(EXCEL_PATH).fillna("")
        esempi = json.dumps(
            [{"Testo": str(r["Testo"]), "Formule": str(r["Formule"]), "Dizionario": str(r["Dizionario"])}
             for _, r in df_esempi.head(5).iterrows()],
            ensure_ascii=False, indent=2
        )
    except Exception:
        esempi = "[]"

    # --- Variabili per il template ---
    selected_option = None
    testonormativo = None
    solo_formule = None
    solo_dizionario = None
    articoli = []
    articoli_error = None
    numeroarticolo_scelto = None
    domande_presupposti = []
    esiti_messaggi = None
    testo_articolo = None

    if request.method == "POST":
        selected_option = request.form.get("tipologia")

        # ===================== RAMO CONFIGURAZIONE =====================
        if selected_option == "configurazione":
            # carico elenco articoli
            try:
                df_norme = pd.read_excel("elenconorme.xlsx")
                articoli = (
                    df_norme["Numeroarticolo"]
                    .dropna()
                    .astype(str)
                    .tolist()
                )
            except Exception as e:
                articoli_error = f"Errore nel leggere 'elenconorme.xlsx': {e}"
                articoli = []

            # --- 1) Primo step: scelta articolo -> genero domande sì/no ---
            if request.form.get("form_id") == "configurazione-selezione-corpus":
                numeroarticolo_scelto = request.form.get("numeroarticolo")

                try:
                    riga = df_norme[df_norme["Numeroarticolo"].astype(str) == str(numeroarticolo_scelto)].iloc[0]
                except Exception:
                    articoli_error = f"Articolo {numeroarticolo_scelto} non trovato."
                    riga = None

                if riga is not None:
                    raw_diz = riga.get("Dizionario", "")
                    testo_articolo = str(riga.get("Testo", "") or "")
                    # tenta JSON
                    if isinstance(raw_diz, dict):
                        diz = raw_diz
                    else:
                        try:
                            diz = json.loads(str(raw_diz))
                        except Exception:
                            diz = None
                    # fallback "P1: ..., E1: ..." separati da ; o newline
                    if diz is None:
                        diz = {}
                        testo = str(raw_diz)
                        for m in re.finditer(r"(P\d+|E\d+)\s*[:=]\s*(.+?)(?=;\s*(?:P|E)\d+|$)",
                                             testo, flags=re.IGNORECASE | re.DOTALL):
                            diz[m.group(1).upper().strip()] = m.group(2).strip()

                    # estraggo solo Pn come domande
                    presupposti = []
                    for k, v in diz.items():
                        if isinstance(k, str) and k.upper().startswith("P") and k[1:].isdigit():
                            domanda = v.strip()
                            if not domanda.endswith("?"):
                                domanda += "?"
                            presupposti.append((k.upper(), domanda))

                    presupposti.sort(key=lambda kv: int(kv[0][1:]) if kv[0][1:].isdigit() else 9999)
                    domande_presupposti = presupposti

            # --- 2) Secondo step: invio domande -> valutazione formule + messaggi ---
            if request.form.get("form_id") == "configurazione-domande":
                selected_option = "configurazione"
                numeroarticolo_scelto = request.form.get("numeroarticolo")

                # riga dell'articolo
                try:
                    riga = df_norme[df_norme["Numeroarticolo"].astype(str) == str(numeroarticolo_scelto)].iloc[0]
                except Exception:
                    articoli_error = f"Articolo {numeroarticolo_scelto} non trovato."
                    riga = None

                if riga is None:
                    return render_template(
                        "configurazionegiuridicafattispecie.html",
                        selected_option=selected_option,
                        articoli=articoli,
                        articoli_error=articoli_error,
                        numeroarticolo_scelto=None,
                        domande_presupposti=[],
                        solo_formule="",
                        solo_dizionario="{}",
                        esiti_messaggi=None,
                        testo_articolo=None
                    )

                testo_articolo = str(riga.get("Testo", "") or "")

                # Dizionario Pn/En -> descrizione
                raw_diz = riga.get("Dizionario", "") or ""
                if isinstance(raw_diz, dict):
                    diz = raw_diz
                else:
                    try:
                        diz = json.loads(str(raw_diz)) if str(raw_diz).strip() else {}
                    except Exception:
                        diz = {}
                        for p in re.split(r";|\n", str(raw_diz)):
                            p = p.strip()
                            if not p:
                                continue
                            m = re.match(r"^(P\d+|E\d+)\s*[:=]\s*(.+)$", p)
                            if m:
                                diz[m.group(1).upper()] = m.group(2).strip()

                # Risposte sì/no -> booleans
                presupposti_bool = {}
                for k, v in request.form.items():
                    if k.startswith("presupposto_"):
                        var = k.replace("presupposto_", "").strip().upper()
                        presupposti_bool[var] = (v.lower() == "si")

                # Formule dell'articolo (una per riga)
                formule_raw = str(riga.get("Formule", "") or "")
                formule = [f.strip() for f in re.split(r"\r?\n+", formule_raw) if f.strip()]

                # Valutazione: antecedente -> effetti
                messaggi = []

                for f in formule:
                    if "->" in f:
                        antecedente, conseguente = f.split("->", 1)
                    elif "→" in f:
                        antecedente, conseguente = f.split("→", 1)
                    else:
                        continue

                    # normalizza operatori in sintassi Python
                    expr = antecedente
                    expr = expr.replace("∧", " and ").replace("&", " and ")
                    expr = expr.replace("∨", " or ").replace("|", " or ")
                    expr = re.sub(r"\bNOT\b", " not ", expr, flags=re.I)
                    expr = expr.replace("¬", " not ")

                    # valuta in sicurezza via AST
                    node = ast.parse(expr, mode="eval")

                    def _e(n):
                        if isinstance(n, ast.Expression): return _e(n.body)
                        if isinstance(n, ast.BoolOp):
                            vals = [_e(v) for v in n.values]
                            if isinstance(n.op, ast.And): return all(vals)
                            if isinstance(n.op, ast.Or):  return any(vals)
                            raise ValueError("Operatore booleano non supportato")
                        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.Not): return not _e(n.operand)
                        if isinstance(n, ast.Name): return bool(presupposti_bool.get(n.id, False))
                        if isinstance(n, ast.Constant) and isinstance(n.value, bool): return n.value
                        raise ValueError("Nodo AST non consentito")

                    try:
                        antecedente_val = bool(_e(node))
                    except Exception:
                        antecedente_val = False

                    # tutti gli En nel conseguente
                    en_list = re.findall(r"\bE\d+\b", conseguente)
                    for en in en_list:
                        descr = diz.get(en, en)
                        if antecedente_val:
                            messaggi.append(f"si verifica il seguente effetto giuridico: {descr}")
                        else:
                            messaggi.append(f"NON si verifica il seguente effetto giuridico: {descr}")

                esiti_messaggi = messaggi
                # dopo l’esito, non riproponiamo le domande
                domande_presupposti = []

        # ===================== RAMO CONVERSIONE =====================
        if request.form.get("form_id") == "conversione":
            selected_option = "conversione"
            testonormativo = request.form.get("testonormativo", "").strip()

            user_msg = (
                "ISTRUZIONI:\n" + PROMPT +
                "\n\nESEMPI_DA_EXCEL (prime righe):\n" + esempi +
                "\n\nTESTO:\n<<<\n" + testonormativo + "\n>>>"
            )

            resp = client.chat.completions.create(
                model=MODEL,
                response_format={"type": "json_object"},
                temperature=0.1,
                messages=[
                    {"role": "system",
                     "content": "Sei un assistente per l'analisi logico-giuridica. Rispondi SOLO con JSON valido."},
                    {"role": "user", "content": user_msg},
                ],
            )

            contenuto = resp.choices[0].message.content
            try:
                data = json.loads(contenuto)
                solo_formule = "\n".join(data.get("Formule", [])) if isinstance(data.get("Formule"), list) else str(data.get("Formule", ""))
                solo_dizionario = json.dumps(data.get("Dizionario", {}), ensure_ascii=False, indent=2)
            except json.JSONDecodeError:
                solo_formule = contenuto
                solo_dizionario = "{}"

    return render_template(
        "configurazionegiuridicafattispecie.html",
        selected_option=selected_option,
        articoli=articoli,
        articoli_error=articoli_error,
        numeroarticolo_scelto=numeroarticolo_scelto,
        domande_presupposti=domande_presupposti,
        solo_formule=solo_formule,
        solo_dizionario=solo_dizionario,
        esiti_messaggi=esiti_messaggi,
        testo_articolo=testo_articolo
    )
