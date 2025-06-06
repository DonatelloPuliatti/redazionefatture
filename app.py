from flask import Flask, render_template, request
from flask import redirect, url_for
from redazionefatture import *
from redazionefatturesenzafile import *
from compensidm2002 import *

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")



@app.route("/login_redazionefatture", methods=["GET", "POST"])
def login_redazionefatture():
    if request.method == "POST":
        password = request.form.get("password")
        if password == "Federico2017":
            return redirect(url_for('redazionefatture_route'))
        else:
            return "Password errata. <a href='/login_redazionefatture'>Riprova</a>."
    return render_template("login_redazionefatture.html")

@app.route("/redazionefatture", methods=["GET", "POST"])
def redazionefatture_route():
    return redazionefatture()

@app.route("/redazionefatturesenzafile", methods=["GET", "POST"])
def redazionefatturesenzafile_route():
    return redazionefatturesenzafile()

@app.route("/gestionalefatture", methods=["GET", "POST"])
def gestionalefatture():
    return render_template("placeholder.html", titolo="Funzione in lavorazione")

@app.route("/riduzioneformulelogiche", methods=["GET", "POST"])
def riduzioneformulelogiche():
    return render_template("placeholder.html", titolo="Funzione in lavorazione")

@app.route("/configurazionegiuridicafattispecie", methods=["GET", "POST"])
def configurazionegiuridicafattispecie():
    return render_template("placeholder.html", titolo="Funzione in lavorazione")

@app.route("/login_compensidm2002", methods=["GET", "POST"])
def login_compensidm2002():
    if request.method == "POST":
        password = request.form.get("password")
        if password == "Federico2017":
            return redirect(url_for('compensidm2002_route'))
        else:
            return "Password errata. <a href='/login_compensidm2002'>Riprova</a>."
    return render_template("login_compensidm2002.html")

@app.route("/compensidm2002", methods=["GET", "POST"])
def compensidm2002_route():
    return compensidm2002()

if __name__ == "__main__":
    app.run(debug=True)
