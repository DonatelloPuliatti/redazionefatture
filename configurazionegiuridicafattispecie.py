from flask import request, render_template
from docxtpl import DocxTemplate
import os
import json
from openai import OpenAI
import pandas as pd

def configurazionegiuridicafattispecie():
    API_KEY = os.getenv("OPENAI_API_KEY", "***REMOVED***")
    MODEL = "gpt-4o"
    client = OpenAI(api_key=API_KEY)
    PROMPT = """Per ciascun periodo del testo estrai le formule logiche nella forma "P1, P2.., Pn -> E1, E2..., En".
    - P = presupposti; E = effetti giuridici.
    - Usa congiunzione, disgiunzione, negazione (simboli consentiti: &, |, ¬, -> oppure AND, OR, NOT, ->).
    - Analizza TUTTI i periodi, anche se sembrano definitori o indicativi (nel diritto spesso indicano doveri).
    - Mantieni coerenza tra variabili nelle formule e nel dizionario (se una variabile ricorre, definiscila una volta sola).
    - Definizioni P*/E* massimamente dettagliate e granulari. Ad es., spesso un avverbio potrebbe dar luogo ad un presupposto autonomo (come 'intenzionalmente', 'arbitrariamente', ecc.), ma anche un attributo (come "mobile" in "cosa mobile").
    - Tieni presente che, spesso, i periodi successivi al primo intr oducono delle deroghe: le relative formule, quindi, devono riprendere l'insieme dei presupposti della regola di cui al primo periodo.

    Devi restituire SOLO JSON valido con ESATTAMENTE queste due chiavi (niente altro):

    {
      "Formule": [
        "P1 & (P2 | P3) & (P4 | P5) -> E1",
        "(P6 | P7) -> E2",
        "P8 -> E3"
      ],
      "Dizionario": {
        "P1": "…",
        "P2": "…",
        "E1": "…"
      }
    }

    Regole:
    - In "Formule" inserisci SOLO le formule, una per periodo, senza testo del periodo.
    - In "Dizionario" inserisci SOLO la mappa variabili->significato (nessun testo aggiuntivo).
    """

    EXCEL_PATH = "esempioformulelogiche.xlsx"  # cambia se serve
    df = pd.read_excel(EXCEL_PATH).fillna("")
    esempi = json.dumps(
        [{"Testo": str(r["Testo"]), "Formule": str(r["Formule"]), "Dizionario": str(r["Dizionario"])}
         for _, r in df.head(5).iterrows()],
        ensure_ascii=False, indent=2
    )

    selected_option = None
    testonormativo = None
    solo_formule = None
    solo_dizionario = None

    if request.method == "POST":
        # Leggi il radio del primo form
        selected_option = request.form.get("tipologia")
        # (facoltativo) se stai inviando il secondo form, puoi distinguere con form_id:
        if request.form.get("form_id") == "conversione":
            selected_option = "conversione"
            testonormativo = request.form.get("testonormativo")
            TESTO = testonormativo.strip()

            user_msg = (
                    "ISTRUZIONI:\n" + PROMPT +
                    "\n\nESEMPI_DA_EXCEL (prime righe):\n" + esempi +
                    "\n\nTESTO:\n<<<\n" + TESTO + "\n>>>"
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

                # due pezzi separati per l'HTML
                # Formule: come testo multi-riga (comodo anche per una colonna Excel)
                if isinstance(data.get("Formule"), list):
                    solo_formule = "\n".join(data["Formule"])
                else:
                    solo_formule = str(data.get("Formule", ""))

                # Dizionario: ben formattato
                solo_dizionario = json.dumps(data.get("Dizionario", {}), ensure_ascii=False, indent=2)

            except json.JSONDecodeError:
                # fallback: tutto nella parte "formule", e lascia vuoto il dizionario
                solo_formule = contenuto
                solo_dizionario = "{}"

    return render_template(
        "configurazionegiuridicafattispecie.html",
        selected_option=selected_option,
        solo_formule=solo_formule,
        solo_dizionario=solo_dizionario
    )

