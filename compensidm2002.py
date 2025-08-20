from Compensipython.vacazione import *
from Compensipython.art2 import *
from Compensipython.art3 import *
from Compensipython.art4 import *
from Compensipython.art5 import *
from Compensipython.art6c1 import *
from Compensipython.art6c2 import *
from Compensipython.art7 import *
from Compensipython.art8c1 import *
from Compensipython.art8c3 import *
from Compensipython.art9 import *
from Compensipython.art10 import *
from Compensipython.art11 import *
from Compensipython.art12 import *
from Compensipython.art13 import *
from Compensipython.art14 import *
from Compensipython.art15 import *
from Compensipython.art16 import *
from Compensipython.art17 import *
from Compensipython.art18 import *
from Compensipython.art19 import *
from Compensipython.art20 import *
from Compensipython.art21 import *
from Compensipython.art22 import *
from Compensipython.art23 import *
from Compensipython.art24 import *
from Compensipython.art25 import *
from Compensipython.art26 import *
from Compensipython.art27 import *
from Compensipython.art28c1 import *
from Compensipython.art28c2 import *
from Compensipython.art28c3 import *



app = Flask(__name__)

def compensidm2002():

    ipotesiselezionata = None
    tipologiacompenso = None
    selected_option = None


    if request.method == 'POST':
        # Identifichiamo quale form è stato inviato
        selected_option = request.form.get('tipologia')
        form_id = request.form.get('form_id')

        if form_id == 'form art 2':
            return art2()

        if form_id == 'form vacazione':
            return vacazione()

        if form_id == 'form art 3':
            return art3()

        if form_id == 'form art 4':
            return art4()

        if form_id == 'form art 5':
            return art5()

        if form_id == 'form art 6 c 1':
            return art6c1()

        if form_id == 'form art 6 c 2':
            return art6c2()

        if form_id == 'form art 7':
            return art7()

        if form_id == 'form art 8 c 1':
            return art8c1()

        if form_id == 'form art 8 c 3':
            return art8c3()

        if form_id == 'form art 9':
            return art9()

        if form_id == 'form art 10':
            return art10()

        if form_id == 'form art 11':
            return art11()

        if form_id == 'form art 12':
            return art12()

        if form_id == 'form art 13':
            return art13()

        if form_id == 'form art 14':
            return art14()

        if form_id == 'form art 15':
            return art15()

        if form_id == 'form art 16':
            return art16()

        if form_id == 'form art 17':
            return art17()

        if form_id == 'form art 18':
            return art18()

        if form_id == 'form art 19':
            return art19()

        if form_id == 'form art 20':
            return art20()

        if form_id == 'form art 21':
            return art21()

        if form_id == 'form art 22':
            return art22()

        if form_id == 'form art 23':
            return art23()

        if form_id == 'form art 24':
            return art24()

        if form_id == 'form art 25':
            return art25()

        if form_id == 'form art 26':
            return art26()

        if form_id == 'form art 27':
            return art27()

        if form_id == 'form art 28 c 1':
            return art28c1()

        if form_id == 'form art 28 c 2':
            return art28c2()

        if form_id == 'form art 28 c 3':
            return art28c3()

    return render_template('compensidm2002.html', selected_option=selected_option)

if __name__ == "__main__":
    app.run(debug=True)
