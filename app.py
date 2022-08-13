import requests
import atexit 
from apscheduler.schedulers.background import BackgroundScheduler
from pymongo import MongoClient
from flask import Flask, render_template, request
import time

app = Flask(__name__)
client = MongoClient("mongodb+srv://sach:12345@cluster0.zksvv.mongodb.net/?retryWrites=true&w=majority")
db = client.Weather_Dashboard_data

r1 = requests.get("http://api.weatherapi.com/v1/forecast.json?key=4279d0576b514746a63194544220108&q=London&days=7&aqi=no&alerts=no")
r3 = requests.get("http://api.weatherapi.com/v1/forecast.json?key=4279d0576b514746a63194544220108&q=Tokyo&days=7&aqi=no&alerts=no")
r2 = requests.get("http://api.weatherapi.com/v1/forecast.json?key=4279d0576b514746a63194544220108&q=Mumbai&days=7&aqi=no&alerts=no")
r4 = requests.get("http://api.weatherapi.com/v1/forecast.json?key=4279d0576b514746a63194544220108&q=Shanghai&days=7&aqi=no&alerts=no")
r5 = requests.get("http://api.weatherapi.com/v1/forecast.json?key=4279d0576b514746a63194544220108&q=Toronto&days=7&aqi=no&alerts=no")
r6 = requests.get("http://api.weatherapi.com/v1/forecast.json?key=4279d0576b514746a63194544220108&q=Melbourne&days=7&aqi=no&alerts=no")



def data_load():
    #while True:
    if r1.status_code == 200:
        London = r1.json()
        #time.sleep(60)
    else:
        exit()
    if r2.status_code == 200:
        Tokyo = r2.json()
        #time.sleep(60)
    else:
        exit()
    if r3.status_code == 200:
        Mumbai = r3.json()
        #time.sleep(60)
    else:
        exit()
    if r4.status_code == 200:
        Shanghai = r4.json()
        #time.sleep(60)
    else:
        exit()
    if r5.status_code == 200:
        Toronto = r5.json()
        #time.sleep(60)
    else:
        exit()
    if r6.status_code == 200:
        Melbourne = r6.json()
        #time.sleep(60)
    else:
        exit()    
    db.final2.insert_one(London)
    db.final2.insert_one(Mumbai)
    db.final2.insert_one(Tokyo)
    db.final2.insert_one(Shanghai)
    db.final2.insert_one(Toronto)
    db.final2.insert_one(Melbourne)

data_load()

scheduler = BackgroundScheduler()
scheduler.add_job(func=data_load, trigger="interval", hours=24)
scheduler.start()

@app.route('/')
def homepage():
    London = r1.json()
    date1=London['forecast']['forecastday']
    Tokyo = r2.json()
    Shanghai = r3.json()
    Mumbai = r4.json()
    Toronto = r5.json()
    Melbourne = r6.json()

    return render_template('homepage.html', **locals())

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/results', methods=['POST'])
def render_results():
    name = request.form['cityname']
    data = get_weather_results(name)
    return render_template('results.html',data=data)


def get_weather_results(name):
    api_url = "http://api.weatherapi.com/v1/forecast.json?key=4279d0576b514746a63194544220108&q={}&days=7&aqi=no&alerts=no".format(name)
    r = requests.get(api_url)
    return r.json()


if __name__ == '__main__':
    app.run(debug=True)

