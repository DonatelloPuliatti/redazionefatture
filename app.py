from flask import Flask, render_template, request
from somma import *
from moltiplicazione import *
from redazionefatture import *

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/somma", methods=["GET", "POST"])
def somma_route():
    return somma()

@app.route("/moltiplicazione", methods=["GET", "POST"])
def moltiplicazione_route():
    return moltiplicazione()

@app.route("/redazionefatture", methods=["GET", "POST"])
def redazionefatture_route():
    return redazionefatture()

@app.route("/gestionalefatture", methods=["GET", "POST"])
def gestionalefatture():
    return render_template("placeholder.html", titolo="Funzione in lavorazione")

@app.route("/riduzioneformulelogiche", methods=["GET", "POST"])
def riduzioneformulelogiche():
    return render_template("placeholder.html", titolo="Funzione in lavorazione")

@app.route("/configurazionegiuridicafattispecie", methods=["GET", "POST"])
def configurazionegiuridicafattispecie():
    return render_template("placeholder.html", titolo="Funzione in lavorazione")

if __name__ == "__main__":
    app.run(debug=True)
