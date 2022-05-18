from flask import Flask
from flask import render_template
from flask import request
import datetime
from datetime import timedelta

app = Flask(__name__)

ONEYEAR_MINUTES = 525600
MALE_SPAN = 81.64
FEMALE_SPAN = 87.74
YANI = -5
SIBAINU = 7621200 #14.5*365*24*60
WANI = 144000 #100*24*60
YANIPRICE = 13

def smoking_span(yst_date, yend_date):
    yst_dt = datetime.date(yst_date[0], yst_date[1], yst_date[2])
    yend_dt = datetime.date(yend_date[0], yend_date[1], yend_date[2])
    yanidays = ((yst_dt - yend_dt) / timedelta(days=1))

    return yanidays

def noyani_lifespan(sex):
    if sex == "male":
        longevity = ONEYEAR_MINUTES * MALE_SPAN
    else:
        longevity = ONEYEAR_MINUTES * FEMALE_SPAN
    return longevity

def yesyani_lifespan(sex, yst_date, yend_date, quantity):
    yanidays = smoking_span(yst_date, yend_date)

    if sex == "male":
        longevity = ONEYEAR_MINUTES * MALE_SPAN - yanidays * YANI * quantity
    else:
        longevity = ONEYEAR_MINUTES * FEMALE_SPAN - yanidays * YANI * quantity
    return longevity

def yesyani_expectancy(sex, born, yani, yst_date, yend_date, quantity):
    today = datetime.date.today()
    birth = datetime.date(born[0], born[1], born[2])
    diff = ((today - birth) / timedelta(days=1))

    longevity = yesyani_lifespan(sex, yst_date, yend_date, quantity)

    life = longevity - (diff * 24 * 60)
    return life

def noyani_expectancy(sex, born):
    today = datetime.date.today()
    birth = datetime.date(born[0], born[1], born[2])
    diff = ((today - birth) / timedelta(days=1))

    longevity = noyani_lifespan(sex)

    life = longevity - (diff * 24 * 60)
    return life

def animal_lifespan(life):
    dog = int(life / SIBAINU)
    wani = int(life / WANI)

    alife = [dog, wani]
    return alife

def yani_money(yanidays, quantity):
    money = yanidays * quantity * YANIPRICE * (-1)
    return money

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'GET':
        return render_template('result.html')
    else:
        sex = request.form['sex']

        year = int(request.form['year'])
        month = int(request.form['month'])
        day = int(request.form['day'])
        born= [year, month, day]

        yani = request.form['yani']

        if yani == "yes":
            quantity = int(request.form['quantity'])

            yst_year = int(request.form['yst_year'])
            yst_month = int(request.form['yst_month'])
            yst_day = int(request.form['yst_day'])
            yst_date = [yst_year, yst_month, yst_day]

            yend_year = int(request.form['yend_year'])
            yend_month = int(request.form['yend_month'])
            yend_day = int(request.form['yend_day'])
            yend_date = [yend_year, yend_month, yend_day]

            life = yesyani_expectancy(sex, born, yani, yst_date, yend_date, quantity)

            money = yani_money(smoking_span(yst_date, yend_date), quantity)

        else:
            money=0
            life = noyani_expectancy(sex, born)

        alife = animal_lifespan(life)

        animal = request.form["animal"]
        if animal=="dog":
            judge = 0
            animal_name = "柴犬"
            picture = "https://er-animal.jp/pepy/wp-content/uploads/2018/01/051.jpg"
        elif animal=="crocodile":
            judge = 1
            animal_name = "100ワニ"
            picture = "https://emon.webshogakukan.com/hyakuwani/img/hyakuwani2.png"

        return render_template('result.html', life=life, alife=alife,
                                animal_name=animal_name, judge=judge,
                                picture=picture, money=money)

if __name__ == '__main__':
    app.run()
